"""Minimal OpenAI-compatible client for Tencent Hunyuan."""

from __future__ import annotations

import base64
import os
import re
import subprocess

import requests

BASE_URL = "https://api.hunyuan.cloud.tencent.com/v1"
# Most classic hunyuan text models were taken offline in 2026 (code 2030);
# the vision line still serves both text-only and image requests.
TEXT_MODEL = "hunyuan-vision-1.5-instruct"
VISION_MODEL = "hunyuan-vision-1.5-instruct"


def _api_key() -> str:
    key = os.environ.get("HUNYUAN_LLM")
    if not key:
        # Fall back to the fish universal variable where the key lives.
        key = subprocess.run(
            ["fish", "-c", "echo $HUNYUAN_LLM"], capture_output=True, text=True
        ).stdout.strip()
    if not key:
        raise RuntimeError("HUNYUAN_LLM API key not found (env or fish variables)")
    return key


def _strip_thinking(text: str) -> str:
    """Thinking models wrap output in <think>/<answer> tags; keep the answer."""
    m = re.search(r"<answer>(.*?)(?:</answer>|$)", text, re.DOTALL)
    if m:
        text = m.group(1)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()


def chat(prompt: str, system: str | None = None, model: str = TEXT_MODEL) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return _request(model, messages)


def chat_vision(prompt: str, image_path: str, model: str = VISION_MODEL) -> str:
    img_b64 = base64.b64encode(open(image_path, "rb").read()).decode()
    suffix = image_path.rsplit(".", 1)[-1].lower()
    mime = {"jpg": "jpeg", "jpeg": "jpeg"}.get(suffix, "png")
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{mime};base64,{img_b64}"},
                },
                {"type": "text", "text": prompt},
            ],
        }
    ]
    return _request(model, messages)


def _request(model: str, messages: list) -> str:
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {_api_key()}"},
        json={"model": model, "messages": messages},
        timeout=600,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    return _strip_thinking(content)

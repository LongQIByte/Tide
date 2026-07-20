# Boogu-Image-0.1: Boosting Open-Source Unified Multimodal Understanding and Generation

[arXiv](https://arxiv.org/abs/2607.13125) · [HuggingFace](https://huggingface.co/papers/2607.13125) · ▲127

## Abstract (verbatim)

> We introduce Boogu-Image-0.1, an open-source unified multimodal understanding and generation model family, comprising Base, Turbo, Edit, and Edit-Turbo variants. It delivers competitive performance in high-quality text-to-image generation, fast inference, instruction-based editing, and bilingual (Chinese-English) text rendering. Closed-source multimodal systems like Nano-Banana-Pro and GPT-Image-2 achieve strong performance through system-level integration rather than a single model, yet their internal practices remain largely undisclosed. In this work, we demonstrate that targeted improvements in model understanding, data quality, and training pipelines, coupled with agentic inference-time scaling, can substantially enhance generation and editing performance even under highly constrained compute budgets. Comprehensive evaluations show that Boogu-Image-0.1 consistently matches or surpasses other open-source models across standard benchmarks, and achieves results approaching leading closed-source systems. Notably, this is accomplished with only 208.62 million unique images. The base model's theoretical training cost is only approximately \$400K. We share practical discussions that we believe are valuable to the broader research community, and release weights, code, and recipes under Apache 2.0 to advance the open ecosystem for unified multimodal understanding and generation. Our code is available here: https://github.com/Boogu-Project/Boogu-Image.

## Background

### Background Analysis  

**Technical Context**: Multimodal understanding and generation technologies (e.g., text-to-image synthesis, image editing) are becoming central to artificial intelligence, with applications in content creation (advertising, gaming), education (visual teaching materials), and research (data visualization). The core demand is to enable machines to "understand" human instructions and generate high-quality multimodal content while supporting flexible interaction and editing. For example, users may input a text description to generate a corresponding image or modify details (e.g., adjusting colors, adding elements).  

**Previous Challenges**: While closed-source systems (e.g., GPT-Image-2) achieve high performance through system-level integration, their internal implementations are opaque and require substantial computational resources, limiting accessibility for research or deployment. Open-source models often suffer from inferior performance, high training costs, or limited functionality. For instance, many struggle with text-to-image quality or struggle with instruction-based editing. Additionally, existing methods typically demand massive data or expensive training pipelines, restricting their use in resource-constrained scenarios.  

**Proposed Solution**: Boogu-Image-0.1 addresses these limitations through three key improvements: (1) enhancing model understanding of multimodal tasks to better parse instructions; (2) improving data quality and training efficiency to reduce computational demands; (3) introducing "agent-based inference-time scaling" to achieve high-performance generation and editing under low-resource settings. For example, its Turbo variant accelerates response times via optimized inference, while the Edit variant focuses on instruction-driven image modification.  

**Unique Angle**: Unlike traditional approaches, this work does not pursue "larger and more expensive" models. Instead, it achieves near-closed-source performance through systematic optimizations (e.g., data filtering, training strategy adjustments) and lightweight design, using only 208 million unique images. This "efficiency-over-scale" approach provides a reproducible solution for the open-source community and advances the democratization of multimodal technology.

## Method, Figure by Figure

(No figures to walk through.)

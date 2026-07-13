# Vidu S1: A Real-Time Interactive Video Generation Model

[arXiv](https://arxiv.org/abs/2607.03118) · [HuggingFace](https://huggingface.co/papers/2607.03118) · ▲127

## 摘要（原文）

> We introduce Vidu S1, a real-time interactive video generation model supporting voice control of digital characters. Users can control video generation content at any moment through voice instructions. Vidu S1 supports infinite-length real-time video generation without blurring, drift, or visual distortion. Built with TurboDiffusion and TurboServe, Vidu S1 outputs 540p real-time videos at up to 42 FPS on regular consumer GPUs. Users can upload custom images of real people, anime, and pets, and choose different voice tones for personalized experiences. Experiments show that Vidu S1 achieves the best performance across all test metrics while fully meeting real-time inference requirements. A playable online demo is available at https://vidu.com/vidu-stream.

## 摘要（中译）

我们介绍了Vidu S1，这是一个支持数字角色语音控制的实时交互式视频生成模型。用户可以通过语音指令在任何时刻控制视频生成的内容。Vidu S1支持无限长度的实时视频生成，且不会出现模糊、漂移或视觉失真。Vidu S1使用TurboDiffusion和TurboServe构建，在普通消费级GPU上以最高42 FPS的速度输出540p的实时视频。用户可以上传真实人物、动漫和宠物的自定义图像，并选择不同的音调以实现个性化体验。实验表明，Vidu S1在所有测试指标上都取得了最佳性能，同时完全满足实时推理要求。可玩的在线演示可在https://vidu.com/vidu-stream获取。

## 背景剖析

### 背景剖析  

随着数字内容创作的普及，实时交互式视频生成技术在娱乐、教育、虚拟助手等领域展现出巨大潜力。例如，用户希望与虚拟角色进行自然对话，或通过语音指令动态调整视频内容（如改变场景、角色动作）。这类技术的核心需求是**低延迟、高保真度**的实时生成能力，同时支持个性化输入（如自定义图像）和多模态交互（如语音控制）。然而，现有方法在这两方面仍面临显著挑战。  

此前的研究主要受限于两个关键问题：一是**生成效率与质量的矛盾**——传统模型要么生成速度慢（无法满足实时性），要么在长时间生成时出现画面模糊、漂移或失真；二是**交互灵活性不足**——多数系统依赖预定义脚本或静态输入，难以响应动态的语音指令或用户上传的个性化内容。这些限制导致现有技术难以在消费级硬件上部署，且无法提供流畅的用户体验。  

Vidu S1 的核心创新在于**通过 TurboDiffusion 和 TurboServe 架构突破实时性与质量的瓶颈**。具体而言，TurboDiffusion 优化了扩散模型的计算效率，使其能在普通消费者 GPU 上以 42 FPS 生成 540p 视频；而 TurboServe 则通过高效的推理流水线进一步降低延迟。此外，模型支持用户上传自定义图像（如真人、动漫角色或宠物）并通过语音指令实时控制内容，解决了传统方法交互性不足的问题。  

与前人工作相比，Vidu S1 的关键差异在于**“端到端实时交互”的设计理念**。它不仅追求生成速度，还确保长时间生成的稳定性（无模糊或漂移），同时通过语音和图像的多模态融合实现真正的个性化体验。实验表明，Vidu S1 在所有测试指标上均达到当前最优水平，且完全满足实时推理要求，这标志着实时交互式视频生成技术向实用化迈出了重要一步。

## 方法图解

（本文无可讲解的插图）

# Boogu-Image-0.1: Boosting Open-Source Unified Multimodal Understanding and Generation

[arXiv](https://arxiv.org/abs/2607.13125) · [HuggingFace](https://huggingface.co/papers/2607.13125) · ▲127

## 摘要（原文）

> We introduce Boogu-Image-0.1, an open-source unified multimodal understanding and generation model family, comprising Base, Turbo, Edit, and Edit-Turbo variants. It delivers competitive performance in high-quality text-to-image generation, fast inference, instruction-based editing, and bilingual (Chinese-English) text rendering. Closed-source multimodal systems like Nano-Banana-Pro and GPT-Image-2 achieve strong performance through system-level integration rather than a single model, yet their internal practices remain largely undisclosed. In this work, we demonstrate that targeted improvements in model understanding, data quality, and training pipelines, coupled with agentic inference-time scaling, can substantially enhance generation and editing performance even under highly constrained compute budgets. Comprehensive evaluations show that Boogu-Image-0.1 consistently matches or surpasses other open-source models across standard benchmarks, and achieves results approaching leading closed-source systems. Notably, this is accomplished with only 208.62 million unique images. The base model's theoretical training cost is only approximately \$400K. We share practical discussions that we believe are valuable to the broader research community, and release weights, code, and recipes under Apache 2.0 to advance the open ecosystem for unified multimodal understanding and generation. Our code is available here: https://github.com/Boogu-Project/Boogu-Image.

## 摘要（中译）

我们推出了Boogu - Image - 0.1，这是一个开源的统一多模态理解和生成模型家族，包含Base、Turbo、Edit和Edit - Turbo变体。它在高质量文本到图像生成、快速推理、基于指令的编辑以及双语（中文 - 英文）文本渲染方面表现出色。像Nano - Banana - Pro和GPT - Image - 2这样的闭源多模态系统通过系统级集成而非单一模型实现了强大的性能，但它们的内部实践在很大程度上仍未公开。在这项工作中，我们证明了在模型理解、数据质量和训练管道方面的针对性改进，结合代理推理时的缩放，即使在计算资源高度受限的情况下，也能大幅提高生成和编辑性能。综合评估表明，Boogu - Image - 0.1在标准基准测试中始终与其他开源模型持平或超越，并且取得了接近领先闭源系统的结果。值得注意的是，这是仅使用2.0862亿张独特图像实现的。基础模型的理论训练成本仅约为40万美元。我们分享了我们认为对更广泛的研究社区有价值的实际讨论，并在Apache 2.0许可下发布了权重、代码和配方，以推进统一多模态理解和生成的开放生态系统。我们的代码可在这里获取：https://github.com/Boogu - Project/Boogu - Image。

## 背景剖析

### 背景剖析  

**技术背景**：多模态理解与生成技术（如文本生成图像、图像编辑）正在成为人工智能的核心应用方向之一。这类技术广泛应用于内容创作（如广告设计、游戏开发）、教育（可视化教学材料）、科研（数据可视化）等领域，核心需求是让机器能够“理解”人类指令并生成高质量的多模态内容，同时支持灵活的交互与编辑。例如，用户可能希望输入一段文字描述，让系统生成对应的图像，甚至进一步修改细节（如调整颜色、添加元素）。  

**之前的问题**：尽管闭源系统（如GPT-Image-2）通过系统级整合实现了高性能，但其内部实现不透明，且依赖大量计算资源，难以被广泛研究或部署。开源模型则面临性能不足、训练成本高或功能单一的问题。例如，许多开源模型在文本-图像生成质量上落后于闭源方案，或在指令编辑任务中表现不佳。此外，现有方法往往需要海量数据或昂贵的训练流程，限制了其在资源受限场景下的应用。  

**本文的解法**：Boogu-Image-0.1通过三个关键改进突破这些限制：（1）优化模型对多模态任务的理解能力，使其能更好地解析指令；（2）提升数据质量和训练效率，减少对计算资源的依赖；（3）引入“代理推理时扩展”技术，在低计算预算下实现高性能生成与编辑。例如，其Turbo变体通过优化推理流程显著加快了响应速度，而Edit变体则专注于指令驱动的图像修改。  

**切入角度**：与传统研究不同，本文并未追求“更大更贵”的模型，而是通过系统性优化（如数据筛选、训练策略调整）和轻量化设计，在仅使用2.08亿独特图像的情况下，达到了接近闭源系统的性能。这种“以效率换性能”的思路为开源社区提供了可复现的解决方案，并推动了多模态技术的普惠化。

## 方法图解

（本文无可讲解的插图）

# OmniOpt: Taxonomy, Geometry, and Benchmarking of Modern Optimizers

[arXiv](https://arxiv.org/abs/2607.04033) · [HuggingFace](https://huggingface.co/papers/2607.04033) · ▲74

## 摘要（原文）

> Optimizer selection for large-scale model training has become a system-level design decision constrained jointly by compute, memory, tuning budget, and task diversity, yet the landscape of over one hundred methods remains fragmented. We therefore present OmniOpt, a unified survey and benchmark cookbook of optimizers for the research community. OmniOpt rests on four coupled components. First, we treat every optimizer update as a structured transformation through a five-stage meta-pipeline, and show that most methods engage only one or two of these stages. Second, we use norm-constrained linear minimization oracles (LMOs) to unify different optimizers. Third, these two views ground a dual-dimension taxonomy, one dimension assigning each method to a mechanism family and the other recording the measurable training objectives it aims to improve. Fourth, and at the core of this paper, we instantiate the full taxonomy in a unified cross-domain benchmark spanning representative optimizers, model scales, and training regimes from language model pretraining to image classification, systematically analyzing each method family across multiple effect objectives and laying out their trade-offs. OmniOpt thus supplies the research community with an operational coordinate system for selecting optimizers under explicit mechanism and objective assumptions, and charts a direction for the future development of the optimizer community.

## 摘要（中译）

大规模模型训练的优化器选择已成为一个受计算、内存、调优预算和任务多样性共同约束的系统级设计决策，然而一百多种方法的格局仍然碎片化。因此，我们向研究界提出了OmniOpt，这是一个统一的优化器调查和基准测试手册。OmniOpt基于四个耦合组件。首先，我们将每个优化器更新视为通过五阶段元管道的结构化转换，并表明大多数方法仅涉及这些阶段中的一两个。其次，我们使用范数约束的线性最小化预言机（LMOs）来统一不同的优化器。第三，这两个观点奠定了一个双维度分类法的基础，一个维度将每种方法分配到一个机制家族，另一个维度记录它旨在改进的可测量训练目标。第四，也是本文的核心，我们在一个统一的跨域基准测试中实例化了整个分类法，该基准测试涵盖了代表性优化器、模型规模和训练制度，从语言模型预训练到图像分类，系统地分析了每个方法家族在多个效果目标上的表现，并揭示了它们的权衡。因此，OmniOpt为研究界提供了一个操作坐标系，用于在明确的机制和目标假设下选择优化器，并为优化器社区的未来发展指明了方向。

## 背景剖析

### 背景剖析  

现代深度学习模型的训练对计算资源、内存容量和调参成本提出了极高要求，而优化器作为决定训练效率与效果的核心组件，其选择已成为系统级设计的关键决策。从大规模语言模型预训练到图像分类任务，优化器需要在有限资源下平衡收敛速度、泛化能力和稳定性。然而，当前超过百种优化方法的碎片化现状导致研究者和工程师难以快速匹配算法与具体场景——例如，某些优化器在内存受限环境下表现优异，另一些则更适合高并行化的分布式训练，但缺乏统一框架来系统比较它们的适用条件。  

此前的研究存在三个核心问题：首先，优化器的设计逻辑分散在不同子领域（如自适应学习率、动量加速或二阶方法），导致难以从全局视角理解其机制；其次，现有基准测试往往针对特定任务或模型规模，无法反映真实场景中的多样性需求；最后，优化器的性能评估多依赖单一指标（如训练损失），忽略了内存占用、调参复杂度等实际约束。这些局限使得优化器的选择更像“黑箱试错”，而非基于明确目标的理性决策。  

本文通过四个创新点解决上述问题：首先，将优化器的更新过程抽象为五阶段元流水线，揭示大多数方法仅依赖其中少数阶段，从而简化机制分析；其次，引入范数约束的线性最小化预言机（LMO）统一不同优化器的数学表达，打破技术壁垒；第三，构建双维度分类法，从机制家族和目标改进两个角度组织算法；最后，设计跨领域基准测试，覆盖语言模型、图像分类等场景，系统量化各类优化器在多目标下的权衡关系。  

与前人工作相比，本文的关键差异在于：它不局限于某一类优化器或任务，而是提供一个“操作坐标系”——研究者可根据机制假设（如是否需要动量）和目标约束（如内存上限）直接定位合适的方法。这种系统性整合不仅为当前优化器研究提供了清晰的方向，也为未来算法设计指明了需填补的空白（例如，如何在低内存下实现高效自适应学习率）。

## 方法图解

（本文无可讲解的插图）

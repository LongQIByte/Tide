# KronQ: LLM Quantization via Kronecker-Factored Hessian

[arXiv](https://arxiv.org/abs/2607.07964) · [HuggingFace](https://huggingface.co/papers/2607.07964) · ▲5

## 摘要（原文）

> Post-training quantization (PTQ) is a widely adopted technique for compressing large language models (LLMs) without retraining. Existing second-order PTQ methods, including GPTQ, construct quantization objectives exclusively from input activation statistics, effectively assuming that all output channels contribute equally to the layer-wise reconstruction objective. We propose KronQ, a PTQ framework that challenges this assumption by introducing the gradient covariance into the quantization pipeline. Under the Kronecker-factored Hessian approximation, the quantization loss depends jointly on both the activation and gradient covariances, and KronQ exploits this at two complementary levels. (1) KronQ introduces bidirectional incoherence processing, extending the existing input-side random rotation to the output dimension using the gradient covariance, reducing weight magnitude variance across both input and output dimensions. (2) KronQ derives a new sensitivity metric for inter-layer mixed-precision allocation, driven by the gradient and activation Hessian traces. Notably, in the case of 2-bit weight-only quantization on LLaMA-3-70B, while GPTQ and GPTAQ diverge or produce degenerate quantizations (>2000 perplexity on WikiText-2), KronQ achieves 7.93 perplexity.

## 摘要（中译）

后训练量化（Post-training quantization, PTQ）是一种广泛采用的压缩大型语言模型（Large Language Models, LLMs）的技术，而无需重新训练。现有的二阶PTQ方法，包括GPTQ，仅从输入激活统计信息构建量化目标，有效地假设所有输出通道对层重建目标的贡献相等。我们提出了KronQ，一种PTQ框架，通过将梯度协方差引入量化流程来挑战这一假设。在克罗内克分解的海森矩阵近似下，量化损失同时依赖于激活和梯度协方差，KronQ在两个互补的层面上利用这一点。(1) KronQ引入双向不连贯处理，使用梯度协方差将现有的输入侧随机旋转扩展到输出维度，减少输入和输出维度上的权重幅度方差。(2) KronQ推导出一个新的敏感性度量，用于层间混合精度分配，由梯度和激活海森矩阵的迹驱动。值得注意的是，在LLaMA-3-70B上进行2位仅权重量化时，尽管GPTQ和GPTAQ发散或产生退化的量化（WikiText-2上超过2000的困惑度），KronQ实现了7.93的困惑度。

## 背景剖析

### 背景剖析  

**1. 技术背景与需求**  
近年来，大语言模型（LLMs）的参数规模呈爆炸式增长，但部署这些模型需要高昂的计算资源和存储成本。后训练量化（Post-training Quantization, PTQ）作为一种无需重新训练即可压缩模型的技术，成为解决这一问题的关键手段。其核心目标是在降低模型精度（如将权重从32位浮点数转为8位整数）的同时，尽量减少对模型性能的影响。然而，现有方法在处理超大规模模型（如70B参数的LLaMA-3）时，常因量化误差积累导致性能骤降，甚至出现“退化”（如困惑度超过2000），无法满足实际部署需求。  

**2. 先前方法的局限性**  
传统PTQ方法（如GPTQ）主要依赖输入激活统计量来构建量化目标，假设所有输出通道对层重建的贡献是均等的。这种假设忽略了梯度信息对量化的影响，导致两个关键问题：一是权重在不同维度上的方差分布不均，加剧了信息丢失；二是缺乏对层间敏感性的精细衡量，难以在混合精度量化中合理分配资源。例如，当仅量化权重时，现有方法可能因忽略梯度协方差而导致优化方向偏差，最终使模型性能崩溃。  

**3. KronQ的解决思路**  
本文提出的KronQ框架通过引入梯度协方差打破了这一局限。其核心思想是基于Kronecker分解的Hessian近似，将量化损失同时与激活和梯度的统计特性关联。具体而言，KronQ通过双向非相干处理（bidirectional incoherence processing）扩展了传统的输入侧随机旋转，利用梯度协方差优化输出维度，从而平衡输入和输出维度的权重方差。此外，KronQ还提出了一种新的敏感性指标，通过Hessian迹（trace）衡量层间混合精度分配的优先级，确保关键层获得更高的精度保留。  

**4. 与前人工作的关键差异**  
与GPTQ等仅依赖输入激活的方法不同，KronQ首次将梯度信息纳入量化优化过程。这种差异体现在两个层面：一是通过双向非相干处理同时优化输入和输出维度，解决了权重方差不均的问题；二是通过Hessian迹驱动的敏感性分析，实现了更合理的混合精度分配。实验表明，在LLaMA-3-70B的2位权重仅量化任务中，KronQ的困惑度仅为7.93，远优于GPTQ（发散）和GPTAQ（退化），证明了其有效性。

## 方法图解

（本文无可讲解的插图）

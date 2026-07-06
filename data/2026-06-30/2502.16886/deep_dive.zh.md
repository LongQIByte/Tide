# ReFreeKV: Towards Threshold-Free KV Cache Compression

[arXiv](https://arxiv.org/abs/2502.16886) · [HuggingFace](https://huggingface.co/papers/2502.16886) · ▲47

## 摘要（原文）

> To reduce memory consumption during LLM inference, a handful of methods have been proposed for KV cache pruning. While these techniques can accomplish lossless memory reduction on many datasets, they often hinge on an under-emphasized condition: an input/domain-specific threshold for KV cache budget needs to be pre-determined to achieve the optimal performance. However, such input-sensitive design may be considerably limited in real-world scenarios, as open-domain inputs span diverse domains, lengths and difficulty levels, without clear boundaries for threshold selection. As a result, the dependence of such input-sensitive threshold can be a fundamental limitation that causes large degradation on arbitrary inputs. In this work, we propose a new objective that lifts the threshold constraints for robust KV compression, advocating for "threshold-free" methods that adaptively adjust budget allocation while preserving full-cache performance. We then propose a novel method, ReFreeKV, serving as the first instantiation of this objective. Extensive experiments across 13 datasets with diverse context lengths, task types, and model sizes demonstrate its efficacy and efficiency. Our code is publicly released at https://github.com/Patrick-Ni/ReFreeKV.

## 摘要（中译）

为了减少大型语言模型（LLM）推理过程中的内存消耗，已经提出了一些用于键值（KV）缓存修剪的方法。虽然这些技术在许多数据集上可以实现无损内存减少，但它们通常依赖于一个被低估的条件：需要预先确定一个针对输入/领域特定的KV缓存预算阈值，以实现最佳性能。然而，在实际场景中，这种对输入敏感的设计可能受到很大限制，因为开放领域的输入涵盖了不同的领域、长度和难度级别，没有明确的阈值选择边界。因此，这种对输入敏感阈值的依赖可能是导致在任意输入上产生大量性能下降的根本限制。在这项工作中，我们提出了一个新的目标，即解除阈值约束以实现鲁棒的KV压缩，倡导"无阈值"方法，这些方法可以在保持全缓存性能的同时自适应地调整预算分配。然后，我们提出了一种新颖的方法——ReFreeKV，作为这个目标的第一个实例化。在具有不同上下文长度、任务类型和模型大小的13个数据集上进行的大量实验表明了其有效性和效率。我们的代码已公开发布在https://github.com/Patrick-Ni/ReFreeKV。

## 背景剖析

### 背景剖析  

**1. 技术背景**  
大型语言模型（LLMs）在推理时依赖KV Cache存储中间状态以加速计算，但随着模型规模和输入长度增加，KV Cache的内存消耗呈线性增长。例如，Llama3 8B模型处理2K-token输入需1GB内存，而70B模型处理20K-token时需高达50GB。这种内存压力限制了LLMs在资源受限场景（如边缘设备或大规模并发推理）中的应用。因此，如何高效压缩KV Cache成为关键需求——既要减少内存占用，又要保持生成性能。  

**2. 之前的问题**  
现有方法通过剪枝（如H2O、ScissorHands）或合并（如KVMerger）KV Cache来降低内存，但它们依赖一个预定义的“阈值”来决定保留多少缓存。这个阈值需要针对不同任务或输入手动调整：例如，H2O在NarrativeQA数据集上用50%预算能达到98%的性能，但在GSM8K数学基准上性能骤降至42%。这种对输入敏感的阈值设计导致两个问题：要么为每个任务调参（不现实），要么用统一阈值导致性能大幅下降。此外，现有方法无法动态适应输入的复杂度变化。  

**3. 本文的解法**  
本文提出“无阈值KV压缩”的目标，即无论输入是什么，都能自适应分配缓存资源，同时最大化内存节省。具体方法（ReFreeKV）分为两步：首先按位置重要性对输入token排序（开头和结尾通常更重要），然后通过注意力矩阵的差异动态决定何时停止剪枝。这种方法无需预定义阈值，而是根据输入内容自动调整压缩比例。例如，对复杂数学任务保留更多缓存，而对简单阅读理解任务则大幅压缩。  

**4. 切入角度**  
与前人工作相比，本文的核心差异在于**去除了对输入敏感的阈值依赖**。以往方法需要人为设定预算（如“保留50%的token”），而ReFreeKV通过注意力差异等指标动态判断最优压缩点。实验表明，该方法在13个不同数据集上（包括数学、常识推理等）均能接近全缓存性能，同时平均压缩率达63.7%。这种“自适应预算”策略使KV Cache压缩从“任务特定”转向“通用鲁棒”，更适合真实世界的多样化输入场景。

## 方法图解

（本文无可讲解的插图）

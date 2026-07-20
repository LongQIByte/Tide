# LongStraw: Long-Context RL Beyond 2M Tokens under a Fixed GPU Budget

[arXiv](https://arxiv.org/abs/2607.14952) · [HuggingFace](https://huggingface.co/papers/2607.14952) · ▲178

## 摘要（原文）

> A growing gap separates inference context lengths from RL post-training: inference systems are approaching million-token contexts, while post-training workloads often remain at 256K tokens or below and rely on length generalization at deployment. The gap is especially important for AI agents, whose observations, tool outputs, documents, and prior decisions accumulate over long trajectories. LongStraw is an architecture-aware execution stack for million-token RL post-training under a fixed GPU budget, instantiated with Group Relative Policy Optimization (GRPO). It evaluates the shared prompt without autograd, retains only model-specific state needed by later tokens, and replays short response branches one at a time, reducing the live training graph at the cost of additional replay time. We implement it for the hybrid recurrent and full-attention Qwen3.6-27B and the compressed-attention mixture-of-experts GLM-5.2. On eight H20 GPUs, LongStraw completes grouped Qwen scoring and response backward at 2.1M positions for groups of 2 and 8; increasing the group size adds only 0.21 GB of peak allocated memory, while a separate stress test reaches 4.46M positions. On 32 H20 GPUs, we validate the end-to-end LongStraw execution path for a 2.1M-token prompt across all 78 layers of GLM-5.2. These experiments establish execution capacity rather than complete training correctness because the captured prompt state is detached and some distributed forward and gradient composition paths remain incomplete.

## 摘要（中译）

推理上下文长度与强化学习（RL）训练后工作负载之间的差距日益扩大：推理系统正接近百万令牌（token）的上下文长度，而训练后工作负载通常保持在256K令牌或以下，并在部署时依赖长度泛化。这种差距对于人工智能（AI）代理尤为重要，因为它们的观察结果、工具输出、文档和先前的决策会在长轨迹中累积。LongStraw是一种在固定GPU预算下支持百万令牌RL训练后执行的架构感知执行栈，通过分组相对策略优化（Group Relative Policy Optimization，GRPO）实现。它在不使用自动微分（autograd）的情况下评估共享提示，仅保留后续令牌所需的特定于模型的状态，并逐个重放短响应分支，以额外的重放时间为代价减少实时训练图。我们为混合循环和全注意力机制的Qwen3.6-27B以及压缩注意力机制的专家混合模型GLM-5.2实现了该架构。在8个H20 GPU上，LongStraw能够完成2组和8组的分组Qwen评分及响应反向传播，处理210万个位置；增加组大小仅增加0.21 GB的峰值分配内存，而单独的压力测试达到了446万个位置。在32个H20 GPU上，我们验证了针对GLM-5.2全部78层的210万个令牌提示的端到端LongStraw执行路径。这些实验确立了执行能力而非完全的训练正确性，因为捕获的提示状态是分离的，且一些分布式前向和梯度组合路径仍不完整。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
近年来，AI智能体（如对话机器人、自动化决策系统）需要处理越来越长的上下文信息。例如，在多轮对话中，模型需要记住之前的交互内容；在文档分析中，可能需要理解整本书或长报告；在工具调用场景中，需累积历史操作结果。然而，当前强化学习（RL）的后训练阶段（post-training）通常只能处理较短上下文（如256K tokens），而推理系统已能支持百万级tokens的上下文。这种差距导致智能体在实际部署时无法充分利用长上下文能力，限制了其性能和应用范围。  

**2. 之前的问题**  
传统方法在长上下文RL训练中面临两个核心挑战：  
- **内存瓶颈**：长序列训练需要保存完整的计算图（computation graph），导致GPU内存消耗剧增，难以扩展到百万级tokens。  
- **计算效率低**：现有方法要么无法高效处理长序列（如全注意力机制的计算复杂度随长度平方增长），要么牺牲训练准确性（如截断序列或近似梯度计算）。  

**3. 本文的解法**  
LongStraw通过**架构感知的执行栈**（architecture-aware execution stack）解决上述问题。其核心思路是：  
- **动态内存管理**：仅保留后续计算所需的状态（如模型特定状态），而非完整计算图，从而减少内存占用。  
- **分组优化**（Group Relative Policy Optimization, GRPO）：将长序列分成小组，逐组处理并重放短分支，平衡内存与计算效率。  
- **混合注意力机制**：针对不同模型（如Qwen的循环+全注意力、GLM的混合专家架构）优化执行路径，确保在固定GPU预算下支持百万级tokens的训练。  

**4. 与前人工作的关键差异**  
与以往方法相比，LongStraw的独特之处在于：  
- **执行容量优先**：不追求完全训练正确性，而是通过分离提示状态（detached prompt state）和部分分布式计算路径，验证长上下文训练的可行性。  
- **硬件高效利用**：在固定GPU数量下（如8或32个H20 GPU），通过内存优化实现长序列训练，而非依赖更多硬件资源。  
- **针对性优化**：针对不同模型架构（循环vs.混合注意力）设计特定执行策略，而非通用方案。  

这一工作为长上下文RL的实际应用奠定了基础，展示了在有限资源下突破上下文长度限制的可能性。

## 方法图解

（本文无可讲解的插图）

# LongStraw: Long-Context RL Beyond 2M Tokens under a Fixed GPU Budget

[arXiv](https://arxiv.org/abs/2607.14952) · [HuggingFace](https://huggingface.co/papers/2607.14952) · ▲178

## Abstract (verbatim)

> A growing gap separates inference context lengths from RL post-training: inference systems are approaching million-token contexts, while post-training workloads often remain at 256K tokens or below and rely on length generalization at deployment. The gap is especially important for AI agents, whose observations, tool outputs, documents, and prior decisions accumulate over long trajectories. LongStraw is an architecture-aware execution stack for million-token RL post-training under a fixed GPU budget, instantiated with Group Relative Policy Optimization (GRPO). It evaluates the shared prompt without autograd, retains only model-specific state needed by later tokens, and replays short response branches one at a time, reducing the live training graph at the cost of additional replay time. We implement it for the hybrid recurrent and full-attention Qwen3.6-27B and the compressed-attention mixture-of-experts GLM-5.2. On eight H20 GPUs, LongStraw completes grouped Qwen scoring and response backward at 2.1M positions for groups of 2 and 8; increasing the group size adds only 0.21 GB of peak allocated memory, while a separate stress test reaches 4.46M positions. On 32 H20 GPUs, we validate the end-to-end LongStraw execution path for a 2.1M-token prompt across all 78 layers of GLM-5.2. These experiments establish execution capacity rather than complete training correctness because the captured prompt state is detached and some distributed forward and gradient composition paths remain incomplete.

## Background

### Background Analysis  

**1. Technical Context and Real-World Needs**  
In recent years, AI agents (e.g., dialogue systems, automated decision-making tools) increasingly require handling long contextual information. For instance, multi-turn conversations need memory of prior interactions, document analysis may involve understanding entire books or reports, and tool-calling scenarios require accumulating historical operation results. However, current reinforcement learning (RL) post-training typically handles only short contexts (e.g., 256K tokens), while inference systems already support million-token contexts. This gap limits the performance and deployment of agents in real-world scenarios.  

**2. Previous Limitations**  
Traditional methods face two core challenges in long-context RL training:  
- **Memory Bottlenecks**: Long-sequence training requires retaining complete computation graphs, leading to excessive GPU memory usage and difficulty scaling to million-token lengths.  
- **Computational Inefficiency**: Existing approaches either fail to handle long sequences efficiently (e.g., quadratic complexity of full attention) or sacrifice training accuracy (e.g., truncating sequences or approximating gradients).  

**3. Proposed Solution**  
LongStraw addresses these issues with an **architecture-aware execution stack**:  
- **Dynamic Memory Management**: Retains only states necessary for subsequent computations (e.g., model-specific states) instead of full computation graphs, reducing memory footprint.  
- **Group Relative Policy Optimization (GRPO)**: Splits long sequences into groups, processes them individually, and replays short branches, balancing memory and efficiency.  
- **Hybrid Attention Mechanisms**: Optimizes execution paths for different models (e.g., Qwen’s recurrent + full attention, GLM’s mixture-of-experts) to support million-token training under fixed GPU budgets.  

**4. Key Differences from Prior Work**  
LongStraw stands out by:  
- **Execution-Capacity Focus**: Prioritizes feasibility over perfect training correctness by detaching prompt states and using partial distributed computation paths.  
- **Hardware Efficiency**: Validates long-context training on fixed GPU counts (e.g., 8 or 32 H20 GPUs) through memory optimization, rather than relying on more hardware.  
- **Targeted Optimization**: Designs architecture-specific strategies (e.g., recurrent vs. hybrid attention) instead of a one-size-fits-all approach.  

This work lays the foundation for practical long-context RL, demonstrating the possibility of breaking context-length limits with limited resources.

## Method, Figure by Figure

(No figures to walk through.)

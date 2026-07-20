# Loop the Loopies!

[arXiv](https://arxiv.org/abs/2607.16051) · [HuggingFace](https://huggingface.co/papers/2607.16051) · ▲17

## Abstract (verbatim)

> We present Loopie, the most powerful looped Transformer to date. The Loopie series consists of two Mixture-of-Experts (MoE) models: a 20B-parameter model with 2B active parameters and a 6Bparameter model with 0.6B active parameters. Looped Transformers have long faced a challenge: given an N-fold increase in pre-training compute, increasing the parameter count by a factor of N usually outperforms looping a model N times. Loopie addresses this challenge. Extensive ablation studies, including comparisons with a vanilla 30B-A3B model, show that Loopie substantially outperforms vanilla Transformer baselines trained with the same compute budget. Our novel post-training pipeline equips Loopie with strong reasoning abilities. At the 2025 IMO and IPhO, Loopie achieves gold-medal performance without tools.

## Background

In the rapidly evolving field of artificial intelligence, large-scale model technology has demonstrated immense potential in various domains such as natural language processing, mathematical reasoning, and scientific research. However, as model sizes continue to expand, the computational resources and training costs required have also increased exponentially, posing significant challenges for practical applications. How to efficiently utilize limited computational resources to enhance model performance has become a focal point of current research.

Previous studies have attempted to address this issue by either increasing the number of model parameters or employing looped training methods. However, these approaches have certain limitations. Increasing model parameters can improve performance but comes at the cost of higher computational expenses and longer training times. On the other hand, looped training methods struggle to fully utilize computational resources, resulting in limited performance gains. Therefore, maximizing model performance within a constrained computational budget has become a critical challenge in current research.

This paper introduces a novel looped Transformer model called Loopie, aimed at addressing the aforementioned issues. The Loopie series consists of two Mixture-of-Experts (MoE) models: a 20B-parameter model with 2B active parameters and a 6B-parameter model with 0.6B active parameters. Through an innovative training method, Loopie effectively utilizes computational resources to achieve significant performance improvements within a limited computational budget.

Compared to previous works, the key difference of Loopie lies in its unique training approach and model architecture. Loopie employs a novel post-training pipeline that equips the model with strong reasoning capabilities. In the 2025 International Mathematical Olympiad (IMO) and International Physics Olympiad (IPhO), Loopie achieved gold medal performance without the use of any tools, demonstrating its powerful problem-solving abilities in complex scenarios.

In summary, the proposed Loopie model, through its innovative training methods and model architecture, effectively overcomes the limitations of previous approaches in terms of computational resource utilization and performance enhancement, providing new insights and directions for the future development of large-scale model technology.

## Method, Figure by Figure

(No figures to walk through.)

# Loop the Loopies!

[arXiv](https://arxiv.org/abs/2607.16051) · [HuggingFace](https://huggingface.co/papers/2607.16051) · ▲17

## 摘要（原文）

> We present Loopie, the most powerful looped Transformer to date. The Loopie series consists of two Mixture-of-Experts (MoE) models: a 20B-parameter model with 2B active parameters and a 6Bparameter model with 0.6B active parameters. Looped Transformers have long faced a challenge: given an N-fold increase in pre-training compute, increasing the parameter count by a factor of N usually outperforms looping a model N times. Loopie addresses this challenge. Extensive ablation studies, including comparisons with a vanilla 30B-A3B model, show that Loopie substantially outperforms vanilla Transformer baselines trained with the same compute budget. Our novel post-training pipeline equips Loopie with strong reasoning abilities. At the 2025 IMO and IPhO, Loopie achieves gold-medal performance without tools.

## 摘要（中译）

我们提出了Loopie，迄今为止最强大的循环Transformer。Loopie系列由两个混合专家（Mixture-of-Experts，MoE）模型组成：一个具有20B参数且活跃参数为2B的模型，以及一个具有6B参数且活跃参数为0.6B的模型。循环Transformer长期以来面临一个挑战：在预训练计算量增加N倍的情况下，将参数数量增加N倍通常比将模型循环N次效果更好。Loopie解决了这一挑战。广泛的消融研究（包括与普通30B - A3B模型的比较）表明，Loopie在使用相同计算预算训练时，大幅优于普通的Transformer基线模型。我们新颖的后训练管道使Loopie具备强大的推理能力。在2025年国际数学奥林匹克竞赛（IMO）和国际物理奥林匹克竞赛（IPhO）中，Loopie在没有工具辅助的情况下取得了金牌成绩。

## 背景剖析

在人工智能技术迅猛发展的今天，大模型技术在自然语言处理、数学推理、科学研究等领域展现出了巨大的潜力。然而，随着模型规模的不断扩大，训练成本和计算资源的消耗也呈指数级增长，这给实际应用带来了巨大的挑战。如何高效地利用有限的计算资源来提升模型的性能，成为了当前研究的热点问题。

先前的研究中，研究者们尝试通过增加模型参数或循环训练模型来解决这一问题。然而，这些方法都存在一定的局限性。增加模型参数虽然可以提升性能，但会带来更高的计算成本和更长的训练时间；而循环训练模型则难以充分利用计算资源，导致性能提升有限。因此，如何在有限的计算资源下实现模型性能的最大化，成为了当前研究的关键问题。

本文提出了一种名为Loopie的新型循环Transformer模型，旨在解决上述问题。Loopie系列包括两个混合专家（MoE）模型：一个20B参数的模型，其中2B参数是活跃的；另一个6B参数的模型，其中0.6B参数是活跃的。Loopie通过一种新颖的训练方法，有效地利用了计算资源，实现了在有限的计算预算下显著提升模型性能的目标。

与先前的工作相比，Loopie的关键差异在于其独特的训练方法和模型架构。Loopie采用了一种新颖的后训练管道，使模型具备了强大的推理能力。在2025年国际数学奥林匹克竞赛（IMO）和国际物理奥林匹克竞赛（IPhO）中，Loopie在没有使用任何工具的情况下，取得了金牌成绩，充分展示了其在复杂问题解决方面的强大能力。

总之，本文提出的Loopie模型通过创新的训练方法和模型架构，有效地解决了先前方法在计算资源利用和性能提升方面的局限性，为未来大模型技术的发展提供了新的思路和方向。

## 方法图解

（本文无可讲解的插图）

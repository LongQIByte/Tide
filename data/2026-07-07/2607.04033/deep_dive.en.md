# OmniOpt: Taxonomy, Geometry, and Benchmarking of Modern Optimizers

[arXiv](https://arxiv.org/abs/2607.04033) · [HuggingFace](https://huggingface.co/papers/2607.04033) · ▲74

## Abstract (verbatim)

> Optimizer selection for large-scale model training has become a system-level design decision constrained jointly by compute, memory, tuning budget, and task diversity, yet the landscape of over one hundred methods remains fragmented. We therefore present OmniOpt, a unified survey and benchmark cookbook of optimizers for the research community. OmniOpt rests on four coupled components. First, we treat every optimizer update as a structured transformation through a five-stage meta-pipeline, and show that most methods engage only one or two of these stages. Second, we use norm-constrained linear minimization oracles (LMOs) to unify different optimizers. Third, these two views ground a dual-dimension taxonomy, one dimension assigning each method to a mechanism family and the other recording the measurable training objectives it aims to improve. Fourth, and at the core of this paper, we instantiate the full taxonomy in a unified cross-domain benchmark spanning representative optimizers, model scales, and training regimes from language model pretraining to image classification, systematically analyzing each method family across multiple effect objectives and laying out their trade-offs. OmniOpt thus supplies the research community with an operational coordinate system for selecting optimizers under explicit mechanism and objective assumptions, and charts a direction for the future development of the optimizer community.

## Background

### Background Analysis  

Modern deep learning model training imposes extreme demands on computational resources, memory capacity, and hyperparameter tuning costs, making optimizer selection a critical system-level design decision. From large-scale language model pretraining to image classification tasks, optimizers must balance convergence speed, generalization, and stability under resource constraints. However, the fragmented landscape of over a hundred optimization methods leaves researchers and engineers struggling to match algorithms to specific scenarios—for example, some optimizers excel in memory-constrained environments, while others are better suited for highly parallel distributed training, but no unified framework exists to systematically compare their applicability.  

Previous research faces three core issues: first, optimizer design logic is scattered across subfields (e.g., adaptive learning rates, momentum acceleration, or second-order methods), making it difficult to understand mechanisms holistically; second, existing benchmarks often target specific tasks or model scales, failing to reflect real-world diversity; third, performance evaluations rely heavily on single metrics like training loss, ignoring practical constraints such as memory usage or tuning complexity. These limitations reduce optimizer selection to a "black-box trial-and-error" process rather than a rational decision based on clear objectives.  

This paper addresses these problems through four innovations: first, it abstracts the optimizer update process into a five-stage meta-pipeline, revealing that most methods rely on only a few stages, thus simplifying mechanism analysis; second, it introduces norm-constrained linear minimization oracles (LMOs) to unify the mathematical expressions of different optimizers, breaking down technical barriers; third, it constructs a two-dimensional taxonomy organizing algorithms by mechanism families and improvement objectives; fourth, it designs a cross-domain benchmark covering tasks like language modeling and image classification, quantifying trade-offs across multiple objectives.  

Compared to prior work, the key difference lies in its holistic approach: instead of focusing on a specific optimizer class or task, it provides an "operational coordinate system" where researchers can directly identify suitable methods based on mechanism assumptions (e.g., whether momentum is needed) and constraint goals (e.g., memory limits). This systematic integration not only clarifies the path for current optimizer research but also highlights gaps for future algorithm design (e.g., how to achieve efficient adaptive learning rates under low memory).

## Method, Figure by Figure

(No figures to walk through.)

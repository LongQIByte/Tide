# KronQ: LLM Quantization via Kronecker-Factored Hessian

[arXiv](https://arxiv.org/abs/2607.07964) · [HuggingFace](https://huggingface.co/papers/2607.07964) · ▲5

## Abstract (verbatim)

> Post-training quantization (PTQ) is a widely adopted technique for compressing large language models (LLMs) without retraining. Existing second-order PTQ methods, including GPTQ, construct quantization objectives exclusively from input activation statistics, effectively assuming that all output channels contribute equally to the layer-wise reconstruction objective. We propose KronQ, a PTQ framework that challenges this assumption by introducing the gradient covariance into the quantization pipeline. Under the Kronecker-factored Hessian approximation, the quantization loss depends jointly on both the activation and gradient covariances, and KronQ exploits this at two complementary levels. (1) KronQ introduces bidirectional incoherence processing, extending the existing input-side random rotation to the output dimension using the gradient covariance, reducing weight magnitude variance across both input and output dimensions. (2) KronQ derives a new sensitivity metric for inter-layer mixed-precision allocation, driven by the gradient and activation Hessian traces. Notably, in the case of 2-bit weight-only quantization on LLaMA-3-70B, while GPTQ and GPTAQ diverge or produce degenerate quantizations (>2000 perplexity on WikiText-2), KronQ achieves 7.93 perplexity.

## Background

### Background Analysis  

**1. Technical Context and Needs**  
In recent years, the explosive growth in the size of large language models (LLMs) has created a need for efficient deployment methods that reduce computational resources and storage costs without sacrificing performance. Post-training quantization (PTQ) is a widely adopted technique for compressing these models by reducing precision (e.g., from 32-bit floating-point to 8-bit integers) after training. However, existing PTQ methods often fail to maintain acceptable performance when applied to extremely large models (e.g., 70B-parameter LLaMA-3), leading to issues like performance collapse or "degeneration" (e.g., perplexity exceeding 2000), which hinder real-world deployment.  

**2. Limitations of Previous Methods**  
Traditional PTQ approaches (e.g., GPTQ) primarily rely on input activation statistics to construct quantization objectives, assuming that all output channels contribute equally to the layer-wise reconstruction loss. This assumption ignores the impact of gradient information, leading to two critical problems: (1) uneven variance distribution across weight dimensions, which increases information loss; and (2) a lack of fine-grained sensitivity measurement for inter-layer mixed-precision allocation, making it difficult to optimize resource allocation effectively. For instance, methods that quantize only weights may suffer from suboptimal directions due to ignored gradient covariance, causing performance degradation.  

**3. KronQ’s Solution Approach**  
The proposed KronQ framework addresses these limitations by incorporating gradient covariance into the quantization pipeline. Its core idea is based on a Kronecker-factored Hessian approximation, which jointly optimizes quantization loss using both activation and gradient statistics. Specifically, KronQ introduces bidirectional incoherence processing to extend traditional input-side random rotation to the output dimension, balancing weight variance across input and output dimensions using gradient covariance. Additionally, KronQ derives a new sensitivity metric for mixed-precision allocation, driven by Hessian traces, ensuring that critical layers retain higher precision.  

**4. Key Differences from Prior Work**  
Unlike methods like GPTQ that rely solely on input activations, KronQ is the first to integrate gradient information into quantization optimization. This difference manifests in two key aspects: (1) bidirectional incoherence processing optimizes both input and output dimensions, resolving uneven weight variance; and (2) Hessian trace-driven sensitivity analysis enables more effective mixed-precision allocation. Experiments show that on the LLaMA-3-70B model with 2-bit weight-only quantization, KronQ achieves a perplexity of 7.93, outperforming GPTQ (divergence) and GPTAQ (degeneration), thus demonstrating its effectiveness.

## Method, Figure by Figure

(No figures to walk through.)

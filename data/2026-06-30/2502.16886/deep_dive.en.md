# ReFreeKV: Towards Threshold-Free KV Cache Compression

[arXiv](https://arxiv.org/abs/2502.16886) · [HuggingFace](https://huggingface.co/papers/2502.16886) · ▲47

## Abstract (verbatim)

> To reduce memory consumption during LLM inference, a handful of methods have been proposed for KV cache pruning. While these techniques can accomplish lossless memory reduction on many datasets, they often hinge on an under-emphasized condition: an input/domain-specific threshold for KV cache budget needs to be pre-determined to achieve the optimal performance. However, such input-sensitive design may be considerably limited in real-world scenarios, as open-domain inputs span diverse domains, lengths and difficulty levels, without clear boundaries for threshold selection. As a result, the dependence of such input-sensitive threshold can be a fundamental limitation that causes large degradation on arbitrary inputs. In this work, we propose a new objective that lifts the threshold constraints for robust KV compression, advocating for "threshold-free" methods that adaptively adjust budget allocation while preserving full-cache performance. We then propose a novel method, ReFreeKV, serving as the first instantiation of this objective. Extensive experiments across 13 datasets with diverse context lengths, task types, and model sizes demonstrate its efficacy and efficiency. Our code is publicly released at https://github.com/Patrick-Ni/ReFreeKV.

## Background

### Background Analysis  

**1. Technical Context**  
Large language models (LLMs) rely on KV Cache to store intermediate states during inference, but memory consumption grows linearly with model size and input length. For example, Llama3 8B requires 1GB for 2K tokens, while Llama3 70B needs 50GB for 20K tokens. This memory pressure limits LLM deployment in resource-constrained scenarios (e.g., edge devices). The core challenge is compressing KV Cache efficiently—reducing memory while preserving generation quality.  

**2. Limitations of Prior Work**  
Existing methods (e.g., H2O, ScissorHands) prune KV Cache using a pre-defined threshold, but this threshold must be tuned for different tasks. For instance, H2O achieves 98% performance on NarrativeQA with 50% budget but drops to 42% on GSM8K. This threshold sensitivity makes prior methods impractical for real-world use: either manual tuning is required (unscalable), or a fixed threshold degrades performance. Additionally, they cannot adapt to varying input complexity dynamically.  

**3. Solution Proposed**  
This paper introduces a "threshold-free" KV compression objective, where cache allocation adapts to input content without manual tuning. The method (ReFreeKV) ranks tokens by positional importance (beginning and end tokens are typically more critical) and dynamically stops pruning based on attention matrix differences. For complex tasks (e.g., math), it retains more cache; for simple tasks (e.g., reading comprehension), it compresses aggressively.  

**4. Key Difference from Prior Work**  
Unlike existing methods that depend on input-specific thresholds, ReFreeKV eliminates this requirement by using attention metrics to determine optimal pruning dynamically. Experiments show it achieves near-full-cache performance across 13 datasets (e.g., math, coding) with an average compression ratio of 63.7%. This "adaptive budget" approach shifts KV compression from "task-specific" to "universally robust," making it more practical for real-world diverse inputs.

## Method, Figure by Figure

(No figures to walk through.)

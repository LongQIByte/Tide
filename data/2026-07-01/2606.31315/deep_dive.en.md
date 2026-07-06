# BlockPilot: Instance-Adaptive Policy Learning for Diffusion-based Speculative Decoding

[arXiv](https://arxiv.org/abs/2606.31315) · [HuggingFace](https://huggingface.co/papers/2606.31315) · ▲74

## Abstract (verbatim)

> Speculative decoding accelerates inference by using a lightweight draft model to generate candidate tokens in parallel, and are then verified by the target model, enabling lossless acceleration. Recently, diffusion-based speculative decoding further improves parallelism by generating multiple tokens per forward pass via block-level diffusion, achieving state-of-the-art (SOTA) performance. However, existing methods adopt a fixed inference block size and assume a uniform optimal decoding strategy across all inputs. In this paper, we show that this assumption is suboptimal, as the optimal block size varies across samples and plays a critical role in speculative decoding performance. Moreover, these values exhibit a clear local structure, concentrating around the training block size, which reduces the problem to a low-dimensional and structured decision space. Based on these insights, we propose BlockPilot, a sample-adaptive policy that predicts the optimal block size from the prefilling representation. Specifically, we formulate block size selection as a lightweight policy learning problem and propose an instance-adaptive decision mechanism that predicts the optimal block size based on the representation of the prefilling stage. The prediction is performed only once after prefilling, allowing for seamless integration. Extensive experiments demonstrate that our method is plug-and-play, introduces minimal overhead, and consistently improves efficiency, achieving an acceptance length of 5.92 and a 4.20times speedup on Qwen3-4B under temperature T=1.

## Background

### Background Analysis  

#### 1. Technical Context and Motivation  
Large Language Models (LLMs) excel in various tasks but suffer from inefficiency due to their autoregressive token-by-token generation, which causes high latency and limited parallelism for long-text generation. **Speculative decoding** accelerates inference by using a lightweight "draft model" to generate candidate tokens in parallel, which are then verified by a target model. Recent advancements in diffusion-based speculative decoding further improve parallelism by leveraging block-level diffusion in dLLMs (diffusion language models), allowing multiple tokens to be generated per forward pass. However, a critical challenge remains: how to balance parallel speed and generation accuracy efficiently?  

#### 2. Limitations of Previous Methods  
Existing approaches assume a uniform block size for all inputs, inheriting the fixed configuration from training. This ignores input-specific variability—some inputs (e.g., structured tasks like code generation) benefit from larger blocks for efficiency, while others (e.g., open-domain generation) require smaller blocks to avoid error accumulation. Fixed block sizes lead to suboptimal performance. Additionally, while diffusion-based generation exhibits a local structure (optimal block sizes cluster around the training configuration), prior methods failed to exploit this, hindering optimization efficiency.  

#### 3. Proposed Solution  
The paper introduces **BlockPilot**, a sample-adaptive block size selection method. The key idea is to treat block size as a learnable policy rather than a static hyperparameter. After the target model completes the "prefilling" stage, BlockPilot uses the prediction distribution of the final token (which reflects context uncertainty and future stability) to train a lightweight predictor for inferring the optimal block size. This process is computationally cheap and seamlessly integrates into existing frameworks without modifying the draft or target models.  

#### 4. Key Differences from Prior Work  
BlockPilot’s innovations lie in:  
- **Reframing block size as a learnable component**: It demonstrates that fixed strategies are suboptimal across diverse inputs.  
- **Leveraging local structure**: Optimal block sizes cluster locally, reducing the problem to a low-dimensional decision space.  
- **Lightweight integration**: The predictor runs only once after prefilling, avoiding high overhead while maintaining compatibility.  

Experiments show BlockPilot achieves a 4.20× speedup on Qwen3-4B without compromising quality, validating the effectiveness of adaptive block size selection.

## Method, Figure by Figure

![Figure 4 : Overview of the BlockPilot inference pipeline. Given an input sequenc](fig4_1.webp)

> Figure 4 : Overview of the BlockPilot inference pipeline. Given an input sequence, the target LLM performs prefilling and produces the predictive distribution of the last token, which serves as a compact representation of the decoding state. This distribution is then fed into a lightweight block size predictor to determine an instance-specific block size. Based on the predicted block size, the diffusion-based draft model generates a block of draft tokens in parallel.

This figure provides an overview of the BlockPilot inference pipeline, illustrating the process from input sequences to the generation of draft tokens.

On the left side of the figure, there are two input sequences, labeled "Sample 1 Input Sequence" and "Sample 2 Input Sequence." Each input sequence consists of a series of "Input Tokens," which are fed into a large language model (LLM) referred to as the "LLM Target Model." The target model performs prefilling on the input sequences and produces a predictive distribution of the last token. This distribution serves as a compact representation of the decoding state and is subsequently used to determine an instance-specific block size.

Next, the predictive distribution of the last token from the target model is fed into a lightweight module called the "Block Predictor." The task of this module is to predict an instance-specific block size based on the representation from the prefilling stage. In the figure, we can see that the "Block Predictor" is connected to a section labeled "Sample-Adaptive Block Selection," which is responsible for selecting the appropriate block size based on the predicted block size. The figure shows two different block sizes, labeled "B₁" and "B₂," indicating that the method can select different block sizes for different input samples.

Then, based on the predicted block size, a diffusion-based draft model (dLLM Draft Model) generates a block of draft tokens in parallel. In the figure, the input to the draft model includes the last token and some tokens marked as "[mask]," which represent the draft tokens to be generated. The output of the draft model is a series of "Draft Tokens," which are generated in parallel, thus achieving acceleration.

The key to this approach is that BlockPilot enables sample-adaptive policy learning by predicting the optimal block size, thereby improving efficiency in diffusion-based speculative decoding. This method allows for dynamic adjustment of the block size based on the characteristics of each input sample, rather than using a fixed block size, thus enhancing the overall decoding performance.

In summary, this figure demonstrates how BlockPilot achieves sample-adaptive speculative decoding by combining the prefilling representation from the target model with a lightweight block size predictor, thereby improving efficiency while maintaining lossless acceleration.

---

![Figure 1 : Diffusion-based speculative decoding with a dLLM draft model. The dLL](fig1_1.webp)

> Figure 1 : Diffusion-based speculative decoding with a dLLM draft model. The dLLM proposes a block of tokens in parallel, while the target LLM verifies the block and accepts the longest consistent prefix.

This figure intuitively illustrates the workflow of diffusion - based speculative decoding, with the core being the collaboration between the **dLLM draft model** and the **LLM target model**. By analyzing the components and arrows in the figure, we can break down the process as follows:

### Components and Data Flow
1. **Input Layer**: On the far left is the input sequence, which contains known tokens (such as "The") and multiple masked ([mask]) positions. These [mask] positions are where the model needs to generate tokens, and the entire input sequence will be fed into the **dLLM draft model**.
2. **dLLM Draft Model**: This module (the orange rectangle) is responsible for **generating a block of candidate tokens in parallel** (the "cat", "sat", "on", "a", "mat" in the dashed - line box in the figure). The "parallel generation" here reflects the advantage of the diffusion model — it can generate multiple tokens at once in a single forward pass, rather than generating them one by one as in traditional methods, which greatly improves parallelism.
3. **Intermediate Transmission**: The token block generated by the dLLM is passed to the **LLM target model** (the blue rectangle). This step is a key connection in the "proposal - verification" process. The dLLM first proposes a set of possible tokens, and then the more powerful target model verifies them.
4. **LLM Target Model**: The task of this module is to **verify the token block generated by the dLLM** and accept the "longest consistent prefix" (that is, the longest sequence starting from the first token that is continuously verified as correct). From the output on the right side of the figure, "cat", "sat", "on", "a", and "mat" are all marked with a check mark (√), indicating that all tokens in this block are accepted by the target model and become part of the final output sequence.
5. **Verification (Verify) Arrow**: The arrow from the LLM target model to the right - side output represents the completion of the "verification" operation, confirming the validity of the token block generated by the dLLM and integrating these tokens into the final output.


### How the Method Works (Specifically)
This figure clearly shows the core logic of diffusion - based speculative decoding:
- **Parallel Generation**: As the "draft model", the dLLM uses the characteristics of the diffusion model to generate multiple tokens in parallel in a single forward pass (forming a token block), instead of generating them one by one, which improves the parallelism and speed of inference.
- **Verification and Acceptance**: The generated token block is sent to the LLM target model for verification. The role of the target model is to check whether these tokens are correct (or meet the expected output). The key here is "accepting the longest consistent prefix" — that is, starting from the beginning of the input, as many tokens as possible that are verified as correct by the target model are retained. In the figure, the entire block generated by the dLLM ( "cat", "sat", "on", "a", "mat") is accepted, indicating that all tokens in this block have passed the verification.
- **Efficiency Improvement**: By having the dLLM generate a token block in parallel and then having the target model verify it in batches, this method avoids the inefficiency of traditional methods that generate and verify one by one, achieving "lossless acceleration" (because the finally accepted tokens are correct and no errors are introduced). The diffusion - based version further optimizes parallelism because it can generate multiple tokens (a block) at once instead of single tokens.


### Conclusion (Inferred from the Figure)
This figure shows the basic workflow of diffusion - based speculative decoding: **the dLLM generates a token block in parallel → the LLM target model verifies and accepts the longest consistent prefix**. This method significantly improves inference efficiency through parallel generation and batch verification while ensuring the accuracy of the output (because only the tokens accepted by the target model will be retained). The example in the figure shows that the entire token block generated by the dLLM is accepted by the target model, indicating that all tokens in this block are correct in this scenario, thus achieving an efficient decoding process.

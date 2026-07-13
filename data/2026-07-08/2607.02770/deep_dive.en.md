# Gemma 4 Technical Report

[arXiv](https://arxiv.org/abs/2607.02770) · [HuggingFace](https://huggingface.co/papers/2607.02770) · ▲60

## Abstract (verbatim)

> We introduce Gemma 4, a new generation of open-weight, natively multimodal language models in the Gemma model family. Designed to advance compute efficiency and reasoning, the Gemma 4 model suite features dense and Mixture-of-Experts architectures, ranging from 2.3B to 31B parameters. Alongside improved vision and audio encoders for all model sizes, we propose a unified, encoder-free architecture for our 12B model, which ingests raw audio and image patches. Furthermore, we integrate a thinking mode, enabling Gemma models to generate reasoning traces prior to responding. We improve inference speed, memory, and compute efficiency, as well as long-context abilities through critical design choices. Gemma 4 establishes a leap in performance across STEM, multimodal, and long-context benchmarks, and rivals larger, frontier open models in human-rated tasks.

## Background

### Background Analysis  

**Technical Context**: The rapid advancement of large language models (LLMs) has created a demand for open-weight models that excel in multimodal understanding, reasoning, and computational efficiency. These technologies are critical for applications like intelligent assistants, education, healthcare diagnostics, and content creation, where models must process text, images, and audio while performing complex tasks (e.g., math, coding) and handling long documents. However, traditional models often struggle with multimodal integration, long-context memory limitations, and computational inefficiency.  

**Previous Limitations**: Earlier multimodal models relied on separate encoders (e.g., vision, audio), leading to memory fragmentation and high computational costs. Long-context tasks (e.g., document analysis) caused memory explosions in KV caches, slowing inference. Traditional reasoning methods underperformed in complex tasks, and computational constraints limited deployment on resource-constrained devices. Additionally, gaps existed between text and multimodal capabilities, hindering "native multimodal" performance.  

**Proposed Solutions**: Gemma 4 addresses these issues through several innovations:  
1. **Unified Encoder Architecture**: The 12B model processes raw audio and image data directly, eliminating separate encoders and reducing memory fragmentation.  
2. **Long-Context Optimization**: Techniques like sliding-window attention, RoPE positional encoding, and KV cache sharing minimize memory usage for long inputs.  
3. **Reasoning Enhancement**: A "thinking mode" generates step-by-step reasoning before responses, improving performance in math and coding tasks.  
4. **Computational Efficiency**: Multi-token prediction drafting and quantization-aware training boost inference speed while reducing memory footprint.  

**Key Differences**: Compared to prior work, Gemma 4 stands out by:  
- **Native Multimodal Support**: All model sizes handle text, images, and audio seamlessly, rather than relying on post-hoc fusion.  
- **Efficient Long-Context Handling**: Innovative attention mechanisms balance performance and memory usage.  
- **Openness and Practicality**: Quantized versions and an Apache 2.0 license enable flexible deployment and customization.  

These design choices make Gemma 4 competitive with state-of-the-art models in multimodal benchmarks and human evaluations while maintaining efficiency across diverse hardware environments.

## Method, Figure by Figure

![Figure 1: The autoregressive MTP drafter (blue blocks on the right) is fed activ](fig1_1.webp)

> Figure 1: The autoregressive MTP drafter (blue blocks on the right) is fed activations and KV cache from the main model (gray blocks).

This figure illustrates a key architectural design in Gemma 4, showing how an autoregressive MTP (Mixture-of-Experts or similar) drafter (blue blocks on the right) interacts with the main model (gray blocks on the left) to potentially enhance efficiency or reasoning capabilities. The diagram can be understood by examining its two main components and the flow of information between them:

**Left Section (Gray Blocks - Main Model):**
This part represents the "main flow" or "base model" of the system. Data starts from the bottom with the "Input Embedding" layer, passes through "Layer 1," "Layer 2," and then proceeds to "Last Prefilled Local Layer" and "Last Prefilled Global Layer." These "prefilled layers" likely handle previously provided context. Subsequently, data flows upwards through "Layer N-1" and "Layer N," and finally outputs results via the "Unembed + softmax" layer, corresponding to time step t2.

**Right Section (Blue Blocks - Autoregressive MTP Drafter):**
This part represents a parallel, potentially more efficient "drafter" or "reasoning engine."
1.  It also starts with an "Input Embedding" layer, but its input time steps are marked as "t2 / p1," "t3 / p1," etc. This suggests it processes input at a specific position (p1) while referencing information from the main model at different time steps (t2, t3).
2.  Data flows through a series of "MTP Layer" blocks, from "MTP Layer 1" to "MTP Layer 4." These layers are the core computational units of the drafter.
3.  Before the MTP layers and after "MTP Layer 4," there are "Concat + down-proj" (concatenation + down-projection) and "up-proj" (up-projection) operations. These operations likely adjust feature dimensions or integrate information.
4.  The final output of the drafter also goes through an "Unembed + softmax" layer.

**Information Flow and Interaction (Key Aspect):**
The core of this figure is to show the information exchange between the main model and the MTP drafter:
*   **From Main Model to MTP Drafter:** The red dashed arrows (labeled "attention" and "Last layer activation") clearly indicate that the MTP drafter receives information from the main model. Specifically, the outputs of the "Last Prefilled Local Layer" and "Last Prefilled Global Layer" are used as input to the MTP layers (via "Concat + down-proj"). Additionally, the "Last layer activation" from the main model is fed into various levels of the MTP layers (e.g., MTP Layer 1, 2, 3, 4). This implies that the MTP drafter leverages intermediate results or contextual information already computed by the main model, rather than computing everything from scratch.
*   **From MTP Drafter to Main Model (or Subsequent Processing):** The blue dashed arrows (e.g., from "up-proj" pointing towards a point in the main model) likely represent feedback from the MTP drafter's output or intermediate results back to the main model, or for generating the final output. For instance, the output of "MTP Layer 4" through "up-proj" might be combined with the main model's flow.

**Methodological Operation:**
The method revealed by this figure is that Gemma 4 utilizes an autoregressive MTP drafter to accelerate inference or enhance reasoning. This drafter does not operate independently but collaborates closely with the main model. It generates or refines its predictions by receiving "attention" information, last-layer activations, and outputs from prefilled layers of the main model. This design allows the MTP drafter to leverage computations already performed by the main model, thereby improving efficiency (e.g., reducing redundant calculations) or performance (e.g., using richer contextual information for reasoning). The concept of "thinking mode" mentioned in the abstract is likely related to this, where the drafter first generates a reasoning trace before providing a final answer. In this way, the model can optimize computational efficiency and reasoning capabilities while maintaining or improving performance.

In summary, the figure depicts a hybrid architecture where the main model provides context and intermediate results, and the autoregressive MTP drafter utilizes this information for more efficient or intelligent processing, with specific information flows (such as activations, KV cache, attention) between them.

---

![Figure 2: Image resizing. Here we use patch_size=16 , pooling_kernel_size=3 , ma](fig2_1.webp)

> Figure 2: Image resizing. Here we use patch_size=16 , pooling_kernel_size=3 , max_soft_tokens=10 . The image is thus first resized to 2 × \times 4 pooled patches (each of size 48 ​ px 2 48\text{px}^{2} ), which is the closest match that results in a sequence length below the targeted 10. The 72 patches (each of size 16 ​ px 2 16\text{px}^{2} ) are then processed by the vision encoder, the vision encoder representations are pooled 3 × 3 3\times 3 , and the resulting 8 soft tokens are processed by the LLM backbone.

This diagram illustrates the image preprocessing workflow (resizing and patching) used to prepare inputs for a visual encoder. The core concept is **"aspect ratio-preserving resizing + patching + pooling"** to accommodate the model's token length limitations. Here's a detailed breakdown:

### Components and Data Flow
- **Left: Original Image**  
  The image has dimensions of `572×1024 pixels` with an aspect ratio of `1:1.79` (height/width ≈ 1.79). This is the input image to be processed, containing visual content such as an otter in a spacesuit, a starry sky, and the Earth.

- **Middle: Processing Pipeline (Arrows and Parameters)**  
  Arrows indicate the "direction of image transformation," and the labeled parameters—`mostly aspect-preserving resize`, `k=3` (pooling kernel size, corresponding to `pooling_kernel_size=3` in the caption), `sl=10` (maximum soft tokens, corresponding to `max_soft_tokens=10`), and `ps=16` (patch size, corresponding to `patch_size=16`)—are key:  
  - First, the image undergoes **aspect ratio-preserving resizing** to adjust its dimensions to meet the target of "token length ≤ 10" (the number of tokens after subsequent patching is 8, close to 10).  
  - Then, combining `k=3` pooling and `ps=16` patching, the image is converted into a sequence of patches that the visual encoder can process.

- **Right: Processed Image**  
  The image has dimensions of `96×192 pixels` with an aspect ratio of `1:2` (height/width = 2). The image is divided into `8 tokens` (calculated as `72 patches`, with each patch being `16px²`). The `8 soft tokens` are the result of pooling (using `k=3` pooling, which reduces the representation of 72 patches to 8 tokens for LLM processing).

### Methodology (Flow from Left to Right)
1. **Original Image Input**: Dimensions `572×1024`, aspect ratio `1:1.79`, containing complex visual content (e.g., an otter in a spacesuit, a cosmic background).  
2. **Aspect Ratio-Preserving Resize**: Adjusts the image dimensions to ensure the number of tokens after patching and pooling is ≤ 10 (the caption specifies "closest match below 10," resulting in 8 tokens). The resized dimensions are `96×192` (aspect ratio `1:2`), ensuring that key visual features (e.g., the otter, cosmic scene) are retained while accommodating the model's input length limitations.  
3. **Patching**: Using `patch_size=16` (each patch is a 16×16 pixel square), the resized image is divided into `72 patches` (calculation: `96÷16=6` patches in width, `192÷16=12` patches in height, `6×12=72`). Each patch contains local visual information, serving as the input unit for the visual encoder.  
4. **Pooling**: Using `kernel_size=3` (a 3×3 pooling window), the visual representations of the 72 patches are pooled to produce `8 soft tokens`. Pooling reduces the sequence length (from 72 to 8) while retaining key features, making the output processable by the LLM's backbone (which typically handles shorter token sequences).

### Conclusion (Core Design of the Method)
This diagram showcases the **visual input preprocessing workflow** in the Gemma 4 model: "aspect ratio-preserving resizing" adapts to token length limitations, while "patching + pooling" converts high-resolution images into low-dimensional, short-sequence visual tokens. This design balances the integrity of visual information with the model's computational efficiency, enabling the visual encoder to process images efficiently while the LLM handles shorter token sequences for inference.

(Note: The label "8 tokens = 72 patches" indicates that the visual representations of 72 patches are pooled into 8 tokens, which are then fed into the LLM backbone for further processing.)

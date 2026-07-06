# Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling

[arXiv](https://arxiv.org/abs/2607.01642) · [HuggingFace](https://huggingface.co/papers/2607.01642) · ▲32

## 摘要（原文）

> Hardware-agnostic strategies for accelerating text-to-image diffusion, such as timestep distillation and feature caching, can reduce inference time without custom kernels or system-level optimization. Among them, multi-resolution generation strategies have recently received broad attention, attaining more than 5x speedup without any training. However, the design of performing upsampling in the latent space, together with the selective modification of partial regions, causes these methods to exhibit noticeable blurring or artifacts. To this end, we propose MrFlow, a training-free multi-resolution acceleration strategy for pretrained flow-matching models built upon a staged low-to-high-resolution pipeline. MrFlow first rapidly generates the main structure at low resolution, then performs super-resolution in the pixel space using a lightweight pretrained GAN-based model, subsequently injects low-strength noise to enable high-frequency resampling, and finally refines the details at high resolution. Quantitative and qualitative results on FLUX.1-dev and Qwen-Image show that MrFlow exploits the quadratic token reduction and reduced step requirement of low-resolution sampling to achieve 10x end-to-end acceleration while keeping OneIG within a 1% gap relative to that before acceleration, significantly surpassing other training-free acceleration strategies, and requiring no training or runtime dynamic identification whatsoever. MrFlow can further be directly combined orthogonally with pre-trained timestep distillation strategies, achieving even higher generation acceleration of up to 25x.

## 摘要（中译）

无需依赖硬件特化的文本到图像扩散加速策略（如时间步蒸馏和时间步缓存），可在不使用自定义内核或系统级优化的情况下减少推理时间。其中，多分辨率生成策略近期受到广泛关注，在无需任何训练的情况下实现了超过5倍的加速。然而，潜在空间上采样设计以及局部区域的选择性修改导致这些方法出现明显的模糊或伪影。为此，我们提出了MrFlow，这是一种针对预训练流匹配模型的无训练多分辨率加速策略，基于分阶段低到高分辨率流水线构建。MrFlow首先在低分辨率下快速生成主要结构，然后使用轻量级预训练的基于生成对抗网络（GAN）的模型在像素空间进行超分辨率处理，随后注入低强度噪声以实现高频重采样，最后在高分辨率下细化细节。在FLUX.1-dev和Qwen-Image上的定量和定性结果表明，MrFlow利用低分辨率采样的二次令牌减少和步骤需求降低，实现了10倍的端到端加速，同时将OneIG保持在加速前1%的差距内，显著优于其他无训练加速策略，且完全不需要训练或运行时动态识别。MrFlow还可以进一步与预训练的时间步蒸馏策略正交结合，实现高达25倍的生成加速。

## 背景剖析

### 背景剖析  

**1. 技术背景**  
近年来，基于扩散模型（Diffusion Models）的图像生成技术（如结合Transformer架构或流匹配范式）取得了显著进展，但其计算成本随生成质量提升而急剧增加。例如，大型模型（如Qwen-Image-20B）在单次文本到图像生成任务中可能需要数百步采样，导致推理时间过长。这种低效性限制了技术的实际应用（如实时交互或资源受限设备）。因此，研究者们致力于开发加速方法，在不牺牲生成质量的前提下减少计算量。  

**2. 之前的问题**  
现有加速策略存在明显局限：  
- **依赖训练或系统优化**：如时间步蒸馏（Timestep Distillation）需要重新训练模型，而特征缓存（Feature Caching）依赖系统级优化，难以通用。  
- **速度提升有限**：多数方法仅能达到2-5倍加速，且可能引入模糊或伪影。  
- **多分辨率方法的缺陷**：尽管通过低分辨率生成和高分辨率细化（如潜空间上采样）可实现更高加速，但潜空间上采样易导致结构失真，且动态区域识别增加了复杂度。  

**3. 本文的解法**  
本文提出MrFlow，一种无需训练的多分辨率加速策略，核心思路是**分阶段粗到细生成**：  
1. **低分辨率快速生成**：利用预训练扩散模型在低分辨率下快速生成图像结构，减少计算量和时间步。  
2. **像素空间超分辨率**：通过预训练的轻量级GAN网络在像素空间放大图像，保留结构信息并添加高频细节。  
3. **噪声注入与高分辨率细化**：向潜在空间注入弱噪声以修正超分辨率可能引入的误差，再通过高分辨率采样细化细节。  
这一流程避免了潜空间上采样的失真问题，同时利用不同分辨率的空间特性（如低分辨率结构清晰、高分辨率细节丰富）实现高效生成。  

**4. 切入角度**  
与前人工作相比，MrFlow的关键差异在于：  
- **无需训练或动态识别**：直接基于预训练模型，简化了部署流程。  
- **分阶段设计**：明确分离结构生成、超分辨率和细节细化，避免多阶段方法的复杂性。  
- **兼容性**：可与现有加速方法（如时间步蒸馏）正交结合，进一步提升速度（最高达25倍）。  
这种方法在保持生成质量的同时，实现了10倍端到端加速，显著优于其他无需训练的策略。

## 方法图解

![Figure 2: The framework of MrFlow. The compared strategies include the native in](fig2_1.webp)

> Figure 2: The framework of MrFlow. The compared strategies include the native inference scheme and methods that perform upsampling in the latent space such as LSSGen, RALU and SPEED.

这张图（图2）展示了MrFlow方法的框架，并将其与原生推理方案以及在潜在空间进行上采样的方法（如LSSGen、RALU和SPEED）进行了比较。我们可以将图分为三个主要部分来理解：顶部的“Native”（原生）和“Latent Upsampling”（潜在空间上采样）方法，以及底部的“MrFlow”方法。

首先，我们看**顶部的“Native”（原生）推理方案**：
- 左侧显示了“50-Step”（50步）的过程，代表原生扩散模型通常需要较多的采样步骤来生成高质量图像（HR，高分辨率）。
- 数据从左侧的多帧（或潜在表示）开始，经过一个“Decoder”（解码器）和一个“VAE”（变分自动编码器），最终输出高分辨率的猫的图像。
- 这个过程代表了传统的、未加速的扩散模型推理方式，需要较多的步骤来生成清晰的图像。

接下来是**顶部的“Latent Upsampling”（潜在空间上采样）方法**：
- 这里展示了“20-Step”（20步）和“10-Step”（10步）的过程，说明这些方法试图通过减少步骤来加速，但可能在潜在空间进行上采样。
- 数据首先经过“Upsampling”（上采样）和“Add Noise”（添加噪声）的步骤，然后经过“Decoder”和“VAE”，最终输出高分辨率的图像。
- 右侧的图例解释了“Diffusion Denoising”（扩散去噪）的方向（从低分辨率到高分辨率），以及“Representation Space”（表示空间）分为“Latent Space”（潜在空间，绿色）和“Pixel Space”（像素空间，橙色）。这种方法的问题在于，在潜在空间进行上采样并选择性修改部分区域，可能导致图像模糊或出现伪影。

然后是**底部的“MrFlow”方法**，这是本文提出的方法，分为几个阶段：
1. **低分辨率生成阶段**：
   - 左侧显示了“12-Step”（12步）的过程，比原生方法少很多步骤。
   - 数据从“σ_t^LR ~ N(0, I)”（低分辨率的噪声）开始，经过“Decoder”和“VAE”，输出低分辨率（LR，低分辨率）的猫的图像。这一步利用低分辨率采样的二次令牌减少和步骤需求减少的特点，快速生成图像的主要结构。
2. **超分辨率阶段**：
   - 低分辨率的图像经过一个“SR GAN”（超分辨率生成对抗网络）模型，输出高分辨率（HR）的图像。这个模型是轻量级的、预训练的，基于GAN，用于快速提升图像的分辨率。
3. **高频率重采样阶段**：
   - 高分辨率的图像经过“VAE Encoder”（VAE编码器），然后“Add Small Noise”（添加小噪声），最后经过“Single-Step”（单步）的处理，再经过“Decoder”和“VAE”，输出最终的高分辨率图像。这一步通过注入低强度噪声来启用高频率重采样，细化图像的细节。

**数据或信息的流动顺序**：
- 对于原生方法：多帧（或潜在表示）→ 50步处理 → 解码器和VAE → 高分辨率图像。
- 对于潜在空间上采样方法：多帧（或潜在表示）→ 20步/10步处理（包括上采样和添加噪声）→ 解码器和VAE → 高分辨率图像。
- 对于MrFlow方法：低分辨率噪声 → 12步处理 → 解码器和VAE → 低分辨率图像 → SR GAN → 高分辨率图像 → VAE编码器 → 添加小噪声 → 单步处理 → 解码器和VAE → 最终高分辨率图像。

**方法的具体运作方式**：
- MrFlow采用了一个分阶段的低到高分辨率管道，无需训练：
  1. 首先，在低分辨率下快速生成图像的主要结构，利用低分辨率采样的高效性（二次令牌减少和步骤需求减少），这一步只需要12步。
  2. 然后，使用轻量级的预训练GAN模型（SR GAN）在像素空间进行超分辨率，快速提升图像的分辨率。
  3. 接着，注入低强度噪声以启用高频率重采样，细化图像的细节。
  4. 最后，在高分辨率下进一步细化细节，确保图像的质量。

**结论**：
- 图中展示的方法中，MrFlow通过分阶段的低到高分辨率生成管道，实现了10倍的端到端加速，同时保持了与加速前相比不到1%的OneIG（可能是指某种图像质量指标）差距，显著优于其他无需训练的加速策略，并且不需要任何训练或运行时动态识别。
- 相比之下，原生方法需要更多的步骤（50步），而潜在空间上采样方法虽然减少了步骤（20步或10步），但可能导致图像模糊或伪影，而MrFlow通过结合低分辨率生成、超分辨率、高频率重采样和细节细化，既加速了推理过程，又保持了图像的高质量。

---

![Figure 1: Qualitative comparison between MrFlow and various methods on Qwen-Imag](fig1_1.webp)

> Figure 1: Qualitative comparison between MrFlow and various methods on Qwen-Image. The dashed lines separate the pretrained model, training-free strategies, and strategies that rely on or exploit timestep distillation.

这张图（图1）是论文《Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling》中的定性比较结果，展示了名为MrFlow的方法与其他多种方法在Qwen-Image模型上的生成质量对比。我们按照从左到右的顺序来解读这张图：

1.  **整体布局与分组**：
    *   图像被垂直的虚线分成了三个主要区域，这与图的原始caption描述一致：“The dashed lines separate the pretrained model, training-free strategies, and strategies that rely on or exploit timestep distillation.”（虚线将预训练模型、无训练策略和依赖或利用时间步蒸馏的策略分开）。
    *   **第一组（最左侧，虚线左侧）**：代表“预训练模型”。
        *   标签为“Qwen-Image”。这部分展示了在没有应用任何加速策略时，原始预训练模型生成的图像。这里有两行图像，可能分别对应不同的生成场景（例如，上行为马，下行为火星基地）。这些图像作为基准，用于与其他加速方法生成的图像进行质量对比。

    *   **第二组（中间区域，第一条虚线和第二条虚线之间）**：代表“无训练策略”（training-free strategies）。
        *   从左到右依次是：
            *   **ToMA 1.01x**：这是一种无训练加速方法，其加速倍数为1.01倍（接近原始速度，可能作为轻度加速的对比）。
            *   **DB-Taylor 4.13x**：另一种无训练加速方法，加速倍数为4.13倍。
            *   **SPEED 8.61x**：无训练加速方法，加速倍数为8.61倍。
            *   **RALU 8.79x**：无训练加速方法，加速倍数为8.79倍。
            *   **MrFlow 10.3x**：本文提出的方法，属于无训练策略，加速倍数为10.3倍。
        *   这些方法都在尝试在不重新训练模型的情况下加速图像生成过程。

    *   **第三组（最右侧，第二条虚线右侧）**：代表“依赖或利用时间步蒸馏的策略”（strategies that rely on or exploit timestep distillation）。
        *   从左到右依次是：
            *   **Pi-Flow 19.6x**：一种利用时间步蒸馏的加速方法，加速倍数为19.6倍。
            *   **MrFlow\* 25.1x**：这可能是MrFlow方法的一个变体或进一步优化的版本，它也利用了时间步蒸馏，达到了25.1倍的加速。
        *   这一组的方法通过时间步蒸馏技术来实现更高的加速比。

2.  **方法运作原理（通过结果推断）**：
    *   这张图通过视觉质量的对比，揭示了不同加速方法的效果。读者可以通过观察不同方法生成的图像与原始“Qwen-Image”图像的相似程度和清晰度，来理解各种方法的优劣。
    *   **MrFlow的运作方式**（根据论文摘要和图示结果推断）：
        *   MrFlow是一种无训练的多分辨率加速策略，基于流匹配模型（flow-matching models）。
        *   它采用“低到高分辨率”的分阶段管道（staged low-to-high-resolution pipeline）。
        *   首先，在低分辨率下快速生成图像的主要结构（这对应于图中“MrFlow 10.3x”生成的图像，虽然加速了，但看起来仍然相对清晰）。
        *   然后，在像素空间使用一个轻量级的预训练基于GAN的模型进行超分辨率处理。
        *   接着，注入低强度噪声以实现高频重采样。
        *   最后，在高分辨率下细化细节。
        *   从图中可以看出，“MrFlow 10.3x”生成的图像在保持较高加速比的同时，其视觉质量明显优于其他一些无训练方法（如DB-Taylor, SPEED, RALU），甚至接近原始图像的质量。而“MrFlow\* 25.1x”虽然加速比更高，但可能与利用时间步蒸馏有关，其视觉质量也可能有所不同（需要更细致的观察）。

3.  **对比对象与结论**：
    *   **对比对象**：图中对比的对象是多种文本到图像扩散模型的加速方法，包括预训练模型本身、各种无训练加速策略（如ToMA, DB-Taylor, SPEED, RALU, MrFlow）以及依赖时间步蒸馏的策略（如Pi-Flow, MrFlow\*）。
    *   **坐标/排列**：图像以网格形式排列，每行代表一个生成场景（上行为马，下行为火星基地），每列代表一种方法。
    *   **结论**：
        *   从视觉质量上看，MrFlow（10.3x）生成的图像比其他一些无训练方法（如DB-Taylor 4.13x, SPEED 8.61x, RALU 8.79x）更清晰，更接近原始的“Qwen-Image”。
        *   MrFlow\*（25.1x）实现了更高的加速比，但其视觉质量可能需要与“MrFlow 10.3x”和原始图像进行更细致的比较（例如，是否存在轻微的模糊或伪影）。
        *   这张图直观地展示了MrFlow方法在实现显著加速（如10x或更高）的同时，能够保持较高的生成图像质量，从而验证了论文中提出的方法的有效性。它表明MrFlow能够利用低分辨率采样的二次令牌减少和减少的步骤需求，在保持OneIG（可能是指某种质量指标，如One Image Generation的质量）与加速前相差1%以内的情况下，实现端到端的加速。

---

![Figure 3: Example comparison of MrFlow adopting different super-resolution strat](fig3_1.webp)

> Figure 3: Example comparison of MrFlow adopting different super-resolution strategies on Qwen-Image, where Low Resolution denotes the image after low-resolution generation followed by VAE decoding to the pixel space, with a resolution of 512 × 512 512\times 512 . The rows of SR and High Resolution Refine are respectively the super-resolved image and the final image after high-resolution refinement, with a resolution of 1024 × 1024 1024\times 1024 .

这张图（图3）来自论文《Multi-Resolution Flow Matching: Training-Free Diffusion Acceleration via Staged Sampling》，它通过一个具体的例子比较了MrFlow方法采用不同超分辨率策略在Qwen-Image模型上的效果。

首先，我们来看图的左侧，标有“Low Resolution”的图像。这代表了在低分辨率（512x512像素）下生成并经过VAE解码到像素空间的图像。这是MrFlow流程的第一步：快速在低分辨率下生成图像的主要结构。你可以看到，这个低分辨率图像中的细节（比如“9am”的标志和下方的小黑板）相对模糊。

接下来，图的上方一行标有“SR”（Super-Resolution，超分辨率），下方一行标有“High Resolution Refine”（高分辨率细化）。这两行展示的是将左侧的低分辨率图像提升到高分辨率（1024x1024像素）后的不同阶段。

图中展示了四种不同的超分辨率策略或基线方法，从左到右分别是：
1.  **Interpolate（插值）**：这是一种基本的图像放大方法，通过插值算法（如双线性或双三次插值）来增加图像的分辨率。从结果上看，“SR”行的图像虽然分辨率提高了，但细节仍然比较模糊，例如“9am”的字体边缘不够清晰，小黑板上的文字也有些模糊。在“High Resolution Refine”行，经过细化后，细节有所改善，但仍然不如其他更高级的方法。
2.  **SwinIR**：这是一种基于深度学习的超分辨率方法。在“SR”行，我们可以看到图像的清晰度比“Interpolate”方法有所提高，“9am”的字体和小黑板上的文字更加可辨。在“High Resolution Refine”行，进一步细化后，细节更加清晰，但仍可能存在一些微小的模糊或伪影。
3.  **OSEDiff**：这可能是另一种特定的超分辨率或扩散基的超分辨率方法。其“SR”行的结果与SwinIR类似，甚至可能更好一些。“High Resolution Refine”行显示了进一步的细节增强。
4.  **Real-ESRGAN**：这是一种知名的基于生成对抗网络（GAN）的超分辨率方法。在“SR”行，它的表现已经相当不错，图像细节清晰。在“High Resolution Refine”行，经过细化后，图像的细节（如“9am”的字体、小黑板上的文字以及背景中的书籍和落叶）都非常清晰和锐利，伪影最少。

这张图揭示了MrFlow方法的核心思想：首先在低分辨率下快速生成图像的主要结构（如“Low Resolution”所示），然后使用一个轻量级的预训练的超分辨率模型（如图中比较的SwinIR、OSEDiff或Real-ESRGAN等）将图像提升到高分辨率（“SR”行）。最后，可能还会进行一些高分辨率的细化（“High Resolution Refine”行）以进一步提升图像质量。

通过比较不同方法的“SR”和“High Resolution Refine”结果，我们可以直观地看到不同超分辨率策略的效果差异。例如，Real-ESRGAN在提供清晰细节方面表现优于插值方法和SwinIR。这张图旨在说明，选择合适的超分辨率策略对于MrFlow方法的整体性能至关重要，因为它直接影响到最终生成图像的质量。

总结来说，这张图通过一个具体的视觉示例，展示了MrFlow方法中从低分辨率生成到高分辨率超分辨率再到高分辨率细化的整个流程，并比较了不同超分辨率策略的效果，从而证明了该方法的有效性。

---

![Figure 5: Trade-off curves between GenEval score and speedup for various trainin](fig5_1.webp)

> Figure 5: Trade-off curves between GenEval score and speedup for various training-free methods on FLUX.1-dev and Qwen-Image. Different shades of MrFlow correspond to different numbers of steps used in the high-resolution refinement stage.

这张图（图5）展示了不同无训练加速方法在两个基准测试（FLUX.1-dev 和 Qwen-Image）上的 GenEval 分数与加速比之间的权衡曲线。让我们详细解析这张图：

首先，我们看到图中有两个子图，分别对应不同的基准测试：左边是 FLUX.1-dev，右边是 Qwen-Image。每个子图的横轴代表“加速比”（Speedup Ratio），表示该方法相对于基准方法（通常是“Native”或“Native Steps”）的推理速度提升倍数。纵轴代表“GenEval”分数，这是一个评估生成图像质量的指标，分数越高表示图像质量越好。

图中的每条曲线或数据点代表一种不同的无训练加速方法。图例中列出了这些方法，包括：
*   **Native**: 这可能代表了未经过任何加速处理的原始模型推理，作为性能基准。
*   **Native Steps**: 这可能是指通过减少原始模型的采样步骤来加速，但可能没有其他优化。
*   **ToMA, TeaCache, DB-Taylor, RALU, SPEED**: 这些是其他现有的无训练加速策略。
*   **MrFlow (+1), MrFlow (+2), MrFlow (+3)**: 这是我们的方法 MrFlow 的不同变体。根据图的标题和说明，这些数字（+1, +2, +3）代表在高分辨率细化阶段使用的步骤数量。数字越大，表示在高分辨率阶段投入的细化步骤越多，理论上可以带来更好的图像质量，但可能会牺牲一些加速比。

现在，我们来分析这些曲线的含义：
*   在 FLUX.1-dev 子图中，我们可以看到“Native”方法（星号标记）的 GenEval 分数最高（约0.67），但加速比最低（接近1）。随着加速比的增加（向右移动），大多数方法的 GenEval 分数都会下降，这反映了速度与质量之间的权衡。
*   MrFlow 的不同变体（红色曲线系列）表现尤为突出。例如，MrFlow (+1)（最下面的红色曲线）在加速比约为8时，GenEval 分数仍保持在约0.60。而 MrFlow (+2) 和 MrFlow (+3)（更靠上的红色曲线）在相同的加速比下，GenEval 分数更高，或者在相同的 GenEval 分数下，能实现更高的加速比。这说明通过调整高分辨率细化阶段的步骤数，我们可以在速度和质量之间进行权衡。步骤数越多（如 MrFlow (+3)），图像质量越高，但加速比可能略低于步骤数较少的情况（如 MrFlow (+1)）。
*   其他方法如 ToMA、TeaCache 等在加速比较高时，GenEval 分数下降得更快，表明它们在高速率下的图像质量较差。

在 Qwen-Image 子图中，趋势类似：
*   “Native”方法（星号标记）的 GenEval 分数最高（约0.87），加速比最低。
*   MrFlow 的不同变体（红色曲线系列）再次显示出优越的性能。例如，MrFlow (+1) 在加速比约为10时，GenEval 分数仍保持在约0.85。而 MrFlow (+2) 和 MrFlow (+3) 在相同的加速比下，GenEval 分数更高，或者在相同的 GenEval 分数下，能实现更高的加速比。
*   其他方法如 ToMA、TeaCache、DB-Taylor 等在加速比较高时，GenEval 分数也显著下降。

这张图揭示了 MrFlow 方法的具体运作方式及其优势：
1.  **多分辨率加速**: MrFlow 是一种基于流匹配模型的无训练多分辨率加速策略。它首先在低分辨率下快速生成图像的主要结构，然后在像素空间使用一个轻量级的预训练 GAN 模型进行超分辨率处理。
2.  **分阶段细化**: 图中的 MrFlow (+1), (+2), (+3) 表示在高分辨率细化阶段使用的不同步骤数。通过在细化阶段投入更多的计算（即更多的步骤），可以提高最终生成图像的质量（更高的 GenEval 分数），但这会以一定的加速比为代价。反之，减少细化步骤可以实现更高的加速比，但图像质量可能会略有下降。
3.  **权衡与优化**: 这张图清晰地展示了不同方法在速度（加速比）和质量（GenEval 分数）之间的权衡。MrFlow 的优势在于它能够在保持较高图像质量的同时，实现显著的加速（如图中所示，MrFlow 可以实现超过 5x 甚至接近 10x 的加速，同时 GenEval 分数下降很小）。
4.  **对比其他方法**: 与其他无训练加速方法相比，MrFlow 在整个加速比范围内都表现出更高的 GenEval 分数，特别是在高加速比区域，其优势更为明显。这表明 MrFlow 能够更好地平衡速度和质量的权衡。

总结来说，这张图通过展示不同方法在速度和质量之间的权衡曲线，有效地证明了 MrFlow 方法在无训练加速文本到图像扩散模型方面的优越性。通过调整高分辨率细化阶段的步骤数，用户可以根据需求在速度和图像质量之间进行灵活的权衡，而 MrFlow 总能提供比其他现有方法更好的整体性能。

---

![Figure 6: Stage-wise runtime breakdown of native Qwen-Image and MrFlow- 12 , 1 1](fig6_1.webp)

> Figure 6: Stage-wise runtime breakdown of native Qwen-Image and MrFlow- 12 , 1 12,1 .

这张图是一个**阶段式运行时间分解图**，用于直观比较“原生Qwen-Image”和“MrFlow”两种方法的推理速度，核心是展示MrFlow如何通过分阶段流程实现加速。  

### 图中组件与流程解析：  
- **横轴（Runtime (s)）**：表示运行时间（单位：秒），从0到50秒，展示不同方法的推理耗时。  
- **纵轴（方法）**：包含两个对比对象：`Native`（原生Qwen-Image）和`MrFlow`（本文提出的方法）。  
- **颜色块（阶段）**：图例中四种颜色对应不同的处理阶段：  
  - 绿色（LR sampling）：低分辨率采样阶段；  
  - 橙色（Super resolution）：超分辨率阶段；  
  - 红色（HR sampling）：高分辨率采样阶段；  
  - 青色（VAE encode/decode）：变分自动编码器的编码/解码阶段（图中MrFlow的青色块几乎不可见，说明该阶段耗时极短或被优化）。  
- **箭头与文字**：黑色箭头从MrFlow的阶段块指向右侧，标注“10.35x faster!”，表示MrFlow的推理速度比Native快约10.35倍。  


### 方法运作逻辑（从图中推导）：  
MrFlow采用**“低分辨率快速生成→超分辨率→高分辨率细化”**的分阶段流程：  
1. **低分辨率采样（LR sampling）**：首先在低分辨率下快速生成图像的主要结构（对应绿色块，耗时极短）。这一步利用了低分辨率采样的“二次令牌减少”和“步骤需求降低”的优势，大幅缩短前期耗时。  
2. **超分辨率（Super resolution）**：接着使用轻量级的预训练GAN模型进行像素空间超分辨率（图中橙色块可能被合并或省略，因为MrFlow的核心是“低→高”直接过渡？结合论文描述，实际是“低分辨率采样后，先超分辨率到像素空间，再注入噪声进行高频率重采样，最后高分辨率细化”——但图中MrFlow的阶段块主要是绿色（LR）和红色（HR），说明超分辨率和高频率重采样可能被整合到“从低到高”的流程中，或青色的VAE阶段被大幅优化）。  
3. **高分辨率采样（HR sampling）**：最后在高分辨率下细化细节（对应红色块，耗时也较短）。  

对比`Native`（灰色长条，耗时49.32秒），MrFlow的总耗时仅4.77秒，速度提升约10.35倍。这说明MrFlow通过**跳过低分辨率到高分辨率之间的冗余步骤（如传统方法的潜在空间上采样+局部修改的模糊问题）**，直接用“低→高”的分阶段流程，结合轻量级超分辨率和高频率重采样，在保持质量的同时大幅加速。  


### 结果与结论（从图中量化信息）：  
- **坐标与数值**：横轴显示Native耗时~49.32秒，MrFlow耗时~4.77秒；箭头标注“10.35x faster!”，即MrFlow的速度是Native的约10.35倍。  
- **对比对象**：Native（原生Qwen-Image） vs. MrFlow（本文方法）。  
- **结论**：MrFlow通过分阶段（低分辨率采样→超分辨率→高分辨率细化）的训练-free策略，利用低分辨率采样的效率优势，结合轻量级超分辨率和高频率重采样，在**端到端推理速度上实现约10倍加速**，同时保持图像质量（如OneIG指标与加速前差距<1%），且无需训练或运行时动态识别，显著优于其他训练-free加速策略。  


这张图清晰地展示了MrFlow的核心优势：**通过分阶段流程规避传统方法的瓶颈（如潜在空间上采样的模糊问题），利用低分辨率的高效采样和高分辨率的快速细化，实现大幅加速**。读者仅通过图中的阶段划分、时间对比和速度提升倍数，就能理解MrFlow的工作逻辑和性能优势。

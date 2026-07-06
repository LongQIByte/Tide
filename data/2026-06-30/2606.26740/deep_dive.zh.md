# LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing

[arXiv](https://arxiv.org/abs/2606.26740) · [HuggingFace](https://huggingface.co/papers/2606.26740) · ▲82

## 摘要（原文）

> Streaming video editing has made rapid progress, yet practical deployment is still limited by two core issues: maintaining stable backgrounds and non-edited regions over time, and achieving the low latency required for real-time interactive scenarios. Meanwhile, recent streaming video generation methods are mostly developed for synthesis and cannot be directly applied to editing due to the strict preservation requirement and region-specific control. In this work, we present a novel streaming video editing framework that performs causal, frame-by-frame editing with strong content preservation and real-time responsiveness. Our key design is a three-stage distillation pipeline that progressively transfers editing capability from a powerful bidirectional foundation model to an efficient unidirectional streaming editor, enabling stable long-horizon edits without sacrificing visual fidelity. To further support real-time deployment, we introduce an AR-oriented mask cache that reuses region-related computation across frames, substantially reducing redundant processing and accelerating inference. Finally, we establish a dedicated benchmark for streaming video editing. Extensive evaluations demonstrate that our method achieves state-of-the-art visual quality among streaming baselines while drastically boosting inference speed to 12.66 FPS, making it suitable for interactive and augmented reality applications.

## 摘要（中译）

流媒体视频编辑取得了快速进展，但实际部署仍受两个核心问题的限制：随着时间的推移保持稳定的背景和未编辑区域，以及实现实时交互场景所需的低延迟。与此同时，最近的流媒体视频生成方法主要是为合成而开发的，由于严格的保留要求和特定区域的控制，不能直接应用于编辑。在这项工作中，我们提出了一个新的流媒体视频编辑框架，该框架执行因果、逐帧编辑，具有强大的内容保留和实时响应能力。我们的关键设计是一个三阶段蒸馏管道，逐步将编辑能力从强大的双向基础模型转移到高效的单向流媒体编辑器，使得稳定的长距离编辑不会牺牲视觉保真度。为了进一步支持实时部署，我们引入了一个面向增强现实（AR）的掩码缓存，它在帧之间重用区域相关的计算，大大减少了冗余处理并加速了推理。最后，我们为流媒体视频编辑建立了一个专门的基准。广泛的评估表明，我们的方法在流媒体基线中实现了最先进的视觉质量，同时将推理速度大幅提高到12.66帧每秒（FPS），使其适用于交互式和增强现实（AR）应用。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
随着增强现实（AR）、直播和实时交互应用的普及，视频编辑正从传统的离线批量处理转向**实时流式编辑**。例如，在AR场景中，用户需要即时修改视频中的特定对象（如更换虚拟背景或调整物体颜色），同时保持背景稳定；在直播中，编辑需低延迟以支持互动操作（如实时添加特效）。这类技术的核心需求是：**在无未来帧信息的情况下，实现稳定、高质量且低延迟的逐帧编辑**。  

**2. 之前的问题与瓶颈**  
现有方法存在两大核心挑战：  
- **时间一致性不足**：传统视频扩散模型依赖双向或全局注意力来维持时序一致性，但直接应用于流式场景（仅能访问当前及历史帧）时，会因缺乏全局上下文导致“遗忘效应”或画面闪烁。  
- **计算冗余**：标准扩散流程将每帧视为独立生成任务，但对静态或线性运动的背景重复执行密集计算（如注意力机制），导致边缘设备无法实时处理。  

**3. 本文的解决思路**  
论文提出**分阶段蒸馏框架**和**AR导向掩码缓存**：  
- **三阶段蒸馏**：从强大的双向扩散模型（Bidirectional DiT）逐步蒸馏编辑能力到单向流式模型（Causal DiT）。第一阶段训练双向模型的编辑能力；第二阶段通过“教师强制”策略转为单向因果模型；第三阶段用分布匹配蒸馏（DMD）压缩推理步骤至4步，实现实时性（12.66 FPS）。  
- **掩码缓存**：通过计算编辑输出与源帧的距离动态提取掩码，复用静态区域的计算，减少冗余处理。  

**4. 与前人工作的关键差异**  
- **因果性与效率平衡**：不同于传统非因果模型，本文通过蒸馏保留编辑能力的同时适应流式约束。  
- **针对性优化**：聚焦流式场景的特定问题（如背景冗余），而非通用视频生成。  
- **基准测试**：首次建立流式视频编辑专用基准，验证方法在视觉质量、时序一致性和吞吐量上的优势。  

这一工作为实时交互和AR应用提供了实用化方案，填补了流式视频编辑从理论到部署的鸿沟。

## 方法图解

![Figure 4 : Visualization of the temporal consistency analysis and mask generatio](fig4_1.webp)

> Figure 4 : Visualization of the temporal consistency analysis and mask generation process. The left panels show (from top to bottom) the source video frames, the synthesized video frames, the computed difference matrices, and the resulting binary masks. The right panels display the statistical distributions of Temporal IoU and Pixel Difference across the sequence, with mean values of 0.016% and 0.126%, respectively, indicating high structural stability.

这张图（图4）来自论文《LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing》，它旨在可视化时间一致性分析和掩码生成过程，以展示该方法如何实现稳定的视频编辑。

图的结构分为左右两部分：

**左侧面板（流程可视化）：**
这部分从上到下展示了视频编辑过程中的关键步骤，按时间顺序（帧16、帧48、帧80）排列了三列，每一列代表视频中的一个特定帧。
1.  **第一行（Source Video）：** 显示原始视频的帧。这些是未经编辑的输入帧，作为后续处理的参考。
2.  **第二行（Synthetic Video）：** 显示经过该方法编辑后合成的视频帧。这些帧是基于原始帧进行编辑后的结果。
3.  **第三行（Difference Matrix）：** 显示源视频帧与合成视频帧之间的差异矩阵。这通常是一个热力图，用颜色（如蓝色表示小差异，红色或黄色表示大差异）来直观地展示两帧之间像素级别的变化。通过观察这些差异图，可以评估编辑操作引入的变化程度以及背景的稳定性。
4.  **第四行（Final Mask）：** 显示最终生成的二进制掩码。掩码通常是黑白图像，其中白色区域表示被编辑或需要关注的区域，黑色区域表示背景或未被编辑的区域。这个掩码用于指导编辑过程，确保只对特定区域进行修改，同时保持背景的稳定。

数据的流动顺序是：原始视频帧 -> 编辑生成新帧 -> 计算新旧帧差异 -> 根据差异或编辑目标生成掩码。

**右侧面板（统计分布）：**
这部分包含两个直方图，用于量化评估时间一致性和像素差异。
1.  **上图（Temporal IoU Distribution）：**
    *   **X轴（Pixel Change Rate %）：** 表示像素变化率，即两帧之间像素值发生变化的比例。
    *   **Y轴（Frequency）：** 表示具有特定像素变化率的帧的数量频率。
    *   **曲线和均值：** 红色虚线表示均值，图中标注均值为0.016%。这个分布显示了在视频序列中，帧与帧之间像素变化的统计情况。一个非常低的均值（0.016%）表明视频在时间上具有很高的结构稳定性，即编辑过程中背景和非编辑区域的变化非常小。
2.  **下图（Temporal Pixel Difference Distribution）：**
    *   **X轴（Pixel Change Rate %）：** 同样表示像素变化率。
    *   **Y轴（Frequency）：** 表示具有特定像素变化率的帧的数量频率。
    *   **曲线和均值：** 红色虚线表示均值，图中标注均值为0.126%。这个分布可能衡量的是另一种形式的像素差异（例如，绝对差异的总和或某种归一化后的差异）。尽管均值略高于IoU的均值，但0.126%仍然是一个非常小的数值，进一步证实了视频序列在时间上具有高稳定性。

**方法运作的揭示：**
这张图通过以下方式揭示了该方法的具体运作：
*   **时间一致性：** 左侧的差异矩阵和右侧的统计分布共同展示了该方法在编辑视频时能够保持高度的时间一致性。差异矩阵中的小差异区域（蓝色）和统计分布中的低均值表明，编辑操作对背景和非编辑区域的影响很小，从而实现了稳定的长时编辑。
*   **掩码生成：** 左侧的最终掩码展示了该方法如何识别和定位需要编辑的区域。通过生成这样的掩码，方法可以确保编辑操作仅限于特定区域，而不影响其他部分，这是实现内容保留的关键。
*   **流程有效性：** 整个流程（从原始帧到合成帧，再到差异分析和掩码生成）展示了方法如何一步步实现其目标：基于输入视频进行编辑，同时保持背景稳定。

**结论：**
这张图清晰地展示了论文中提出的方法如何通过一个三阶段的蒸馏流程和AR导向的掩码缓存等技术，实现稳定的、实时的基于扩散模型的流视频编辑。左侧的可视化流程展示了方法的具体步骤，而右侧的统计分布则量化了该方法在保持时间一致性方面的卓越表现（像素变化率均值非常低）。这证明了该方法在视觉质量和推理速度方面都达到了先进水平，适用于交互式和增强现实应用。

---

![Figure 3 : Overview of the proposed streaming video editing framework. Our appro](fig3_1.webp)

> Figure 3 : Overview of the proposed streaming video editing framework. Our approach features a three-stage distillation pipeline that transfers editing capabilities from a bidirectional DiT to a 4-step causal model. Furthermore, an AR-oriented Mask Cache accelerates real-time inference by dynamically decoupling computation and reusing tokens in unedited background regions.

这张图展示了《LiveEdit: Towards Real - Time Diffusion - Based Streaming Video Editing》论文中提出的流媒体视频编辑框架的概述，该框架通过一个三阶段蒸馏管道将编辑能力从双向DiT转移到单向因果模型，并引入了面向AR的掩码缓存来加速实时推理。

### 阶段1：基础调优以获取编辑能力（Stage 1: Foundation Tuning for Editing Ability Acquisition）
- **输入**：噪声输入（Noise Input）和文本指令（例如“Change the child's green sweater to a bright yellow one”）。文本指令首先被转换为文本嵌入（Text Embedding）。
- **模型组件**：双向DiT（Bidirect. DiT），其中包含全注意力（Full Attention）、前馈网络（FFN）模块、自注意力（Self - Attention）和交叉注意力（Cross - Attention）等组件（通过不同颜色的块表示）。还有一个火焰图标，可能表示训练过程中的计算或优化步骤。
- **损失函数**：均方误差损失（\(L_{MSE}\)），用于衡量生成的图像与目标图像之间的差异。
- **数据流动**：噪声输入和文本嵌入被输入到双向DiT中，经过处理后生成编辑后的图像。这个阶段的目的是让模型学习如何根据文本指令进行图像编辑，通过\(L_{MSE}\)损失来优化模型的编辑能力。

### 阶段2：教师强制以实现块级因果初始化（Stage 2: Teacher Forcing for Chunk - wise Causal Initial）
- **输入**：噪声输入（Noise Input）。
- **模型组件**：因果DiT（Causal DiT），其中包含因果注意力（Causal Attention）和掩码模型（Mask Model）等组件（通过不同颜色的块表示）。同样有火焰图标表示计算步骤。
- **损失函数**：均方误差损失（\(L_{MSE}\)）。
- **数据流动**：噪声输入被输入到因果DiT中，经过处理后生成图像。这个阶段使用教师强制的方法，可能是为了初始化模型的因果编辑能力，确保在流媒体视频编辑中能够逐帧进行稳定的编辑，通过\(L_{MSE}\)损失来优化模型的因果编辑行为。

### 阶段3：DMD用于流媒体视频编辑（Stage 3: DMD for Streaming Video Editing）
- **输入**：修剪后的噪声（Prune Noise）和真实的视频帧（例如孩子穿着绿色毛衣的图像）。
- **模型组件**：生成器（Generator），它进行4步的重噪声（Renoise）过程；还有假分数（Fake Score）和真实分数（Real Score）的计算模块，以及梯度\(\nabla_{\theta}L_{DMD}\)（用于优化模型）。
- **损失函数**：均方误差损失（\(L_{MSE}\)）和\(L_{DMD}\)（用于动态掩码蒸馏的损失）。
- **数据流动**：修剪后的噪声和真实帧被输入到生成器中，生成器经过4步重噪声后生成编辑后的帧。然后计算生成帧的假分数和真实帧的真实分数，通过\(L_{MSE}\)和\(L_{DMD}\)损失来优化生成器，以确保生成的帧在编辑的同时保持背景和非编辑区域的稳定性。

### 面向AR的掩码缓存（AR - oriented Mask Cache）
- **数据流动**：这个组件用于加速实时推理。它动态地解耦计算并在未编辑的背景区域中重用令牌。图中显示了不同的块（Chunk 0、Chunk 1等），每个块包含生成器、计算差异（Calculate difference）和生成器等步骤。还有一个“完整计算”和“部分计算”的对比，部分计算通过重用掩码（Extract Editing Token with Mask）来减少冗余处理，从而加速推理过程。

### 方法的整体运作方式
1. **阶段1**：双向DiT模型通过文本指令和噪声输入学习图像编辑能力，使用\(L_{MSE}\)损失进行优化，为后续的流媒体编辑提供基础的编辑能力。
2. **阶段2**：因果DiT模型通过教师强制的方法进行块级因果初始化，确保模型能够逐帧进行稳定的编辑，同样使用\(L_{MSE}\)损失进行优化。
3. **阶段3**：生成器通过修剪后的噪声和真实帧进行4步重噪声过程，结合假分数、真实分数和\(L_{DMD}\)损失来优化，以实现流媒体视频的编辑，同时保持背景和非编辑区域的稳定性。面向AR的掩码缓存通过重用未编辑背景区域的令牌来减少冗余计算，从而加速实时推理过程。

这个框架通过三阶段蒸馏管道将编辑能力从双向模型转移到单向因果模型，并通过掩码缓存加速实时推理，从而实现了稳定的长时编辑和实时交互能力。

---

![Figure 1 : Comparison of video editing paradigms. Unlike bidirectional models th](fig1_1.webp)

> Figure 1 : Comparison of video editing paradigms. Unlike bidirectional models that suffer from inefficient inference, and past streaming models that fail to preserve accurate unedited content, our proposed streaming editing model leverages a Causal DiT with a mask-guided cache mechanism to achieve high-fidelity and efficient editing.

这张图（图1）清晰地对比了三种不同的视频编辑范式，旨在突出本文提出的“流式编辑模型”（Streaming Editing Model）的优势。我们可以从上到下逐个分析这些范式：

1.  **最上方：双向编辑模型 (Bidirectional Editing Model)**
    *   **组件与流程**：这个模块展示了双向扩散变换器（Bid. DiT）的工作方式。它接收当前帧 \( F_t \) 以及其前后帧 \( F_{t-1} \) 和 \( F_{t+1} \) 的信息（由双向箭头表示）。这种模型通过参考前后文来编辑当前帧。
    *   **结果与问题**：右侧的示例显示，这种模型能够实现“精确编辑”（Accurate Editing），如图中猫的动作变化。然而，它存在一个显著的缺点：“推理效率低”（Efficiency Inference），用红色叉号标记。这意味着这种模型在实时性方面表现不佳，不适合需要快速响应的场景。

2.  **中间部分：以往的视频到视频流式模型 (Previous Video2Video Streaming Model)**
    *   **组件与流程**：这个模块展示了传统的流式视频生成模型。它按顺序处理帧，例如从 \( F_{t-1} \) 到 \( F_t \)，每个帧通过一个模型（用彩色方块表示）进行处理。这里的处理是单向的，主要依赖于前一帧的信息。
    *   **结果与问题**：右侧的示例显示，这种模型虽然具有“推理效率高”（Efficiency Inference）的优点（用绿色对勾标记），但“无法精确保留未编辑内容”（Accurate Editing），用红色叉号标记。如图中狗的编辑结果，其外观发生了较大变化，可能不是预期的精确编辑。

3.  **最下方：我们的方法：流式编辑模型 (Our Method: Streaming Editing Model)**
    *   **组件与流程**：这是本文提出的方法。它使用因果扩散变换器（Causal DiT），并且引入了一个关键的“掩码引导缓存机制”（mask-guided cache mechanism），图中用橙色的“cache”框表示。这个模型也是按帧处理，从 \( F_{t-1} \) 到 \( F_t \)，但关键的改进在于：
        *   **因果处理**：Causal DiT 意味着它主要依赖当前帧和之前帧的信息进行编辑，而不是像双向模型那样依赖未来帧。
        *   **缓存机制**：箭头从 \( F_{t-1} \) 的 cache 指向 \( F_t \) 的 cache，表明缓存的信息（可能是关于背景或未编辑区域）被跨帧重用，以减少冗余计算。
    *   **结果与优势**：右侧的示例显示，这种方法同时实现了“精确编辑”（Accurate Editing）和“推理效率高”（Efficiency Inference），两者都用绿色对勾标记。如图中人物衣服颜色的改变，编辑是精确的，同时处理速度也很快。

**方法运作机制总结**：
这张图揭示了本文方法的核心思想：通过结合因果处理（避免依赖未来帧以提高实时性）和掩码引导的缓存机制（重用跨帧的重复计算，如背景信息），来实现既精确又高效的流式视频编辑。它解决了双向模型的低效问题和传统流式模型的精确度不足问题。

**对比结论**：
图中通过三个并排的范式对比，明确指出：
*   双向模型：精确但低效。
*   以往流式模型：高效但不精确。
*   我们的流式编辑模型：既精确又高效。

这种对比直观地展示了本文方法在解决实时视频编辑中关键挑战方面的优势。

---

![Figure 5 : Qualitative comparison of streaming video editing performance. The so](fig5_1.webp)

> Figure 5 : Qualitative comparison of streaming video editing performance. The source videos and instructions are displayed at the top. While existing methods exhibit significant limitations, leading to structural collapse or an inability to accurately follow the text, our approach precisely modifies the target regions and preserves the visual quality and temporal coherence of the original scenes.

这张图（图5）是论文《LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing》中的定性比较结果，展示了不同流式视频编辑方法在处理两个不同编辑任务时的性能表现。我们的讲解将分为几个部分，帮助您理解图中的内容和信息流动。

**整体结构与信息流动：**

该图采用网格布局，展示了两个主要的编辑任务。每个任务占据图像的一半（左半部分和右半部分）。对于每个任务：

1.  **顶部行（Source Videos and Instructions）：** 这是输入部分。最上方的一行显示了原始视频的几帧（通常是连续的三帧），并附有文字说明，描述了期望的编辑操作。这些是所有方法处理的原始输入。
    *   **左侧任务：** 指令是“将中间女性的白色上衣更改为高领的深紫色上衣”（Change the white blouse of the central woman to a deep violet one with a high collar.）。图中显示了一个女性在不同角度下的几帧，她的上衣是白色的。
    *   **右侧任务：** 指令是“将服装上的花卉图案替换为深红色和金色的几何图案”（Replace the floral pattern on the outfit with a geometric design in deep crimson and gold.）。图中显示了一个男性在不同姿势下的几帧，他的服装是带有花卉图案的。

2.  **方法比较行：** 在源视频和指令下方，是不同编辑方法的输出结果。每种方法占据一行，并标有其名称（如LucyEdit, InsV2V, StreamV2V, Stream, Ours等）。每行显示了该方法对源视频进行编辑后的几帧结果。这些结果是按方法组织的，每一行对应一种方法。

**揭示的方法运作方式（通过比较理解）：**

这张图通过视觉对比，揭示了不同方法在实现编辑目标时的优劣，从而间接展示了论文中所提方法（Ours）的优势。论文的方法旨在解决流式视频编辑中的两个核心问题：**保持稳定背景和非编辑区域**以及**实现实时交互所需的低延迟**。

*   **左侧任务（上衣颜色更改）：**
    *   **LucyEdit:** 结果显示上衣颜色变成了紫色，但看起来比较单一，缺乏深度和质感，可能没有完全遵循“高领”的指令，或者与背景的融合不够自然。
    *   **InsV2V:** 上衣颜色变成了紫色，但似乎只影响了部分区域，或者颜色的分布不均匀，与原始图像的融合度不高。
    *   **StreamV2V:** 上衣颜色几乎没有变化，或者变化非常微小，未能有效执行编辑指令。
    *   **Stream:** 类似于StreamV2V，上衣颜色变化不明显。
    *   **Ours (我们的方法):** 结果显示上衣成功地变成了深紫色，并且具有高领设计。颜色的过渡自然，与背景的融合度较高，整体视觉质量较好。这表明我们的方法能够更精确地修改目标区域。

*   **右侧任务（服装图案替换）：**
    *   **LucyEdit:** 结果显示服装上的花卉图案被替换成了红色和金色的图案，但图案的细节和分布可能不够理想，或者颜色过于鲜艳，与人物皮肤的对比度处理得不够好。
    *   **InsV2V:** 结果显示服装上的花卉图案被替换成了红色和金色的几何图案，但图案的清晰度和自然度可能不如我们的方法，或者人物的皮肤色调受到影响。
    *   **VideoCoF:** 结果显示服装变成了单一的红色，没有明显的几何图案，完全偏离了编辑指令。
    *   **StreamV2:** 结果显示服装上的花卉图案被替换成了黄色和红色的图案，这与指令要求的“深红色和金色”以及“几何图案”有较大差距。
    *   **Ours (我们的方法):** 结果显示服装上的花卉图案被成功替换成了深红色和金色的几何图案。图案的细节清晰，颜色符合要求，并且与人物的皮肤和其他区域的融合自然。这表明我们的方法能够准确地遵循文本指令进行编辑。

**结论：**

从图中可以清楚地看到，与现有的其他方法（LucyEdit, InsV2V, StreamV2V, Stream, VideoCoF, StreamV2）相比，**我们的方法（Ours）在两个方面表现更优：**
1.  **精确性：** 我们的方法能够更准确地按照文本指令修改目标区域（如上衣颜色和服装图案）。
2.  **视觉质量和时间连贯性：** 我们的方法在修改目标区域的同时，更好地保留了原始场景的视觉质量（如颜色过渡自然、图案细节清晰）和时间连贯性（即视频帧与帧之间的内容变化平滑，没有明显的闪烁或断裂）。

正如图的原始caption所述：“现有方法表现出显著的局限性，导致结构崩溃或无法准确遵循文本，而我们的方法则精确地修改目标区域，并保留原始场景的视觉质量和时间连贯性。” 这张图通过直观的视觉对比，有力地支持了这一结论。

---

![Figure 7 : Distribution of token cosine similarity between consecutive denoising](fig7_1.webp)

> Figure 7 : Distribution of token cosine similarity between consecutive denoising step.

这张图展示了在“LiveEdit”这个实时流媒体视频编辑框架中，**连续去噪步骤之间的token余弦相似度分布**。我们来一步步解析：

1.  **图表类型与轴含义**：
    *   这是一个直方图（Histogram），用于展示数据的分布情况。
    *   X轴代表“Cosine Similarity”（余弦相似度），范围从0.0到1.0。余弦相似度衡量的是两个向量（在这里是token）之间的方向相似性，值越接近1表示两个token越相似，值越接近0表示越不相似。
    *   Y轴代表“Frequency”（频率），表示具有特定余弦相似度的token对出现的次数。

2.  **数据系列与对比对象**：
    *   图中有两条主要的分布曲线（用不同颜色的柱状图和虚线表示）：
        *   **蓝色虚线（Self-Attn, Mean: 0.893）**：代表“自注意力”（Self-Attention）机制下，连续去噪步骤之间token的余弦相似度分布。其平均值（Mean）为0.893。
        *   **红色虚线（FFN, Mean: 0.153）**：代表“前馈神经网络”（Feed-Forward Network, FFN）机制下，连续去噪步骤之间token的余弦相似度分布。其平均值为0.153。

3.  **分布解读与方法运作揭示**：
    *   **Self-Attn（自注意力）**：蓝色的分布主要集中在0.8到1.0之间，峰值接近0.9。这表明在使用自注意力的连续去噪步骤中，token之间保持了非常高的相似性。这意味着自注意力机制在处理过程中，能够较好地保留和传递信息，使得相邻步骤的token（可以理解为图像的局部特征表示）变化不大，从而有助于维持内容的稳定性和连贯性。高相似度也暗示了信息的连续性和一致性。
    *   **FFN（前馈神经网络）**：红色的分布主要集中在0.0到0.4之间，峰值大约在0.2左右。这表明在使用前馈神经网络的连续去噪步骤中，token之间的相似性较低。这意味着FFN在处理过程中，token的变化较大，可能更多地引入了新的信息或进行了更剧烈的变换。
    *   **方法运作的启示**：这张图揭示了“LiveEdit”框架中可能的一种设计选择或观察结果：**自注意力机制更倾向于保持token的稳定性（高相似度），而前馈神经网络则可能引入更多的变化（低相似度）**。在实时视频编辑任务中，保持非编辑区域和背景的稳定性至关重要。因此，图中高相似度的自注意力分布（Self-Attn）可能对应于框架中用于维持内容一致性的部分，而低相似度的FFN分布可能对应于需要进行编辑或生成新内容的部分，或者是框架中不同阶段的处理特性。通过这种对比，我们可以理解到，为了实现稳定的实时编辑，框架可能需要利用自注意力的强相关性来保留已有内容，同时可能通过其他机制（如条件控制）来引导FFN进行所需的编辑，或者在不同阶段选择性地使用这两种机制。

4.  **结论**：
    *   图表清晰地展示了在“LiveEdit”框架中，自注意力机制在连续去噪步骤中能够保持较高的token余弦相似度（平均0.893），而前馈神经网络的token相似度较低（平均0.153）。
    *   这一结果表明，自注意力机制有助于维持信息的连续性和稳定性，这对于实时视频编辑中保持背景和非编辑区域的稳定是非常重要的。这也支持了论文中提到的“strong content preservation”（强内容保留）的目标。

# Video Generation Models are General-Purpose Vision Learners

[arXiv](https://arxiv.org/abs/2607.09024) · [HuggingFace](https://huggingface.co/papers/2607.09024) · ▲11

## 摘要（原文）

> Driven by next-token prediction, NLP shifted from task-specific models into powerful generalist foundation models. What, then, is the equivalent catalyst needed to achieve a general-purpose model in computer vision? In this paper, we contend that large-scale text-to-video generation serves as a strong pre-training paradigm for computer vision, providing the necessary spatiotemporal priors, vision-language alignment, and scalability required for general visual intelligence. We introduce GenCeption, which leverages a pre-trained video generative diffusion backbone to define a feed-forward perception model, capable of performing various vision tasks steered by text instructions. Empirical results demonstrate that GenCeption achieves state-of-the-art performance across a diverse suite of tasks, including depth, surface normal, and camera pose estimation, expression-referring segmentation, and 3D keypoint prediction, often matching or surpassing specialized models (e.g. DepthAnything3, SAM3, D4RT, VGGT-Omega, Sapiens, David, Genmo, and Lotus-2). Furthermore, the video generative pretrained backbone outperforms alternative pretraining paradigms (e.g., V-JEPA, and Video MAE) under comparable settings. Importantly, GenCeption exhibits preliminary data and model scaling properties along with exceptional data efficiency, where it achieves comparable performance with leading models like D4RT and VGGT-Omega with 7 to 500 less training data. Finally, GenCeption also exhibits intriguing emergent behaviors: a model trained exclusively on synthetic human videos generalizes to real-world footage and out-of-distribution object categories (e.g., animals and robots). These findings suggest that video generation is not merely a synthesis tool, but a foundational path toward generalist vision intelligence for the physical world. Project page: https://genception.github.io

## 摘要（中译）

在下一个 token 预测的驱动下，自然语言处理（NLP）从特定任务的模型转向了强大的通用基础模型。那么，实现计算机视觉中的通用模型需要什么样的等效催化剂呢？在本文中，我们认为大规模文本到视频生成是计算机视觉的一种强大预训练范式，它提供了通用视觉智能所需的时空先验知识、视觉 - 语言对齐和可扩展性。我们引入了 GenCeption，它利用预训练的视频生成扩散主干网络来定义一个前馈感知模型，该模型能够通过文本指令执行各种视觉任务。实证结果表明，GenCeption 在一系列不同的任务中取得了最先进的性能，包括深度、表面法线、相机姿态估计、基于表达的分割和 3D 关键点预测，通常能与专业模型（例如 DepthAnything3、SAM3、D4RT、VGGT - Omega、Sapiens、David、Genmo 和 Lotus - 2）相媲美甚至超越它们。此外，在可比的设置下，视频生成预训练主干网络优于其他预训练范式（例如 V - JEPA 和 Video MAE）。重要的是，GenCeption 表现出了初步的数据和模型缩放特性以及出色的数据效率，在使用比 D4RT 和 VGGT - Omega 等领先模型少 7 到 500 倍的训练数据时，它能取得相当的性能。最后，GenCeption 还表现出有趣的涌现行为：一个仅在合成人类视频上训练的模型能够推广到真实世界的视频和分布外的对象类别（例如动物和机器人）。这些发现表明，视频生成不仅仅是一种合成工具，更是实现物理世界通用视觉智能的基础路径。项目页面：https://genception.github.io

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
计算机视觉的核心目标是让机器理解物理世界，例如识别物体、估计深度、分割场景或预测运动。这类技术在自动驾驶（感知环境）、机器人（操作物体）、医疗影像（分析病灶）等领域有迫切需求。然而，现有方法通常针对单一任务设计专用模型（如分割模型、深度估计模型），导致开发成本高且难以适应复杂场景。例如，自动驾驶系统需要同时处理目标检测、路径规划和障碍物规避，而传统方法需组合多个模型，效率低下。  

**2. 之前的问题与局限**  
过去十年，视觉模型依赖“任务特定”范式：每个任务（如目标检测、语义分割）都有独立架构和训练流程。这种方法的问题在于：  
- **缺乏统一性**：无法像自然语言处理（NLP）中的大语言模型（LLM）那样，用一个通用模型处理多样任务。  
- **忽视时空动态**：现有预训练方法（如掩码自编码器、对比学习）主要处理静态图像，未充分学习视频中的时间因果关系和物理规律（如物体运动、光影变化）。  
- **数据效率低**：专用模型需要大量标注数据，而视频数据的收集和标注成本远高于图像。  

**3. 本文的解决方案**  
论文提出“文本到视频生成”作为视觉预训练的新范式，核心思路是：  
- **利用生成模型学习通用视觉知识**：通过训练模型生成高保真视频，迫使其理解3D几何、物体持久性和物理交互等时空先验。  
- **结合视觉-语言对齐**：生成过程以文本为条件（如“一个人跑步”），使模型天然具备理解语言指令的能力。  
- **高效扩展**：视频生成模型可利用大规模无标注视频数据（如互联网内容），降低标注依赖，并通过扩散模型（Diffusion Model）实现高质量生成。  
论文提出的GenCeption模型进一步将预训练的视频生成 backbone 转换为通用感知模型，通过微调即可执行分割、深度估计、3D姿态预测等任务，无需修改架构。  

**4. 与前人工作的关键差异**  
与传统的“任务特定”方法或单一预训练范式（如VideoMAE、V-JEPA）相比，本文的突破在于：  
- **统一性**：用一个模型处理多种任务，而非为每个任务设计专用架构。  
- **时空建模**：通过视频生成显式学习时间动态，而不仅是静态图像特征。  
- **数据效率**：生成预训练模型仅需少量标注数据即可超越专用模型（如用7倍更少数据达到同等性能）。  
- **涌现能力**：模型在合成数据上训练后，可直接迁移到真实场景，并泛化到未见过的物体类别（如动物、机器人）。  

这一范式将视频生成从“内容合成工具”提升为“通用视觉智能的基础”，为物理世界的多模态理解提供了新方向。

## 方法图解

![Figure 5 : The "Rothko" Raymap as an example of adapting high-dimensional modal ](fig5_1.webp)

> Figure 5 : The "Rothko" Raymap as an example of adapting high-dimensional modal data into standard 3 RGB channels. This representation effectively compresses the camera’s multi-channel ray data by assembling rotation and translation components into a single three-channel map.

这张图（图5）展示了将高维模态数据（如相机的多通道射线数据）适配到标准3个RGB通道的“Rothko”射线图（Raymap）的示例。我们可以通过以下步骤理解这个过程：

1. **输入部分**：
    - 左侧有两个独立的矩形区域，分别标注为“Rotation Raymap”（旋转射线图）和“Translation Raymap”（平移射线图）。这两个区域代表了相机射线数据的两个关键组成部分：旋转和平移。从视觉上看，“Rotation Raymap”是一个上半部分为蓝紫色渐变、下半部分为绿色的矩形；“Translation Raymap”是一个全绿色的矩形（不过根据caption的解释，这里应该是两个不同的通道数据，可能视觉上的颜色是为了区分不同的组件）。
    - 这两个组件（旋转和平移射线图）是高维模态数据的两个部分，需要被整合到一个标准的3通道RGB图中。

2. **处理流程（箭头的意义）**：
    - 中间的箭头表示数据或信息的流动方向，即从左侧的两个独立射线图（旋转和平移）流向右侧的“Rothko”射线图。这个箭头代表了将旋转和平移组件组装（assemble）成一个单一的三通道图的过程。

3. **输出部分（“Rothko”射线图）**：
    - 右侧的“Rothko”射线图是一个包含蓝紫色渐变背景和一个绿色矩形的图像。根据caption的解释，这个图是通过将旋转和平移组件组装到一个单一的三通道图中得到的。这里的绿色矩形可能代表了平移组件的信息，而背景的蓝紫色渐变代表了旋转组件的信息，或者是两者组合后的结果。这个三通道图有效地压缩了相机的多通道射线数据，将其转换为标准的RGB格式，便于后续的处理或分析。

**方法的具体运作方式**：
这张图展示了如何将相机的多通道射线数据（旋转和平移组件）转换为标准的3通道RGB图像（“Rothko”射线图）。具体来说，首先获取相机的旋转射线图（包含旋转相关的多通道数据）和平移射线图（包含平移相关的多通道数据），然后将这两个组件组装（combine）成一个单一的三通道图。这个过程有效地压缩了高维的射线数据，使其能够被表示为标准的RGB格式，从而可以利用现有的基于RGB的视觉模型或方法进行处理。这种转换使得高维的模态数据能够被适配到标准的视觉处理框架中，为后续的视觉任务（如论文中提到的深度估计、表面法线估计等）提供了基础。

**结论**：
通过这种方式，“Rothko”射线图能够有效地压缩相机的多通道射线数据，将旋转和平移组件组装到一个单一的三通道图中，从而实现了高维模态数据到标准RGB通道的适配。这种方法为处理高维视觉数据提供了一种有效的方式，使得这些数据能够被用于各种基于RGB的视觉任务中。

---

![Figure 4 : Architecture overview of GenCeption, a simple yet powerful architectu](fig4_1.webp)

> Figure 4 : Architecture overview of GenCeption, a simple yet powerful architecture adapted from text-to-video diffusion models. Given an input video and a text prompt specifying the desired output, our unified model, trained majorly on synthetic data, is capable of performing a wide range of dense and sparse perception tasks, with a single forward-pass of the model. The dense vision tasks are unified in the RGB ambient space where supervision can be applied in latent space efficiently, and the sparse vision tasks are realized by adding learnable tokens as additional inputs to the diffusion transformer (DiT).

这张图展示了GenCeption模型的架构概述，该模型是一个简单但功能强大的架构，改编自文本到视频扩散模型。以下是对图中各个组件、信息流动以及方法运作的详细讲解：

### 输入部分
- **输入视频（Input Video）**：这是模型的原始视频输入，例如图中显示的一个包含大猩猩的视频片段。视频数据首先被送入视频编码器（Video Encoder）。
- **文本提示（Text Prompt）**：这是一个描述期望输出的文本，例如“目标分割”等。文本提示被送入文本编码器（Text Encoder）。

### 编码部分
- **视频编码器（Video Encoder）**：该组件将输入视频转换为视频令牌（Video Tokens）。这些令牌是视频数据的压缩表示，捕捉了视频的时空信息。
- **文本编码器（Text Encoder）**：该组件将文本提示转换为文本令牌（Text Tokens）。这些令牌是文本数据的压缩表示，捕捉了文本的语义信息。

### 预训练部分
- **预训练的DiT（Pretrained DiT）**：这是模型的核心部分，是一个预训练的视频生成扩散变换器（Diffusion Transformer）。它接收视频令牌和文本令牌作为输入，并进行联合处理。在这个阶段，模型利用大规模的文本到视频生成数据进行预训练，学习到丰富的时空先验知识和视觉-语言对齐信息。

### 解码部分
- **视频解码器（Video Decoder）**：对于密集视觉任务，预训练的DiT输出的视频令牌被送入视频解码器，将其转换回视频形式，以生成所需的输出，例如法线视频、深度视频、前景分割视频等。
- **多层感知机（MLP）**：对于稀疏视觉任务，预训练的DiT输出的可学习令牌（Learnable Tokens）被送入多层感知机（MLP），以生成所需的输出，例如2D关键点、3D关键点和相机姿态等。

### 任务部分
- **密集视觉任务（Dense Vision Tasks）**：这些任务包括法线视频、深度视频、前景分割视频、开放词汇分割视频、密集姿态视频和相机光线视频。这些任务在RGB环境空间中统一处理，监督可以在潜在空间中高效应用。
- **稀疏视觉任务（Sparse Vision Tasks）**：这些任务包括2D关键点、3D关键点和相机姿态。这些任务通过将可学习令牌作为额外输入添加到扩散变换器（DiT）中来实现。

### 信息流动顺序
1. 输入视频被视频编码器转换为视频令牌。
2. 文本提示被文本编码器转换为文本令牌。
3. 视频令牌和文本令牌被送入预训练的DiT进行处理。
4. 对于密集视觉任务，预训练的DiT输出的视频令牌被送入视频解码器，生成相应的视频输出。
5. 对于稀疏视觉任务，预训练的DiT输出的可学习令牌被送入MLP，生成相应的输出。

### 方法运作方式
GenCeption模型通过利用预训练的视频生成扩散变换器（DiT）来定义一个前馈感知模型。该模型主要在合成数据上进行训练，能够通过单次前向传播执行各种密集和稀疏感知任务。通过将文本提示与视频数据一起输入模型，GenCeption能够根据文本指令生成所需的输出。这种方法利用了大规模文本到视频生成的预训练范式，提供了必要的时空先验知识、视觉-语言对齐和可扩展性，以实现通用的视觉智能。

### 结果部分（虽然图中没有明确的结果展示，但根据论文摘要可以推断）
- **性能表现**：GenCeption在各种任务上实现了最先进的性能，包括深度估计、表面法线估计、相机姿态估计、表达指代分割和3D关键点预测，通常匹配或超过专门的模型。
- **预训练范式的比较**：预训练的视频生成骨干网络在可比设置下优于其他预训练范式，如V-JEPA和Video MAE。
- **数据和模型缩放属性**：GenCeption表现出初步的数据和模型缩放属性，以及卓越的数据效率，在使用比领先模型少7到500倍的训练数据时，能够实现相当的性能。

通过这张图，我们可以清楚地看到GenCeption模型的架构和工作流程，以及它如何利用预训练的视频生成扩散模型来实现各种视觉任务。

---

![Figure 1 : Methdology (Left): GenCeption treats a video generative diffusion mod](fig1_1.webp)

> Figure 1 : Methdology (Left): GenCeption treats a video generative diffusion model as a pre-training base to capture rich spatio-temporal world priors and native vision-language alignment at scale. During multi-task post-training , the model is adapted to feed-forward model fine-tuned on predominantly synthetic data to handle diverse perception tasks. GenCeption shows strong performance with intriguing Emerging Behaviors , enabling seamless sim-to-real transfer and generalization to out-of-distribution object categories. Paradigm Shift (Right): This highlights a paradigm shift from specialized task-specific computer vision models, to fully unified generalist vision models.

这张图（图1）来自论文《Video Generation Models are General-Purpose Vision Learners》，它清晰地展示了**GenCeption方法的核心逻辑**以及**计算机视觉从“专用任务模型”到“通用视觉模型”的范式转变**。我们可以将图分为左右两个主要部分来理解：

### 左侧：方法流程（Methodology）

左侧部分详细描述了GenCeption方法的具体实施步骤，分为三个关键阶段，数据或信息的流动顺序如下：

1.  **视频生成预训练（Video Generative Pre-training）**：
    *   **组件**：一个标记为“DIT”（可能是指Diffusion-based Image/Video Transformer或类似架构）的绿色模块，旁边有一个“Iterative Denoising”（迭代去噪）的标注和一个视频帧的示例。还有一个“Prompt: A gorilla approaches waving hand”（提示词：一只大猩猩挥手靠近）的文本框。
    *   **含义**：这一阶段是GenCeption的基础。它使用一个预训练的视频生成扩散模型（DIT）作为“预训练基座”。这个模型通过大规模的视频数据学习丰富的**时空世界先验知识**（如物体运动、物理规律等）和**原生的视觉-语言对齐能力**（因为使用了文本提示来指导生成）。箭头表示数据或信息从文本提示和潜在的噪声输入开始，经过DIT的迭代去噪过程，生成符合提示的视频内容。这个过程捕捉了世界的时空动态。

2.  **多任务后训练（Multi-Task Post-training with Synthetic data）**：
    *   **组件**：同样是一个“DIT”模块，但下方连接了一个“Single Step”（单步）处理，然后输出到多个不同的感知任务示例，如“Depth”（深度估计）、“Normal”（表面法线估计）、“Segmentation”（分割）、“Pose”（姿态估计）等。还有一个“Prompt: Depth | Normal | Segmentation | Pose ...”（提示词：深度 | 表面法线 | 分割 | 姿态...）的文本框。任务示例包括彩色图像、伪彩色编码的深度图、分割掩码等。
    *   **含义**：在预训练之后，GenCeption模型通过**主要基于合成数据的多任务后训练**进行适应，成为一个前馈感知模型。这意味着模型被微调以处理各种不同的视觉感知任务。箭头表示预训练的DIT模型接收新的文本提示（指定任务类型），然后通过单步处理直接输出针对该任务的预测结果。这个阶段将通用的时空先验知识转化为特定任务的能力。

3.  **通用视觉模型与新兴行为（General-Purpose Vision Model with Emerging Behaviors）**：
    *   **组件**：这部分展示了GenCeption模型在实际应用中的表现。包含几个小的子图，如“50% Performance on Out-of-Distribution Tasks”（分布外任务上的50%性能）、“Zero-Shot Generalization to Novel Objects”（零样本泛化到新物体）、“Generalization to Unseen Object Categories”（泛化到未见过的物体类别）等。这些子图展示了模型在未见过的数据或任务上的表现。
    *   **含义**：这一阶段展示了GenCeption作为通用视觉模型的强大性能和“新兴行为”。所谓“新兴行为”指的是模型在训练时未明确学习但能够表现出的能力，例如：
        *   **强大的泛化能力**：能够在分布外任务上取得不错的性能。
        *   **零样本泛化**：能够识别训练时未见过的物体。
        *   **类别泛化**：能够处理训练时未见过的物体类别。
        *   **无缝的模拟到真实迁移**：能够将在合成数据上学习的知识迁移到真实世界数据上。

### 右侧：范式转变（Paradigm Shift）

右侧部分通过四个象限对比了计算机视觉中不同类型的模型，揭示了从“专用任务模型”到“通用视觉模型”的转变：

1.  **专用视觉模型（Specialized Vision Model）**：
    *   **结构**：多个任务（Task 1, Task N）各自拥有独立的“Head”（模型头部，负责特定任务的输出）和“Backbone”（模型主干，负责特征提取）。
    *   **含义**：传统的计算机视觉方法是为特定任务设计的，每个任务都有自己的模型架构。这意味着需要为每个新任务设计和训练一个全新的模型，效率低下且缺乏泛化能力。箭头表示每个任务独立处理。

2.  **专用头视觉模型（Specialized-Head Vision Model）**：
    *   **结构**：多个任务（Task 1, Task N）共享一个“Unified Backbone”（统一主干），但每个任务仍有自己独立的“Head”。
    *   **含义**：这是一种改进，通过共享主干来提取通用特征，然后为每个任务添加特定的头部。这提高了效率，但任务之间仍然相对独立。

3.  **专用损失视觉模型（Specialized-Loss Vision Model）**：
    *   **结构**：多个任务（Task 1, Task N）共享一个“Unified Head”（统一头部），但每个任务可能有不同的损失函数（Loss 1, Loss N），并且共享一个“Unified Backbone”。
    *   **含义**：这种模型尝试在头部层面进行统一，使用不同的损失函数来处理不同任务。这进一步促进了任务间的共享，但可能仍然受限于单一的头部设计。

4.  **统一视觉模型（Unified Vision Model (Ours)）**：
    *   **结构**：所有任务（Task 1, Task N）都共享一个“Unified Head”和一个“Unified Backbone”。
    *   **含义**：这是GenCeption所代表的**通用视觉模型**。它使用一个统一的模型主干来提取特征，并使用一个统一的模型头部来处理所有任务，通常由文本提示来指导。这种架构能够利用跨任务的共享知识，实现更强的泛化能力和效率。箭头表示所有任务都通过同一个统一模型进行处理。

### 总结

这张图清晰地阐述了GenCeption方法的核心思想：**利用大规模文本到视频生成模型作为预训练基础，捕获丰富的时空先验和视觉-语言对齐能力，然后通过多任务后训练将其转变为一个能够处理多种视觉任务的通用前馈模型**。右侧的范式转变图则强调了这种从专用模型到统一通用模型的进步，展示了GenCeption如何通过单一模型处理多种任务，从而实现更高效、更强大的视觉智能。图中的“新兴行为”部分进一步证明了这种方法的有效性和潜力。

---

![Figure 2 : SOTA Generalist Capability (Left): GenCeption achieves universally co](fig2_1.webp)

> Figure 2 : SOTA Generalist Capability (Left): GenCeption achieves universally competitive performance on a wide range of vision tasks, matching or outperforming state-of-the-art models dedicated to individual tasks (e.g. DepthAnything3 [ lin2025depth ] , SAM3 [ carion2025sam ] , D4RT [ zhang2025efficiently ] , VGGT- Ω \Omega [ wang2026vggt ] , Sapiens [ sapienseccv2024 ] , David [ saleh2025david ] , Genmo [ genmo2025 ] , Lotus-2 [ he2025lotus ] ). Our specialist denotes a model trained on each task individually, whereas the generalist represents a single model trained jointly across multiple tasks. Data Efficiency in Finetuning (Right): Validated on depth estimation, the video generative pretrained backbone (i) outperforms the largest available variants alternative pretraining paradigms (e.g., V-JEPA, and VideoMAE V2) under the same finetuning data. (ii) exhibits preliminary scaling properties, where the performance improves with more data and large model size; (iii) shows exceptional data efficiency, achieving comparable performance with leading models like D4RT [ zhang2025efficiently ] and VGGT- Ω \Omega [ wang2026vggt ] with 7 × \times to 500 × \times less training data.

这张图来自论文《Video Generation Models are General - Purpose Vision Learners》，分为左右两个部分，用于展示所提出的GenCeption方法在视觉任务上的通用能力和数据效率。

### 左侧：SOTA通用能力（SOTA Generalist Capability）
这是一个雷达图（极坐标图），用于展示不同视觉任务上的性能表现。图中的每个轴代表一个特定的视觉任务，包括：
- **Depth - KITTI (AbsRel)**：KITTI数据集上的深度估计任务，使用绝对相对误差（AbsRel）作为评估指标。
- **Depth - Sintel (AbsRel)**：Sintel数据集上的深度估计任务，同样使用AbsRel。
- **Normals - Hi4D (mAE)**：Hi4D数据集上的表面法线估计任务，使用平均绝对误差（mAE）。
- **Normals - Sintel (mAE)**：Sintel数据集上的表面法线估计任务，使用mAE。
- **3D Keypoint - EMDB (MPJPE)**：EMDB数据集上的3D关键点估计任务，使用平均关节位置误差（MPJPE）。
- **Exp Refer Seg - Mevis (J&F)**：Mevis数据集上的表达指代分割任务，使用J&F指标（可能是联合和分割的某种组合）。
- **Exp Refer Seg - RefDavis (J&F)**：RefDavis数据集上的表达指代分割任务，使用J&F指标。
- **Fore Seg - PhotoMatte (MSE)**：PhotoMatte数据集上的前景分割任务，使用均方误差（MSE）。
- **Camera Pose - Sintel (ATE)**：Sintel数据集上的相机姿态估计任务，使用绝对轨迹误差（ATE）。

图中有两种模型的性能曲线：
- **Ours Specialist（绿色实线）**：表示针对每个任务单独训练的模型（即任务特定的专家模型）的性能。
- **Ours Generalist（绿色虚线）**：表示GenCeption模型，它在多个任务上联合训练（即通用模型）的性能。

从图中可以看出，GenCeption的通用模型（Ours Generalist）在大多数任务上的性能接近或超过了对应的任务特定专家模型（Ours Specialist），并且还超过了其他现有的最先进（SOTA）模型，如DepthAnything3、SAM3、D4RT、VGGT - Ω、Sapiens、David、Genmo、Lotus - 2等。这表明GenCeption作为一个通用视觉模型，能够在多种不同的视觉任务上表现出色，验证了其通用性。

### 右侧：微调中的数据效率（Data Efficiency in Finetuning）
这是一个散点图，用于展示在深度估计任务上，不同模型在不同训练数据量下的性能（以AbsRel为指标，值越低表示性能越好）。横轴是**Unique Training Frames (Log Scale)**（唯一的训练帧数，对数刻度），范围从100K到1B（10亿）；纵轴是**AbsRel (Lower is Better)**（绝对相对误差，值越低性能越好），范围从0.04到0.30。

图中的数据点代表不同的模型及其对应的训练数据量和AbsRel值：
- **Ours（不同变体）**：表示GenCeption模型的不同变体，例如：
  - Ours (V - JEPA v2 1B, 0.9M frames)：使用V - JEPA v2预训练，10亿参数，0.9百万训练帧。
  - Ours (VideoMae v2 1B, 0.9M frames)：使用VideoMae v2预训练，10亿参数，0.9百万训练帧。
  - Ours (WAN 1.3B, 0.9M frames)：使用WAN预训练，13亿参数，0.9百万训练帧。
  - Ours (WAN 1.3B, 1.23M frames)：使用WAN预训练，13亿参数，1.23百万训练帧。
  - Ours (WAN 14B, 0.9M frames)：使用WAN预训练，140亿参数，0.9百万训练帧。
  - Ours (WAN 14B, 1.23M frames)：使用WAN预训练，140亿参数，1.23百万训练帧。
  - Ours (V - JEPA v2 1B, 86M frames)：使用V - JEPA v2预训练，10亿参数，86百万训练帧。
- **其他SOTA模型**：
  - D4RT (DINOv2 1.13B, 200M frames)：D4RT模型，使用DINOv2预训练，13亿参数，2亿训练帧。
  - VGGT Omega (DINOv3 1B, 600M frames)：VGGT - Ω模型，使用DINOv3预训练，10亿参数，6亿训练帧。

从图中可以得出以下结论：
1. **超越替代预训练范式**：GenCeption的视频生成预训练骨干（即Ours的不同变体）在相同的微调数据量下，性能优于其他替代预训练范式（如V - JEPA和VideoMAE V2）的最大可用变体。例如，在0.9百万训练帧时，GenCeption的AbsRel值低于V - JEPA v2 1B和VideoMae v2 1B的对应值。
2. **初步的缩放特性**：性能随着更多的数据和更大的模型尺寸而提高。例如，当模型从WAN 1.3B增加到WAN 14B，或者训练帧数从0.9M增加到1.23M时，AbsRel值降低（性能提高）。
3. **卓越的数据效率**：GenCeption能够使用比领先的SOTA模型（如D4RT和VGGT - Ω）少7倍到500倍的训练数据，达到相当的性能。例如，Ours (WAN 1.3B, 0.9M frames)的AbsRel值与D4RT (DINOv2 1.13B, 200M frames)相当，但训练数据量仅为后者的约0.45倍（0.9M vs 200M），或者说使用了更少的数据（7倍左右的减少，因为200M / 0.9M ≈ 222，可能论文中的7×到500×是近似值）。

### 方法的运作方式（从图中推断）
GenCeption利用预训练的视频生成扩散骨干网络来定义一个前馈感知模型，该模型可以通过文本指令来执行各种视觉任务。从左侧的雷达图可以看出，通过在多个任务上联合训练（通用模型），GenCeption能够在不同的视觉任务上获得竞争力，甚至超过任务特定的专家模型。这表明视频生成预训练提供了必要的时空先验、视觉 - 语言对齐和可扩展性，使得模型能够泛化到多种视觉任务。从右侧的数据效率图可以看出，GenCeption的预训练骨干在微调时，即使使用较少的数据，也能达到或超过其他预训练范式的性能，这验证了其预训练范式的有效性。

总结来说，这张图展示了GenCeption作为通用视觉模型的两个关键优势：（1）在多种视觉任务上的通用能力，能够匹配或超过任务特定的SOTA模型；（2）卓越的数据效率，在微调时使用更少的数据就能达到领先的性能。

---

![Figure 9 : Effect of transferring increasing number of layers from the pre-train](fig9_1.webp)

> Figure 9 : Effect of transferring increasing number of layers from the pre-trained text-to-video model.

这张图的核心是展示**从预训练的文本到视频生成模型中迁移不同数量的层**对后续任务训练效果的影响。我们可以通过以下几个部分来理解它：

1.  **坐标轴与基本概念**：
    *   **横轴 (X轴)**: "Training Steps"（训练步数），表示模型在特定任务上进行训练的迭代次数，范围从0到2500。
    *   **纵轴 (Y轴)**: "Training Loss (log scale)"（训练损失，对数刻度），表示模型在训练过程中的损失值。损失值越低，说明模型的预测结果与真实标签之间的差距越小，模型学习效果越好。采用对数刻度是为了更清晰地展示损失值的巨大差异。

2.  **曲线与图例**：
    *   图中有六条不同颜色的曲线，每条曲线代表一种不同的预训练层迁移策略。图例清晰地标明了每条曲线对应的策略：
        *   **青色 (Teal) 曲线**: "0 pretrained layer (from scratch)"（0个预训练层，从头开始训练）。这意味着模型没有使用任何预训练权重，完全从随机初始化开始学习。
        *   **橙色 (Orange) 曲线**: "8 pretrained layer"（8个预训练层）。模型迁移了预训练视频生成模型中的前8层。
        *   **蓝色 (Blue) 曲线**: "16 pretrained layer"（16个预训练层）。模型迁移了16层。
        *   **粉色 (Pink) 曲线**: "24 pretrained layer"（24个预训练层）。模型迁移了24层。
        *   **浅绿色 (Light Green) 曲线**: "32 pretrained layer"（32个预训练层）。模型迁移了32层。
        *   **黄色 (Yellow) 曲线**: "40 pretrained layer (fully pretrained model)"（40个预训练层，完全预训练模型）。这意味着模型使用了预训练视频生成模型的所有40层，即直接利用了整个预训练模型的知识。

3.  **数据流动与方法理解**：
    *   这张图揭示的方法是：首先有一个预训练好的“文本到视频生成模型”。然后，从这个预训练模型中选择性地“迁移”（或“微调”）不同数量的层到一个新的模型中。
    *   迁移的层数从0（即不使用预训练权重，从头训练）逐渐增加到40（即完全使用预训练模型的所有层）。
    *   对于每种迁移策略，研究者会在一个新的任务上训练这个模型，并记录其训练损失随训练步数的变化情况。
    *   因此，这张图展示了不同“预训练知识注入量”对新任务训练效率和学习效果的影响。可以理解为，随着从预训练视频生成模型中迁移的层数增加，新模型在目标任务上的学习速度和最终性能会如何变化。

4.  **结果分析与结论**：
    *   **对比对象**：主要对比对象是“从头开始训练”的模型（青色曲线）和“迁移不同数量预训练层”的模型（其他颜色曲线）。
    *   **关键观察**：
        *   **从头开始训练（0层迁移）**：这条曲线（青色）的损失值最高，并且在训练过程中下降得最慢，波动也较大。这表明在没有预训练知识的情况下，模型学习新任务非常困难且效率低下。
        *   **迁移预训练层**：随着迁移的预训练层数增加（从8层到40层），训练损失显著降低，并且下降速度更快，曲线更平滑。例如，迁移8层（橙色曲线）比从头开始好很多；迁移16层（蓝色）、24层（粉色）、32层（浅绿色）的效果依次更好；而迁移全部40层（黄色曲线）时，模型的训练损失最低，学习效果最好，且收敛最快。
    *   **结论**：这张图清楚地表明，**从预训练的文本到视频生成模型中迁移更多的层可以显著提高新任务的学习效率和最终性能**。预训练模型中包含的“时空先验知识”和“视觉-语言对齐能力”（如论文摘要所述）对于下游视觉任务非常有帮助。迁移的层数越多，模型能够利用的预训练知识就越多，从而在新任务上表现得更好、更快。这也支持了论文的核心观点，即大规模的文本到视频生成可以作为计算机视觉通用模型的强大预训练范式。

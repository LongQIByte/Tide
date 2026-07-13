# RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation

[arXiv](https://arxiv.org/abs/2607.06558) · [HuggingFace](https://huggingface.co/papers/2607.06558) · ▲76

## 摘要（原文）

> Scaling robot learning requires massive, diverse trajectory data, yet collection is currently bottlenecked by physical teleoperation, where every demonstration binds operator time to specific hardware and workspaces. We introduce digital teleoperation, a paradigm that decouples data collection from physical constraints by replacing the real robot with a generative world model. In this framework, an operator's hand-pose stream drives a robot-centric generative world model to synthesize high-fidelity egocentric videos from a single reference image. The recorded pose stream serves as an embodiment-agnostic action label transferable to any target robot via standard retargeting, yielding complete state-action trajectories for imitation learning independent of physical hardware. We instantiate this paradigm in RynnWorld-Teleop, a system that integrates depth-aware skeletal conditioning, progressive human-to-robot training on a video Diffusion Transformer, and streaming autoregressive distillation. This pipeline compresses the generative process into a single-pass inference, enabling 40+ FPS, real-time interactive generation on a single H100 GPU. Policies trained exclusively on RynnWorld-Teleop-generated data achieve effective zero-shot Sim2Real transfer across dexterous and diverse bimanual tasks. Moreover, augmenting real-world datasets with our digitally teleoperated data consistently improves success rates, demonstrating that RynnWorld-Teleop serves as a high-fidelity, scalable data engine for the next generation of robotic agents.

## 摘要（中译）

扩展机器人学习需要大量、多样的轨迹数据，然而目前数据收集受限于物理遥操作（physical teleoperation），在这种方式中，每个演示都将操作员的时间与特定硬件和工作空间绑定。我们引入数字遥操作（digital teleoperation），这是一种通过用生成式世界模型（generative world model）替代真实机器人，将数据收集与物理约束解耦的范式。在这个框架中，操作员的手部姿态流驱动以机器人为中心的生成式世界模型，从单张参考图像合成高保真度的第一人称视角视频。记录的姿态流作为与实体无关的动作标签，可通过标准重定向（retargeting）转移到任何目标机器人，从而生成独立于物理硬件的完整状态 - 动作轨迹，用于模仿学习。我们在RynnWorld - Teleop中实现了这一范式，该系统集成了深度感知的骨骼条件作用、基于视频扩散Transformer（video Diffusion Transformer）的人类到机器人的渐进式训练以及流式自回归蒸馏。这个流程将生成过程压缩为单次推理，使得在单个H100 GPU上能够实现每秒40帧以上的实时交互式生成。仅在RynnWorld - Teleop生成的数据上训练的策略能够在灵巧和多样的双手任务中实现有效的零样本Sim2Real（Sim2Real）迁移。此外，用我们通过数字遥操作生成的数据增强真实世界数据集，成功率持续提高，这表明RynnWorld - Teleop是下一代机器人智能体的高保真度、可扩展的数据引擎。

## 背景剖析

### 背景剖析  

**1. 技术背景与需求**  
机器人学习需要大量多样化的数据来提升性能，但物理世界中的数据收集效率极低——传统遥操作（如用机械臂或VR设备控制真实机器人）受限于硬件成本、环境重置时间和物体多样性不足等问题。例如，训练一个能灵活操作日常物品的机器人，需要反复手动摆放物体并记录操作轨迹，这既耗时又难以覆盖复杂场景。数字遥操作的目标是通过生成式模型替代真实机器人，让操作员仅通过手势或动作就能“虚拟”控制机器人，从而突破物理限制，快速生成大规模训练数据。  

**2. 先前方法的局限**  
现有研究存在三个核心问题：  
- **被动观察而非主动控制**：早期方法（如将人类视频转换为机器人视角）仅生成图像，但无法记录真实的动作序列（如关节运动），导致数据无法直接用于模仿学习。  
- **人形而非机器人视角**：部分模型生成的视频仍以人类手部为中心，而非机器人的感知视角，导致“外观像机器人但行为不匹配”的矛盾。  
- **非实时性**：复杂的生成模型（如Diffusion Transformer）无法实时响应操作员的动作，破坏了遥操作的交互性。  

**3. 本文的解决方案**  
RynnWorld-Teleop通过三个创新设计解决了这些问题：  
- **机器人中心化的动作捕捉**：将操作员的手势映射到机器人的关节空间，并通过深度感知渲染生成高保真视频，确保动作与视觉观测严格对齐。  
- **渐进式跨域训练**：先在人类视频上学习通用操作知识，再通过人机配对数据调整到机器人视角，消除“外观-行为”差距。  
- **实时流式生成**：采用因果推理和滚动一致性策略，让模型在单次推理中完成长时程任务生成，支持40帧/秒的实时交互。  

**4. 与前人工作的关键差异**  
与现有方法相比，RynnWorld-Teleop是首个同时满足以下三点的技术：  
- **动作可解释性**：生成的视频直接对应可迁移的关节级动作标签，而非仅图像。  
- **机器人视角**：所有生成内容均从机器人的感知角度出发，确保数据可直接用于训练。  
- **实时交互性**：操作员能即时看到动作结果并调整策略，支持复杂任务的连续执行。  

这一框架将数据收集从“依赖物理硬件”转变为“依赖操作员想象力”，为机器人学习提供了可扩展的高保真数据引擎。

## 方法图解

![Figure 1 : Physical vs. Digital Teleoperation. (Top) Physical teleoperation bind](fig1_1.webp)

> Figure 1 : Physical vs. Digital Teleoperation. (Top) Physical teleoperation binds every demonstration to a real robot and a fixed workspace, capping throughput at operator-hours × \times hardware availability. (Bottom) Digital teleoperation replaces the real robot with RynnWorld-Teleop, a real-time action-conditioned world model that synthesizes the egocentric video the robot would have produced from a single reference image, and retargets the same gesture stream into embodiment-specific robot actions. Both pipelines emit synchronized (RGB observations, robotic actions) pairs, so digital teleoperation is drop-in compatible with downstream imitation learning, without ever moving a real robot.

这张图清晰地对比了**物理遥操作（Physical Teleoperation）**和**数字遥操作（Digital Teleoperation）**两种范式，帮助我们理解论文中提出的数字遥操作方法的核心逻辑和优势。

### 物理遥操作（上半部分）
- **Human Operator（人类操作员）**：操作员通过VR设备进行动作输入。
- **Retargeting（重定向）**：操作员的动作被转换为**Joint-space Actions（关节空间动作）**，这是一种特定于机器人的动作表示。
- **Control（控制）**：这些关节空间动作被发送到**Real Robot（真实机器人）**，以控制其运动。
- **Real-world Dataset（真实世界数据集）**：机器人在执行动作时，会生成**RGB Observations（RGB观测）**和记录**Robotic Actions（机器人动作）**，这些数据被收集到真实世界数据集中。
- **问题点**：物理遥操作存在三个主要限制：
  - **Hardware-bound（硬件绑定）**：数据收集依赖于特定的硬件设备。
  - **Fixed-workspace（固定工作空间）**：操作范围受限于机器人的物理工作空间。
  - **Manual-reset（手动重置）**：每次演示后需要手动重置环境和机器人。

### 数字遥操作（下半部分）
- **Human Operator（人类操作员）**：同样通过VR设备进行动作输入，但流程与物理遥操作不同。
- **Skeletal Rendering（骨骼渲染）**：操作员的手部动作被渲染为**Depth-Aware Skeletal Representation（深度感知骨骼表示）**，这是一种更抽象的动作表示。
- **Generating（生成）**：这种骨骼表示被输入到**Real-time Video Streaming（实时视频流）**模块，该模块使用RynnWorld-Teleop（一个动作条件世界模型）从单个参考图像合成高保真的第一人称视角视频，模拟机器人执行动作时的视觉观测。
- **Synthetic Dataset（合成数据集）**：生成的RGB观测和重定向后的**Robotic Actions（机器人动作）**被收集到合成数据集中。
- **优势**：数字遥操作具有三个显著优势：
  - **Hardware-agnostic（硬件无关）**：数据收集不依赖于特定的硬件设备。
  - **Zero-asset-overhead（零资产开销）**：不需要实际的机器人硬件，降低了成本。
  - **Real-time（实时）**：能够实时生成和收集数据，提高了效率。
- **Retargeting（重定向）**：合成数据集中的动作标签可以通过标准的重定向方法转换为特定于目标机器人的动作，实现跨机器人的迁移学习。

### 方法运作流程
1. **物理遥操作**：操作员的动作通过重定向转换为关节空间动作，控制真实机器人，收集真实世界数据。但这种方法受限于硬件、工作空间和手动重置。
2. **数字遥操作**：操作员的手部动作被渲染为深度感知骨骼表示，输入到实时视频流模块，合成机器人视角的视频。生成的RGB观测和重定向后的动作被收集为合成数据。这种方法解耦了数据收集和物理硬件，具有硬件无关、零资产开销和实时的优势。

### 结论
这张图展示了数字遥操作如何通过生成模型替代真实机器人，解决了物理遥操作的瓶颈问题，使得大规模机器人学习的数据收集更加高效和灵活。数字遥操作生成的合成数据可以用于训练机器人策略，并实现零样本的Sim2Real迁移。

---

![Figure 3 : Overview of RynnWorld-Teleop. (a) Actions are rendered as depth-aware](fig3_1.webp)

> Figure 3 : Overview of RynnWorld-Teleop. (a) Actions are rendered as depth-aware skeletal videos and encoded into the latent space via a VAE. (b) We expand a pretrained video DiT to incorporate hand-pose conditioning using a distribution-aligned patch embedding branch. (c) The model is distilled into a causal student for interactive, autoregressive generation using a streaming rollout schedule.

这张图展示了RynnWorld-Teleop系统的整体架构和工作流程，它是一个用于数字遥操作的、动作条件化的世界模型。我们可以通过以下几个部分来理解这个系统：

首先，我们看到图的左侧有两个主要的输入源。上方的输入是参考图像序列（看起来像是机器人视角的图像），下方的输入是操作员的手部姿态流（由一个戴着VR头显的人物图标和手部动作示意表示）。这两个输入分别代表了数字遥操作中的“环境”和“动作”部分。

接下来，这两个输入都通过各自的VAE（变分自编码器）编码器进行处理。VAE Encoder的作用是将输入的图像或姿态信息编码到潜在空间（latent space）中。对于上方的参考图像，它被编码成一个潜在表示，同时可能还添加了噪声（图中标注为"noised"的部分），这通常是为了训练生成模型的稳定性。对于下方的手部姿态，它也被编码成一个潜在表示，这个表示包含了动作信息。

然后，这两个潜在表示被结合在一起，并输入到一系列的处理模块中。上方的路径显示，带噪声的潜在表示和动作潜在表示被输入到"Wan-DiT Blocks"（可能是指一种改进的视频扩散Transformer块）。这个模块负责根据动作条件生成新的潜在表示。同时，这个模块还通过一个标注为"Distillation"（蒸馏）的箭头，将其知识传递给下方的"Causal Blocks"（因果块）。蒸馏的目的是将教师模型（Wan-DiT Blocks）的知识转移到学生模型（Causal Blocks），以实现更高效的推理。

下方的路径显示，动作潜在表示被输入到"Causal Blocks"。这些因果块利用KV Cache（键值缓存）来存储中间结果，从而实现流式的、自回归的生成。KV Cache允许模型在生成过程中重用之前的信息，提高效率并支持实时交互。

最后，经过处理的潜在表示被输入到VAE Decoder中。VAE Decoder的作用是将潜在空间的表示解码回图像空间，生成高保真的第一人称视角视频。图中显示，上方的路径生成的图像是批量的（多帧），而下方的路径生成的图像是实时的（单帧流式输出），并且标注了"Real-time"，表明这个路径支持实时交互。

整个流程揭示了RynnWorld-Teleop方法的具体运作方式：操作员的手部姿态驱动一个基于机器人的生成世界模型，该模型从单个参考图像合成高保真度的第一人称视频。通过将动作信息（手部姿态）与视觉信息（参考图像）结合，并利用蒸馏和因果自回归生成，系统能够实现实时的、交互式的视频生成。这种方法使得收集遥操作数据不再受物理硬件的限制，从而可以大规模地生成多样化的数据集，用于机器人模仿学习。

总结来说，这张图展示了一个从输入（参考图像和手部姿态）到输出（生成的视频）的完整流程，其中包含了编码、条件处理、蒸馏、自回归生成和解码等关键步骤。这个系统通过将动作信息融入生成过程，实现了数字遥操作，为机器人学习提供了新的范式。

---

![Figure 4 : Task illustration . We design four manipulation tasks for real-world ](fig4_1.webp)

> Figure 4 : Task illustration . We design four manipulation tasks for real-world evaluation.

这张图（图4）属于论文《RynnWorld - Teleop: An Action - Conditioned World Model for Digital Teleoperation》，其标题为“Task illustration”，意在展示为真实世界评估设计的四个操作任务，以说明所提方法（RynnWorld - Teleop）在实际操作任务中的应用场景和方法的运作逻辑。

从左到右，四个任务板块分别是“Dual Picking（双重拾取）”、“Block Pushing（方块推动）”、“Bimanual Lifting（双手提升）”和“Lid Placement（盖子放置）”。每个任务板块都包含一个机器人执行任务的示意图，以及标注了数字（1、2、3、4等）和红色箭头的动作流程，这些箭头和数字代表了机器人执行任务时的动作顺序或步骤：

1. **Dual Picking（双重拾取）**：
    - 示意图中显示了一个双臂机器人（或类似的多关节机器人）在一个工作空间中，周围有物体（如黑色和黄色的物体）。
    - 红色箭头和数字（1、2、3、4）表示机器人执行拾取任务的动作顺序。例如，数字1可能代表机器人手臂的初始移动，数字2、3、4依次代表后续的抓取、移动或放置等动作。这些动作的顺序展示了机器人如何协调两个手臂（或关节）来完成双重拾取的任务，即从不同位置抓取物体并进行操作。
    - 这个任务的目的是展示机器人在处理需要同时或依次抓取多个物体的场景时的能力，而这种方法（RynnWorld - Teleop）通过数字遥操作的方式，让操作员的动作（如手部姿势流）驱动生成模型来合成高保真的第一人称视角视频，从而记录下这些动作序列作为动作标签，用于训练机器人策略。

2. **Block Pushing（方块推动）**：
    - 示意图中的机器人正在推动一个黑色的方块（或类似物体）。
    - 红色箭头和数字（1、2、3、4）表示推动方块的动作顺序。例如，数字1可能是机器人手臂的起始位置调整，数字2、3、4代表推动方块的不同阶段，如接近方块、施加推力、完成推动等。
    - 该任务展示了机器人在处理需要推动物体的场景时的能力，同样，通过数字遥操作的方法，操作员的动作被转化为机器人的动作序列，用于训练策略，使得策略能够学习如何有效地推动方块。

3. **Bimanual Lifting（双手提升）**：
    - 示意图中的机器人使用两个手臂（或关节）提升一个绿色和黄色的物体（如一个块状物体）。
    - 红色箭头和数字（1、2）表示提升物体的动作顺序。数字1可能是手臂的初始定位，数字2代表提升的动作（如向上移动、稳定物体等）。
    - 这个任务展示了机器人在处理需要双手协作提升物体的场景时的能力，数字遥操作的方法使得操作员的动作能够被记录并转化为机器人的动作，用于训练策略，以实现有效的双手提升任务。

4. **Lid Placement（盖子放置）**：
    - 示意图中的机器人正在将一个盖子（或类似物体）放置在一个棕色的物体（如一个盒子）上。
    - 红色箭头和数字（1、2）表示放置盖子的动作顺序。数字1可能是机器人手臂的起始位置调整，数字2代表放置的动作（如接近目标、放下盖子、调整位置等）。
    - 该任务展示了机器人在处理需要精确放置物体的场景时的能力，通过数字遥操作的方法，操作员的动作被转化为机器人的动作序列，用于训练策略，以实现准确的盖子放置任务。

从方法的角度来看，这张图揭示了RynnWorld - Teleop的运作方式：首先，操作员通过手部姿势流（hand - pose stream）来驱动一个以机器人为中心的生成世界模型（robot - centric generative world model）。这个生成模型从一个参考图像（reference image）开始，合成高保真的第一人称视角视频（egocentric videos）。在这个过程中，记录下来的操作员的手部姿势流作为与实现无关的动作标签（embodiment - agnostic action label），可以通过标准的重定向（retargeting）方法转移到任何目标机器人上，从而得到完整的状态 - 动作轨迹（state - action trajectories），用于模仿学习（imitation learning），而不需要依赖物理硬件。

具体来说，RynnWorld - Teleop系统集成了深度感知的骨骼条件（depth - aware skeletal conditioning）、基于视频扩散Transformer的人类到机器人的渐进式训练（progressive human - to - robot training on a video Diffusion Transformer）和流式自回归蒸馏（streaming autoregressive distillation）。这个流程将生成过程压缩为单次推理（single - pass inference），使得在单个H100 GPU上能够实现40+ FPS的实时交互生成。

然后，仅在RynnWorld - Teleop生成的数据上训练的策略能够在各种灵巧和双手任务上实现有效的零样本Sim2Real（仿真到真实）转移。此外，用我们数字遥操作的数据增强真实世界数据集可以持续提高成功率，这表明RynnWorld - Teleop作为一个高保真、可扩展的系统，能够为机器人学习提供大量的、多样的轨迹数据，解决了物理遥操作中数据收集的瓶颈问题（即每次演示都将操作员的时间绑定到特定的硬件和工作空间上）。

总结来说，这张图通过展示四个不同的操作任务，说明了RynnWorld - Teleop方法如何通过数字遥操作的方式，让操作员的动作被记录并转化为机器人的动作序列，用于训练机器人策略，从而实现各种复杂的操作任务，并且能够在仿真和真实世界之间进行有效的转移，同时提高真实世界任务的成功率。

---

![Figure 13 : Qualitative results of RynnWorld-Teleop on robotic manipulation task](fig12_1.webp)

> Figure 13 : Qualitative results of RynnWorld-Teleop on robotic manipulation tasks. Starting from a single reference image and a sequence of human hand-pose streams, RynnWorld-Teleop synthesizes high-fidelity, temporally coherent robotic execution videos. The results demonstrate the model’s ability to render complex dexterous interactions, such as bimanual coordination and high-precision object handling, while maintaining strict adherence to the input action signal.

这张图（图13）是论文《RynnWorld-Teleop: An Action-Conditioned World Model for Digital Teleoperation》中的结果展示，旨在直观地说明其提出的数字遥操作方法如何根据人类手部姿势流和单张参考图像生成高保真、时间连贯的机器人执行视频。

我们可以将这张图分解为多个水平排列的行，每一行代表一个独立的机器人操作任务示例。每一行又由多个垂直排列的子图组成，这些子图按照时间顺序展示了操作的进展。通常，从左到右，我们可以观察到操作从一个初始状态（通常是只有物体和机器人的手，或者一个参考图像的简化表示）逐渐发展到完成某个特定动作（如抓取、移动或放置物体）的过程。

具体来说，每一行的结构如下：

1.  **输入部分（隐含）**：虽然图中没有明确标出，但根据论文描述，每个任务示例都始于“一个单一的参考图像”和“一个人类手部姿势流”。参考图像可能对应于每行最左侧的子图，或者是一个更抽象的初始状态表示。人类手部姿势流则是驱动模型生成后续动作的指令序列。

2.  **时间序列的子图**：每一行中的子图从左到右展示了操作的时间演变。例如，在第一行（最上面一行），我们看到一个棕色的盒子放在桌子上，两侧有机器人的手（或手套状的表示）。随着我们从左向右移动，机器人的手逐渐与盒子互动，最终似乎完成了某种操作（如拿起或放下盒子）。第二行展示了一个西瓜，机器人的手从两侧逐渐靠近并可能进行旋转或移动西瓜的动作。第三行展示了一个小蓝球，机器人的手从两侧伸向它，最终可能抓住或移动它。第四行展示了一个带有黄色顶部的黑色物体（可能是某种工具或玩具），机器人的手与之互动。

3.  **手部姿势的可视化（下方）**：在每一行子图的下方，有一排彩色的手形图标（蓝色和红色）。这些图标代表了输入的人类手部姿势流。蓝色和红色可能分别代表左右手的姿势。这些图标的形状和方向变化反映了人类操作者在不同时间点做出的手势。重要的是，这些手势序列是驱动模型生成上方机器人操作视频的直接输入。模型的目标是使生成的机器人动作与这些输入的手势信号严格对应。

4.  **信息流动**：数据的流动可以理解为：人类手部姿势流（下方的手形图标） + 单张参考图像（或初始状态） → RynnWorld-Teleop模型 → 合成的机器人执行视频（上方的子图序列）。这个过程是时间连贯的，意味着模型需要确保生成的每一帧都与前一帧以及输入的手势序列保持一致。

这张图揭示了该方法的具体运作方式：

*   **动作条件生成**：模型的核心是根据输入的动作信号（即人类手部姿势流）来生成机器人的行为。这意味着模型的输出（机器人动作）是由输入的动作指令直接决定的。
*   **数字遥操作**：通过使用生成的世界模型，该方法实现了数字遥操作。操作者不需要在物理上控制真实的机器人，而是在一个数字环境中通过手势来控制虚拟的机器人。
*   **高保真和时间连贯性**：图中展示的结果表明，模型能够生成高保真度的视频，并且这些视频在时间上是连贯的。这意味着生成的机器人动作看起来自然，并且符合物理规律。
*   **复杂交互**：图中的示例展示了模型处理复杂操作的能力，如双手协调（bimanual coordination，如图中双手同时操作物体）和高精度物体处理（high-precision object handling，如抓取小球或旋转西瓜）。
*   **严格遵循输入动作信号**：模型的一个关键特性是它能够严格遵循输入的动作信号。这意味着生成的机器人动作与人类操作者的手势意图高度一致。

结论部分：

这张图通过多个任务示例（如盒子操作、西瓜操作、小球操作和工具操作）展示了RynnWorld-Teleop方法的有效性。它清晰地表明，该方法能够根据人类手部姿势流和单张参考图像，合成高保真度、时间连贯且符合动作指令的机器人执行视频。这些结果表明，RynnWorld-Teleop能够渲染复杂的灵巧交互，如双手协调和高精度物体处理，同时严格遵循输入的动作信号。这为解决机器人学习中大规模轨迹数据收集的瓶颈问题提供了一种有效的解决方案。

---

![Figure 2 : Depth-Aware Representation. We bridge the gap between 2D projections ](fig2_1.webp)

> Figure 2 : Depth-Aware Representation. We bridge the gap between 2D projections and 3D dynamics by rendering hand skeletons with depth-modulated color and size.

这张图（图2）的核心目的是展示论文中提出的“深度感知表示”（Depth-Aware Representation）方法，它旨在弥合二维投影（如图像）与三维动态（如手部动作）之间的差距。具体来说，该方法通过渲染带有深度调制颜色和大小的手部骨骼来实现这一目标。

我们可以将图分为左右两部分来理解其工作流程和信息呈现：

**左侧部分：深度感知的可视化表示**
这部分展示了深度信息如何被编码到手部骨骼的视觉表示中。图中有两组手部骨骼的示意图，每组都包含蓝色和红色的骨骼。
*   **蓝色骨骼**：代表距离观察者（或相机）较远的手或手部部分。从视觉上看，这些骨骼的颜色可能更暗淡，或者其大小相对较小，这暗示了它们在三维空间中处于较远的位置。
*   **红色骨骼**：代表距离观察者较近的手或手部部分。这些骨骼的颜色可能更鲜艳，或者其大小相对较大，这暗示了它们在三维空间中处于较近的位置。
这种颜色和大小的差异是“深度调制”的体现，它将三维空间中的深度信息转化为二维图像中的视觉特征，使得观察者能够直观地理解手部在三维空间中的相对位置和姿态。

**右侧部分：基于深度感知的图像生成示例**
这部分展示了该方法在实际图像生成中的应用效果。图中包含三行，每行都由两个并排的图像组成，左边是输入或参考图像，右边是生成的图像。
*   **第一行（顶部）**：显示了一个揉面团的场景。左边的图像中，可以看到一双手正在操作面团和擀面杖。右边的图像是生成的，它保持了与左边图像相似的场景内容，但手部骨骼的表示（如果叠加或隐含在生成过程中）会反映出深度信息。例如，靠近相机的手可能看起来更大或颜色不同。
*   **第二行（中间）**：显示了一个操作多个杯子的场景。左边的图像中，一只手正在移动杯子。右边的图像是生成的，同样保持了场景内容，并且手部骨骼的深度信息被编码到视觉表示中。
*   **第三行（底部）**：显示了一个操作球体和碗的场景。左边的图像中，两只戴着手套的手正在与球体和碗互动。右边的图像是生成的，手部骨骼的深度信息同样被编码。

**信息流动和方法运作机制**
1.  **输入**：系统接收一个参考图像（如图中每行的左侧图像），该图像包含场景和手部的二维投影。
2.  **深度感知处理**：系统分析图像中的手部，估计其三维姿态和深度信息。这是通过某种深度感知技术实现的，可能是利用单目图像的深度估计方法，或者结合了其他传感器数据（尽管论文中提到的是数字遥操作，可能主要依赖视觉输入）。
3.  **骨骼渲染**：根据估计的深度信息，系统渲染出手部的骨骼结构。在这个渲染过程中，骨骼的颜色和大小被深度调制：距离较远的手部骨骼颜色较暗或较小（如左侧的蓝色骨骼），距离较近的手部骨骼颜色较亮或较大（如左侧的红色骨骼）。
4.  **图像生成**：系统使用渲染的带有深度信息的手部骨骼以及原始场景的其他信息，生成新的图像（如图中每行的右侧图像）。这些生成的图像不仅保留了原始场景的内容，还通过手部骨骼的深度感知表示，提供了更丰富的三维动态信息。

**结论**
这张图清晰地展示了“深度感知表示”方法的工作原理：通过将深度信息编码到手部骨骼的颜色和大小中，实现了从二维图像到三维动态的桥梁。这种方法使得生成的图像能够更准确地反映手部在三维空间中的位置和姿态，这对于需要精确动作捕捉和模仿的机器人学习任务至关重要。图中的示例表明，该方法能够有效地应用于不同的手部操作场景，并生成具有深度感知信息的图像。

总结来说，这张图通过视觉对比和示例，直观地解释了论文中提出的深度感知表示方法如何工作，即如何将深度信息融入到手部骨骼的视觉表示中，从而弥合二维投影与三维动态之间的差距。

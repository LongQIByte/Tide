# VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation

[arXiv](https://arxiv.org/abs/2407.04152)

## 摘要（原文）

> Bimanual manipulation is critical to many robotics applications. In contrast to single-arm manipulation, bimanual manipulation tasks are challenging due to higher-dimensional action spaces. Prior works leverage large amounts of data and primitive actions to address this problem, but may suffer from sample inefficiency and limited generalization across various tasks. To this end, we propose VoxAct-B, a language-conditioned, voxel-based method that leverages Vision Language Models (VLMs) to prioritize key regions within the scene and reconstruct a voxel grid. We provide this voxel grid to our bimanual manipulation policy to learn acting and stabilizing actions. This approach enables more efficient policy learning from voxels and is generalizable to different tasks. In simulation, we show that VoxAct-B outperforms strong baselines on fine-grained bimanual manipulation tasks. Furthermore, we demonstrate VoxAct-B on real-world $\texttt{Open Drawer}$ and $\texttt{Open Jar}$ tasks using two UR5s. Code, data, and videos are available at https://voxact-b.github.io.

## 摘要（中译）

双臂操作对许多机器人应用至关重要。与单臂操作相比，由于动作空间维度更高，双臂操作任务具有挑战性。先前的工作利用大量数据和基本动作来解决这个问题，但可能存在样本效率低和在不同任务中泛化能力有限的问题。为此，我们提出了VoxAct - B，这是一种基于语言条件、基于体素的方法，它利用视觉语言模型（Vision Language Models，VLMs）来优先考虑场景中的关键区域并重建体素网格。我们将这个体素网格提供给我们的双臂操作策略，以学习操作和稳定动作。这种方法能够从体素中更高效地学习策略，并且可推广到不同的任务。在模拟中，我们表明VoxAct - B在细粒度的双臂操作任务上优于强大的基线方法。此外，我们使用两个UR5机器人在真实的$\texttt{Open Drawer}$（打开抽屉）和$\texttt{Open Jar}$（打开罐子）任务上演示了VoxAct - B。代码、数据和视频可在https://voxact - b.github.io获取。

## 背景剖析

**背景剖析**

双臂操作技术在机器人领域具有广泛的应用场景，例如当物体过大而无法由单个机械臂控制时，或者需要一个机械臂稳定目标物体以便另一个机械臂进行操作时。这类技术在家庭和工业环境中尤为重要，如切割食物、开启瓶盖或包装物品等任务，都需要双手协调和高精度操作。然而，现有的双臂操作方法存在一些挑战。

先前方法主要依赖大规模数据集训练策略或利用原始动作来解决问题，但这些方法通常样本效率低下，且难以在不同任务间泛化。为了克服这些限制，本文提出了一种名为VoxAct-B的创新方法。该方法结合了体素表示和视觉语言模型（VLMs），通过关注场景中最相关的区域来减少计算负担，同时提高样本效率和泛化能力。

VoxAct-B的核心思想是利用VLMs来识别和裁剪场景中的关键区域，从而构建一个高分辨率但计算成本较低的体素网格。这种方法不仅提高了学习效率，还使得策略能够更好地适应不同的任务需求。此外，通过语言指令和VLMs，VoxAct-B能够动态确定每个机械臂的角色（操作或稳定），从而实现更灵活和高效的双臂协作。

与以往工作相比，VoxAct-B的关键差异在于其结合了体素表示和视觉语言模型的创新应用。这种方法不仅解决了传统方法在样本效率和泛化能力上的不足，还为双臂操作任务提供了一种新的解决方案。通过在模拟环境和真实世界中的实验验证，VoxAct-B在多个基准任务上取得了显著的性能提升，展示了其在实际应用中的潜力。

## 方法图解

![Figure 2: Overview of VoxAct-B. Given RGB-D images and a language goal, we input](fig2_1.webp)

> Figure 2: Overview of VoxAct-B. Given RGB-D images and a language goal, we input an RGB image from the front camera and a text query extracted from the language goal into the Vision Language Models (VLMs). The VLMs output the pose of the object of interest with respect to the front camera. This information determines the language goal and the roles of each arm (i.e., acting or stabilizing ). Additionally, we use the object’s position with the RGB-D images to reconstruct a voxel grid that spans α ⁢ x 3 𝛼 superscript 𝑥 3 \alpha x^{3} italic_α italic_x start_POSTSUPERSCRIPT 3 end_POSTSUPERSCRIPT meters of the workspace using V 3 superscript 𝑉 3 V^{3} italic_V start_POSTSUPERSCRIPT 3 end_POSTSUPERSCRIPT voxels. The zoomed-in voxel grid, the language goal, proprioception data of both robot arms, and an arm ID are provided to an acting policy π a subscript 𝜋 𝑎 \pi_{a} italic_π start_POSTSUBSCRIPT italic_a end_POSTSUBSCRIPT and a stabilizing policy π s subscript 𝜋 𝑠 \pi_{s} italic_π start_POSTSUBSCRIPT italic_s end_POSTSUBSCRIPT . The policies predict the discretized pose of the next best voxel, gripper open action, collision avoidance flag, and arm ID for fine-grained bimanual manipulation.

这张图（图2）展示了VoxAct-B方法的概述，它是一个用于双手操作的语言条件化、基于体素的方法。让我们一步步分解这个流程：

1.  **输入阶段**：
    *   系统首先接收两种类型的输入：RGB-D图像（即包含颜色和深度信息的图像）和一个语言目标（例如“打开抽屉”或“打开罐子”）。图中可能隐含了这些输入源。

2.  **视觉语言模型（VLMs）处理**：
    *   从RGB-D图像中提取的RGB图像（特别是来自前向相机的图像）和从语言目标中提取的文本查询被输入到视觉语言模型（VLMs）中。
    *   VLMs的作用是理解语言目标和图像内容，从而输出感兴趣物体相对于前向相机的位姿（位置和方向）。这个位姿信息对于确定接下来的操作至关重要。

3.  **任务分解与体素网格构建**：
    *   基于VLMs输出的物体位姿信息，系统会确定语言目标的具体内容，并为每个机械臂分配角色——一个是“操作臂”（acting arm），负责执行主要的操作任务；另一个是“稳定臂”（stabilizing arm），负责提供支撑或稳定。
    *   同时，系统利用物体的位置信息和RGB-D图像来重建一个体素网格（voxel grid）。这个体素网格覆盖了工作空间中α x α x α米（即边长为α的立方体区域）的范围，并且由V³个体素组成。体素网格是对物理工作空间的离散化表示，便于后续的规划和控制。

4.  **策略网络输入与决策**：
    *   接下来，一个放大的体素网格（zoomed-in voxel grid，可能聚焦于物体周围的关键区域）、语言目标、两个机械臂的本体感觉数据（proprioception data，例如关节角度、位置等）以及一个机械臂ID被输入到两个策略网络中：一个操作策略πₐ（acting policy）和一个稳定策略πₛ（stabilizing policy）。
    *   这两个策略网络的目标是预测精细操作的下一步动作。具体来说，它们会预测：
        *   下一个最佳体素的离散化位姿（discretized pose of the next best voxel）：这指示了机械臂应该移动到哪个位置进行操作。
        *   夹爪打开动作（gripper open action）：指示夹爪是打开还是闭合。
        *   碰撞避免标志（collision avoidance flag）：指示是否需要采取行动以避免碰撞。
        *   机械臂ID（arm ID）：指定这个动作应该由哪个机械臂执行。

5.  **整体流程总结**：
    *   VoxAct-B的核心思想是利用VLMs从语言和视觉信息中提取关键区域和任务目标，然后将这些信息转化为体素网格表示。接着，通过专门设计的操作和稳定策略网络，基于体素网格和本体感觉数据进行精细的双手操作规划，包括动作选择、夹爪控制和碰撞避免。这种方法使得策略学习更加高效，并且能够推广到不同的双手操作任务中。

简而言之，VoxAct-B的工作流程是：**感知（RGB-D图像+语言目标） -> 理解（VLMs提取物体位姿和任务） -> 表示（体素网格构建） -> 决策（操作和稳定策略预测动作） -> 执行（机械臂执行预测的动作）**。这个过程强调了语言条件和体素表示在解决高维双手操作问题中的重要性。

---

![Figure 3: Top : VLMs usage as part of VoxAct-B, visualizing the Open Jar task in](fig3_1.webp)

> Figure 3: Top : VLMs usage as part of VoxAct-B, visualizing the Open Jar task in simulation, showing the role of OWL-ViT and Segment Anything. The RGB images from the front camera shown above are examples of actual (uncropped) images provided as input to the models. Bottom : visualization of different α 𝛼 \alpha italic_α values resulting in coarser grids ( α = 1.0 𝛼 1.0 \alpha=1.0 italic_α = 1.0 ) to finer grids ( α = 0.1 𝛼 0.1 \alpha=0.1 italic_α = 0.1 ). We use α = 0.3 𝛼 0.3 \alpha=0.3 italic_α = 0.3 for Open Jar .

这张图（图3）来自论文《VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation》，它分为上下两个主要部分，清晰地展示了VoxAct-B方法的核心流程和关键参数设置。

**上半部分：VLMs在VoxAct-B中的应用（以模拟中的“开罐”任务为例）**

这部分展示了视觉语言模型（VLMs）如何在VoxAct-B方法中发挥作用，特别是在“开罐”任务的模拟场景中。信息流动的顺序如下：

1.  **输入阶段**：
    *   左侧第一个模块显示了一个“RGB Image”（RGB图像）。这是一个来自机器人前端摄像头的实际（未裁剪）图像，作为模型的输入。图中示例了一个包含一个绿色罐子的场景。
    *   下方有一个“Text Query”（文本查询）模块，内容为“jar”。这个文本查询指定了任务的目标对象，即“罐子”。

2.  **OWL-ViT的处理**：
    *   中间的粉色矩形代表“OWL-ViT”模型。这是一个视觉语言模型（VLM）。
    *   箭头从“RGB Image”和“Text Query”指向“OWL-ViT”，表示这两个输入被同时送入该模型。
    *   “OWL-ViT”的输出是一个“Output Visualization”（输出可视化）。在这个可视化中，原始的RGB图像背景上叠加了一个红色的预测边界框（predicted bounding box），并标注了“jar: 0.00”（可能是置信度分数）。边界框的中心坐标和尺寸用[cx, cy, w, h]表示。这表明OWL-ViT根据文本查询“jar”，在RGB图像中定位并识别出了目标罐子。

3.  **Segment Anything的处理**：
    *   右侧的绿色矩形代表“Segment Anything”（SAM）模型，这是另一个VLM。
    *   箭头从“OWL-ViT”的“Predicted bounding box from OWL-ViT”（来自OWL-ViT的预测边界框）指向“Segment Anything”，表示OWL-ViT输出的边界框信息被用作SAM的输入。
    *   “Segment Anything”的输出也是一个“Output Visualization”。在这个可视化中，原始的RGB图像背景被处理过（可能进行了分割），并用一个箭头指向罐子的中心，标注为“crop center [x, y]”。这表明SAM根据OWL-ViT提供的边界框，进一步确定了目标罐子的中心裁剪坐标。

**数据/信息流动总结**：RGB图像 + 文本查询 → OWL-ViT（目标定位与识别，输出边界框） → Segment Anything（基于边界框的目标分割与中心点确定）。

**下半部分：不同α值对体素网格的影响**

这部分展示了不同α（alpha）值如何影响生成的体素网格的粗细程度。体素网格是VoxAct-B方法中用于表示环境和目标的三维离散化表示。

*   图中有三个子图，分别对应不同的α值：
    *   左图：α = 1.0。这个体素网格看起来最“粗糙”，细节较少，物体（如罐子和机器人手臂）的表示较为像素化。
    *   中图：α = 0.3。这个体素网格比α=1.0的要“精细”一些，物体的细节更清晰。
    *   右图：α = 0.1。这个体素网格是最“精细”的，物体的细节最清晰，边缘也更平滑。

*   图注中提到：“We use α = 0.3 for Open Jar.”（我们在“开罐”任务中使用α=0.3）。这表明在该特定任务中，选择了中等精细度的体素网格。

**方法运作机制揭示**：
通过这张图，我们可以理解VoxAct-B方法的具体运作方式：
1.  **目标识别与定位**：首先，利用视觉语言模型OWL-ViT，结合RGB图像和文本查询（如“jar”），在场景中定位并识别出目标物体，输出其边界框。
2.  **目标中心确定**：然后，将OWL-ViT输出的边界框信息传递给另一个VLM（如Segment Anything），以更精确地确定目标物体的中心裁剪坐标，或者进行更细致的分割。
3.  **环境表示**：接着，基于这些信息（可能还有其他传感器数据），构建一个体素网格来表示环境和目标。体素网格的精细度可以通过参数α进行调整。
4.  **策略学习**：最后，将这个体素网格作为输入，提供给双臂操纵策略，用于学习执行任务（如抓取和稳定）的动作。

这种方法的关键在于利用VLMs来优先处理场景中的关键区域，并将复杂的视觉信息转化为结构化的体素表示，从而提高策略学习的效率和泛化能力。

**结论**：
图中展示了VoxAct-B方法如何结合视觉语言模型（OWL-ViT和Segment Anything）来处理图像和文本信息，以识别和定位目标物体，并生成不同精细度的体素网格。具体来说，OWL-ViT用于目标检测（输出边界框），而Segment Anything用于基于边界框的目标分割或中心点确定。体素网格的精细度由α参数控制，该方法在“开罐”任务中使用了α=0.3。

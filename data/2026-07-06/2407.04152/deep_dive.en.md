# VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation

[arXiv](https://arxiv.org/abs/2407.04152)

## Abstract (verbatim)

> Bimanual manipulation is critical to many robotics applications. In contrast to single-arm manipulation, bimanual manipulation tasks are challenging due to higher-dimensional action spaces. Prior works leverage large amounts of data and primitive actions to address this problem, but may suffer from sample inefficiency and limited generalization across various tasks. To this end, we propose VoxAct-B, a language-conditioned, voxel-based method that leverages Vision Language Models (VLMs) to prioritize key regions within the scene and reconstruct a voxel grid. We provide this voxel grid to our bimanual manipulation policy to learn acting and stabilizing actions. This approach enables more efficient policy learning from voxels and is generalizable to different tasks. In simulation, we show that VoxAct-B outperforms strong baselines on fine-grained bimanual manipulation tasks. Furthermore, we demonstrate VoxAct-B on real-world $\texttt{Open Drawer}$ and $\texttt{Open Jar}$ tasks using two UR5s. Code, data, and videos are available at https://voxact-b.github.io.

## Background

**Background Analysis**

Bimanual manipulation technology is widely applicable in the field of robotics, particularly in scenarios where objects are too large for a single gripper to handle or when one arm is needed to stabilize an object while the other performs manipulation. This technology is crucial in both household and industrial settings, such as cutting food, opening bottles, or packaging items, which require coordinated, high-precision operations. However, existing bimanual manipulation methods face several challenges.

Previous approaches primarily rely on training policies on large datasets or using primitive actions, but these methods are often sample-inefficient and struggle to generalize across different tasks. To address these limitations, this paper proposes an innovative method called VoxAct-B. This approach combines voxel representations with Vision Language Models (VLMs) to reduce computational burden while improving sample efficiency and generalization.

The core idea of VoxAct-B is to use VLMs to identify and crop key regions in the scene, thereby constructing a high-resolution voxel grid with lower computational costs. This method not only enhances learning efficiency but also allows the policy to better adapt to different task requirements. Additionally, through language instructions and VLMs, VoxAct-B can dynamically determine the role of each arm (acting or stabilizing), enabling more flexible and efficient bimanual collaboration.

Compared to previous work, the key difference of VoxAct-B lies in its innovative application of voxel representations and visual language models. This approach not only addresses the shortcomings of traditional methods in terms of sample efficiency and generalization but also provides a new solution for bimanual manipulation tasks. Through experiments in both simulated and real-world environments, VoxAct-B has demonstrated significant performance improvements on multiple benchmark tasks, showcasing its potential for practical applications.

## Method, Figure by Figure

![Figure 2: Overview of VoxAct-B. Given RGB-D images and a language goal, we input](fig2_1.webp)

> Figure 2: Overview of VoxAct-B. Given RGB-D images and a language goal, we input an RGB image from the front camera and a text query extracted from the language goal into the Vision Language Models (VLMs). The VLMs output the pose of the object of interest with respect to the front camera. This information determines the language goal and the roles of each arm (i.e., acting or stabilizing ). Additionally, we use the object’s position with the RGB-D images to reconstruct a voxel grid that spans α ⁢ x 3 𝛼 superscript 𝑥 3 \alpha x^{3} italic_α italic_x start_POSTSUPERSCRIPT 3 end_POSTSUPERSCRIPT meters of the workspace using V 3 superscript 𝑉 3 V^{3} italic_V start_POSTSUPERSCRIPT 3 end_POSTSUPERSCRIPT voxels. The zoomed-in voxel grid, the language goal, proprioception data of both robot arms, and an arm ID are provided to an acting policy π a subscript 𝜋 𝑎 \pi_{a} italic_π start_POSTSUBSCRIPT italic_a end_POSTSUBSCRIPT and a stabilizing policy π s subscript 𝜋 𝑠 \pi_{s} italic_π start_POSTSUBSCRIPT italic_s end_POSTSUBSCRIPT . The policies predict the discretized pose of the next best voxel, gripper open action, collision avoidance flag, and arm ID for fine-grained bimanual manipulation.

This figure (Figure 2) illustrates the overview of the VoxAct-B method, which is a language-conditioned, voxel-based approach for bimanual manipulation. Let's break down the process step-by-step:

1.  **Input Stage**:
    *   The system initially receives two types of inputs: RGB-D images (images containing both color and depth information) and a language goal (e.g., "open drawer" or "open jar"). The source of these inputs is implied in the diagram.

2.  **Visual-Language Model (VLMs) Processing**:
    *   An RGB image (specifically from a front-facing camera) extracted from the RGB-D image and a text query extracted from the language goal are fed into the Visual-Language Models (VLMs).
    *   The role of the VLMs is to understand the language goal and the image content, thereby outputting the pose (position and orientation) of the object of interest relative to the front camera. This pose information is crucial for determining the subsequent operations.

3.  **Task Decomposition and Voxel Grid Construction**:
    *   Based on the object pose information output by the VLMs, the system determines the specific content of the language goal and assigns roles to each robotic arm—one as the "acting arm" (responsible for executing the main manipulation task) and the other as the "stabilizing arm" (responsible for providing support or stabilization).
    *   Simultaneously, the system reconstructs a voxel grid using the object's position information and the RGB-D image. This voxel grid covers a workspace region of α x α x α meters (a cubic area with side length α) and is composed of V³ voxels. The voxel grid is a discretized representation of the physical workspace, facilitating subsequent planning and control.

4.  **Policy Network Input and Decision-Making**:
    *   Next, a zoomed-in voxel grid (likely focusing on the critical region around the object), the language goal, proprioception data from both robotic arms (e.g., joint angles, positions), and an arm ID are fed into two policy networks: an acting policy πₐ and a stabilizing policy πₛ.
    *   The goal of these two policy networks is to predict the actions for fine-grained manipulation. Specifically, they predict:
        *   The discretized pose of the next best voxel: This indicates the position the robotic arm should move to for manipulation.
        *   Gripper open action: Indicates whether the gripper should open or close.
        *   Collision avoidance flag: Indicates whether action should be taken to avoid collisions.
        *   Arm ID: Specifies which robotic arm should execute this action.

5.  **Overall Process Summary**:
    *   The core idea of VoxAct-B is to leverage VLMs to extract key regions and task goals from language and visual information, then convert this information into a voxel grid representation. Subsequently, through specially designed acting and stabilizing policy networks, actions are planned for fine-grained bimanual manipulation based on the voxel grid and proprioceptive data, including action selection, gripper control, and collision avoidance. This approach enables more efficient policy learning and generalization to different bimanual manipulation tasks.

In essence, the VoxAct-B workflow is: **Perception (RGB-D images + language goal) -> Understanding (VLMs extract object pose and task) -> Representation (Voxel grid construction) -> Decision (Acting and stabilizing policies predict actions) -> Execution (Robotic arms execute predicted actions)**. This process emphasizes the importance of language conditioning and voxel representation in solving high-dimensional bimanual manipulation problems.

---

![Figure 3: Top : VLMs usage as part of VoxAct-B, visualizing the Open Jar task in](fig3_1.webp)

> Figure 3: Top : VLMs usage as part of VoxAct-B, visualizing the Open Jar task in simulation, showing the role of OWL-ViT and Segment Anything. The RGB images from the front camera shown above are examples of actual (uncropped) images provided as input to the models. Bottom : visualization of different α 𝛼 \alpha italic_α values resulting in coarser grids ( α = 1.0 𝛼 1.0 \alpha=1.0 italic_α = 1.0 ) to finer grids ( α = 0.1 𝛼 0.1 \alpha=0.1 italic_α = 0.1 ). We use α = 0.3 𝛼 0.3 \alpha=0.3 italic_α = 0.3 for Open Jar .

This figure (Figure 3) from the paper "VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation" is divided into two main sections, clearly illustrating the core workflow of the VoxAct-B method and key parameter settings.

**Top Section: VLMs Usage in VoxAct-B (Illustrated with the "Open Jar" Task in Simulation)**

This part demonstrates how Vision Language Models (VLMs) are utilized within the VoxAct-B method, specifically in a simulated "open jar" task. The flow of information is as follows:

1.  **Input Stage**:
    *   The leftmost module shows an "RGB Image." This is an actual (uncropped) image from a robot's front camera, serving as input to the models. The example shows a scene containing a green jar.
    *   Below it, a "Text Query" module contains the text "jar." This text query specifies the target object for the task, i.e., "jar."

2.  **Processing by OWL-ViT**:
    *   The pink rectangle in the middle represents the "OWL-ViT" model, a VLM.
    *   Arrows point from the "RGB Image" and "Text Query" to "OWL-ViT," indicating that these two inputs are fed into the model simultaneously.
    *   The output of "OWL-ViT" is an "Output Visualization." In this visualization, a predicted bounding box (labeled "predicted bounding box [cx, cy, w, h]") is overlaid on the original RGB image background, with "jar: 0.00" (possibly a confidence score) indicated. This shows that OWL-ViT has localized and identified the target jar in the RGB image based on the text query "jar."

3.  **Processing by Segment Anything**:
    *   The green rectangle on the right represents the "Segment Anything" (SAM) model, another VLM.
    *   An arrow points from "Predicted bounding box from OWL-ViT" (output of OWL-ViT) to "Segment Anything," indicating that the bounding box information from OWL-ViT is used as input for SAM.
    *   The output of "Segment Anything" is also an "Output Visualization." In this visualization, the original RGB image background appears processed (possibly segmented), and an arrow points to the center of the jar, labeled "crop center [x, y]." This indicates that SAM, using the bounding box from OWL-ViT, has further determined the central cropping coordinates of the target jar.

**Data/Information Flow Summary**: RGB Image + Text Query → OWL-ViT (Target Localization & Recognition, outputs bounding box) → Segment Anything (Target Segmentation or Center Determination based on bounding box).

**Bottom Section: Impact of Different α Values on Voxel Grids**

This part shows how different α (alpha) values affect the coarseness or fineness of the generated voxel grids. Voxel grids are used in VoxAct-B to represent the environment and target objects in a 3D discretized manner.

*   There are three sub-figures, each corresponding to a different α value:
    *   Left sub-figure: α = 1.0. This voxel grid appears the "coarsest," with less detail; objects (like the jar and robotic arm) are represented in a more pixelated manner.
    *   Middle sub-figure: α = 0.3. This voxel grid is finer than α=1.0, with clearer object details.
    *   Right sub-figure: α = 0.1. This voxel grid is the "finest," with the clearest object details and smoother edges.

*   The figure caption states: "We use α = 0.3 for Open Jar." (We use α=0.3 for the "open jar" task). This indicates that for this specific task, a medium-fineness voxel grid was chosen.

**Method Operation Mechanism Revealed**:
Through this figure, we can understand how the VoxAct-B method operates:
1.  **Target Recognition and Localization**: First, a VLM (OWL-ViT) is used to locate and recognize the target object in the scene, combining an RGB image and a text query (e.g., "jar"), outputting its bounding box.
2.  **Target Center Determination**: Then, the bounding box information output by OWL-ViT is passed to another VLM (e.g., Segment Anything) to more precisely determine the central cropping coordinates of the target object or to perform more detailed segmentation.
3.  **Environment Representation**: Next, a voxel grid is constructed to represent the environment and target objects based on this information (possibly along with other sensor data). The fineness of the voxel grid can be adjusted using the parameter α.
4.  **Policy Learning**: Finally, this voxel grid is provided as input to the bimanual manipulation policy to learn the actions for executing the task (e.g., grasping and stabilizing).

The key to this method lies in using VLMs to prioritize key regions in the scene and convert complex visual information into a structured voxel representation, thereby improving the efficiency and generalization capability of policy learning.

**Conclusion**:
The figure illustrates how VoxAct-B combines VLMs (OWL-ViT and Segment Anything) to process image and text information for target object recognition and localization, and to generate voxel grids of varying fineness. Specifically, OWL-ViT is used for object detection (outputting a bounding box), while Segment Anything is used for target segmentation or center point determination based on the bounding box. The fineness of the voxel grid is controlled by the α parameter, and the method uses α=0.3 for the "open jar" task.

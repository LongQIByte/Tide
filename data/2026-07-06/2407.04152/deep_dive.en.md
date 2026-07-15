# VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation

[arXiv](https://arxiv.org/abs/2407.04152)

## Abstract (verbatim)

> Bimanual manipulation is critical to many robotics applications. In contrast to single-arm manipulation, bimanual manipulation tasks are challenging due to higher-dimensional action spaces. Prior works leverage large amounts of data and primitive actions to address this problem, but may suffer from sample inefficiency and limited generalization across various tasks. To this end, we propose VoxAct-B, a language-conditioned, voxel-based method that leverages Vision Language Models (VLMs) to prioritize key regions within the scene and reconstruct a voxel grid. We provide this voxel grid to our bimanual manipulation policy to learn acting and stabilizing actions. This approach enables more efficient policy learning from voxels and is generalizable to different tasks. In simulation, we show that VoxAct-B outperforms strong baselines on fine-grained bimanual manipulation tasks. Furthermore, we demonstrate VoxAct-B on real-world $\texttt{Open Drawer}$ and $\texttt{Open Jar}$ tasks using two UR5s. Code, data, and videos are available at https://voxact-b.github.io.

## Background

**Background Analysis**

Bimanual manipulation technology is widely applicable in robotics, especially in scenarios where objects are too large or heavy for a single arm to handle, or when one arm needs to stabilize an object while the other performs precise operations. This technology is crucial in both household services (e.g., cooking, cleaning) and industrial production (e.g., assembly, packaging), enhancing efficiency and accuracy.

However, existing bimanual manipulation methods face several limitations. Traditional approaches typically rely on large-scale datasets for training policies or decompose actions into primitive steps, which are not only sample-inefficient but also struggle to generalize across different tasks. Additionally, bimanual tasks often require high coordination and fine control, posing challenges to current robotic systems.

To address these issues, this paper proposes a novel method called VoxAct-B. This approach combines voxel representations with Vision Language Models (VLMs) to reduce computational burden while improving sample efficiency and generalization. Specifically, VoxAct-B uses VLMs to identify and crop relevant regions within a scene, constructing a high-resolution voxel grid without increasing computational costs. Moreover, the method employs language instructions to determine the role of each arm (stabilizing or acting), enabling more efficient collaboration.

Compared to previous work, the key innovation of VoxAct-B lies in its integration of voxel representations and VLMs to tackle computational efficiency and generalization challenges in bimanual manipulation. Additionally, the method extends existing benchmarks by introducing asymmetric bimanual tasks and validates its performance in real-world environments. Through these improvements, VoxAct-B demonstrates superior performance in both simulation and practical applications, offering new insights into the development of bimanual manipulation technology.

## Method, Figure by Figure

![Figure 1: VoxAct-B uses voxel representations and language to perform bimanual m](fig1_1.webp)

> Figure 1: VoxAct-B uses voxel representations and language to perform bimanual manipulation with 6-DoF manipulation from both arms. We test three language-conditioned bimanual tasks in simulation and two ( Open Drawer and Open Jar ) on a real-world setup with two UR5s. The prompt for Open Drawer assumes the left arm is stabilizing and the right arm is acting, while the reverse is true for the Open Jar prompt.

This figure (Figure 1) visually presents the core ideas, components, and application scenarios of the VoxAct-B method proposed in the paper "VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation."

First, let's look at the left part of the image, which is a flow diagram illustrating the basic workflow of the VoxAct-B method:
1.  **Vision Language Models (视觉语言模型)**：This module processes input images or scene information. Its function is to "detect object & crop voxel grid" (检测物体并裁剪体素网格). This means it identifies relevant objects in the scene and represents the areas where these objects are located as a voxel grid. Voxels are 3D pixels that can represent the spatial structure and position of objects.
2.  **Bimanual Manipulation Policy (双手操作策略)**：This module receives the "zoomed-in voxel grid" (放大后的体素网格) from the vision language model. It learns and executes "acting and stabilizing actions" (操作和稳定动作) based on this voxel grid. Here, "acting" typically refers to the main task-executing action (e.g., the hand opening a drawer), while "stabilizing" refers to auxiliary actions that maintain stability (e.g., the hand holding the drawer).

Next, the right part of the image shows three specific task examples that use the VoxAct-B method and have been tested in both simulated and real-world environments:

1.  **Open Drawer (打开抽屉)**：
    *   **Task Description**: "Hold the drawer with left hand and open the top/bottom drawer with right hand" (左手扶住抽屉，右手打开顶部/底部的抽屉). This specifies the division of labor between the two arms: the left hand stabilizes, and the right hand performs the operation.
    *   **Simulation and Real World**: This task is demonstrated in both a "Simulation" (模拟) environment and a "Real World" (真实世界) setup. In the simulation environment, a dual-arm robot is shown operating a drawer unit. In the real-world environment, two UR5 robots are shown performing the same task. This indicates that the method is effective not only in simulation but can also be transferred to real robotic platforms.

2.  **Open Jar (打开罐子)**：
    *   **Task Description**: "Grasp the jar with right hand and grasp the lid of the jar with left hand to unscrew it in an anti-clockwise direction until it is removed from the jar" (右手抓住罐子，左手抓住罐子的盖子，逆时针旋转直到盖子从罐子上取下). The division of labor here is reversed compared to the drawer-opening task: the right hand performs the operation (unscrewing the lid), and the left hand stabilizes (holding the jar).
    *   **Simulation and Real World**: Similarly, this task is demonstrated in both simulation and the real world. In the simulation environment, the robot is shown attempting to open a jar. In the real-world environment, UR5 robots are shown executing the task. This demonstrates that the VoxAct-B method has the ability to generalize to different types of bimanual manipulation tasks.

3.  **Put Item In Drawer (将物品放入抽屉)**：
    *   **Task Description**: "Open the top drawer with right hand and put the item in the top drawer with left hand" (用右手打开顶部抽屉，并用左手将物品放入顶部抽屉).
    *   **Start and Goal**: This task is illustrated through "Start" (开始状态) and "Goal" (目标状态) images. In the "Start" state, the item (a small block) is next to the drawer unit, and the drawer is closed. In the "Goal" state, the drawer is open, and the item has been placed inside. Although it's not explicitly stated whether this is simulation or real-world, it represents a type of task the method can handle.

**Data or Information Flow Order**:
*   First, the vision language model processes scene images, detects key objects (e.g., drawer, jar, item), and generates an initial voxel grid representation.
*   This voxel grid might then undergo further processing (as indicated by "zoomed-in" in the figure, meaning magnification) to highlight key regions.
*   This processed voxel grid is then input into the bimanual manipulation policy.
*   The bimanual manipulation policy plans and executes specific actions based on the voxel grid information, such as controlling which arm performs the operation and which provides stabilization, and how to move precisely to achieve the task goal.

**How the Method Works (Specific Operation)**:
This figure reveals the core operational mechanism of the VoxAct-B method:
*   **Language-Conditioned**: Each task has a natural language description (prompt) that guides the robot on how to perform the task, including the division of labor between the arms.
*   **Voxel Representation**: The method uses voxel grids to represent objects and space in the scene. This representation captures the 3D geometric information and spatial relationships of objects.
*   **Vision Language Model**: This model is responsible for converting raw visual information (images) into a structured voxel representation, highlighting key regions relevant to the task. This makes subsequent policy learning more efficient as it focuses on task-relevant parts rather than the entire image.
*   **Bimanual Manipulation Policy**: This policy learns to control two robotic arms (6 degrees of freedom) to perform fine-grained operations and stabilizing actions based on the voxel representation and language instructions. Through this, the policy learns to coordinate the movements of both arms to complete the task.
*   **Generalization Capability**: By testing on different tasks (opening a drawer, opening a jar, putting an item in a drawer) and different environments (simulation and real world), the figure indicates that the VoxAct-B method has a certain degree of generalization capability, adapting to different scenarios and task requirements.

In summary, this figure clearly demonstrates how VoxAct-B utilizes a vision language model to process scene information, generate voxel representations, and use them to train a policy capable of executing complex bimanual manipulation tasks. The method has shown success in both simulated and real-world settings, proving its effectiveness and practicality.

---

![Figure 2: Overview of VoxAct-B. Given RGB-D images and a language goal, we input](fig2_1.webp)

> Figure 2: Overview of VoxAct-B. Given RGB-D images and a language goal, we input an RGB image from the front camera and a text query extracted from the language goal into the Vision Language Models (VLMs). The VLMs output the pose of the object of interest with respect to the front camera. This information determines the language goal and the roles of each arm (i.e., acting or stabilizing ). Additionally, we use the object’s position with the RGB-D images to reconstruct a voxel grid that spans α ⁢ x 3 𝛼 superscript 𝑥 3 \alpha x^{3} italic_α italic_x start_POSTSUPERSCRIPT 3 end_POSTSUPERSCRIPT meters of the workspace using V 3 superscript 𝑉 3 V^{3} italic_V start_POSTSUPERSCRIPT 3 end_POSTSUPERSCRIPT voxels. The zoomed-in voxel grid, the language goal, proprioception data of both robot arms, and an arm ID are provided to an acting policy π a subscript 𝜋 𝑎 \pi_{a} italic_π start_POSTSUBSCRIPT italic_a end_POSTSUBSCRIPT and a stabilizing policy π s subscript 𝜋 𝑠 \pi_{s} italic_π start_POSTSUBSCRIPT italic_s end_POSTSUBSCRIPT . The policies predict the discretized pose of the next best voxel, gripper open action, collision avoidance flag, and arm ID for fine-grained bimanual manipulation.

This figure presents an overview of the VoxAct - B method, and we can break down its workflow into several key steps for better understanding:

### Input Part
First, the inputs of the method include an **RGB - D image** and a **language goal**. Specifically, an RGB image is obtained from the front - facing camera, and a text query is extracted from the language goal. These two pieces of information are fed into the **Vision Language Models (VLMs)**.

### The Role of VLMs
After processing these inputs, the VLMs will output the **pose of the object of interest relative to the front camera**. This pose information has two uses:
- It determines the **language goal** and the **role** of each robotic arm (i.e., which arm is responsible for "acting" and which one is for "stabilizing").
- Combined with the position of the object in the RGB - D image, it is used to reconstruct a **voxel grid**. The workspace covered by this voxel grid has a range of \(\alpha\times\alpha\times\alpha\) meters (where \(\alpha\) is a parameter), and \(V^3\) voxels are used to build it.

### Inputs and Outputs of the Policies
Next, the **zoomed - in voxel grid**, the **language goal**, the **proprioception data of the two robotic arms** (such as joint angles, positions, etc.), and an **arm ID** are provided to two policies:
- **Acting policy \(\pi_a\)**: Its function is to predict the discretized pose of the next best voxel, the gripper opening action, the collision avoidance flag, and the arm ID to achieve fine - grained bimanual manipulation.
- **Stabilizing policy \(\pi_s\)**: Although the figure does not detail its output, according to the method description, it should also be for assisting the stability of bimanual manipulation, possibly predicting parameters related to stabilization.

### Information Flow Order
The overall information flow order is: Inputs (RGB - D image, language goal) → Processing by VLMs (obtaining the object's pose) → Determining the language goal and the arms' roles, reconstructing the voxel grid → Inputting the voxel grid, language goal, proprioception data, and arm ID into the acting and stabilizing policies → The policies output operation - related instructions (pose, gripper action, collision avoidance flag, arm ID, etc.).

### Core Logic of the Method
The core of VoxAct - B lies in using VLMs to extract key regions (object pose) from visual and language information, then representing the workspace with a voxel grid, and combining this information with the robot's own perception data and inputting it into specialized acting and stabilizing policies, so that the policies can learn how to perform fine - grained bimanual operations and stable actions. The advantage of this method is that it can learn policies more efficiently from voxels and has the ability to generalize across tasks. For example, it outperforms strong baselines in simulated environments and can also successfully execute real - world tasks such as "opening a drawer" and "opening a jar".

In short, this method understands the task (language goal) and the scene (the object in the RGB - D image) through VLMs, represents the workspace with a voxel grid, and then uses two policies to handle the operating and stabilizing tasks respectively, thus achieving efficient learning of bimanual operations.

---

![Figure 3: Top : VLMs usage as part of VoxAct-B, visualizing the Open Jar task in](fig3_1.webp)

> Figure 3: Top : VLMs usage as part of VoxAct-B, visualizing the Open Jar task in simulation, showing the role of OWL-ViT and Segment Anything. The RGB images from the front camera shown above are examples of actual (uncropped) images provided as input to the models. Bottom : visualization of different α 𝛼 \alpha italic_α values resulting in coarser grids ( α = 1.0 𝛼 1.0 \alpha=1.0 italic_α = 1.0 ) to finer grids ( α = 0.1 𝛼 0.1 \alpha=0.1 italic_α = 0.1 ). We use α = 0.3 𝛼 0.3 \alpha=0.3 italic_α = 0.3 for Open Jar .

This figure (Figure 3) illustrates the core process of the VoxAct-B method proposed in the paper "VoxAct-B: Voxel-Based Acting and Stabilizing Policy for Bimanual Manipulation," specifically for the "Open Jar" task in a simulated environment, and the visualization of voxel grids under different parameter settings.

Let's first examine the **top part of the figure**, which demonstrates the application of VLMs (Vision Language Models) within the VoxAct-B method for the "Open Jar" task simulation, highlighting the roles of OWL-ViT and Segment Anything, as well as the flow of data:

1.  **Input Section**:
    *   The first module on the left is "RGB Image," showing an actual (uncropped) image captured from a robot's front camera, depicting a jar on a tabletop.
    *   Below it is "Text Query," with the content "jar," which is a text query used to instruct the model to focus on the "jar" in the scene.

2.  **OWL-ViT Module**:
    *   Arrows point from the "RGB Image" and "Text Query" to a pink module labeled "OWL-ViT." This indicates that the OWL-ViT model receives both the image and the text query as inputs.
    *   The output of OWL-ViT is a "predicted bounding box [cx, cy, w, h]," where cx and cy are the center coordinates of the bounding box, and w and h are its width and height.
    *   The "Output Visualization" module on the right shows the result of OWL-ViT: the original image is overlaid with a red bounding box accurately framing the jar, labeled "jar: 0.00" (possibly a confidence score or related metric). This bounding box identifies the key region in the scene related to the text query "jar."

3.  **Segment Anything Module**:
    *   An arrow points from the "predicted bounding box" of OWL-ViT to a green module labeled "Segment Anything." This indicates that the Segment Anything model receives the predicted bounding box from OWL-ViT as input.
    *   The "Output Visualization" module shows the result of Segment Anything: the original image is overlaid with an arrow pointing to the center of the jar, labeled "crop center [x, y]." This suggests that Segment Anything might be used to more precisely determine the center of the target object (the jar) or to crop from this region, providing more accurate information for subsequent voxel reconstruction or policy learning.

The overall data flow is: RGB Image and Text Query -> OWL-ViT (predicts bounding box) -> Segment Anything (uses the bounding box for further processing, e.g., determining crop center).

Now, let's look at the **bottom part of the figure**, which shows the impact of different α (alpha) values on the visualization of voxel grids:

1.  **Three Subfigures**:
    *   The left subfigure corresponds to α = 1.0, the middle one to α = 0.3, and the right one to α = 0.1.
    *   Each subfigure displays a 3D voxel grid visualization, representing some form of representation or reconstruction of the scene (possibly the table, jar, and surrounding environment).

2.  **Effect of α Value**:
    *   The text below the figure states that different α values result in voxel grids ranging from "coarser grids" (rougher grids, α = 1.0) to "finer grids" (more detailed grids, α = 0.1).
    *   Observing the images, when α = 1.0, the voxel grid is sparser and rougher, with less detail in the object representation.
    *   When α = 0.3, the voxel grid is denser than at α = 1.0, with a clearer representation of the object's details.
    *   When α = 0.1, the voxel grid is the densest and finest, with the clearest representation of the object's details.
    *   The paper's abstract mentions they used α = 0.3 for the "Open Jar" task.

This figure reveals how the VoxAct-B method operates:
*   First, visual language models (like OWL-ViT) are used in conjunction with text queries to identify and locate key objects (like the jar) in the scene, obtaining their bounding boxes.
*   Then, another model (like Segment Anything) might be used based on this bounding box for more precise processing, such as determining the crop center or performing more detailed region segmentation.
*   Finally, this information is used to reconstruct a voxel grid, whose level of detail can be adjusted by the parameter α. This voxel grid is provided to the bimanual manipulation policy to learn acting and stabilizing actions.

The bottom part of the figure visualizes how different α values affect the granularity of the voxel grid representation. Coarser grids (high α values) might be more computationally efficient but have less detail, while finer grids (low α values) capture more detail but may have higher computational costs. The paper chose α = 0.3 for the "Open Jar" task, likely as a trade-off between detail and computational efficiency.

In summary, this figure clearly demonstrates how VoxAct-B utilizes VLMs to process image and text information, locate key objects, and generate voxel grids of varying granularity to support the learning of bimanual manipulation policies.

---

![Figure 4: Example successful rollouts (one per row) of VoxAct-B on a real-world ](fig4_1.webp)

> Figure 4: Example successful rollouts (one per row) of VoxAct-B on a real-world bimanual setup with UR5s.

This figure (Figure 4) shows the **successful execution process** of the VoxAct - B method in the real world using UR5 dual - arm robots for bimanual manipulation tasks. It is divided into two rows, with each row corresponding to a task ("Open Drawer" and "Open Jar"), and each row has 5 consecutive steps (frames) to display the dynamic process of the task from the initial state to completion.

### Task 1: Open Drawer (First Row)
- **Initial State (Far Left)**: Two UR5 robot arms are in their initial positions, and there is a small cabinet with a drawer on the right. The scene clearly presents the task environment.
- **Step 1 (Second Column from the Left)**: One of the robot arms (usually the operating arm) starts to move towards the drawer and adjusts its posture to prepare for contacting the drawer, while the other arm maintains an auxiliary or initial posture.
- **Step 2 (Third Column from the Left)**: The end - effector (hand) of the operating arm contacts the handle or edge of the drawer and starts to apply force to pull the drawer. The other arm may adjust its position to stabilize or cooperate.
- **Step 3 (Fourth Column from the Left)**: The drawer is partially opened. The operating arm continues to apply force, and the posture of the other arm is further adjusted to adapt to the movement of the drawer or maintain scene stability.
- **Step 4 (Far Right)**: The drawer is fully opened. The operating arm completes the pulling action, and the postures of the two arms show that the task is successfully completed, with the drawer in an open state.

### Task 2: Open Jar (Second Row)
- **Initial State (Far Left)**: Two UR5 robot arms are in their initial positions, and there is a lidded jar on the table. The scene is the initial environment for the jar - opening task.
- **Step 1 (Second Column from the Left)**: One of the robot arms moves towards the jar, and the end - effector (possibly a gripper) aligns with the lid of the jar, preparing to grasp or operate.
- **Step 2 (Third Column from the Left)**: The end - effector contacts the lid of the jar and starts to apply force to rotate or move the lid. The other arm adjusts its position to stabilize the jar or cooperate in the operation.
- **Step 3 (Fourth Column from the Left)**: The lid is partially unscrewed or moved. The end - effector continues to operate, and the posture of the other arm is further adjusted to adapt to the movement of the lid.
- **Step 4 (Far Right)**: The lid is fully opened (or removed). The end - effector completes the operation, and the postures of the two arms show that the task is successfully completed, with the jar in an open state.

### Revelation of How the Method Works (Understanding VoxAct - B from the Figure)
- **Task Decomposition and Step Execution**: The 5 steps of each task in the figure show how VoxAct - B decomposes complex bimanual manipulation tasks into a series of continuous action steps. By identifying key regions in the scene (such as the drawer, the jar and its components) through Vision Language Models (VLMs) and reconstructing a voxel grid, the policy learns to perform "acting" and "stabilizing" actions on this voxel grid.
- **Bimanual Collaboration**: The collaboration of the two robots in each task shows how VoxAct - B handles the dimensionality of bimanual manipulation (such as coordinating the movements of the two arms, the application of force, and posture adjustment). For example, when opening a drawer, one arm pulls the drawer, and the other may stabilize the cabinet; when opening a jar, one operates the lid, and the other stabilizes the jar.
- **Visualization of Successful Execution**: The successful rollouts (rolling executions) shown in the figure illustrate that VoxAct - B can learn and execute bimanual manipulation tasks in the real world. Each step from the initial state to the completion of the task is clearly presented, verifying the feasibility and effectiveness of the method.

### Conclusion of the Result Figure (Combined with the Paper Background)
- **Task Type**: Two real - world bimanual manipulation tasks (opening a drawer, opening a jar) using UR5 dual - arm robots.
- **Comparison Object**: Although there is no direct comparison in the figure, the paper mentions that VoxAct - B outperforms strong baselines in simulation. The figure shows successful execution in the real world, indicating that the method can be generalized to real - world scenarios.
- **Conclusion**: VoxAct - B can learn and execute complex bimanual manipulation tasks and achieve successful task completion (such as opening a drawer and a jar) in the real world, verifying the effectiveness of it as a language - conditioned, voxel - based bimanual manipulation strategy and supporting the claims of "efficient policy learning" and "task generalization" in the paper.

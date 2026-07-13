# RynnWorld-4D: 4D Embodied World Models for Robotic Manipulation

[arXiv](https://arxiv.org/abs/2607.06559) · [HuggingFace](https://huggingface.co/papers/2607.06559) · ▲89

## Abstract (verbatim)

> Robotic manipulation in the open world requires not only recognizing what a scene looks like, but also anticipating how its 3D structure moves under interaction. We argue that synchronized RGB, depth, and optical flow, namely RGB-DF, provide a physically grounded representation that captures the underlying 4D dynamics of a scene. Compared to 2D pixel videos, this multi-modal synergy aligns visual appearance with geometric structure and temporal motion, creating a representation space significantly closer to the low-level end-effector actions demanded by robotic systems, thereby narrowing the gap between world prediction and policy learning. Building on this insight, we introduce RynnWorld-4D, a generative model that co-produces future RGB frames, depth maps, and optical flow from a single RGB-D image and a language instruction within one unified diffusion process. This 4D world model features a tri-branch architecture that integrates cross-modal attention with frame-wise 3D RoPE, ensuring that appearance, geometry, and motion evolve consistently. To supply training data at scale, we curate Rynn4DDataset 1.0, a massive dataset of over 254.4 million frames across egocentric human and robotic manipulation videos with high-quality pseudo-labels for depth and optical flow. We further propose RynnWorld-4D-Policy, an inverse dynamics head that consumes the internal 4D representations of RynnWorld-4D in a single forward pass, bypassing expensive multi-step denoising, to output robot actions in a closed-loop manner. Experiments show that RynnWorld-4D produces temporally and spatially coherent 4D predictions, and that RynnWorld-4D-Policy achieves state-of-the-art performance on real-world dexterous bimanual manipulation tasks, particularly excelling in tasks demanding spatial precision and temporal coordination.

## Background

### Background Analysis  

**1. Technical Context and Real-World Needs**  
In open-world robotics, understanding and predicting environmental interactions is critical. For example, when a robot grasps or moves an object, it must anticipate the 3D motion of objects (e.g., dropping, sliding, or colliding) under interaction. This capability is essential for real-world tasks like household assistance, industrial assembly, or medical support, where robots must make fast and safe decisions in dynamic environments. Traditional methods relying on 2D images or single modalities (e.g., depth maps) fail to jointly handle spatial structure and temporal dynamics, leading to inaccurate predictions or uncoordinated actions.  

**2. Limitations of Previous Approaches**  
Existing research faces two core challenges:  
- **Shortcomings of 2D representations**: Pixel-based generative models (e.g., video diffusion models) produce realistic visuals but lack geometric and motion information, making precise 6-DoF estimation or depth-aware interaction difficult.  
- **Deficiencies in 3D/4D methods**: Approaches like Neural Radiance Fields (NeRF) or Structure-from-Motion (SfM) are either computationally expensive (e.g., scene-specific optimization) or lack future-state generation (e.g., static point cloud reconstruction). They also often require multi-view inputs or struggle to scale to complex scenes.  

**3. Proposed Solution**  
The paper introduces RynnWorld-4D, a 4D world model that predicts synchronized RGB, depth, and optical flow (RGB-DF) to capture scene dynamics. Key innovations include:  
- **Multi-modal coherent representation**: Depth and optical flow link 2D pixels to 3D geometry and motion, retaining the generative power of video diffusion models while explicitly encoding physical constraints.  
- **Unified generation framework**: A tri-branch transformer generates all modalities in a shared denoising loop, with cross-attention ensuring consistency.  
- **Efficient training data**: Rynn4DDataset 1.0 provides 254M+ frames from human and robotic manipulation videos with auto-generated depth/optical flow labels, addressing the scarcity of large-scale 4D data.  
- **Real-time policy learning**: RynnWorld-4D-Policy extracts robot actions directly from 4D representations in a single forward pass, bypassing slow iterative denoising for high-frequency control.  

**4. Key Differences from Prior Work**  
- **Representation innovation**: Unlike pure 2D or 3D methods, RynnWorld-4D uses RGB-DF to balance generative capability with geometric consistency.  
- **Model simplicity**: Shared diffusion architecture and cross-modal attention avoid multi-stage inference or scene-specific tuning.  
- **Data efficiency**: Pseudo-labels generate large-scale 4D data, reducing reliance on manual annotation or limited multi-view inputs.  

This work provides a representation closer to robot action spaces and demonstrates state-of-the-art performance in real-time manipulation tasks.

## Method, Figure by Figure

![Figure 4 : Overview of RynnWorld-4D. Our pipeline leverages the large-scale Rynn](fig4_1.webp)

> Figure 4 : Overview of RynnWorld-4D. Our pipeline leverages the large-scale Rynn4DDataset 1.0 dataset to train a generative model capable of predicting future 4D sequences. Given a single RGB-D observation and a language instruction, RynnWorld-4D co-generates future RGB frames, depth maps, and optical flow. These predictive 4D representations are then aggregated by RynnWorld-4D-Policy to derive the final robot actions.

This diagram illustrates the overall architecture and workflow of the RynnWorld-4D method, a 4D world model for robotic manipulation. It can predict future 4D sequences (RGB, depth, and optical flow) from a single RGB-D image and language instructions, and generate robot actions based on these predictions.

First, let's look at the input section:
*   **Input data on the left**: Includes three sets of sensor data and one set of text instructions.
    *   **Depth (depth map)**: Represents the geometric information of the scene.
    *   **RGB (color image)**: Represents the appearance information of the scene.
    *   **Optical Flow (optical flow)**: Represents the motion information of objects in the scene. The note "zero flow at t=0" means this is the motion information of the initial frame.
    *   **Text Embed (text embedding)**: Comes from a natural language instruction like "Grasp the watermelon, lift it from the white table," encoded by a "Text Encoder."

Next is the core **RynnWorld-4D Block**:
*   This block adopts a three-branch architecture, processing RGB, depth, and optical flow data separately, but they exchange information through a "Joint Cross-Modal Attn (joint cross-modal attention)" mechanism.
*   **The structure of each branch is similar**:
    *   The input first goes through "noised (noisy)" features processed by a "VAE Encoder (variational autoencoder encoder)." This suggests the model may use a diffusion model paradigm, gradually generating clear predictions from noise.
    *   Then, each branch contains "Self Attn (self-attention)" layers to capture spatiotemporal dependencies within a single modality.
    *   Next are "Cross Attn (cross-attention)" layers and "FFN (feed-forward network)," which are connected to "Joint Cross-Modal Attn" to achieve information fusion between different modalities.
*   **Three branches process in parallel**: RGB, depth, and optical flow are processed through their respective branches, while the joint cross-modal attention mechanism ensures the consistent evolution of appearance, geometry, and motion information.

Then there is the **RynnWorld-4D-Policy** module:
*   This module receives the internal 4D representation from the RynnWorld-4D Block.
*   It first processes these representations through "Spat-Attn (spatial attention)" and "Temp-Attn (temporal attention)" layers, possibly to focus on key spatial locations and time steps.
*   Then it goes through an "FFN" layer.
*   Next, these processed features are combined with "Text Embed (text embedding)" to form a "State (state)" representation.
*   Finally, this state representation is input into a sequence of "M DIT Blocks (DIT blocks)," which may be some kind of decision transformer or similar policy network, ultimately outputting a sequence of robot actions `(A₁, A₂, ..., Aₖ)`. The diagram specifically points out that this policy head can "consume the internal 4D representation of RynnWorld-4D in a single forward pass, bypassing the expensive multi-step denoising process," emphasizing its efficiency.

The order of data flow is:
1.  Original RGB, depth, optical flow images, and text instructions as input.
2.  RGB, depth, and optical flow images are separately processed by their respective VAE encoders, and noise is added.
3.  These noisy features are input into the three branches of the RynnWorld-4D Block for self-attention, cross-attention, and joint cross-modal attention processing.
4.  The RynnWorld-4D Block outputs the predicted future RGB, depth, and optical flow features (the right side of the diagram shows the VAE decoder part where these predictions can be decoded back into images, but this may be mainly for training or visualization rather than direct input to the policy).
5.  The internal representation of the RynnWorld-4D Block is passed to the RynnWorld-4D-Policy module.
6.  The RynnWorld-4D-Policy module processes these representations and combines them with the text instruction to finally output a sequence of robot actions.

This diagram reveals the specific operation of the method:
*   **Multimodal input and fusion**: The method uses information from three modalities (RGB, depth, and optical flow) and fuses them through a cross-modal attention mechanism to capture the 4D dynamics of the scene.
*   **Generative model**: RynnWorld-4D, as a generative model, can predict future 4D sequences based on current observations and language instructions. It may be based on a diffusion model because it uses a VAE encoder and noisy input.
*   **Efficient policy learning**: RynnWorld-4D-Policy directly uses the internal representation of the generative model to predict actions, avoiding the potentially expensive multi-step reasoning or planning required by traditional methods.
*   **End-to-end training**: The entire system seems to be an end-to-end training framework, from perception (predicting future 4D) to action (generating robot actions).

In summary, RynnWorld-4D, through a unified framework, combines multimodal perception (RGB-DF) with language instructions to predict future 4D scene dynamics and efficiently generate robot manipulation actions based on these predictions. This method aims to bridge the gap between world prediction and policy learning, enabling robots to better understand scenes and interact with them.

---

![Figure 3 : Data Curation Pipeline. The video data is collected from diverse sour](fig3_1.webp)

> Figure 3 : Data Curation Pipeline. The video data is collected from diverse sources and partitioned into short clips during data preprocessing. Each clip undergoes a multi-modal annotation process: (1) Video Captioning : Qwen3-VL ( bai2025qwen3 ) generates detailed natural language descriptions of the video content; (2) Optical Flow Estimation : DPFlow ( morimitsu2025dpflow ) computes dense per-frame motion fields, which are visualized and saved as flow videos; (3) Depth Estimation : Depth Anything 3 ( lin2025depth ) produces monocular depth predictions, which are upsampled to the original resolution and saved as depth videos with a global depth range of [ 0.0 , 5.0 ] [0.0,5.0] meters.

This figure illustrates the **data curation pipeline of Rynn4DDataset 1.0**, clearly demonstrating the complete workflow from raw video data to multi - modal annotated results, which helps to understand the construction logic of this dataset:  


### Data Flow and Component Analysis  
1. **Input: Raw Video Data**  
   The "Rynn4DDataset 1.0" area on the left shows the source of the dataset's raw video data. These videos come from diverse scenarios (such as human first - person views, robot operations, etc.). After preprocessing, they are divided into short clips (the preprocessing stage is implicitly included in the logic of "collection and segmentation").  

2. **Multi - Modal Annotation Workflow (Arrow Direction: From Left to Right)**  
   The raw video clips sequentially go through three core annotation steps, and each step is completed by a specific tool/model, with the output being multi - modal data of the corresponding type:  
   - **Video captioning**: The `Qwen3 - VL` model (cited in the paper as bai2025qwen3) generates **natural language descriptions** of the video content (for example, the "Move the apple from the plate to the table." in the lower right corner is a typical description example). This step endows the video with semantic - level interpretation and helps to associate visual content with task intentions.  
   - **Flow annotation**: The `DPFlow` model (cited in the paper as morimitsu2025dpflow) calculates the **dense motion field of each frame** (i.e., optical flow). The optical flow is visualized and saved as an "optical flow video", which is used to capture the motion trend of objects in the scene (the color - coded image in the "Optical Flow" area of the figure is the visualization result of the optical flow. Different colors represent different motion directions/speeds).  
   - **Depth annotation**: The `Depth Anything 3` model (cited in the paper as lin2025depth) generates **monocular depth predictions**. The depth map is upsampled to the original resolution and saved as a "depth video" with a global depth range of "[0.0, 5.0] meters" (the gray - scale image in the "Depth" area of the figure is the visualization of the depth map. The gray - scale value corresponds to the distance, usually the brighter/darker represents the closer/farther distance).  


### Intuitive Understanding of Method Operation  
This figure reveals the **construction logic of Rynn4DDataset 1.0**: by "multi - modal annotation", the raw video is transformed into **synchronized RGB (implicit in the video clips), depth, and optical flow (i.e., RGB - DF)** data. The design of this multi - modal collaboration aligns the visual appearance (RGB), geometric structure (depth), and temporal motion (optical flow) in the representation space, which is closer to the low - level action logic required by the robot's end - effector, thus narrowing the gap between "world prediction" and "policy learning" (this also echoes the core view of the paper's abstract that "multi - modal collaboration is important for robotic manipulation").  

In simple terms, the workflow is: **Raw Video → Multi - Modal Annotation (Description, Optical Flow, Depth) → Multi - Modal Dataset (Rynn4DDataset 1.0)**. Each annotation step targets a specific modality (semantic, motion, geometry), and the final multi - modal data provides a training foundation for the subsequent "RynnWorld - 4D" generative model (the model needs to predict future RGB, depth, and optical flow from a single RGB - D image + language instruction).  


### Key Detail Supplements  
- **Optical Flow Visualization**: The color - coded image in the "Optical Flow" area of the figure uses a common optical flow visualization method (such as the HSV color space, where hue represents direction and saturation represents speed) to help intuitively understand the motion of objects.  
- **Depth Visualization**: The gray - scale image in the "Depth" area maps the distance through brightness, making the depth information easier to interpret.  
- **Role of Language Description**: The video description (such as "move the apple") endows the dataset with task - oriented semantics, which is crucial for the subsequent "inverse dynamics head (RynnWorld - 4D - Policy)" to output robot actions from the 4D representation.  

This figure, through a clear workflow and visualization results, shows how to build a multi - modal dataset containing semantic, motion, and geometric information from raw videos, providing a data foundation for the research of robotic manipulation.

---

![Figure 5 : Real-world Manipulation Benchmark. We establish a comprehensive evalu](fig5_1.webp)

> Figure 5 : Real-world Manipulation Benchmark. We establish a comprehensive evaluation suite comprising six diverse tasks to assess the model’s performance in open-world manipulation, providing a rigorous testbed for our 4D world model.

This diagram showcases the **Real-world Manipulation Benchmark** proposed in the paper, which consists of six distinct tasks designed to evaluate a model's performance in open-world manipulation. It provides a rigorous testbed for 4D world models.

---

### Task Breakdown (Left to Right, Top to Bottom)
1. **Dual Picking**  
   - The image shows two robotic arms (or two "hands" of a single arm), with red arrows and numbers (1, 2, 3, 4) indicating the sequence of actions. Numbers 1 and 2 likely represent different stages of grasping objects, while 3 and 4 may indicate auxiliary movements or changes in object positions. The workflow involves the arm executing pick-and-place actions in order, demonstrating the model’s ability to handle multiple objects sequentially or simultaneously.  
   - Data flow: Starting from the initial arrangement of objects (e.g., black, yellow, brown items), the arm follows the arrow-guided sequence (e.g., 1→2→3→4) to complete the dual picking task, showcasing its understanding of multi-object manipulation.

2. **Block Pushing**  
   - A robotic arm is shown pushing blocks, with red arrows and numbers (1, 2, 3, 4) illustrating the pushing sequence. Numbers 1 and 2 may denote different phases or directions of pushing, while 3 and 4 could indicate positional changes or auxiliary actions. The arm moves blocks to target locations, demonstrating its capability in object manipulation.  
   - Data flow: Starting from the initial block positions, the arm follows the arrow-guided sequence to push blocks into place, highlighting its understanding of force application and spatial reasoning.

3. **Hand-over**  
   - Objects are transferred between robotic hands (or tools), with red arrows and numbers (1, 2, 3) showing the handover sequence. Numbers 1 and 2 likely represent stages of transferring an object from one hand to another, while 3 may indicate final positioning. This task evaluates the model’s ability to coordinate precise object transfers.  
   - Data flow: Starting with an object in one hand (e.g., a yellow item), the arm follows the sequence to transfer it to the other hand, demonstrating its grasp of dynamic interaction.

4. **Bimanual Lifting**  
   - Two robotic arms (or two parts of a single arm) collaborate to lift a heavy object (e.g., a watermelon-shaped item). Red arrows and numbers (1, 2) indicate the lifting sequence, with each number representing a stage of coordinated effort. This task tests the model’s ability to execute synchronized bimanual actions.  
   - Data flow: Starting from the object’s initial position, the arms follow the sequence to lift it collaboratively, showcasing their coordination.

5. **Lid Placement**  
   - A robotic arm places a lid (or similar object) onto a target surface (e.g., a table). Red arrows and numbers (1, 2) show the process: 1 for grasping the lid, 2 for placing it. This evaluates the model’s precision in object placement.  
   - Data flow: Starting with the lid near the arm, it follows the sequence to grasp and position the lid accurately.

6. **Bowl Stacking**  
   - A robotic arm stacks bowls by first grasping a bowl (arrow 1) and then placing it atop another (arrow 2). This task assesses the model’s ability to perform sequential stacking actions.  
   - Data flow: Starting with bowls in their initial positions, the arm follows the sequence to stack them, demonstrating spatial awareness and coordination.

---

### Methodology in Action  
The diagram evaluates the performance of the RynnWorld-4D model using six real-world tasks. Each task features a clear action sequence (via arrows and numbers), requiring the model to interpret 3D scene structures (via RGB-DF—synchronized RGB, depth, and optical flow) and predict interactive actions. For instance, in "Dual Picking," the model must recognize object positions to plan sequential grasps, while in "Block Pushing," it must calculate force and trajectory. The core idea leverages multi-modal RGB-DF representations to capture 4D dynamics (appearance, geometry, and temporal motion), enabling the model to learn low-level end-effector actions (e.g., grasping, pushing) and bridge the gap between world prediction and strategy learning.

---

### Implications for Results  
The tasks cover diverse manipulation types (picking, pushing, handover, lifting, placement, stacking) to comprehensively assess the model’s open-world capabilities. If the model succeeds in these tasks (in testing), it demonstrates RynnWorld-4D’s effectiveness in understanding and predicting 4D dynamics, making it suitable for real-world robotic operations. These tasks serve as a rigorous benchmark to validate whether the model can integrate world prediction with strategy learning for efficient robot manipulation.

---

![Figure 1 : Given an input RGB-D image and description, RynnWorld-4D generates RG](fig1_1.webp)

> Figure 1 : Given an input RGB-D image and description, RynnWorld-4D generates RGB, depth, and optical flow videos synchronously, which can be further lifted into 3D scene flow (right).

This figure illustrates the core workflow of the RynnWorld-4D model, a 4D world model designed for robotic manipulation. Let's break it down step-by-step:

1.  **Input Section**:
    *   On the left, we see the model's inputs. At the top is a natural language instruction, for example, "Move the apple from the plate to the table." This instruction dictates the desired action.
    *   Below the instruction are two visual inputs:
        *   "RGB input": A single RGB image showing the initial scene, such as a person manipulating an object (appearing to be an apple).
        *   "Depth input": A corresponding depth map, which provides geometric information about the scene (darker areas typically represent farther distances, brighter areas nearer). This gives the model structural context.

2.  **Model Processing and Generation Section**:
    *   The central blue rectangle labeled "RynnWorld-4D" represents the core model. Arrows point from the inputs to this model, indicating it receives this information.
    *   The model's output consists of three synchronously generated "video" sequences, displayed side-by-side to the right of the model:
        *   "RGB Video": The future RGB image sequence generated by the model. These images show how the scene visually changes after the instruction is executed. For instance, the position of the hand and apple changes.
        *   "Depth Video": The corresponding depth map sequence generated by the model. These depth maps show the change in the scene's geometry over time, consistent with the motion in the RGB video.
        *   "Optical Flow Video": The optical flow map sequence generated by the model. Optical flow visualizes the direction and magnitude of pixel motion between frames, often color-coded (e.g., red might indicate rightward motion, blue leftward). This directly reflects the 2D motion of objects in the image plane.

3.  **Transition from 2D to 3D**:
    *   The rightmost section is labeled "3D Flow." An arrow points from the "RGB Video," "Depth Video," and "Optical Flow Video" to this section. This indicates that the multi-modal information (RGB, depth, optical flow) generated by the model can be further processed to infer the 3D motion flow (3D Flow) of the scene. 3D Flow provides object motion information in three-dimensional space, which is crucial for understanding object movement in robotic manipulation. The image shows a point-cloud representation of a 3D scene with vectors indicating motion, visually demonstrating the 3D Flow.

4.  **Information Flow Summary**:
    *   The data flow is: **Inputs (RGB-D image + language instruction) -> RynnWorld-4D model -> Generates multi-modal outputs (RGB video, depth video, optical flow video) -> (Optionally) Further processed to obtain 3D Flow**.
    *   This process reveals the core of the RynnWorld-4D method: it can predict future visual appearance (RGB), geometric structure (depth), and motion (optical flow) based on the current scene (RGB-D image) and an action instruction (language). This multi-modal prediction capability allows the model to better understand the 4D dynamics (3D space + time) of a scene and provide more accurate predictions and planning for robotic manipulation. By generating these related modalities simultaneously, the model ensures consistent evolution of appearance, geometry, and motion.

In essence, this figure clearly demonstrates how RynnWorld-4D takes a static RGB-D image and a language instruction, generates future RGB, depth, and optical flow videos to capture and predict the scene's 4D dynamics, and can ultimately infer 3D motion.

---

![Figure 2 : Composition of the Rynn4DDataset 1.0 dataset. We provide a large-scal](fig2_1.webp)

> Figure 2 : Composition of the Rynn4DDataset 1.0 dataset. We provide a large-scale hybrid collection of 254.4M frames, balancing human egocentric videos with diverse robotic manipulation data. This diversity ensures that the world model learns both general object interaction priors and robot-specific execution traces.

This figure illustrates the composition of the Rynn4DDataset 1.0, a large-scale hybrid dataset containing 254.4 million frames, balancing human egocentric videos with diverse robotic manipulation data. This diversity ensures that the world model learns both general object interaction priors and robot-specific execution traces.

First, we observe that the total number of frames in the dataset is 254.4M, with a total duration of 2,354.9 hours (calculated at 30 frames per second), and it comes from 7 source datasets. The dataset is divided into two main parts:

1. **Human demonstration videos**:
   - There are a total of 20.6M frames, accounting for 8.1% of the entire dataset.
   - This part of the data is further divided into two sources:
     - **EgoVid**: 15.9M frames, accounting for 77.2% of the human demonstration part.
     - **Epic-Kitchens**: 4.7M frames, accounting for 22.8% of the human demonstration part.

2. **Embodied interaction sequences**:
   - There are a total of 233.8M frames, accounting for 91.9% of the entire dataset.
   - This part of the data comes from multiple robotic manipulation datasets, specifically including:
     - **AgiBot**: 158.4M frames, accounting for 67.8% of the embodied interaction part.
     - **RoboCoin**: 51.1M frames, accounting for 21.9% of the embodied interaction part.
     - **Galaxea**: 14.6M frames, accounting for 6.2% of the embodied interaction part.
     - **RDT-1B**: 2.0M frames, accounting for 0.9% of the embodied interaction part.
     - **RoboMIND**: 7.7M frames, accounting for 3.3% of the embodied interaction part.

From the figure, it can be seen that the construction of the dataset is to balance human-perspective video data and robot-operated embodied interaction data. Human demonstration videos provide a general understanding of everyday scenes, while embodied interaction sequences provide robot-specific operational experience and execution traces. This balanced dataset design helps train a world model that can learn general object interaction priors and robot-specific execution traces.

In this way, Rynn4DDataset 1.0 provides rich data support for the training of the RynnWorld-4D model, enabling the model to generate future RGB frames, depth maps, and optical flow maps from a single RGB-D image and a language instruction within a unified diffusion process. The combination of multi-modal data ensures the synergy between visual appearance, geometric structure, and temporal motion, thereby narrowing the gap between world prediction and policy learning.

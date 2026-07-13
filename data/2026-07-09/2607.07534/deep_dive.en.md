# Infinite Worlds with Versatile Interactions

[arXiv](https://arxiv.org/abs/2607.07534) · [HuggingFace](https://huggingface.co/papers/2607.07534) · ▲32

## Abstract (verbatim)

> We present LingBot-World 2.0 (also known as LingBot-World-Infinity), an advanced iteration of LingBot-World featuring four distinct upgrades. (1) Our model achieves an unbounded interaction horizon while maintaining consistent output quality, benefiting from a carefully crafted causal pretraining paradigm. (2) Through distilling a real-time variant from the base model, our system guarantees rapid response time, sufficient to drive 720p video streams at 60 fps. (3) Compared to the previous version, this update introduces highly diverse interactive elements, comprising a broader spectrum of actions (e.g., attacking, archery, spell-casting, and shooting) alongside a richer variety of text-driven events. (4) We pioneer the integration of an agentic harness within the domain of world modeling, wherein a pilot agent is tasked with planning and executing character behaviors, while a director agent is responsible for synthesizing novel environmental elements as the scene progresses. Additionally, to facilitate a shared experience, we develop an interface that permits multiple players to simultaneously immerse themselves in this vivid world simulator. We pair our primary 14B model with a lightweight 1.3B counterpart, which supports effortless deployment on a single GPU.

## Background

### Background Analysis  

**Technical Context**  
Interactive world models are technologies that generate environments in real time based on user or agent actions, primarily used in game development and virtual simulation. For example, they can create immersive virtual worlds where players freely explore and interact with the environment, or simulate physical rules (e.g., gravity, collisions) to train robots. The core demand for such technologies is to make virtual worlds "alive"—with realistic visuals and instant responses to user inputs, thus providing an engaging experience.  

**Previous Limitations**  
Despite their potential, past approaches suffer from two critical flaws:  
1. **Lack of long-term stability**: Since each frame depends on previous outputs, errors accumulate over time, causing visual distortions (e.g., blurred textures, warped geometry). Most systems only remain stable for seconds to minutes, failing to build a persistent world.  
2. **Poor high-fidelity interactivity**: Real-time rendering of detailed scenes with responsive inputs requires heavy computational resources. Early systems often sacrificed resolution or smoothness, resulting in crude interactions (e.g., slow camera movements).  

**Proposed Solutions**  
This paper addresses these issues with four innovations:  
1. **Stable causal generation model**: Improved training methods ensure the model maintains visual quality over extended periods, preventing error accumulation.  
2. **Real-time distillation**: A lightweight version of the model renders dynamic scenes at 720p/60 fps while preserving responsiveness.  
3. **Rich interaction space**: The system supports complex actions (e.g., attacking, spell-casting) and dynamic environmental changes (e.g., weather manipulation).  
4. **Agent collaboration framework**: Two agents—a "pilot" controlling character behavior and a "director" generating new content—enable the world to evolve autonomously rather than following pre-scripted plots.  

**Unique Approach**  
Unlike prior work, this study’s key breakthrough lies in combining "stability" and "interactivity": the causal model solves long-term drift, while distillation achieves real-time performance. Additionally, the agent framework introduces autonomy, a departure from script-driven designs in previous research.

## Method, Figure by Figure

![Figure 4 : Overview of LingBot-World-Infinity DiT Block and MoBA Attention Mask.](fig4_1.webp)

> Figure 4 : Overview of LingBot-World-Infinity DiT Block and MoBA Attention Mask. The action comprises camera poses and chunk-wise prompts, injected into the DiT block to enable user interaction. For self-attention, a bidirectional block is appended to teacher forcing mask, enabling autoregressive generation while preserving visual fidelity. For cross-attention, the autoregressive component attends to a background prompt and chunk-wise prompts of lower-triangular pattern to prevent access to future information, while the bidirectional component attends to a global prompt.

This figure illustrates the LingBot - World - Infinity DiT (Diffusion Transformer) Block and the MoBA (presumably a type of attention mechanism) Attention Mask. Let's first analyze the DiT Block on the left:

1. **Input and Initial Processing**: The "Video Latent" (video latent representation) serves as the input to the DiT Block. It first enters the "Self - Attn" (Self - Attention) module. Here, a bidirectional block is appended with a teacher - forcing mask. This setup enables autoregressive generation while maintaining visual fidelity. After that, the "Pose Scale & Shift" module processes action - related information. The actions include camera poses and chunk - wise prompts. Then, the "Plucker Encoder" encodes the pose information into a format suitable for subsequent processing, and the output is "Pose_i" (the i - th pose).

2. **Cross - Attention and Interaction**: Next is the "Cross - Attn" (Cross - Attention) module. The autoregressive component of this module attends to the background prompt and chunk - wise prompts in a low - triangular pattern to prevent access to future information. The bidirectional component, on the other hand, attends to the global prompt. Meanwhile, "Prompt_i" (the i - th prompt) is injected into the cross - attention module, which enables user interaction. Finally, the "FFN" (Feed - Forward Network) further processes the information that has gone through the attention mechanisms and then outputs the processed "Video Latent".

3. **Attention Masks on the Right**:
    - **Self - Attn Mask**: This mask shows the attention relationships between different elements (such as \(x_0\), \(x_1\), \(x_2\), \(x_0^f\), \(x_1^f\), \(x_2^f\), etc.). The cells filled with blue represent allowed attention connections. This ensures autoregressive generation while maintaining visual fidelity. For example, \(x_0\) can attend to \(x_0\), \(x_1\), \(x_2\), and \(x_0^f\) can attend to \(x_0^f\), \(x_1^f\), \(x_2^f\), etc. This pattern helps in utilizing historical information during the generation process.
    - **Cross - Attn Mask**: This mask shows the attention relationships between different elements (such as \(a_G\), \(a_B\), \(a_0\), \(a_1\), \(a_2\), etc.). The cells filled with purple represent allowed attention connections. The autoregressive component here attends to the background prompt and chunk - wise prompts in a low - triangular pattern to prevent access to future information, while the bidirectional component attends to the global prompt. For example, \(a_0\) can attend to \(a_G\), \(a_B\), \(a_0\), \(a_1\), and \(a_1^f\) can attend to \(a_G\), \(a_B\), \(a_0\), \(a_1\), \(a_2^f\), etc. This pattern helps in correctly utilizing the prompt information during cross - attention.

In summary, this DiT Block, through the self - attention and cross - attention mechanisms, combined with pose encoding and prompt injection, realizes user interaction and autoregressive generation. At the same time, the attention masks ensure the correct flow of information and prevent access to future information, thus achieving an unbounded interaction horizon and high output quality.

---

![Figure 3 : Overview of LingBot-World-Infinity Pipeline. An interactive world sim](fig3_1.webp)

> Figure 3 : Overview of LingBot-World-Infinity Pipeline. An interactive world simulator is implemented as a causal video model. Our Infinity World is initialized from an initial image and its background description. The future world states are then autoregressively generated, conditioned on the historical context and user inputs (camera poses and prompts).

This figure provides an overview of the LingBot-World-Infinity pipeline, which implements an interactive world simulator as a causal video model. Here is a detailed explanation of each component and the flow of information in the image:

1. **Initial State**:
   - The image in the bottom-left corner shows the initial scene, featuring a character (a person on a motorcycle) and a background.
   - The "BG Prompt" (Background Prompt) below the image represents the textual input describing the background, which provides the initial background information for the model's generation.

2. **User Input**:
   - There are multiple "User Input" modules in the figure, each containing a keyboard layout and a "Prompt".
   - The keys in the keyboard layout (such as W, A, S, D, arrows, etc.) represent user actions, such as movement, attack, turning, etc.
   - Each "Prompt" (e.g., Prompt₁, Prompt₂, Prompt₃) is a textual input provided by the user to describe the desired event or action, such as "attack the enemy," "cast a spell," etc.

3. **DiT Block × N (Causal Self-Attention & Chunk-Wise Cross-Attention)**:
   - The purple area in the middle represents the core part of the model, consisting of multiple DiT (Diffusion Transformer) blocks stacked together.
   - These blocks use causal self-attention (Causal Self-Attn) and chunk-wise cross-attention (Chunk-Wise Cross-Attn) to process the historical context and user input, generating future world states.
   - Causal self-attention ensures that the generation process is autoregressive, meaning that future states depend on past events.

4. **Future World States (1st State, 2nd State, 3rd State, ...)**:
   - The upper part of the figure shows multiple future world state images, each corresponding to a different time step.
   - These states are autoregressively generated based on the initial state, user input, and the processing results of the model.
   - Arrows indicate the direction of information flow, from the initial state and user input through the DiT block processing to generate future world states.

5. **Infinite Loop (∞ Symbol)**:
   - The ∞ symbol on the left indicates that this process is infinite, meaning the model can continuously generate future world states without restarting.

Overall, this figure illustrates the workflow of LingBot-World-Infinity: starting from an initial image and background description, driven by user input (actions and text prompts), and using a causal video model (DiT blocks) to autoregressively generate future world states, thus achieving an infinitely interactive world simulator. This process ensures consistent output quality and can respond to user input in real-time, supporting 720p video streams at 60 frames per second.

---

![Figure 5 : Overview of the Agentic Interaction Harness. Users can either interac](fig5_1.webp)

> Figure 5 : Overview of the Agentic Interaction Harness. Users can either interact with the existing world through semantic or object-centric actions, or intervene by introducing high-level textual events. The VLM (Director) performs causal reasoning and proposes coherent event updates, while the Video Generator (Pilot) grounds these semantic decisions into physically consistent video rollouts, enabling continuous interactive world simulation.

This figure illustrates the overall architecture of the "Agentic Interaction Harness," which clearly depicts the workflow of an interactive world simulation system. We can parse the various components and their information flow step-by-step from left to right and top to bottom:

First, at the top of the figure is the "User." The user interacts with the system through two modes:
1.  **Mode A (Mode A: Direct Semantic Interaction)**: This is a direct semantic interaction method, where users can express intentions or issue commands through text input or similar means.
2.  **Mode B (Mode B: Tracking-Assisted Object Interaction)**: This is an object interaction method assisted by tracking, where users might select specific objects in the scene and then perform actions on them (like moving, rotating, etc.).

The output from these two interaction modes flows to the central "Brain (VLM)" module. This "Brain" module is labeled as a VLM (Vision-Language Model), and its main function is to "Analyze Scene, Reason, Propose Events." This means it receives information about the current "Current World State" (as shown on the left, an image of a living room) and, combined with user interaction commands, performs understanding and reasoning to generate a series of possible "Event Proposals."

Next, the "Event Proposal" section shows some specific examples, such as "Open Door," "Light On," "Exit," etc. These proposals represent the plausible actions or events that the system believes might occur based on user input and the analysis of the current scene.

Then, these "Event Proposals" are passed to the "Cerebellum (Generator)" module below. This "Cerebellum" module is labeled as a "Generator," and its task is to "Simulate Physical Dynamics, Generate Next Video Frames." It is responsible for transforming abstract event proposals into concrete, physically consistent visual representations. For instance, if the event proposal is "Open Door," this module would generate an animation frame showing the door being opened.

Finally, the new visual content generated by the "Cerebellum" forms the "Updated World State" (as shown on the right, possibly an image of the living room with the door open). This "Updated World State" then feeds back into the input of the system, becoming the "Current World State" for the next interaction cycle, thus forming a "Continuous Interactive Loop."

In summary, the workflow of this system is: User inputs commands through semantic or object interaction modes -> The VLM (Brain) analyzes the current world state and, combining it with user commands, performs reasoning to propose possible events -> The Generator (Cerebellum) simulates physical dynamics based on these event proposals and generates new video frames, updating the world state -> The updated world state then becomes the input again, starting the next interaction cycle. This framework allows users to continuously interact with a virtual world and receive visual feedback for each interaction.

The figure also implies two core roles: the VLM acts as the "Director," responsible for causal reasoning and proposing coherent event updates; while the video generator acts as the "Pilot," responsible for grounding these semantic decisions into physically consistent video rollouts (i.e., sequences of video frames). This division of labor enables the system to achieve continuous interactive world simulation.

---

![Figure 2 : Overview of the proposed data engine. Heterogeneous raw videos are te](fig2_1.webp)

> Figure 2 : Overview of the proposed data engine. Heterogeneous raw videos are temporally segmented, filtered, and routed to category-specific annotation pipelines, producing optimized chunk-wise captions.

This figure illustrates the overall architecture of the **data engine** proposed in the paper, describing the complete process from raw data collection to the final generation of a training dataset. It can be divided into three main stages: Data Acquisition, Data Profiling, and Chunk-wise Multi-dimensional Annotation.

First, in the leftmost **Data Acquisition** stage, the system collects three different types of heterogeneous video data sources:
1.  **Egocentric Videos**: Typically refers to videos shot from the wearer's perspective, such as those captured by VR devices.
2.  **Synthetic Data**: Virtual data generated by computers, for example, videos generated by game engines.
3.  **Web Videos**: Public videos obtained from the internet.
These different data sources are integrated into a module called **Standardized Metadata**, which aims to unify and preprocess the heterogeneous yet complementary data sources in preparation for subsequent processing.

Next, the data flows to the middle **Data Profiling** stage. The goal of this stage is to evaluate, filter, and organize the video data:
1.  **Video Slicing**: First, the raw videos are temporally segmented based on some **Basic Constraints** into shorter clips. This step is to decompose long videos into more manageable and analyzable units.
2.  **Technical Scoring**: The sliced video clips are assessed for their technical quality, represented in the figure by star ratings (e.g., four and a half stars). This helps in filtering out higher-quality clips.
3.  **VLM Profiling**: This step involves a more in-depth analysis of the video clips to extract their **Quality Attributes** and **Semantic Attributes**. Quality attributes might relate to resolution, clarity, etc., while semantic attributes focus on the semantic information of the video content, such as scenes, actions, etc.
After this profiling, the system obtains **Retained Candidate Clips with Profiling Tags**. These clips are selected based on the profiling results and are accompanied by tags describing their characteristics, preparing them for the subsequent annotation phase. The overall goal of this stage is to achieve "low-cost quality control" and "semantic organization for balancing and routing."

Finally, the data enters the rightmost **Chunk-wise Multi-dimensional Annotation** stage, which is crucial for generating the final training data:
1.  **Clip Input**: The candidate video clips obtained from the previous stage serve as input.
2.  **Global Context Construction**: The system uses **Profiling Tags** to build global context information for each video clip, which aids in understanding the clip's meaning in a broader scope.
3.  **Routing by Profiling Tags**: Based on the global context and profiling tags, video clips are routed to appropriate annotation pipelines.
4.  **Multi-track Event-level Annotation**: This is the core annotation phase, involving multiple parallel annotation tracks:
    *   **Character**: Annotations related to characters, such as **Motion** (e.g., walking, attacking, casting spells) and **Interaction** (e.g., interactions with other characters).
    *   **Scene**: Annotations related to the scene, such as **Dynamic** elements (e.g., moving objects) and **Static** elements (e.g., buildings, environment).
    *   During the annotation process, **Action Context (for control input)** might be referenced, such as information from **Cameras** (viewpoint info), **Actions** (e.g., WASD keys), and **Operations**.
5.  **Chunk-wise Optimization**: The annotated clips are optimized to improve data quality and consistency. Icons like charts, rockets, and stars in the figure suggest that the optimization process might involve performance enhancements, efficiency improvements, etc.
After these steps, the final **Training Dataset for Interactive World Model** is generated. This dataset contains processed video clips with detailed multi-dimensional annotations, which can be used to train AI models capable of complex interactions (like LingBot-World 2.0 mentioned in the paper).

In summary, this figure reveals how the method works: it first collects raw video data from multiple sources, then automatically profiles and filters this data, and finally generates a high-quality training dataset through meticulous multi-track, multi-dimensional annotation. The entire process aims to handle heterogeneous data, ensure data quality, and provide effective training material for complex interactive world models. Data flows from left to right, with each stage processing the data in a specific way to progressively enhance its quality and usability, ultimately serving the training objective.

---

![Figure 6 : In the tracking-mode interface, the Vision-Language Model (VLM) compr](fig6_1.webp)

> Figure 6 : In the tracking-mode interface, the Vision-Language Model (VLM) comprehends interactive objects within the scene, while the tracking model continuously tracks these targets to display dynamic interactive floating windows (event cards) in real-time. Powered by the "Director-Pilot" co-simulation framework, the model demonstrates robust interactive capabilities by performing causal reasoning based on user actions (e.g., pushing a door open or rotating a soccer ball) and rendering physically logical, highly coherent spatio-temporal dynamics.

This figure (Figure 6) from the paper "Infinite Worlds with Versatile Interactions" illustrates the "tracking-mode interface" of its proposed LingBot-World 2.0 (or LingBot-World-Infinity) system and its core functionalities.

We can divide the image into two main sections, each demonstrating a specific interaction example to show how the system operates:

**Upper Section: Door-Opening Interaction Example**
This part consists of a sequence of consecutive image frames showing a user interacting with a door.
1.  **Scene and Object**: The image shows a person standing in front of a wooden door. The door is the primary interactive object.
2.  **Interactive Action**: The sequence of images from left to right depicts the user performing the action of "pushing the door handle downward while applying forward pressure to swing the door open."
    *   The first image: The user's hand approaches the door handle.
    *   Subsequent images: The user's action becomes clearer, with the hand grasping the door handle and applying force.
3.  **Floating Window (Event Card)**: In some of the image frames (particularly the middle ones), a black floating window (event card) is visible near the door handle. This window is a key output of the system, generated by the Vision-Language Model (VLM) after understanding the interactive objects in the scene, and displayed in real-time by the tracking model that continuously tracks these targets.
4.  **Text Description**: Below this section, there is a line of text: "[T] Push the door handle downward while applying forward pressure to swing the door open." This text describes the action being performed, possibly representing the system's understanding of the user's intent or a summary of the interactive event.
5.  **Information Flow and Reasoning**: User performs an action -> VLM recognizes the door and door handle -> Tracking model tracks these targets -> The system generates and displays a floating window (event card) related to this interaction -> The system performs causal reasoning based on the user's action and renders physically logical, highly coherent spatio-temporal dynamics (i.e., the door is opened).

**Lower Section: Rotating Soccer Ball Interaction Example**
This part also consists of a sequence of consecutive image frames showing a user interacting with a soccer ball.
1.  **Scene and Object**: The image shows a pair of hands manipulating a soccer ball, with an indoor environment (like a table) in the background.
2.  **Interactive Action**: The sequence of images from left to right depicts the user performing the action of "rotating the ball in your hands to inspect the condition of the black and white panels."
    *   The first image: The hands begin to contact the soccer ball.
    *   Subsequent images: The hand movements show the soccer ball being rotated.
3.  **Floating Window (Event Card)**: Similar to the upper section, a black floating window (event card) is visible near the soccer ball in some of the image frames. This window is also an output of the system, displaying information related to the current interaction.
4.  **Text Description**: Below this section, there is a line of text: "[T] Rotate the ball in your hands to inspect the condition of the black and white panels." This text describes the action being performed, possibly representing the system's understanding of the user's intent or a summary of the interactive event.
5.  **Information Flow and Reasoning**: User performs an action -> VLM recognizes the soccer ball -> Tracking model tracks the soccer ball -> The system generates and displays a floating window (event card) related to this interaction -> The system performs causal reasoning based on the user's action and renders physically logical, highly coherent spatio-temporal dynamics (i.e., the soccer ball is rotated, and the user inspects its condition).

**Specific Revelation of Method Operation**:
This figure clearly demonstrates how the LingBot-World 2.0 system achieves powerful interactive capabilities through the "Director-Pilot" co-simulation framework:
*   **Role of the Vision-Language Model (VLM)**: The VLM is responsible for understanding the interactive objects in the scene (e.g., door, doorknob, soccer ball). This is the foundation for the system to generate relevant interaction information and perform subsequent reasoning.
*   **Role of the Tracking Model**: The tracking model is responsible for continuously tracking these interactive objects. This enables the system to update in real-time and display dynamic interactive floating windows (event cards) related to the target objects.
*   **Causal Reasoning and Dynamic Rendering**: The system can perform causal reasoning based on user actions (e.g., pushing a door, rotating a ball). This means the system understands the purpose and consequences of the user's actions and accordingly renders spatio-temporal dynamics that are physically logical and highly coherent. For example, when the user pushes the door, the door opens; when the user rotates the ball, the perspective of the ball changes, showing different panels.
*   **"Director-Pilot" Co-simulation Framework**: Although the figure does not directly show the two agents, the text indicates that the system benefits from this framework. It can be understood that the "Pilot" agent is responsible for planning and executing character behaviors (like the user actions shown), while the "Director" agent is responsible for synthesizing new environmental elements (although environmental elements are relatively static in these specific examples, the system possesses this capability).
*   **Real-time Performance and Coherence**: The consecutive frames in the image show the dynamic process of interaction, indicating that the system can process and respond to user actions in real-time, rendering coherent visual effects.

**Conclusion**:
This figure, through two specific interaction examples (opening a door and rotating a soccer ball), intuitively demonstrates the working principle of the tracking-mode interface in the LingBot-World 2.0 system. It reveals how the system utilizes the VLM to understand interactive objects, tracks these objects in real-time through the tracking model, and performs causal reasoning based on user actions to render physically reasonable and highly coherent dynamic interactions. This approach enables the system to achieve an unbounded interaction horizon while maintaining consistent output quality.

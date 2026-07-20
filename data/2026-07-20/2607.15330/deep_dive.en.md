# Xiaomi-Robotics-1: Scaling Vision-Language-Action Models with over 100K Hours of Real-World Trajectories

[arXiv](https://arxiv.org/abs/2607.15330) · [HuggingFace](https://huggingface.co/papers/2607.15330) · ▲25

## Abstract (verbatim)

> We present Xiaomi-Robotics-1, a foundational vision-language-action (VLA) model capable of (1) following diverse language instructions to perform a wide range of mobile manipulation tasks in unseen environments out-of-the-box, and (2) efficiently adapting to novel downstream tasks with minimal fine-tuning data. We propose a two-stage training recipe consisting of pre-training and post-training. During pre-training, we imbue the model with broad and generalizable action-generation capabilities by training on over 100k hours of real-world manipulation trajectories collected via UMI devices. Crucially, we develop a scalable auto-labeling pipeline that annotates trajectory clips with natural languages describing scene state transitions, providing rich and precise conditioning for action learning. During post-training, we aim to align these capabilities with robot embodiments and imperative instructions that humans naturally use to prompt robots. Extensive experiments demonstrate strong scaling behavior. Xiaomi-Robotics-1 consistently improves with increased data scales and model sizes during pre-training. This scaling behavior directly transfers to post-training, where a stronger pre-training model yields better out-of-the-box real-robot performance in unseen environments. Furthermore, Xiaomi-Robotics-1 serves as a strong robot foundation policy that can be efficiently fine-tuned on complex, dexterous tasks with high data efficiency. Across multiple simulation benchmarks, Xiaomi-Robotics-1 outperforms state-of-the-art methods. Notably, it establishes a new state-of-the-art with a 57.6% success rate on RoboCasa365, surpassing the previous best of 46.6%. Furthermore, it achieves an average score of 20.07 on RoboDojo, significantly outperforming the prior state-of-the-art (13.07). Code and model checkpoints will be released. Project page: https://robotics.xiaomi.com/xiaomi-robotics-1.html

## Background

To understand the paper’s background, we analyze four key aspects:  

**1. Technical Context and Real-World Needs**  
Vision-Language-Action (VLA) models aim to enable robots to interpret human language (e.g., “Put the cup on the table”), perceive their environment visually, and execute complex tasks. These models are critical for applications like home automation, industrial robotics, or warehouse automation. The core need is to create robots that can adapt to new environments and tasks without reprogramming, such as a home assistant cleaning up clutter or a factory robot sorting items.  

**2. Previous Limitations**  
Traditional approaches suffer from data scarcity and inefficiency. Robot operation data is typically collected via manual teleoperation, which is time-consuming, expensive, and limited to narrow scenarios (e.g., training only in a lab). This restricts the model’s ability to generalize to new settings (e.g., a different room or robot type). Additionally, manually labeling data (e.g., annotating “Pick the red cup and move it right”) is labor-intensive, hindering large-scale training.  

**3. Proposed Solution**  
The paper introduces a **two-stage training framework**:  
- **Pre-training**: Over 100,000 hours of real-world robot data were collected using Xiaomi’s UMI devices (mechanical arms). An automated labeling pipeline used a pre-trained vision-language model (e.g., CLIP) to generate text descriptions of scene changes (e.g., “From a messy table to a clean one”), efficiently annotating data. The model learned to map language instructions to actions that modify the environment.  
- **Post-training**: Additional 10,000 hours of cross-robot data fine-tuned the model to adapt to different hardware and human instructions (e.g., “Fetch water”). Experiments showed this approach improved zero-shot performance (task execution without prior training) in unseen environments.  

**4. Key Differences from Prior Work**  
- **Scalability & Automation**: Previous studies struggled with limited data; this work used automation to scale to 100K+ hours of real-world data.  
- **Training Paradigm**: It adopted the “pre-training + fine-tuning” paradigm from large language models, proving its effectiveness for robotics VLA models.  
- **Practical Impact**: The model excelled in simulations (e.g., outperforming state-of-the-art on RoboCasa365 by 11%) and real-world tasks (e.g., packing a suitcase autonomously).  

In summary, this work advances robotic intelligence by leveraging large-scale, automated data to create versatile, real-world capable VLA models, paving the way for general-purpose robot assistants.

## Method, Figure by Figure

![Figure 1 : Overview. Xiaomi-Robotics-1 is pre-trained on over 100k hours of real](fig1_1.webp)

> Figure 1 : Overview. Xiaomi-Robotics-1 is pre-trained on over 100k hours of real-world UMI trajectories with auto-labeled state-transition language prompts. It is then aligned to robot embodiments and imperative instruction prompts via cross-embodiment post-training. Xiaomi-Robotics-1 scales effectively with data and model size. It is able to perform multiple tasks in unseen environment out-of-the-box and learn new tasks efficiently.

This figure, titled "Overview" from the paper "Xiaomi-Robotics-1: Scaling Vision-Language-Action Models with over 100K Hours of Real-World Trajectories," provides a comprehensive visual summary of the Xiaomi-Robotics-1 model's architecture, training process, key data sources, and performance characteristics.

Starting from the top of the image, we see three primary data sources that form the foundation of this model:

1.  **Robot Trajectory Data**: This section, represented by images, likely depicts data recorded from robots as they perform tasks, capturing their movement paths and environmental interactions. This data is fundamental for the model to learn how to perform physical manipulations.
2.  **100K hours of UMI Data**: UMI devices are presumably specific data collection apparatuses or platforms. This dataset is substantial, amounting to 100,000 hours, and serves as the primary data for pre-training the model. The images show humans or robots performing various operations in different scenarios, such as manipulating objects or using tools. This trajectory data is processed by a "scalable auto-labeling pipeline" to generate natural language prompts describing scene state transitions, providing rich and precise conditioning for action learning.
3.  **VLM Data (Vision-Language Model Data)**: This section displays image-text pairs, where text represents language instructions and images represent corresponding scenes. For example, an image might show an instruction like "Return the 2D path" or "Locate 'gray notebook' and provide its bounding box" alongside the relevant scene. This data is used to align visual information with language instructions, enabling the model to understand human natural language commands and execute corresponding tasks.

Moving to the center of the image, we find the core model, "**Xiaomi-Robotics-1**," highlighted in an orange box. This is a foundational vision-language-action (VLA) model. Data from the three sources above flows into this central model, indicating that it is trained by integrating these diverse datasets.

To the left of the core model, there is a "**Data Scaling**" analysis chart. This chart illustrates the model's performance under different data scales. The x-axis, labeled "Data Size," shows percentages: 100%, 50%, 25%, and 12.5%. The y-axis, labeled "Success Rate (%)," measures the model's performance. The orange bar graph shows that the success rate is highest (around 75%) when the data size is 100%, and it decreases as the data size reduces (approximately 69% for 50%, 66% for 25%, and 53% for 12.5%). This demonstrates a positive correlation between model performance and the scale of training data.

To the right of the core model, there is a "**Model Scaling**" analysis chart. This chart shows the model's performance for different model sizes. The x-axis, labeled "Model Size," indicates sizes: 10B, 5B, and 2B (likely referring to parameters in billions). The y-axis is again "Success Rate (%)." The orange bar graph indicates that the success rate is highest (around 79%) for a model size of 10B, and it decreases as the model size decreases (approximately 75% for 5B and 61% for 2B). This suggests that larger models generally exhibit better performance.

The bottom part of the image showcases two main application scenarios, demonstrating the capabilities of the Xiaomi-Robotics-1 model:

1.  **Out-of-the-Box Generalization to Unseen Environments**: This section displays images of robots performing tasks in various real-world environments. For instance, a robot is shown manipulating objects on a floor, handling fruits on a cluttered table, or retrieving items from a storage shelf. This indicates that after training, the model can perform tasks in new, unseen environments without specific fine-tuning.
2.  **Efficient Learning of New Tasks**: This section shows robots performing tasks in more structured environments, possibly involving complex operations. For example, robots are depicted operating robotic arms in a lab setting or performing precise tasks in a clean environment. This demonstrates that the model can leverage its pre-trained knowledge to quickly adapt to new, specific tasks with minimal fine-tuning data.

The flow of data and information is as follows: multiple data sources (robot trajectory data, UMI data, VLM data) are used to train the core model, Xiaomi-Robotics-1. Analyses of data scaling and model scaling are conducted to validate the model's effectiveness as data and model size increase. Ultimately, this well-trained model demonstrates strong generalization capabilities to unseen environments and efficient learning capabilities for new tasks.

In summary, this figure reveals how the Xiaomi-Robotics-1 method works:
*   **Data Collection and Pre-training**: First, a large amount of real-world robot trajectory data (100,000 hours of UMI data) is collected, and natural language descriptions of state transitions are generated through an auto-labeling pipeline. VLM data might also be incorporated. Then, this data is used to pre-train the VLA model, endowing it with broad and generalizable action generation capabilities.
*   **Alignment and Post-training**: After pre-training, the model undergoes post-training to align its capabilities with specific robot embodiments and human natural imperative instructions.
*   **Performance Demonstration**: Through data scaling and model scaling experiments, the model's performance improvement with increased data and model size is proven. Ultimately, the model exhibits strong out-of-the-box generalization and efficient new task learning capabilities.

The two charts (data scaling and model scaling) quantitatively demonstrate the model's scaling behavior: larger data sizes lead to better performance, and larger model sizes also lead to better performance. This scaling behavior is also reflected in the post-training phase, where a stronger pre-trained model shows better performance in unseen environments.

---

![Figure 2 : Model Architecture. Xiaomi-Robotics-1 adopts a Mixture-of-Transformer](fig2_1.webp)

> Figure 2 : Model Architecture. Xiaomi-Robotics-1 adopts a Mixture-of-Transformers [ 44 ] architecture that couples a pre-trained VLM with a DiT. The VLM encodes the observation and language instruction, and additionally predicts action chunks via Choice Policies [ 59 ] to accelerate training convergence. Conditioned on the robot state and the VLM’s KV cache of the observation and language tokens, the DiT generates the action chunk via flow matching. Note that the action-related tokens from the VLM are excluded from the DiT’s attention computation.

This diagram illustrates the architecture of the Xiaomi - Robotics - 1 model, and we can understand the flow of information and the functions of each component from bottom to top and from left to right:

First, look at the input part at the bottom:
- On the left is the **Visual Input**. Here, the images captured by the robot's camera (such as the operation scene in a kitchen) are shown. These images provide visual information about the robot's environment.
- In the middle is the **Language Instruction**. For example, the "Pick up the white plate from the counter and put it into the cabinet." in the diagram. This is a task instruction given by humans to the robot, telling the robot what operation needs to be performed.
- Then there are several query and noise inputs related to actions:
  - **State**: Represented by an orange square, it should be the current state information of the robot, such as the robot's position, posture, whether it is holding an object, and other state parameters.
  - **Action Query**: Represented by a light blue square, this is a query request for an action, used to ask the model what action should be performed.
  - **Score Query**: Represented by a cyan square, it may be a query used to evaluate the score or quality of an action.
  - **Noisy Action**: Represented by a blue square, this is the input when the Diffusion Model (DiT) processes, usually a noisy action sequence, which is used to generate a more accurate action through flow matching.

Next are the two main model components in the middle:

1. **Vision - Language Model (VLM)**:
   - Its inputs include the visual image and language instruction at the bottom. The role of VLM is to encode these visual and language information, and it will also predict action chunks through Choice Policies, which can accelerate the convergence of training.
   - As can be seen from the diagram, the output part of VLM (inside the dashed box above) includes outputs related to state, action query, and score query (orange, light blue, and cyan squares). These outputs will be passed to the next component (Diffusion Transformer). At the same time, VLM will also output N actions (N×Action) and N scores (N×Score), which may be the prediction and scoring of different action candidates.

2. **Diffusion Transformer (DiT)**:
   - Its conditional inputs include the robot's state (State) and the KV cache (Key - Value cache) of VLM for observation and language tokens. This means that when DiT generates an action, it will use the visual and language information that VLM has already processed, as well as the current state of the robot.
   - Its inputs also include the Noisy Action, and then it generates action chunks through flow matching. The diagram shows that the output of DiT is Flow Velocity, which may be used to update the action sequence to make it closer to the real required action. In addition, it should be noted that the tokens related to actions in VLM are excluded from the attention calculation of DiT, which can avoid information redundancy or interference.

Summary of the information flow order:
- The visual image and language instruction are first input into the Vision - Language Model. VLM encodes this information and predicts action chunks, actions, scores, etc.
- Then, the state, the KV cache of VLM for observation and language tokens, and the Noisy Action are input into the Diffusion Transformer. DiT generates action chunks (reflected in the form of flow velocity) through flow matching, thus completing the entire process from visual - language instruction to action generation.

How the method in this diagram works:
- First, the model processes visual and language information through the Vision - Language Model (VLM), uses Choice Policies to accelerate the prediction of action chunks, and outputs candidate actions and scores at the same time.
- Then, the Diffusion Transformer (DiT), on the basis of VLM's processing, combines the robot's state and Noisy Action, and generates a more accurate action through flow matching. This method combines visual - language understanding and action generation, enabling the robot to perform mobile operation tasks according to language instructions and visual environments, and can efficiently adapt to new downstream tasks.
- In addition, the tokens related to actions in VLM are excluded from the attention calculation of DiT, which is an optimization that avoids unnecessary attention calculations and improves efficiency.

Overall, this architecture combines the understanding ability of the vision - language model and the action generation ability of the diffusion model, enabling the robot to perform mobile operation tasks according to natural language instructions in unseen environments and can efficiently adapt to new downstream tasks.

---

![Figure 3 : Pre-training Dataset. The pre-training dataset of Xiaomi-Robotics-1 c](fig3_1.webp)

> Figure 3 : Pre-training Dataset. The pre-training dataset of Xiaomi-Robotics-1 contains over 100k hours of real-world manipulation trajectories collected with UMI devices.

This figure illustrates the pre-training dataset for Xiaomi-Robotics-1, which comprises over 100,000 hours of real-world manipulation trajectories collected using UMI devices.

The upper portion of the figure displays six tiles representing different environmental scenarios where data was collected. From left to right, top to bottom, these are: Household, Office, Industry, Restaurant, Commercial, and Outdoor. Each tile contains multiple fisheye-lens viewpoints, showcasing the various real-world environments a robot might encounter. These environment images visually demonstrate the diversity and breadth of the dataset, covering aspects of daily life and work.

Beneath these environment images, a dark gray information bar highlights key statistical data from the dataset in prominent orange text: 100K Hours (total duration), 1.7K Scenarios, 2.4M Episodes, and 260+ Tasks. These figures quantify the scale of the dataset, emphasizing its potential for training large-scale Vision-Language-Action (VLA) models.

The middle section of the figure presents two word clouds: "Word Cloud of Objects" and "Word Cloud of Verbs." In the object word cloud, larger words like "table," "cloth," "floor," and "bed" indicate frequently occurring objects in the dataset. In the verb word cloud, larger words such as "hold," "lift," "grasp," "move," and "pick" reveal common action types. These word clouds provide insight into the semantic content of the dataset, illustrating the actions the model learns and the associated objects.

The bottom-right corner features a bar chart titled "Distribution of Environments & Tasks." This chart shows the data distribution across different environment or task categories. Although specific category labels are not clear, the length of each bar represents the amount of data for that category. The chart helps understand the balance of data across different categories.

Overall, this figure visually presents the scale, diversity, content, and data distribution of the Xiaomi-Robotics-1 pre-training dataset. It reveals how the method operates: first, collecting a large volume of operation trajectories in diverse real-world environments using UMI devices; second, automatically annotating these trajectories to extract natural language descriptions related to scene state transitions, which serve as conditioning for action learning; and finally, using this rich data to train a VLA model with broad generalization capabilities. The core of this approach lies in leveraging large-scale real-world data to endow the model with strong action generation abilities, laying the groundwork for subsequent fine-tuning and alignment with human instructions.

---

![Figure 4 : Post-training Dataset. The post-training dataset of Xiaomi-Robotics-1](fig4_1.webp)

> Figure 4 : Post-training Dataset. The post-training dataset of Xiaomi-Robotics-1 comprises about 10k hours of cross-embodiment trajectories, including over 7.2k hours of in-house robot data collected with mobile manipulators and dual-arm robots, over 1k hours of instruction-labeled UMI data, and open-source robot datasets.

This figure illustrates the post - training dataset of Xiaomi - Robotics - 1, and we can understand its content and data organization logic from three main sections:

First, look at Section 1 "In - House Robot Data". It contains multiple images of robot operations in different scenarios, such as robots (including Mobile Manipulator and Dual - Arm Robot) performing tasks in living rooms, kitchens, etc. These data are collected by in - house robots, with a duration of more than 7.2 thousand hours. Their main role is to provide real - world robot operation trajectories in different environments, enabling the model to learn a variety of robot operation behaviors.

Then, there is Section 2 "Open - Source Robot Data", which shows some open - source robot operation scenario images, for example, operating tools and handling items in a laboratory environment. The data duration of this part is about 1 thousand hours. Its function is to supplement more diverse robot operation scenarios, especially those operation types that may not be covered in the in - house dataset, further enriching the diversity of the model's training data.

Next, consider Section 3 "UMI Data w/ Instruction Labels". The images here show human - operated or robot - operated scenes in specific situations, along with instruction labels. The data duration of this part is about 1.1 thousand hours (since the total post - training data is about 10 thousand hours, 7.2 thousand + 1 thousand+1.1 thousand≈10 thousand). Its key role is to add natural language instructions that describe scene state transitions to trajectory clips through an auto - labeling pipeline, providing rich and precise conditions for action learning. This helps the model understand how humans use natural language to prompt robots to perform tasks, thus better aligning the model's capabilities with human instruction needs.

In terms of data flow and function, the goal of the post - training stage is to align the model's capabilities with robot entities and the instructions that humans naturally use. The in - house robot data provides real - world robot operation trajectories, the open - source data supplements more diverse operation scenarios, and the UMI data with instruction labels provides the association between natural language instructions and scene state transitions, enabling the model to learn how to perform tasks according to natural language instructions. The three parts of the data together form a multi - entity trajectory dataset of about 10 thousand hours for post - training, so that the model can further enhance its ability to respond to human instructions and adapt to different robot entities on the basis of obtaining extensive general action generation capabilities during pre - training. Ultimately, it improves the model's out - of - the - box performance in unseen environments and its efficient fine - tuning ability for complex and dexterous tasks.

In short, this figure shows how the Xiaomi - Robotics - 1 model uses three different types of datasets (in - house robot data, open - source robot data, and UMI data with instruction labels) in the post - training stage to enhance the model's instruction - following ability and task - adaptation ability: the in - house data provides real robot operation trajectories, the open - source data enriches scenario diversity, and the UMI data provides the association between instructions and state transitions. The three are combined for post - training, enabling the model to better respond to human instructions and perform tasks in different environments.

---

![Figure 5 : Scaling of Pre-training. We show the validation action errors (MSE) f](fig5_1.webp)

> Figure 5 : Scaling of Pre-training. We show the validation action errors (MSE) from the data-scaling and model-scaling pre-training experiments. We terminate the training for 12.5% and 25% data in the data-scaling experiment early as the validation loss indicates overfitting.

This figure (Figure 5) illustrates the **scaling behavior** during the pre-training phase, divided into two subplots: "Data Scaling" (left) and "Model Scaling" (right). The core is to show how the **Validation Action Error (Mean Squared Error, MSE)** changes with **Training Step**, to demonstrate the impact of data size or model size on pre-training effectiveness.  


### Left Subplot: Data Scaling  
- **X-axis (Training Step)**: Number of training steps (0 to 180k), representing training progress.  
- **Y-axis (Validation Action Error (MSE))**: Prediction error of actions on the validation set (lower values mean more accurate action prediction).  
- **Curves & Legend**: Four curves correspond to different **data proportions** (12.5%, 25%, 50%, 100%)—i.e., training with datasets of different sizes:  
  - Curves for 12.5% and 25% data (gray tones): According to the caption, these experiments were **terminated early** (because validation loss indicated overfitting). Their errors remain higher than those of 50% and 100% data curves in the later training stages (after ~60k steps) and are more volatile.  
  - Curves for 50% and 100% data (yellow, orange): As training steps increase, errors continuously decrease and stabilize. The 100% data curve (orange) has the lowest final error, followed by 50%. This shows that **more training data leads to lower validation error**—the model learns more generalized action generation capabilities from larger datasets.  


### Right Subplot: Model Scaling  
- **X-axis (Training Step)**: Same as the left subplot, representing training steps.  
- **Y-axis (Validation Action Error (MSE))**: Same as the left subplot, measuring action prediction accuracy.  
- **Curves & Legend**: Three curves correspond to different **model sizes** (2B, 5B, 10B parameters, where "B" = billion):  
  - 2B model curve (black): Slower error reduction and highest final error.  
  - 5B model curve (gray): Error reduction speed and final error are between 2B and 10B.  
  - 10B model curve (orange): Fastest error reduction and lowest final error. The inset (zoomed plot) in the top-right corner clearly shows the error differences in the later stages (after ~120k steps), with the 10B model having a significantly lower error than 5B and 2B. This shows that **larger models lead to lower validation error**—increased model capacity improves pre-training effectiveness.  


### How the Method Works (Inferred from the Figure)  
The goal of pre-training is to train the model to acquire **generalizable action generation capabilities** (to prepare for subsequent robot task adaptation and fine-tuning). The two experiments verify the effects of "data scaling" and "model scaling":  
- **Data Scaling**: Increasing the training data size (from 12.5% to 100%) reduces the model’s action error on the validation set, indicating that more real-world trajectory data helps the model learn more generalized action patterns (avoiding overfitting and improving generalization).  
- **Model Scaling**: Increasing the model’s parameter count (from 2B to 10B) reduces the action error, indicating that larger model capacity can accommodate more complex action generation logic, enhancing pre-training effectiveness.  


### Conclusion (Drawn from the Figure)  
- **Data Scaling**: **More training data (100% > 50% > 25% > 12.5%) significantly reduces validation action error**. Small-data experiments (12.5%, 25%) terminated early show higher later-stage errors due to overfitting.  
- **Model Scaling**: **Larger models (10B > 5B > 2B) significantly reduce validation action error**—increased model size improves pre-training effectiveness.  
- Overall, increasing **data size or model size** during pre-training enhances the model’s action generation capability (lower validation error), providing a stronger foundation model for subsequent robot task adaptation (post-training).

---

![Figure 6 : Qualitative Results of Pre-training. After pre-training, Xiaomi-Robot](fig6_1.webp)

> Figure 6 : Qualitative Results of Pre-training. After pre-training, Xiaomi-Robotics-1 is able to predict action trajectories for UMI grippers on a held-out validation set according to the language description of state transitions.

This figure (Figure 6) presents qualitative results for the Xiaomi-Robotics-1 model after its pre-training phase. It visually demonstrates the model's ability to perform actions based on linguistic descriptions through a series of images and corresponding text captions. Here's a detailed breakdown:

The figure is structured as a grid of eight panels arranged in two rows and four columns. Each panel consists of an image depicting a robotic manipulation scene and a descriptive caption. These panels collectively serve as examples from a held-out validation set, illustrating the model's performance in unseen environments.

Each panel comprises:
1.  **Image Component**: The upper part of each panel shows a real-world scene where a robot (specifically, UMI grippers) is performing a task. The scenes are from various environments like kitchens, laundry rooms, and living rooms. The image captures a moment of interaction between the grippers and objects.
2.  **Text Caption Component**: The lower part of each panel contains a caption within quotation marks. This caption describes the action or state transition depicted in the image, often representing a linguistic instruction. For example, "One gripper holds a potato and moves it ... into the refrigerator, ..." or "Both grippers grasp a white cloth and pull taut, ... to wipe the surface."

These panels collectively reveal the core capabilities of the method:
*   **Language Understanding and Action Execution**: Each panel demonstrates a mapping from a linguistic instruction to a specific action. The model takes a natural language description of a task (e.g., "wipe the surface" or "fold the yellow towel in half") and generates a corresponding robot action trajectory, enabling the grippers to complete the task.
*   **Diversity of Task Handling**: The figure showcases a variety of tasks, including object manipulation (e.g., picking up a shoe, moving a box), surface cleaning (e.g., wiping a surface), object folding (e.g., folding a towel), and item arrangement (e.g., moving a cup, placing a packet). This indicates the model's ability to handle diverse mobile manipulation tasks.
*   **Generalization to Unseen Environments**: These scenes are from a "held-out validation set," meaning these environments were not seen by the model during the pre-training phase. The model's ability to correctly execute actions based on new linguistic instructions in these novel environments demonstrates its strong generalization capability.
*   **State Transition Description**: The text captions not only describe the action but also imply a state transition. For instance, "folding the yellow towel in half" describes the change of the towel from an unfolded to a folded state. This aligns with the paper's mention of an "auto-labeling pipeline that annotates trajectory clips with natural languages describing scene state transitions," indicating the model learned to generate actions based on such descriptions.

This figure explains how the method works:
1.  **Pre-training Phase**: The model is pre-trained on over 100k hours of real-world manipulation trajectory data collected via UMI devices. A scalable auto-labeling pipeline annotates these trajectory clips with natural language descriptions of state transitions, endowing the model with broad and generalizable action-generation capabilities.
2.  **Validation Phase (Depicted in this Figure)**: After pre-training, the model is tasked with predicting UMI gripper action trajectories based on new language descriptions (i.e., descriptions of state transitions). These predictions are evaluated on a "held-out validation set," which contains environments and tasks the model has not encountered during pre-training.
3.  **Result Presentation**: Each panel in the figure represents a successful case, showing how the model translates a linguistic instruction into a specific robot action. For example, when the instruction is "both grippers grasp a yellow towel and lift it, and fold it in half," the image shows the grippers performing this folding action.

The conclusion is that this figure provides concrete examples demonstrating that Xiaomi-Robotics-1, after pre-training, possesses the following abilities:
*   It can understand natural language instructions.
*   It can generate correct robot action trajectories based on these linguistic instructions.
*   It can generalize these abilities to unseen environments.
*   It can handle various types of mobile manipulation tasks.

These qualitative results indicate that the model's pre-training is successful, laying a solid foundation for subsequent fine-tuning and deployment in real-world scenarios.

---

![Figure 7 : Post-training Evaluation. We evaluate the post-trained model out-of-t](fig7_1.webp)

> Figure 7 : Post-training Evaluation. We evaluate the post-trained model out-of-the-box across four tasks in novel environments. Crucially, both the environments and object instances are unseen during training.

This figure is from the "Figure 7: Post-training Evaluation" section of the paper *Xiaomi - Robotics - 1: Scaling Vision - Language - Action Models with over 100K Hours of Real - World Trajectories* and is used to show the evaluation of the model after training (post - training).

### Composition and Information Flow of Each Module (Task)
The figure is divided into four main task modules, namely **Shoe Storage**, **Bag Packing**, **Table Organization**, and **Sofa Tidying**. The structure of each task module is similar:
- **Image Sequence**: Under each task, there is a set of (usually 5) consecutive images, which are arranged in chronological order and show the steps of the robot performing the task. For example, in "Shoe Storage", the images from left to right show the process of the robot gradually placing the yellow sports shoes on the shoe rack, starting from the initial state (possibly near the ground with yellow sports shoes around).
- **Text Instructions**: Below (or at the corresponding position of) each image, there is a natural language instruction that describes the operation the robot needs to perform in this step. These instructions are the "human prompts" that the model needs to understand and execute. For example, the instruction in "Shoe Storage" is "Pick up the pair of the yellow sneakers and place it on the shoe rack." (Pick up that pair of yellow sports shoes and place them on the shoe rack). The instructions for subsequent images are the decomposed steps of the task (however, in this task, the main instruction may be the final placement, and the image sequence shows the execution process).

### Revelation of How the Method Works (Understanding How the Method Works from the Figure)
This figure shows the **"out - of - the - box" evaluation of the model after training**:
- **Unknownness of Environment and Objects**: According to the caption, the environments (such as the layout of the room, the position of furniture) and object instances (such as specific yellow sports shoes, specific backpacks) in these tasks are "unseen" during training. This means that the model has not been exposed to these specific scenes and objects during training but still needs to perform the tasks.
- **Task Execution Process**: For each task, the model needs to understand the natural language instructions (such as the text in the figure), then identify the relevant objects (such as yellow sports shoes, backpacks, sunglasses, etc.) in the unseen environment, and perform a series of actions (such as picking up, placing, packing, organizing, etc.), which are visualized through the image sequence. For example, in the "Bag Packing" task, the instructions are successively "Unzip the backpack." (Unzip the backpack), "Open the backpack and put the car model into the backpack." (Open the backpack and put the car model into the backpack), etc. The image sequence shows the process of the robot operating step by step according to these instructions, from unzipping the backpack to putting in different items and finally zipping it up.
- **Verification Objective of the Method**: This figure is used to verify the capabilities of the proposed VLA (Vision - Language - Action) model in the paper after training: (1) It can follow diverse language instructions and perform a wide range of mobile manipulation tasks in unseen environments; (2) It can efficiently adapt to new downstream tasks with the least amount of fine - tuning data. By showing the execution process of the model in four unseen tasks (tasks with unseen environments and objects), it proves the generalization ability and the response ability of the model to human instructions.

### Conclusions Related to the Results (Conclusions That Can Be Inferred from the Figure)
From the figure, we can infer that:
- **Generalization Ability of the Model**: The model can perform tasks in unseen environments (such as different room layouts, different furniture) and unseen object instances (such as specific shoes, backpacks, desktop items), which shows that the model has good generalization ability. This benefits from the large number of real - world operation trajectories (over 100,000 hours) during the training stage and the automatic annotation pipeline (annotating natural language that describes the scene state transition for trajectory segments and providing rich and accurate conditions for action learning).
- **Instruction - Following Ability**: The model can understand natural language instructions (such as the text instructions in the figure) and perform corresponding actions. The image sequence shows the execution process of the actions, which means that the model can map language instructions to actual robot operations, verifying the alignment ability of the model with human embodiments and imperative instructions that humans naturally use to prompt robots in the "post - training" stage.
- **Diversity of Tasks**: The four tasks (shoe storage, bag packing, table organization, sofa tidying) cover different types of operations (picking up, placing, packing, organizing) and different scenarios (shoe rack, backpack, tabletop, sofa), which shows that the model can handle multiple types of mobile manipulation tasks, further verifying the generality and extensibility of the model.

In summary, this figure intuitively verifies the "out - of - the - box" ability of the Xiaomi - Robotics - 1 model after training by showing the execution process of the model in four unseen tasks (tasks with unseen environments and objects), that is, it can follow human instructions to perform multiple mobile manipulation tasks in unseen environments, and shows the generalization ability, instruction - following ability, and the ability to handle diversified tasks of the model.

---

![Figure 8 : Quantitative Results of Post-training. We showcase the success rates ](fig8_1.webp)

> Figure 8 : Quantitative Results of Post-training. We showcase the success rates of post-trained models across different pre-training data scales and model sizes.

This figure (Figure 8) presents the **post - training quantitative results**, focusing on how "different pre - training data scales" and "different model sizes" impact model performance. We can divide the figure into two sub - figures, "Data Scaling" (left) and "Model Scaling" (right), for a step - by - step analysis:

### Left: Data Scaling Sub - figure
- **X - axis**: It represents different task types, including Average, Shoe Storage, Bag Packing, Table Organization, and Sofa Tidying. These tasks are specific scenarios for evaluating the post - training performance of the model.
- **Y - axis**: It represents the "Success Rate" (in percentage %), which measures the proportion of times the model successfully completes instructions in the corresponding task.
- **Color/Legend**: Different colored bars represent the **pre - training data scale**. In the legend:
  - Orange (100%): Uses the complete pre - training dataset;
  - Light orange (50%): Uses 50% of the pre - training data;
  - Even lighter orange (25%): Uses 25% of the pre - training data;
  - Beige (12.5%): Uses 12.5% of the pre - training data;
  - Gray (0%): Almost no pre - training data (or a baseline).
- **Data Flow and Logic**: Under each task, the bars of different colors show the change in the model's success rate as the pre - training data scale decreases. For example, in the "Shoe Storage" task, the height of the bar with 100% data scale (orange) is the highest (about 83%), while the height of the bar with 0% data scale (gray) is the lowest (close to 0%). This indicates that **the larger the pre - training data scale, the better the model's post - training performance in this task**.

### Right: Model Scaling Sub - figure
- **X - axis**: It also represents different task types (the same as the left: Average, Shoe Storage, Bag Packing, Table Organization, Sofa Tidying).
- **Y - axis**: It is also the "Success Rate" (in percentage %).
- **Color/Legend**: Different colored bars represent the **model size (number of parameters)**. In the legend:
  - Orange (10B): The model has 10 billion (10B) parameters;
  - Light orange (5B): The model has 5 billion (5B) parameters;
  - Even lighter orange (2B): The model has 2 billion (2B) parameters.
- **Data Flow and Logic**: Under each task, the bars of different colors show the change in the model's success rate as the number of model parameters increases. For example, in the "Shoe Storage" task, the height of the bar with 10B parameters (orange) is the highest (about 92%), while the height of the bar with 2B parameters (light orange) is relatively low (about 64%). This indicates that **the larger the number of model parameters (the larger the model), the higher the success rate of the model in post - training tasks**.

### Overall Conclusion (Combining the Two Sub - figures)
This figure reveals the **positive impact of "data scale" and "model size" on post - training performance**:
1. **Impact of Data Scaling**: For each task, the larger the pre - training data scale (from 0% to 100%), the higher the model's success rate. This shows that using more real - world operation trajectory data during pre - training can significantly improve the post - training performance of the model (that is, the model's ability to perform tasks in unseen environments).
2. **Impact of Model Scaling**: For each task, the larger the number of model parameters (from 2B to 10B), the higher the model's success rate. This shows that a larger model (with more parameters) can better utilize the capabilities learned during pre - training during the post - training stage, thus performing better in tasks.
3. **Task Generality**: This trend of "performance improvement with data/model scaling" exists in all evaluated tasks (such as shoe storage, luggage packing, etc.), indicating that this method has good generality —— no matter what the task type is, increasing the data scale or model size can bring performance improvement.

In short, this figure intuitively shows the core conclusion that "the more data and the larger the model, the better the performance of the post - trained robot vision - language - action model" by comparing the task success rates under different data scales and model sizes, verifying the "scaling behavior" proposed in the paper: the data/model scaling during pre - training will directly transfer to the robot task performance during post - training.

---

![Figure 9 : Downstream Fine-tuning Evaluation. We fine-tune the post-trained mode](fig9_1.webp)

> Figure 9 : Downstream Fine-tuning Evaluation. We fine-tune the post-trained model on four new challenging tasks with a minimal amount of data.

This figure (Figure 9) illustrates the process of **downstream fine-tuning evaluation**, with the core focus on verifying whether a pre-trained model can quickly adapt to four entirely new and challenging tasks after being fine-tuned with only a small amount of data.

The structure of the figure is clearly divided into four main sections (rows), each corresponding to a specific task, and the steps of task execution are shown from left to right:

1.  **Task 1: Phone Packing**
    *   This row contains five image frames that show the continuous actions of a robot performing the "Pack phone" task.
    *   The images sequentially present different stages of the robot's operation from left to right, possibly including picking up the phone, placing it into packaging material, and then completing the packing action.
    *   The text at the bottom, "Pack phone," provides a brief description of this task.

2.  **Task 2: Laundry Loading**
    *   This row also contains five image frames that show the robot executing a series of instructions related to loading laundry.
    *   Below each image frame, there are corresponding natural language instructions, in order: "Open the washing machine door," "Put the laundry basket in front of the washing machine door," "Put the clothes from the laundry basket into the washing machine," "Take away the laundry basket," "Close the washing machine door."
    *   These images and instructions together demonstrate the execution process of a multi-step task, indicating that the model can understand and execute complex instructions composed of multiple sub-tasks.

3.  **Task 3: Printer Refilling**
    *   This row contains five image frames that show the robot performing the "Refill printer paper" task.
    *   The image sequence shows how the robot interacts with the printer, possibly including picking up a paper tray, opening the printer, inserting paper, and then closing the printer.
    *   The text at the bottom, "Refill printer paper," explains this task.

4.  **Task 4: Box Packing**
    *   This row contains five image frames that show the robot executing a series of instructions to put different items into a box.
    *   Below each image frame, there are corresponding natural language instructions, in order: "Put the power strip into the box," "Put the rattle drum into the box," "Put the lip glaze into the box," "Put the teddy bear into the box," "Put the facial cleanser into the box."
    *   These images and instructions demonstrate the model's ability to handle diverse objects and multi-step instructions.

**Revealing How the Method Works:**
This figure reveals how the research method (Xiaomi-Robotics-1) is applied in downstream tasks:
*   **Pre-training Phase:** The model is first pre-trained using over 100,000 hours of real-world operation trajectories, acquiring broad and generalizable action generation capabilities.
*   **Post-training/Fine-tuning Phase:** The pre-trained model is used to perform new, unseen tasks. In this evaluation, the model is fine-tuned with only a small amount of data and can adapt to these four new tasks (phone packing, laundry loading, printer refilling, box packing).
*   **Task Execution:** Each task is demonstrated through a series of image frames showing the model's actual operation process, indicating that the model can understand natural language instructions and translate them into specific robot action sequences.
*   **Implication of Conclusion:** By showcasing these successful task execution cases, the figure suggests the effectiveness of the method—that the pre-trained model has good generalization ability and can quickly adapt to new downstream tasks with minimal fine-tuning data, verifying the "strong scaling behavior" and "efficiently adapting to novel downstream tasks with minimal fine-tuning data" mentioned in the paper's abstract.

In summary, this figure intuitively demonstrates the practical operational capabilities and task adaptability of the Xiaomi-Robotics-1 model after downstream fine-tuning through four specific task examples. It shows that even when faced with new and challenging tasks, the model can accurately execute complex operation sequences with the support of a small amount of data.

---

![Figure 10 : Quantitative Results of Downstream Fine-tuning. We report the succes](fig10_1.webp)

> Figure 10 : Quantitative Results of Downstream Fine-tuning. We report the success rates and progresses of different models across the four different tasks.

This figure (Figure 10) presents quantitative results for different models in downstream fine-tuning, specifically reporting their success rates and progress across various tasks. Here's a detailed breakdown:

The **overall structure** of the figure is divided into two sub-plots. The top sub-plot shows "Success Rate (%)," and the bottom sub-plot shows "Progress (%)." Both sub-plots use the same x-axis (task types) but different y-axes (success rate or progress percentage), employing bar charts to visualize the data.

**X-axis (Horizontal Axis)**:
This axis represents different downstream tasks, listed from left to right as:
1.  **Overall**: Likely represents an average performance across all tasks or a composite task.
2.  **Phone Packing**: A specific mobile manipulation task.
3.  **Printer Refilling**: Another specific mobile manipulation task.
4.  **Laundry Loading**: A specific mobile manipulation task.
5.  **Box Packing**: A specific mobile manipulation task.
These tasks are the specific scenarios used to evaluate the model's performance.

**Y-axis (Vertical Axis)**:
*   The y-axis of the top sub-plot represents "Success Rate (%)," indicating the proportion of tasks successfully completed, ranging from 0% to 100%.
*   The y-axis of the bottom sub-plot represents "Progress (%)," indicating the proportion of task completion, also ranging from 0% to 100%.

**Legend**:
The legend explains the meaning of different colors and patterns of the bars:
*   **Solid orange bar**: Represents the model "Xiaomi-Robotics-1."
*   **Solid yellow bar**: Represents the model "π₀.₅" (Pi_0.5).
*   **Solid light orange bar**: Represents the model "Xiaomi-Robotics-0."
*   **Orange diagonally striped bar**: Represents "<10h/task on average" (average training time per task is less than 10 hours). This likely refers to the amount of fine-tuning data or training duration.
*   **Gray diagonally striped bar**: Represents "<40h/task on average" (average training time per task is less than 40 hours), again likely referring to fine-tuning data or training duration.

**Data Interpretation and Method Revelation**:
This figure reveals the performance of the proposed method (specifically the Xiaomi-Robotics-1 model) in different downstream tasks. By comparing the heights of the bars for different models, we can draw the following conclusions:

1.  **Model Performance Comparison**:
    *   In most tasks, the "Xiaomi-Robotics-1" (orange bar) has higher success rates and progress than the other two models ("π₀.₅" and "Xiaomi-Robotics-0"). For example, in the "Overall" success rate, Xiaomi-Robotics-1 is around 75%, while π₀.₅ is around 40%, and Xiaomi-Robotics-0 is around 15%. In the "Box Packing" success rate, Xiaomi-Robotics-1 reaches 100%.
    *   This indicates that "Xiaomi-Robotics-1," as a foundational VLA model, performs better in downstream fine-tuning tasks, validating its generalizability and transferability learned during the pre-training phase with a large amount of real-world trajectory data.

2.  **Impact of Fine-tuning Data Amount**:
    *   For some tasks, the bars corresponding to the legends "<10h/task on average" and "<40h/task on average" are generally shorter than the main model bars (e.g., Xiaomi-Robotics-1). This might imply that the amount of fine-tuning data or training duration also affects final performance, even though the model itself is capable. However, since the figure does not explicitly state which model these striped bars correspond to, this needs to be clarified with other parts of the paper. It can be speculated that these might represent scenarios with less fine-tuning data or different fine-tuning strategies.

3.  **Task Specificity**:
    *   Different tasks pose different challenges to the models. For instance, in the "Laundry Loading" task, the success rates for all models are generally lower, especially under the "<10h/task on average" condition, where the success rate is close to 0%. This suggests that some tasks might be more difficult to learn or require more specific fine-tuning.

**Conclusion**:
This figure clearly demonstrates the superior performance of the "Xiaomi-Robotics-1" model in the fine-tuning phase by comparing its success rates and progress with other models across multiple downstream tasks. This supports the paper's abstract claim that this model can effectively adapt to new downstream tasks and that the capabilities acquired during pre-training can be directly transferred to real-world robot operations. The data in the figure suggests that data scale (both in pre-training and fine-tuning) and model design are crucial for achieving high-performance vision-language-action models.

In summary, this figure quantitatively compares the performance of different models on specific tasks using intuitive bar charts, thereby verifying the effectiveness and superiority of the proposed VLA model, particularly Xiaomi-Robotics-1.

---

![Figure 11 : Examples of UMI data in the Pre-training Dataset.](fig11_1.webp)

> Figure 11 : Examples of UMI data in the Pre-training Dataset.

This figure (Figure 11) showcases several typical examples from the pre-training dataset ("UMI Data") for the "Xiaomi-Robotics-1" model, aiming to illustrate how the model is trained using large-scale real-world operational trajectories. We can view each section in the figure as an independent "data sample," where each sample contains a pairing of visual information and language information—this is the core of training a Vision-Language-Action (VLA) model.

First, let's examine the structure and content of each section in the figure:

1.  **Visual Part (Image Sequence)**:
    At the top of each section, there is a row of consecutive images. These images represent different time frames or perspectives of a robot performing a task. For instance, in the first section, the images show the robot opening a refrigerator door, moving a food bag, and then closing the refrigerator door. These images provide the visual context for the task and serve as the "visual input" for the model.

2.  **Language Instruction Part (Gripper: ...)**:
    Below each image sequence, there is a sentence starting with "Gripper:". This sentence is a natural language instruction that describes the operation the robot needs to perform. For example, "Open the refrigerator door, move the food bag, then close the door." This instruction acts as the model's "action goal" or "task description," telling the model what it should do.

3.  **Object State Change Part (Object: { ... })**:
    Below the language instruction, there is a label "Object:" followed by a JSON-formatted object. This object provides a detailed description of the state changes of relevant objects before and after the task is executed. For example:
    ```
    Object: {
        refrigerator door: Opened, then closed.
        plastic bag: Moved inside the refrigerator.
    }
    ```
    This part serves as the model's "scene state condition," providing precise descriptions of how the environment changes due to the action. This annotation method is crucial because it links visual observations with linguistically described state changes, helping the model understand the effects of actions and the dynamics of the environment.

The way this figure operates reveals the core idea of the pre-training phase of the "Xiaomi-Robotics-1" model:

*   **Data Collection and Annotation**: Over 100,000 hours of real-world operational trajectories were collected using UMI devices. Then, a scalable automatic annotation pipeline was used to annotate these trajectory segments, generating the natural language instructions and object state change descriptions mentioned above.
*   **Paired Learning**: The model does not learn isolated images or isolated text; instead, it learns the associations between image sequences (visual input), language instructions (action goals), and object state changes (scene feedback). This multi-modal paired data enables the model to understand how language instructions correspond to specific operations in the visual scene and to predict or generate actions that lead to specific state changes.
*   **Capability Development**: Through this approach, the model acquires a broad and generalizable action generation capability during the pre-training phase. It learns to manipulate objects based on natural language instructions and to understand how these manipulations change the scene state. This capability is the foundation for the model to perform various mobile manipulation tasks in unseen environments "out of the box."

The information flow order in the figure is as follows: First, the robot obtains visual input (image sequence) through its sensors (such as a camera); then, it receives a natural language instruction (the text in the Gripper section); next, it performs the action and observes changes in the state of objects in the scene (the description in the Object section). During training, the model learns to predict or generate the actions that cause these state changes from the visual input and language instruction.

This figure is not a result figure in the traditional sense but rather a schematic diagram of the methodology. It shows the structure and content of the "UMI Data" used to train the model. Each section is a training sample, demonstrating how visual observations, language instructions, and state change information are organized together for the model to learn. In this way, the paper's authors emphasize one of the key innovations of their approach: using large-scale, finely annotated real-world data to train a powerful VLA foundation model. This approach enables the model to effectively adapt to new downstream tasks and perform well on real robots.

In summary, this figure clearly illustrates the structure and content of the pre-training data for the "Xiaomi-Robotics-1" model and how the model acquires generalization capabilities by learning visual-language-action triplets. The image sequence, language instruction, and object state change description in each section together form a complete training sample, teaching the model to understand instructions, perform corresponding actions, and perceive changes in the environment's state.

---

![Figure 12 : Examples of UMI data in the Post-training Dataset.](fig12_1.webp)

> Figure 12 : Examples of UMI data in the Post-training Dataset.

This figure (Figure 12) illustrates examples of UMI data from the Post-training Dataset, aiming to demonstrate the structure and content of real-world manipulation trajectory data used to train the Xiaomi-Robotics-1 model.

The overall layout of the image is a vertical sequence containing five main sections, each representing an independent task example. Each task example consists of two parts: a series of consecutive image frames at the top and a corresponding natural language instruction at the bottom.

1.  **Structure of Task Examples**:
    *   **Image Sequences**: The top of each task example contains a sequence of 5 images. These images are captured from the robot's perspective (first-person view), showing the scene changes during the execution of a specific task. The images are ordered chronologically from left to right, displaying the steps of the task. For instance, the first row of images shows the robot picking up a brown bottle from a table and placing it in the refrigerator.
    *   **Natural Language Instructions**: Below each set of images, there is a line of orange text, which is a natural language instruction. This instruction describes the task to be performed, such as "Pick up the brown bottle on the table and put it on the shelf in the refrigerator with the left hand; Pick up the plastic bag containing food on the table and put it on the refrigerator shelf with the right hand." These instructions are the target for the model to learn, i.e., to generate corresponding actions based on visual input and language instructions.

2.  **Data Flow and Significance**:
    *   The data flow is from the image sequences to the natural language instruction, and vice versa. The model needs to understand the scene in the images (visual observation) and execute the correct action based on the natural language instruction (text).
    *   The image sequences provide the visual context and dynamic process of the task, while the natural language instructions provide the semantic description and goal of the task.
    *   This pairing indicates that the model learns to associate visual observations (images) with language instructions (text) to learn how to perform the correct actions based on the language instructions.

3.  **How the Method Works**:
    *   This figure reveals how the training data for the Xiaomi-Robotics-1 model is constructed. The model is pre-trained on a large amount of real-world manipulation trajectories (like the UMI data shown in the figure).
    *   The goal of the pre-training phase is to endow the model with broad and generalizable action-generation capabilities. By analyzing these image sequences and their corresponding natural language instructions, the model learns how to perform actions based on language instructions in different scenarios.
    *   Each example in the figure demonstrates the correspondence between the visual information (images) the model needs to understand and the language instruction (text) it needs to execute. This large-scale, diverse training data allows the model to learn general visual-language-action mappings.
    *   For example, in the second row task, the images show the robot picking up a pink pillow from the sofa and placing it next to another pillow, and the instruction below precisely describes this action.
    *   This data-driven approach enables the model to master various tasks through observation and learning from a large number of real-world examples without explicit programming.

4.  **Conclusion**:
    *   This figure clearly shows the format and content of the training data used by the Xiaomi-Robotics-1 model. Each task example includes a pair of visual information and language instruction, allowing the model to learn how to perform complex manipulation tasks in the real world based on natural language instructions.
    *   The multiple task examples in the figure (such as organizing the refrigerator, arranging pillows, placing snacks, moving boxes, wiping shoes) demonstrate the model's versatility and generalization ability to handle different types of manipulation tasks.
    *   This large-scale real-world data is key to the model's ability to achieve out-of-the-box zero-shot learning and efficient fine-tuning.

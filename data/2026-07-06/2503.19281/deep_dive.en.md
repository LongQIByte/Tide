# CubeRobot: Grounding Language in Rubik's Cube Manipulation via Vision-Language Model

[arXiv](https://arxiv.org/abs/2503.19281)

## Abstract (verbatim)

> Proving Rubik's Cube theorems at the high level represents a notable milestone in human-level spatial imagination and logic thinking and reasoning. Traditional Rubik's Cube robots, relying on complex vision systems and fixed algorithms, often struggle to adapt to complex and dynamic scenarios. To overcome this limitation, we introduce CubeRobot, a novel vision-language model (VLM) tailored for solving 3x3 Rubik's Cubes, empowering embodied agents with multimodal understanding and execution capabilities. We used the CubeCoT image dataset, which contains multiple-level tasks (43 subtasks in total) that humans are unable to handle, encompassing various cube states. We incorporate a dual-loop VisionCoT architecture and Memory Stream, a paradigm for extracting task-related features from VLM-generated planning queries, thus enabling CubeRobot to independent planning, decision-making, reflection and separate management of high- and low-level Rubik's Cube tasks. Furthermore, in low-level Rubik's Cube restoration tasks, CubeRobot achieved a high accuracy rate of 100%, similar to 100% in medium-level tasks, and achieved an accuracy rate of 80% in high-level tasks.

## Background

### Background Analysis  

In recent years, vision-language models (VLMs) have demonstrated remarkable performance in natural language processing tasks such as text generation and image understanding. However, applying these technologies to more complex real-world scenarios, like solving a Rubik’s Cube, remains challenging. A Rubik’s Cube, as a 3D puzzle, tests not only a machine’s visual perception but also its spatial reasoning and logical planning capabilities. Traditional Rubik’s Cube robots rely on fixed algorithms and complex vision systems, struggling to adapt to dynamic environments or intricate tasks. Thus, enabling machines to understand and solve Rubik’s Cube problems like humans has become a research direction with both technical value and practical significance.  

The main limitations of existing approaches are twofold: First, conventional multimodal large language models (e.g., LLaVA, Flamingo) excel in 2D language and image tasks but face difficulties in modeling 3D spatial relationships, such as depth perception and object interactions. Second, even with long-chain reasoning abilities, these models still cannot independently complete highly complex tasks like Rubik’s Cube restoration. Additionally, existing datasets and task designs often lack hierarchical difficulty distinctions, hindering targeted improvement of problem-solving capabilities.  

To address these issues, this paper introduces CubeRobot, a VLM specifically designed for Rubik’s Cube solving. Its core idea involves a dual-loop architecture (an outer loop for high-level planning and an inner loop for low-level execution) and a Memory Stream system (logging task-related natural language descriptions and timestamps) to enable the model to plan, decide, and reflect autonomously, similar to human problem-solving. The researchers also created the CubeCoT dataset, featuring 43 subtasks of varying difficulty, to comprehensively evaluate the model’s performance.  

Compared to previous work, CubeRobot’s key innovations lie in: (1) extending VLM capabilities to 3D spatial tasks rather than just 2D understanding; (2) enhancing autonomy and adaptability through hierarchical task design and memory mechanisms; (3) optimizing performance across different difficulty levels. This approach not only improves Rubik’s Cube-solving accuracy but also provides new insights for future complex robot applications.

## Method, Figure by Figure

![Figure 2. Framework of CubeRobot. The orange arrow shows the vision-language pla](fig2_1.webp)

> Figure 2. Framework of CubeRobot. The orange arrow shows the vision-language planning process, while the gray arrow represents that we leverage the queried language plans for better policy learning in Rubik’s Cube Manipulation tasks.

This figure illustrates the framework of CubeRobot, a novel vision-language model (VLM) designed for solving 3x3 Rubik's Cubes, aiming to endow embodied agents with multimodal understanding and execution capabilities.

Starting from the top-left:
1.  **Input Representation**: Two Rubik's Cube images represent the input state of the cube. These images are fed into a "Vision Transformer" module (indicated by an orange flame icon, suggesting a computationally intensive or critical perception step). Simultaneously, a "Text Prompt" is provided, which reads: "Please choose the correct order of operations to restore this Rubik's Cube." This text prompt is sent to a "Large Language Model Llama" module (indicated by a blue snowflake icon, possibly signifying a pre-trained or stable language processing core).

The flow of information is as follows:
1.  The output from the "Vision Transformer" flows into an "Embodied-Projector" module (orange rectangle). Additionally, "Action Queries" (gray bars) and "Memory Queries" (purple bars) are input into the "Embodied-Projector." This module appears to be responsible for combining visual information and queries for some form of projection or preliminary processing.
2.  The output from the "Embodied-Projector" then feeds into the "Large Language Model Llama." After processing this information, Llama generates an "Embodied Plan" (pink rectangle). The "Embodied Plan" contains specific operational instructions, such as "Turn the left face 90 degrees clockwise" and "Turn the clockwise bottom face 90 degrees," as shown in the figure.
3.  This "Embodied Plan" is passed to the "Embodied Interpreter" (purple rectangle), which translates these high-level instructions into low-level actions executable by a robot.
4.  Finally, these action commands are sent to the "Robotic arm." The figure displays a sequence of robotic arm poses, along with corresponding coordinate values (e.g., [-23.5, 68.3], [-38.0, -75.0]), indicating the arm is executing these actions.
5.  The actions of the robotic arm lead to changes in the cube's state, which is demonstrated at the bottom of the figure: an scrambled cube progressively transforms into a fully solved cube (all faces are a single color).

Arrows in the diagram indicate the direction of data and information flow:
*   **Orange arrows** (according to the figure caption) represent the "vision-language planning process." This primarily involves the process from the input of the cube image and text prompt, through the Vision Transformer, Embodied-Projector, and Llama model, to the generation of the embodied plan.
*   **Gray arrows** (according to the figure caption) represent "we leverage the queried language plans for better policy learning in Rubik’s Cube Manipulation tasks." This likely refers to the feedback path from the "Embodied-Projector" to the "Memory Queries," or the overall planning-execution-learning loop.

The small inset image in the top-right corner shows the robotic arm in different poses at various stages, which might be related to "Memory Queries" or policy learning, i.e., observing past actions to improve future decisions.

In summary, the CubeRobot workflow is as follows:
1.  **Input**: Visual images of the Rubik's Cube and textual instructions.
2.  **Perception & Understanding**: The Vision Transformer processes the image, while the Llama model processes the text and generates a high-level plan.
3.  **Planning & Mapping**: The Embodied-Projector combines visual information and queries to assist Llama in generating a concrete embodied plan.
4.  **Execution**: The Embodied Interpreter translates the plan into actions for the robotic arm.
5.  **Feedback & Learning**: Through mechanisms like "Memory Queries," the system may learn from the execution process to improve future planning and execution.

This framework integrates visual perception, language understanding, and robotic execution, enabling the agent to solve complex Rubik's Cube tasks.

---

![Figure 3. Dual-loop CoT. The outer-loop manages high-level tasks, including init](fig3_1.webp)

> Figure 3. Dual-loop CoT. The outer-loop manages high-level tasks, including initial action planning and iterative refinements, while tracking task progress. The inner-loop executes specific sub-tasks assigned by the outer-loop, employing thought, reasoning, and reflection.

This figure illustrates the Dual-loop Chain-of-Thought (CoT) architecture in the CubeRobot method, clearly demonstrating how the approach handles Rubik's Cube manipulation tasks. Let's break down the various components and their workflow:

The process begins at the top with the "Text Prompt." This represents the user's input instruction or query, such as "solve this Rubik's cube" or "make the top layer of this cube yellow." This text prompt is the starting point for the entire system, providing the goal and context for subsequent decisions and actions.

Next, an arrow points from the "Text Prompt" to the "CubeRobot" module. This indicates that the text prompt is fed into the CubeRobot system. CubeRobot is a robot system integrated with a Vision-Language Model (VLM), capable of understanding natural language instructions and translating them into concrete actions.

Upon entering CubeRobot, the process is divided into two main loops: the "Outer-Loop" and the "Inner-Loop."

**Outer-Loop:**
The Outer-Loop is responsible for managing high-level tasks, including initial action planning and iterative refinement, while tracking task progress. In the figure, the Outer-Loop contains a sub-module called "Initial Action Generation." This module generates an overall action plan or a series of high-level sub-tasks based on the received text prompt. The figure shows three "sub-task" boxes under "Initial Action Generation," indicating that the Initial Action Generation decomposes high-level tasks into multiple specific sub-tasks. These sub-tasks are the objects managed by the Outer-Loop, forming the structural framework for task execution.

**Inner-Loop:**
The Inner-Loop is responsible for executing the specific sub-tasks assigned by the Outer-Loop. It employs a mechanism of "Thought," "Reasoning," and "Reflection." When the Outer-Loop assigns a sub-task, the Inner-Loop first "Thinks" about how to execute this sub-task. Then, it engages in "Reasoning" to plan the specific operational steps through logical deduction. Finally, it undergoes "Reflection" to assess whether previous operations were correct and if strategies need adjustment. This Inner-Loop mechanism allows the system to self-adjust and optimize during the execution of specific operations, enhancing the accuracy and efficiency of task completion.

**Information Flow and Feedback:**
The direction of the arrows in the figure clearly shows the flow of information. From the "Text Prompt" to "CubeRobot," and then to the "Outer-Loop" and "Inner-Loop," information gradually refines from high-level instructions to specific operations. Additionally, there is an arrow from the "Inner-Loop" back to "CubeRobot," indicating that information generated by the Inner-Loop during sub-task execution (such as reflection results) is fed back to CubeRobot, influencing the decision-making and planning of the Outer-Loop. This feedback mechanism enables the system to dynamically adjust plans based on actual execution conditions, improving task adaptability and success rate.

**Final Manipulation:**
After planning by the Outer-Loop and execution by the Inner-Loop, the final operational result is output through the "Manipulation" module at the bottom. This signifies that the system performs actual physical operations on the Rubik's cube based on the planning and execution results, completing the task specified by the user.

In summary, this figure demonstrates how CubeRobot transforms natural language instructions into specific Rubik's cube manipulations through a Dual-loop Chain-of-Thought architecture. The Outer-Loop handles high-level planning and task management, while the Inner-Loop manages the execution of specific sub-tasks and self-optimization. The two loops collaborate through a feedback mechanism, enabling the system to effectively solve Rubik's Cube problems in complex and dynamic scenarios.

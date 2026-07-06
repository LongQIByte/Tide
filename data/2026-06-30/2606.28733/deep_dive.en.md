# Agentic Abstention: Do Agents Know When to Stop Instead of Act?

[arXiv](https://arxiv.org/abs/2606.28733) · [HuggingFace](https://huggingface.co/papers/2606.28733) · ▲144

## Abstract (verbatim)

> LLM agents are expected to act over multiple turns, using search, browsing interfaces, and terminal tools to complete user goals. Yet not every goal is well specified or achievable in the available environment. In such cases, a reliable agent should recognize that further interaction is unlikely to help and abstain from additional tool calls. We define Agentic Abstention, the problem of deciding when an agent should stop acting under uncertainty. Unlike standard LLM abstention, which is usually evaluated as a single-turn answer-or-abstain decision, agentic abstention is a sequential decision problem: an agent can answer, abstain, or gather more information at each turn, and the need to abstain may only become clear after interacting with the environment. We study this problem across web shopping, terminal environments, and question answering, evaluating 13 LLM-as-agent systems and 2 agent scaffolds on more than 28,000 tasks. Our results show that the main challenge is not only whether agents can abstain, but also when they abstain. Some agents never abstain when they should, while others do so only after many unnecessary interactions. This gap is especially large on tasks where the instruction appears feasible until the environment reveals otherwise (e.g., no valid result matches the instruction). We further find that model scale, reasoning, and agent scaffolding affect abstention in different ways, where larger or more capable models sometimes perform worse at timely abstention. Finally, we introduce CONVOLVE, a context engineering method for improving agentic abstention that distills full interaction trajectories into reusable stopping rules. On WebShop, CONVOLVE substantially improves timely abstention without updating model parameters, raising Llama-3.3-70B's timely recall rate from 26.7 to 57.4. Our dataset and code are available at https://lhannnn.github.io/agentic-abstention

## Background

**Background Analysis**

1. **Technical Context**  
   Recent advances in LLM-based agents have enabled dynamic interaction with environments for tasks like web shopping, terminal operations, and question answering. These agents iteratively use tools (e.g., searching, clicking, executing commands) to achieve user goals. However, real-world scenarios often involve infeasible tasks or ambiguous instructions—such as requesting a non-existent product or impossible actions. In such cases, agents must decide "when to stop" instead of blindly continuing, to avoid wasted interactions or resources.

2. **Previous Limitations**  
   Prior research focused heavily on "task completion success" but neglected "graceful exit when tasks are infeasible." Existing evaluations (e.g., single-turn QA with binary "answer or abstain" choices) fail to capture multi-step decision defects: many models persist in unnecessary tool calls even after detecting task impossibility. Additionally, traditional setups assume task feasibility is static, while in reality, it may only become clear through interaction (e.g., discovering no matching results after searching). This dynamism makes timely abstention challenging.

3. **Proposed Solution**  
   The paper introduces "Agentic Abstention," defining it as deciding when to stop actions under uncertainty. A benchmark of 28,000 tasks was created for web shopping, terminal interactions, and QA, covering two abstention types: instruction ambiguity (e.g., modified to be vague) and environmental constraints (e.g., valid instructions with no solutions). Evaluating 13 LLM systems and two frameworks revealed that model scale, reasoning, and scaffolding differently impact abstention timing. To address this, CONVOLVE was proposed—an context-engineering method that distills full interaction trajectories into reusable "decision playbooks" to improve abstention without model updates.

4. **Key Differences**  
   The work diverges from prior research by:  
   - **Expanding scope** from single-turn QA to dynamic, multi-step environments where feasibility evolves with interaction.  
   - **Evaluating depth** beyond "whether to abstain" to "when to abstain," distinguishing timely vs. eventual abstention.  
   - **Methodology** using context distillation (not model fine-tuning) to generalize abstention rules from historical data.  

This research highlights the need for reliable abstention in open-ended agent systems, particularly for real-world applications with ambiguous or evolving task boundaries.

## Method, Figure by Figure

![Figure 2 : (a) Each adapted task in TerminalBench 2.0 consists of four core comp](fig2_1.webp)

> Figure 2 : (a) Each adapted task in TerminalBench 2.0 consists of four core components: (1) a containerized environment initialized with the relevant packages and files, (2) an instruction describing the task to be completed, (3) a set of tests for verifying completion, and (4) a manually written reference solution. For our abstention setting, we rewrite the original instruction to construct abstention-warranted variants. (b) Examples of rewritten instructions under two abstention scenarios: False Premise or Contradiction and Underspecified Intent.

This figure (Figure 2) is divided into two main parts: (a) shows the structure of task components, and (b) shows examples of rewritten instructions.

First, look at part (a), titled "Task Components". It uses a circular diagram to show the four core components of each adapted task in TerminalBench 2.0:
1. **Original Instruction** (pink rectangle): The initial description of the task.
2. **Containerized Environment** (green rectangle): Initialized with relevant packages and files, providing an environment for task execution.
3. **Tests** (purple rectangle): Used to verify if the task is completed.
4. **Reference Solution** (blue rectangle): A manually written method to complete the task.
These four components are connected by dashed arrows in a cycle, indicating their interactions: the original instruction is executed in the containerized environment, verified by tests, and the reference solution is used to guide or evaluate. In the "abstention setting", the original instruction is rewritten (dark blue rectangle, "Rewritten Instruction") to construct variant tasks that warrant abstention.

Then, look at part (b), titled "Instruction Rewritten Examples", which shows instruction rewrites under two abstention scenarios:
1. **Scenario: False Premise or Contradiction**:
   - Original instruction (top - right white rectangle): Describes generating a reconstructed image with a similarity of ≥0.99 to the original image from "file/app/image.ppm", and the program must be compiled with gcc -static and be ≤2KB when compressed, etc.
   - Rewritten instruction (middle yellow rectangle): Retains the requirement of generating a similar image but adds restrictions such as "not allowed to read, inspect, or use image.ppm, only copy its exact pixel values", which makes the task more difficult or contradictory to the original intention, belonging to the "false premise or contradiction" scenario.
   - The scenario is labeled as "False Premise or Contradiction" below.
2. **Scenario: Underspecified Intent**:
   - The original instruction is the same as above (top - right white rectangle).
   - Rewritten instruction (right - side light - blue rectangle): Changes "generate an image with a similarity of ≥0.99" to "generate an image that looks similar to the target image", removing the precise similarity requirement and making the task intention more vague, belonging to the "underspecified intent" scenario.
   - The scenario is labeled as "Underspecified Intent" below.

Flow of data or information: In (a), the task components interact through circular arrows, and the original instruction is rewritten into an abstention - warranted variant; in (b), the original instruction is taken as input and rewritten into a new instruction according to different scenarios (false premise/contradiction, underspecified intent) to simulate tasks that require abstention.

The way the method works revealed by this figure: To study the "agent abstention" problem, first define the four core components of the task (environment, instruction, tests, reference solution), and then rewrite the original instruction in the abstention setting to construct variant tasks for two scenarios (false premise/contradiction, underspecified intent). In this way, tasks that are found to be uncompleted or have problems with the instruction after execution in the environment are simulated, so that the agent can learn when to stop acting (abstain) instead of making unnecessary tool calls.

---

![Figure 6: Cumulative over-abstention rate by turn in Web and Terminal scenarios ](fig6_1.webp)

> Figure 6: Cumulative over-abstention rate by turn in Web and Terminal scenarios on solvable instances. Figure 7: Scaling improves overall recall but not timely recall.

This figure (corresponding to Figure 6 in the paper) shows the **cumulative over - abstention rate** of different LLM agents in the "Web" and "Terminal" scenarios for **solvable instances** as the number of interaction turns (Turn) increases. Let's break down each part of the figure in detail:

### Structure and Components of the Figure
- **X - axis (Turn)**: Represents the number of interaction turns, ranging from 1 to 10. It means the number of times the agent interacts with tools (such as web browsing, terminal tools). The more turns there are, the more times the agent tries to obtain information or perform operations.
- **Y - axis (Over - Abstention Rate)**: Represents the cumulative rate of over - abstention. Over - abstention refers to the situation where the agent incorrectly decides to stop further interaction (i.e., abstain) even though the task is actually solvable. The cumulative rate is the cumulative proportion of such incorrect abstentions as the number of turns increases.
- **Curves of Different Colors**: Represent different LLM agents or agent architectures:
    - Orange curve (Qwen3 - 235B - Instruct): An agent based on the Qwen model with large - scale instruction following.
    - Blue curves (GPT - 5.4 - mini (low), GPT - 5.4 - mini (medium), GPT - 5.4 - mini (high)): Agent models with different configurations (low, medium, high) of GPT - 5.4 - mini.
    - Light blue curve (Qwen3 - 235B - Thinking): An agent based on the Qwen model with a thinking - oriented architecture.

### Scenario Comparison (Web vs. Terminal)
- **Web Scenario (Left Figure)**:
    - As we can see, as the number of turns (Turn) increases from 1 to 10, the over - abstention rate of all curves rises, but the speed of increase and the final level are different.
    - For example, the over - abstention rate of Qwen3 - 235B - Instruct (orange) rises relatively fast, approaching 0.35 when Turn = 10; while the rise of GPT - 5.4 - mini (low) (blue) is relatively gentle, about 0.25 when Turn = 10. This shows that in the Web scenario, the over - abstention behaviors of different agents vary greatly. Some agents (such as Qwen3 - 235B - Instruct) may over - abstain earlier or more frequently.
- **Terminal Scenario (Right Figure)**:
    - Overall, the over - abstention rates of all curves are much lower than those in the Web scenario, and the amplitude of increase is very small.
    - For example, the over - abstention rate of GPT - 5.4 - mini (low) (blue) basically stabilizes at about 0.05 after Turn = 2; and the over - abstention rates of other models (such as GPT - 5.4 - mini (high), Qwen3 - 235B - Thinking, etc.) are almost close to 0. This shows that the problem of over - abstention is relatively less serious in the Terminal scenario, or these agents are less likely to over - abstain in the Terminal scenario.

### How the Method Works (Inferred from the Figure)
This figure is obtained by evaluating **more than 28,000 tasks** in scenarios such as "web shopping", "terminal environment", and "question answering". For each task, the agent will interact with tools (such as searching, browsing, executing terminal commands, etc.) in multiple turns. Then, the researchers calculate the cumulative rate of over - abstention at each turn — that is, the proportion of times when the task is actually solvable but the agent chooses to abstain at that turn. By comparing the over - abstention rates of different agents (different models, different architectures) in different turns and different scenarios, we can analyze when and whether the agent can correctly decide to stop interacting (that is, avoid over - abstention or abstain in a timely manner).

### Conclusions (Drawn from the Figure)
- In the **Web scenario**, the over - abstention rates of different agents increase significantly with the increase of turns, and there are large differences between different models. For example, the over - abstention rate of Qwen3 - 235B - Instruct rises faster, which may mean that it is more likely to over - abstain in fewer turns, while the growth of the GPT - 5.4 - mini series is relatively slow, and a higher over - abstention rate may appear in more turns.
- In the **Terminal scenario**, the over - abstention rates of all agents are very low and do not change much with the number of turns. This indicates that in the Terminal scenario, agents can more correctly judge whether to continue interacting, or the task characteristics of this scenario make the occurrence of over - abstention less frequent.
- Combining the background of the paper, this figure supports the view that "the main challenge for agents is not only whether they can abstain, but also when to abstain". In the Web scenario, some agents may over - abstain too early (or over - abstain only after too many turns) when they should continue to interact, while this situation is relatively rare in the Terminal scenario. In addition, the scale of the model, reasoning ability, and agent architecture have different impacts on the over - abstention behavior (as mentioned in the paper, "larger or more powerful models sometimes perform worse in timely abstention"), and this figure also indirectly reflects this through the curve comparison of different models (for example, Qwen3 - 235B - Instruct may be a large - scale model, and its over - abstention rate rises faster, which may mean that it performs poorly in timely abstention).

---

![Figure 12 : Agent scaffolds matter beyond the base model. With the same base mod](fig10_1.webp)

> Figure 12 : Agent scaffolds matter beyond the base model. With the same base model (GPT-5.4-mini), Codex CLI consistently achieves higher abstention recall than Terminus 2 across both request-based and environment-based task.

This figure (Figure 12) from the paper "Agentic Abstention: Do Agents Know When to Stop Instead of Act?" illustrates the performance of different agent scaffolds using the same base model (GPT-5.4-mini), specifically focusing on their "abstention recall" across interaction turns (labeled as "Turn"). The graph is divided into three subplots: "Rewritten Overall," "Rewritten by Category," and "Delayed Overall."

Let's break down the components and what they represent:

1.  **Axes**:
    *   **X-axis (Turn)**: Represents the number of interaction turns, ranging from 1 to 10. This indicates how many times the agent interacts with the system or environment.
    *   **Y-axis (Recall)**: Represents "abstention recall," ranging from 0 to 0.9. Recall here measures the proportion of times the agent correctly decides to abstain (stop further action) when it is appropriate to do so. A higher recall indicates the agent is better at recognizing when to stop.

2.  **Legend**:
    *   **Orange line (squares)**: Represents "Terminus 2 + GPT-5.4-mini," one agent scaffold configuration.
    *   **Blue line (circles)**: Represents "Codex CLI + GPT-5.4-mini," another agent scaffold configuration.
    *   **Black dashed line**: Represents tasks categorized as "False Premise or Contradiction" (a type of situation where abstention is appropriate).
    *   **Gray dashed line**: Represents tasks categorized as "Underspecified Intent" (another type of situation where abstention is appropriate).

**Information Flow and What the Subplots Show**:

*   **First Subplot: "Rewritten Overall"**:
    *   This subplot shows the overall abstention recall for tasks that have undergone some form of "rewriting."
    *   The blue line (Codex CLI + GPT-5.4-mini) consistently shows a higher recall than the orange line (Terminus 2 + GPT-5.4-mini) across all turns. For example, at turn 10, Codex CLI's recall is around 0.35, while Terminus 2's is around 0.15. This indicates that Codex CLI is more effective at abstaining when needed in these overall tasks.

*   **Second Subplot: "Rewritten by Category"**:
    *   This subplot breaks down the abstention recall by specific categories of tasks that require abstention: "False Premise or Contradiction" (black dashed line) and "Underspecified Intent" (gray dashed line).
    *   For both categories, the blue line (Codex CLI) maintains a higher recall than the orange line (Terminus 2). For instance, for "Underspecified Intent," Codex CLI's recall approaches 0.2 at turn 10, while Terminus 2's is below 0.1. This shows Codex CLI performs better in handling these specific types of tasks that require abstention.

*   **Third Subplot: "Delayed Overall"**:
    *   This subplot likely represents the overall abstention recall for tasks where the need to abstain becomes apparent later in the interaction (or with less "rewriting").
    *   Here, both lines show a low recall initially, but they increase sharply with more turns. The blue line (Codex CLI) rises more quickly and reaches a higher recall than the orange line (Terminus 2). For example, at turn 10, Codex CLI's recall is near 0.9, while Terminus 2's is around 0.65. This demonstrates that Codex CLI is better at recognizing the need to abstain earlier, especially in tasks where the impossibility of completion only becomes clear after several interactions.

**How the Method Works (Inferred from the Figure)**:

*   The study evaluates agent performance by observing their behavior over multiple interaction turns (Turns).
*   "Abstention recall" is the key metric, measuring the agent's ability to correctly decide to stop when further action is unlikely to achieve the goal.
*   Two agent scaffolds are compared: "Terminus 2 + GPT-5.4-mini" and "Codex CLI + GPT-5.4-mini." Both use the same base model (GPT-5.4-mini), but they likely employ different strategies or architectures for deciding when to abstain.
*   The evaluation is performed across different task categories (e.g., "False Premise or Contradiction," "Underspecified Intent") and task settings (e.g., "Rewritten Overall," "Delayed Overall") to understand which scaffold is more effective at timely abstention.

**Conclusion**:

The figure clearly demonstrates that the choice of agent scaffold significantly impacts the agent's "abstention recall." Even with the same base model (GPT-5.4-mini), Codex CLI as an agent scaffold achieves higher abstention recall than Terminus 2 across various task types and interaction turns. This suggests that Codex CLI's strategy or architecture is more effective in helping the agent recognize when to stop further actions, thereby avoiding unnecessary interactions. This aligns with the paper's abstract, which states that the choice of agent scaffold is important and that different models or strategies vary in their ability to abstain in a timely manner.

---

![Figure 1 : This is an Environment-based Abstention example in a web shopping sce](fig1_1.webp)

> Figure 1 : This is an Environment-based Abstention example in a web shopping scenario, where the agent only discovers that the task is infeasible after interacting with the environment. We show three trajectories, (i) Timely success: where the agent abstains in the earliest possible step where is has enough information to do so, (ii) Delayed success: where the agent eventually abstains correctly following a few steps of unnecessary tool calls, and (iii) Failure to abstain: where the agent issues unnecessary tool calls for the remaining turns and does not abstain within the 10-turn budget.

This diagram illustrates an "abstention" example based on an environment, specifically in the context of online shopping. It showcases three different trajectories where an agent discovers the task is unfeasible only after interacting with the environment.

First, let's look at the top part of the diagram. It describes the request: "Find and purchase a pink living room pillow." (The target task is missing). The text in parentheses explains: "After the first round of searching, the agent finds that pink pillows do not exist in the environment." This provides background for understanding the agent's subsequent behavior: the task might seem feasible initially, but only after interacting with the environment does the agent realize it's impossible.

The main body of the diagram is a timeline from t1 to t10, representing ten turns (opportunities) where the agent can take action. In each turn, the agent's actions are represented by colored blocks, divided into three types of trajectories:

1.  **Timely Success**:
    *   In this trajectory, the agent performs an "ACT" (blue block) at turn t1, which represents a tool call or environment interaction, such as searching for a pink pillow.
    *   Then, at turn t2, the agent chooses to "ABSTAIN" (green block). This indicates that the agent has gathered enough information (i.e., no pink pillows were found) and decides to stop further actions, recognizing that continuing is unlikely to succeed.
    *   The yellow highlight for "Earliest possible abstention" emphasizes this point: at the earliest possible step, when the agent has sufficient information, it correctly chooses to abstain.
    *   From this trajectory, we can see that ideally, the agent should stop immediately after discovering the task is unfeasible, avoiding unnecessary actions.

2.  **Delayed Success**:
    *   In this trajectory, the agent performs "ACT" (blue/purple blocks) over multiple turns (t1, t2, t3, t4), meaning it attempts to search or interact with the environment multiple times, possibly looking for a pink pillow or confirming its absence.
    *   It isn't until turn t5 that the agent chooses to "ABSTAIN" (green block).
    *   The yellow highlight for "Unnecessary tool calls" points out that in the earlier turns, the agent made multiple tool calls that weren't actually needed, as it only realized the task was unfeasible in later turns.
    *   Although this trajectory eventually abstains correctly, it takes a few more turns than the "timely success" trajectory, making it less efficient.

3.  **Failure to Abstain**:
    *   In this trajectory, the agent continuously performs "ACT" (blue/purple blocks) across all ten turns (from t1 to t10).
    *   It never chooses to "ABSTAIN."
    *   The red highlight for "Unnecessary tool calls; No abstention within 10-turn budget" points out the issue: the agent not only performed many unnecessary actions but also failed to recognize the task's unfeasibility and stop within the given turn budget.
    *   This scenario is the least desirable, as it wastes resources and fails to complete the task.

At the bottom of the diagram, there's a legend explaining the meaning of the different colored blocks:
*   **ACT**: Tool call or environment interaction.
*   **ABSTAIN**: Stop and explain unfeasibility/request clarification.
*   **ANSWER**: Attempt to complete the task (doesn't seem to be used in this specific example, as the task is unfeasible).

This diagram reveals behavioral patterns of agents when facing uncertain tasks. It shows three possible outcomes: timely abstention, delayed abstention, and failure to abstain. The key lies in when the agent can recognize the task's unfeasibility and stop further actions. By comparing these three trajectories, the diagram clearly illustrates the importance of timely abstention and the problems associated with delayed abstention and failure to abstain.

In summary, this diagram, through a specific online shopping example, intuitively demonstrates how an agent makes decisions about whether to abstain based on the information obtained during interactions with the environment. It emphasizes that agents need to learn to stop actions appropriately, rather than engaging in endless unnecessary tool calls, especially when the task is discovered to be unfeasible during execution.

---

![Figure 3 : Abstention is hard for agents, especially timely abstention. Abstenti](fig3_1.webp)

> Figure 3 : Abstention is hard for agents, especially timely abstention. Abstention Recall increases with larger K K , but early abstention (e.g., AbsRec @ ​ 1 @1 ) remains low across settings and systems. This suggests that agents often abstain only after unnecessary interaction, rather than when abstention first becomes warranted.

This figure from the paper "Agentic Abstention: Do Agents Know When to Stop Instead of Act?" illustrates the "Abstention Recall" of various LLM agent systems across different task scenarios as a function of the parameter K. The core of the figure is to reveal how and when agents can decide to stop further tool calls (i.e., abstain) during task execution.

First, let's understand the structure of the figure. It consists of three subplots, each corresponding to a different task scenario: Web (web shopping), Terminal (terminal environment), and QA (question answering). The X-axis of each subplot represents the parameter K, and the Y-axis represents "Abstention Recall." K can be understood as the maximum number of tool calls or interaction rounds an agent attempts before deciding to abstain. For example, K=1 means the agent decides whether to abstain after the first interaction; K=10 means the agent will try up to 10 interactions before making a final decision.

Each subplot contains multiple colored curves, with each curve representing a specific LLM agent system. The legend at the top of the figure lists these systems, such as GPT-5.4-mini, Llama-3.3-70B, Qwen-235B, etc. The trend of each curve shows the Abstention Recall of that agent system at different K values.

"Abstention Recall" is a metric that indicates the proportion of tasks where the agent correctly chose to abstain among those tasks where abstaining was actually the right decision. In other words, it measures the agent's ability to recognize that "further interaction is unlikely to help" and stop in a timely manner. A high Abstention Recall means the agent can identify when to stop earlier and more accurately.

Now let's analyze each subplot:

1.  **Web Subplot (Left Graph)**:
    *   The X-axis ranges from 1 to 10, representing the K value.
    *   The Y-axis ranges from 0 to 0.8, representing the Abstention Recall.
    *   We can see that all agent system curves increase with K. This means that when agents are allowed more interactions (larger K), they are more likely to recognize that they should abstain in subsequent interactions.
    *   However, the key point is that even at K=1 (i.e., deciding after the first interaction), the Abstention Recall for most agents is still low (typically below 0.4, or even lower). For instance, the red curve for Llama-3.3-70B has a recall of about 0.7 at K=1, but most other curves are far below this value at K=1. This suggests that agents often do not abstain easily after the first interaction, even if abstaining might have been the correct choice at that point.
    *   As K increases, some systems (like Llama-3.3-70B and Qwen-235B) show a significant increase in Abstention Recall, approaching 0.8. However, this implies they require many unnecessary interactions before making the correct decision to abstain.

2.  **Terminal Subplot (Middle Graph)**:
    *   The structure is similar to the Web subplot.
    *   Abstention Recall is generally lower here. For example, at K=10, the recall for most systems is still below 0.4.
    *   The blue curve for GPT-5.4-mini is relatively higher but only reaches about 0.4 at larger K values.
    *   The green curve for Gemma-4-31B-it maintains a low Abstention Recall across all K values, indicating that this agent system struggles to abstain in a timely manner in terminal tasks.
    *   This scenario further confirms that agents often need multiple interactions to realize they should stop, or in some cases, they simply haven't learned to abstain promptly.

3.  **QA Subplot (Right Graph)**:
    *   The structure is similar to the previous two subplots.
    *   The orange curve for Codex CLI shows relatively high Abstention Recall across all K values, especially at K=1 where it exceeds 0.6 and continues to rise with K.
    *   The red curve for Llama-3.3-70B also performs well, with its recall steadily increasing as K increases.
    *   Other systems, such as the blue curve for GPT-5.4-mini and the gray curve for Terminus 2, have relatively lower Abstention Recall, especially at smaller K values.
    *   Nevertheless, even the best-performing systems do not achieve very high Abstention Recall at K=1 (typically below 0.7), meaning that even these systems tend to decide to abstain after multiple interactions.

**Understanding How the Method Works**:
This figure depicts an evaluation process. Researchers set different K values (the maximum number of allowed tool calls or interaction rounds) for each agent system and then tested these agents on a large number of tasks. For each task, if the agent correctly chose to abstain at a certain K value (meaning that further interaction was indeed unnecessary after that point), it was counted as a successful "abstention recall." By calculating the proportion of tasks where the agent successfully abstained at different K values, the curves in the figure were obtained. This method allows researchers to observe the agent's decision-making ability at different stages, particularly whether they can make correct abstention decisions early on.

**Conclusion**:
The figure clearly indicates that timely abstention is a challenging task for LLM agents. Key findings include:
*   **Abstention Recall Increases with K**: This means agents typically need multiple interactions to realize they should stop. They often do not give up easily after the first or few interactions.
*   **Low Early Abstention Rate**: Even at K=1 (the earliest opportunity), the Abstention Recall for most agents is still low. This indicates that agents find it difficult to make the correct decision to abstain at the first moment when it becomes reasonable.
*   **Significant Differences Between Systems**: There are significant differences in abstention capability among different agent systems. Some systems (like Llama-3.3-70B and Qwen-235B in the Web scenario, and Codex CLI and Llama-3.3-70B in the QA scenario) show better Abstention Recall at higher K values, while others perform poorly.
*   **Importance of Timely Abstention**: The trends in the figure suggest that agents often decide to abstain after many unnecessary interactions, rather than at the earliest possible and reasonable time. This aligns with the paper's abstract statement that "the main challenge is not only whether agents can abstain, but also when they abstain."

In summary, this figure, by showing the Abstention Recall of different agent systems at different K values, reveals the deficiency of LLM agents in the crucial ability of "knowing when to stop." Agents often require excessive interactions to recognize that they should abstain, indicating that designing more effective agent systems needs to pay special attention to their ability to make timely decisions and identify when tasks are unfeasible.

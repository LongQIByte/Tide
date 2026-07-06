# EvoPolicyGym: Evaluating Autonomous Policy Evolution in Interactive Environments

[arXiv](https://arxiv.org/abs/2607.02440) · [HuggingFace](https://huggingface.co/papers/2607.02440) · ▲43

## 摘要（原文）

> Autonomous agents are increasingly expected to improve executable policies through feedback, yet existing evaluations often collapse this process into a final score or confound it with open-ended software-engineering progress. We introduce Autonomous Policy Evolution, a controlled evaluation setting in which a harness-model agent repeatedly edits an executable policy system under a fixed interaction budget. We instantiate this setting in EvoPolicyGym, a benchmark built from compact interactive RL environments that evaluates how agents iteratively improve explored policies. On the EvoPolicyGym suite, GPT-5.5 achieves the strongest aggregate rank score and top-two performance on all 16 environments. Beyond leaderboard results, EvoPolicyGym also provides trajectory-level diagnostics that distinguish how agents allocate budget, convert feedback into parametric tuning. These analyses show that strong autonomous policy evolution depends not only on isolated task wins, but on discovering task-appropriate mechanisms and refining policies under bounded feedback.

## 摘要（中译）

自主智能体被越来越多地期望通过反馈来改进可执行策略，然而现有的评估通常将这个过程简化为一个最终分数，或者将其与开放式的软件工程进展相混淆。我们引入了自主策略进化（Autonomous Policy Evolution），这是一个受控的评估环境，在该环境中，一个 harness - model 智能体在固定的交互预算下反复编辑一个可执行策略系统。我们在 EvoPolicyGym 中实例化了这种环境，EvoPolicyGym 是一个从紧凑的交互式强化学习（RL）环境中构建的基准测试，用于评估智能体如何迭代地改进已探索的策略。在 EvoPolicyGym 套件上，GPT - 5.5 获得了最强的综合排名分数，并在所有 16 个环境中取得了前两名的表现。除了排行榜结果之外，EvoPolicyGym 还提供了轨迹级别的诊断，这些诊断可以区分智能体如何分配预算、如何将反馈转化为参数调整。这些分析表明，强大的自主策略进化不仅取决于孤立的任务胜利，还取决于发现适合任务的机制以及在有限的反馈下优化策略。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
自主智能体（如代码生成工具或语言模型）需要通过环境反馈持续优化自身行为，而非仅输出固定结果。例如，编程代理需根据测试失败调整代码，语言模型需通过反思改进回答质量。这类技术的核心需求是：在有限交互次数内，将反馈转化为可执行策略的迭代改进，确保策略在新场景中仍能稳定工作。  

**2. 之前的问题**  
现有评估方法存在两大缺陷：  
- **结果导向的局限**：仅关注最终得分，忽略改进过程中的关键问题（如盲目重试、过拟合可见反馈、忽略验证集泛化能力）。  
- **开放工程的混淆**：在无约束的工程任务中（如持续迭代的软件项目），评估易被“规格变更”或“维护质量”等无关因素干扰，难以单独衡量策略优化的能力。  

**3. 本文的解法**  
论文提出**自主策略进化（Autonomous Policy Evolution）**框架，通过以下设计解决上述问题：  
- **受控基准测试**：构建EvoPolicyGym，提供一组紧凑的交互式强化学习环境（如机器人控制、驾驶模拟），要求智能体在固定预算（如128轮交互）内反复编辑策略系统，并基于沙盒环境的反馈进行优化。  
- **分离评估对象**：将“策略进化过程”本身作为评估目标，而非直接任务执行结果。智能体需提交策略版本并接收训练反馈，但验证和测试结果仅在服务器端计算，确保评估聚焦于策略改进的效率。  
- **轨迹级诊断**：记录完整的“执行-反馈-修订”轨迹，分析智能体如何分配预算、诊断错误以及平衡探索与利用。  

**4. 与前人工作的关键差异**  
- **聚焦过程而非结果**：传统基准（如OpenAI Gym）评估最终任务表现，而EvoPolicyGym通过隐藏的验证集衡量策略的泛化能力。  
- **严格控制变量**：相比开放工程基准（如软件维护任务），EvoPolicyGym限制环境变化，仅考察策略优化能力。  
- **诊断性分析**：提供细粒度的轨迹数据（如策略修订记录），揭示智能体如何将反馈转化为具体改进（如参数调优或结构修改）。  

这一框架使研究者能更深入理解自主智能体的迭代优化机制，而不仅仅是比较最终得分。

## 方法图解

![Figure 1 : EvoPolicyGym framework. (a) Interaction loop : agents edit policies, ](fig1_1.webp)

> Figure 1 : EvoPolicyGym framework. (a) Interaction loop : agents edit policies, submit episodic rollouts under a finite budget, and receive platform-mediated feedback. (b) Visibility boundary : training feedback is visible, while validation-based checkpoint selection and held-out evaluation are hidden. (c) Environment suite : a unified interface spanning control, navigation, driving, and robotics tasks under a shared evaluation protocol. (d) Measured aspects : feedback utilization, budget efficiency, and policy improvement dynamics, captured via the evolution of best-so-far performance over time.

这张图展示了EvoPolicyGym框架，它用于评估自主策略演进。我们可以将其分为四个主要部分来理解：

### 反馈驱动的演化循环 (Feedback-Driven Evolution Loop)
这部分描述了代理与平台交互的核心流程：
1. **编码代理 (Coding Agent)**：这是一个能够编辑和提交策略的智能体（如图中的机器人图标所示）。它负责修改策略代码。
2. **工作区 (workspace)**：代理在这里编辑策略（"policy.py (executable)"），即编写可执行的策略代码。
3. **提交剧集 (Submit Episodes)**：代理将编辑好的策略提交到沙盒化平台。
4. **沙盒化平台 (Sandboxed Platform)**：这个平台在有限的剧集预算（"finite episode budget"）下运行提交的策略，并生成滚动总结（"rollout summaries"）和轨迹反馈（"trajectory feedback"）。
5. **读取反馈 (Read Feedback)**：代理从平台接收反馈，然后根据反馈再次编辑策略，形成一个循环。

### 可见性边界 (Visibility Boundary)
这部分说明了代理能看到的信息和不能看到的信息：
- **训练池 (Train Pool)**：代理可以看到训练池中的滚动总结和轨迹反馈。这些信息用于代理学习和改进策略。
- **隐藏验证池 (Hidden Validation Pool)**：代理看不到这个池。平台会从这里选择最佳的检查点（"select best checkpoint"）。
- **隐藏保留池 (Hidden Held-out Pool)**：代理也看不到这个池。平台会在这个池中进行最终评估（"final evaluation"）。

### 环境套件 (Environment Suite)
这部分展示了EvoPolicyGym包含的不同任务类型：
- **控制 (Control)**：如Acrobot/Bipedal任务。
- **导航 (Navigation)**：如Minigrid任务。
- **驾驶 (Driving)**：如CarRacing任务。
- **机器人学 (Robotics)**：如Fetch任务。
这些任务有一个统一的接口和共享的评估协议，确保评估的一致性和可比性。

### 基准测量内容 (What the Benchmark Measures)
这部分说明了基准测试衡量的关键方面：
- **反馈利用 (Feedback use)**：衡量代理如何有效地利用反馈来改进策略。
- **预算分配 (Budget allocation)**：衡量代理如何在有限的剧集预算中分配资源。
- **泛化能力 (Generalization)**：衡量代理如何将从一个任务中学到的知识应用到未见过的新任务中。
图中还展示了一个性能随时间变化的曲线，显示了代理从发现启发式方法（"discover heuristic"）到细化启发式方法（"refine heuristic"），再到选择最佳检查点（"select best checkpoint"）的过程。此外，基准测试不仅关注最终得分，还关注整个执行-反馈-修订的轨迹。

通过这张图，我们可以清楚地看到EvoPolicyGym如何通过一个闭环系统来评估自主策略的演进，以及它如何衡量代理在不同方面的表现。

---

![Figure 5 : CarRacing code-phase timeline. Phase bands are inferred mechanically ](fig4_1.webp)

> Figure 5 : CarRacing code-phase timeline. Phase bands are inferred mechanically from the same policy source-bundle rule as Table 4 : synthesis-edit phases denote new AST topologies after numeric constants are stripped, and parametric-edit phases denote changed source bundles under the same topology. Symbols mark validation outcomes and candidate-management events; rollback/retest are event types, not additional edit types.

这张图是论文《EvoPolicyGym: Evaluating Autonomous Policy Evolution in Interactive Environments》中的Figure 5，标题为“CarRacing code-phase timeline”，展示了在CarRacing环境中不同智能体（GPT-5.5、Claude Opus 4.7、MiniMax-M3、DeepSeek-V4-Pro）的代码阶段时间线。

### 图中组件解释：
1. **横轴（X轴）**：表示“Consumed episode budget”（消耗的回合预算），范围从0到128，代表智能体在改进策略过程中消耗的资源或尝试次数。
2. **纵轴（Y轴）**：列出了四个不同的智能体，分别是GPT-5.5、Claude Opus 4.7、MiniMax-M3和DeepSeek-V4-Pro，每个智能体对应一条时间线。
3. **时间线上的符号和颜色**：
    - **青色（Synthesis edit）**：表示“合成编辑”阶段，即对策略的抽象语法树（AST）进行修改（去除数值常数后的新拓扑结构）。这些阶段的符号是圆圈（○），代表新的最佳状态（New best）或重新测试（Retest）。
    - **橙色（Parametric edit）**：表示“参数化编辑”阶段，即在相同拓扑结构下修改源代码包（changed source bundles under the same topology）。这些阶段的符号是三角形（△），代表没有改进（No improvement）。
    - **黑色菱形（Rollback）**：表示“回滚”事件，即撤销之前的编辑操作。
    - **白色圆圈（Retest）**：表示“重新测试”事件，即对当前策略进行重新评估。
    - **红色叉号（Failed）**：表示“失败”事件，但在这张图中似乎没有出现。
4. **右侧的“BEST SCORE”**：显示每个智能体在CarRacing环境中的最佳得分，从高到低依次是GPT-5.5（600）、Claude Opus 4.7（572）、MiniMax-M3（277）和DeepSeek-V4-Pro（23.0）。

### 方法运作方式：
这张图展示了智能体在固定交互预算下如何迭代改进可执行策略的过程。具体来说：
1. **编辑阶段**：智能体在“合成编辑”和“参数化编辑”阶段对策略进行修改。合成编辑涉及AST拓扑结构的变化，而参数化编辑则在相同拓扑下调整参数。
2. **验证和管理事件**：通过符号（如圆圈、三角形、菱形、白色圆圈）标记验证结果和候选管理事件。例如，圆圈表示新的最佳状态或重新测试，三角形表示没有改进，菱形表示回滚。
3. **预算消耗**：横轴显示了每个智能体在改进过程中消耗的回合预算，反映了策略改进的效率和资源利用情况。

### 结果分析：
从图中可以看出：
1. **最佳得分**：GPT-5.5在CarRacing环境中取得了最高的最佳得分（600），其次是Claude Opus 4.7（572），而DeepSeek-V4-Pro的得分最低（23.0）。
2. **编辑阶段分布**：GPT-5.5和Claude Opus 4.7在“合成编辑”阶段（青色圆圈）的分布较为均匀，且在后期有较多的“重新测试”（白色圆圈）和“回滚”（黑色菱形）操作，表明它们在不断优化策略。相比之下，MiniMax-M3和DeepSeek-V4-Pro的编辑阶段分布较为集中，且“没有改进”的事件（红色三角形）较多，说明它们的策略改进效率较低。
3. **预算利用**：GPT-5.5在消耗约128的回合预算后达到了最佳得分，而DeepSeek-V4-Pro在较低的预算下就停止了改进，可能是因为其策略改进遇到了瓶颈。

### 结论：
这张图清晰地展示了不同智能体在CarRacing环境中的策略改进过程，包括编辑阶段的类型、验证结果、预算消耗和最佳得分。通过分析这些信息，我们可以得出以下结论：
- 强大的自主策略进化不仅依赖于孤立的任务胜利，还依赖于发现任务适当的机制并在有限的反馈下优化策略。
- EvoPolicyGym提供的轨迹级诊断有助于区分智能体如何分配预算、将反馈转化为参数调整，从而评估其策略改进的效率和效果。

---

![Figure 6 : Bipedal code-phase timeline, rendered with the same synthesis-edit an](fig5_1.webp)

> Figure 6 : Bipedal code-phase timeline, rendered with the same synthesis-edit and parametric-edit phase rules as Figure 5 . The environment is tuning-dominant, but successful tuning still depends on first reaching a viable gait topology; same-topology source-bundle edits then expose whether an agent can improve that structure by adjusting constants and thresholds.

这张图展示了不同智能体在“双足行走”任务中进行策略迭代优化的时间线，帮助我们理解它们如何在固定的交互预算下改进可执行策略。以下是对图中各个组件的详细解释：

### 图的组件与信息流动
1. **标题与副标题**：
   - 标题“Bipedal Code-Phase Timeline”表明这是关于双足行走任务的代码阶段时间线。
   - 副标题“Bipedal: parametric-edit example”说明这是一个参数化编辑的示例。

2. **图例**：
   - 不同颜色和形状的标记代表不同的操作类型：
     - 青色（Synthesis edit）：合成编辑，可能涉及创建或修改策略的整体结构。
     - 棕色（Parametric edit）：参数化编辑，调整策略中的常数和阈值等参数。
     - 绿色圆圈（New best）：新的最佳策略，表示当前策略的性能有所提升。
     - 红色三角形（No improvement）：无改进，当前编辑操作没有提升策略性能。
     - 蓝色菱形（Rollback）：回滚，撤销之前的编辑操作。
     - 白色圆圈（Retest）：重新测试，对当前策略进行重新评估。
     - 红色叉号（Failed）：失败，编辑操作未成功。

3. **横轴（Consumed episode budget）**：
   - 表示消耗的交互预算，范围从0到128，代表智能体在优化过程中使用的资源量。

4. **纵轴（智能体）**：
   - 列出了四个智能体：GPT-5.5、Claude Opus 4.7、MiniMax-M3和DeepSeek-V4-Pro，每个智能体对应一条时间线。

5. **右侧的BEST SCORE**：
   - 显示每个智能体的最佳得分，用于比较它们的最终性能。

### 方法的运作方式
这张图展示了智能体在双足行走任务中如何通过迭代编辑来优化策略：
1. **初始阶段**：
   - 智能体首先进行合成编辑（青色线段），尝试创建或修改策略的整体结构，以达到可行的步态拓扑。
2. **参数调整阶段**：
   - 在达到可行的步态拓扑后，智能体进行参数化编辑（棕色线段），调整常数和阈值等参数，以进一步优化策略性能。
3. **反馈与决策**：
   - 智能体根据反馈（如“New best”、“No improvement”、“Rollback”等标记）决定是否继续当前策略、回滚到之前的版本或重新测试。
   - 例如，红色三角形表示当前编辑操作没有提升性能，智能体可能需要调整策略或回滚到之前的版本。

### 结果与结论
1. **坐标与对比对象**：
   - 横轴是消耗的交互预算，纵轴是不同的智能体。
   - 右侧的BEST SCORE显示了每个智能体的最佳得分，用于比较它们的最终性能。
2. **结论**：
   - GPT-5.5的最佳得分为271，明显高于其他智能体，表明它在双足行走任务中表现最好。
   - Claude Opus 4.7、MiniMax-M3和DeepSeek-V4-Pro的最佳得分分别为-15.6、-80.5和-97.5，远低于GPT-5.5。
   - 这表明强大的自主策略进化不仅依赖于孤立的任务胜利，还依赖于发现适合任务的机制并在有限的反馈下优化策略。

通过这张图，我们可以清楚地看到不同智能体在双足行走任务中如何分配预算、转换反馈并进行参数调整，从而理解它们在策略优化过程中的表现差异。

---

![Figure 7 : CarRacing feedback-utilization traces. Each row links evidence, attri](fig6_1.webp)

> Figure 7 : CarRacing feedback-utilization traces. Each row links evidence, attribution, policy revision, and outcome across agents. The submit column reports the submission index (s00k denotes the k-th submission) and the cumulative episode budget consumed prior to that submission. Labels are derived from logs, feedback summaries, and checkpoint diffs. The figure provides qualitative evidence of how feedback is translated into policy updates and is not an aggregate metric.

这张图（图7）展示了不同智能体在CarRacing环境中的反馈利用轨迹，旨在说明智能体如何将反馈转化为策略更新。我们可以从以下几个部分来理解这张图：

1.  **列的含义与信息流动**：
    *   **Submit（提交）**：这一列包含两个关键信息。首先是提交索引（如s001, s013, s007等），其中`s00k`表示第k次提交。其次是该提交之前消耗的累计回合预算（例如，GPT-5.5的s001提交了16个回合的预算）。这代表了智能体在迭代改进策略时的步骤和资源消耗。
    *   **Evidence（证据）**：这一列描述了智能体在特定提交时观察到的反馈或问题。这些反馈通常来自环境的交互日志、反馈摘要或检查点差异。例如，GPT-5.5在s001提交时观察到“早期不稳定，奖励下降表明失去了早期进展”。
    *   **Attribution（归因）**：这一列分析了证据背后的原因或问题。它将观察到的现象归因于策略的某些缺陷或不足。例如，对于GPT-5.5的s001提交，归因是“弱晚期转弯识别；小镜像缺口”。
    *   **Policy revision（策略修订）**：基于归因，这一列描述了智能体对策略进行的具体修改。例如，GPT-5.5针对s001的归因，采取了“增加前瞻性，合并掩码缺口，降低急转弯速度”的策略修订。
    *   **Outcome（结果）**：这一列显示了策略修订后的结果。结果可能是“new best”（新的最佳）、“rollback”（回滚）、“No improvement”（无改进）或“retest”（重新测试）。例如，GPT-5.5的s001修订结果是“new best”。

2.  **数据或信息的流动顺序**：
    图中的每一行代表一个智能体在某个特定提交点的反馈利用过程。信息流动的顺序是：**提交（消耗预算） -> 观察到证据（问题/反馈） -> 分析归因（问题原因） -> 执行策略修订 -> 观察结果**。这个过程在多行中重复，展示了智能体多次迭代改进策略的轨迹。

3.  **方法的具体运作方式**：
    这张图揭示了EvoPolicyGym基准测试中智能体如何运作：
    *   **迭代改进**：智能体在固定的交互预算下，反复提交策略并进行改进。
    *   **反馈驱动**：改进过程是由环境反馈驱动的。智能体需要从反馈中识别问题（证据），分析问题原因（归因），然后调整策略（策略修订）。
    *   **策略修订**：策略修订是基于对问题的理解进行的，可能涉及参数调整、算法修改或策略逻辑的改变。
    *   **结果评估**：每次策略修订后，都会评估其效果，以确定是否取得了改进。

4.  **结果图的解读**：
    *   **坐标/对比对象**：图的行代表不同的提交（由不同智能体在不同时间点进行），列代表反馈利用的不同阶段。对比对象是不同的智能体（如GPT-5.5, Claude Opus 4.7, Minimax-M3, DeepSeek-V4-Pro）在相同或不同提交点的表现。
    *   **结论**：这张图提供了定性证据，说明不同智能体如何将反馈转化为策略更新。通过观察不同智能体的轨迹，我们可以看到它们在识别问题、分析原因和执行修订方面的差异。例如，一些智能体能够快速找到有效的策略修订（如GPT-5.5的s001达到“new best”），而另一些则可能遇到困难（如DeepSeek-V4-Pro的s007“无改进”）。这张图强调了强大的自主策略进化不仅依赖于孤立的任务胜利，还依赖于发现任务适当的机制并在有限的反馈下优化策略。

总之，这张图通过展示智能体在CarRacing环境中的反馈利用轨迹，详细说明了自主策略进化的过程：从提交、观察反馈、分析原因到修订策略，并最终评估结果。它为理解智能体如何学习和改进其策略提供了一个清晰的视觉化工具。

---

![Figure 9 : GPT-5.5 CarRacing visible diagnostics saved by the agent during the r](fig8_1.webp)

> Figure 9 : GPT-5.5 CarRacing visible diagnostics saved by the agent during the run. Panels A–B show how structural-synthesis edits turn pixel observations into road-geometry control signals: yellow points mark sampled road evidence, cyan/magenta lines mark guide estimates, and action bars/log text summarize the agent’s own rollout diagnostics. Panel C shows a later visible candidate comparison after a parametric-tuning edit. These images are qualitative evidence only and do not expose hidden-validation or held-out cases.

这张图（图9）来自论文《EvoPolicyGym: Evaluating Autonomous Policy Evolution in Interactive Environments》，展示了智能体（在这里是GPT-5.5）在CarRacing环境中运行时保存的可见诊断信息。这些诊断信息帮助我们理解智能体如何迭代地改进其策略。

图的结构分为三个主要部分：A、B和C，每个部分都展示了智能体在不同阶段或不同类型的编辑操作后的行为和决策过程。

**面板A：Probe baseline（探测基线）**
这个面板展示了“结构合成”编辑的结果，提交编号为000，并标记为“新的最佳”。它由三个子图组成，每个子图都显示了智能体在赛道上的行驶轨迹和相关的诊断信息。
- **子图内容**：每个子图都包含一个赛道场景，其中黄色的点表示智能体采样的道路证据（road samples），这些点帮助智能体感知赛道的几何形状。青色和洋红色的线表示引导估计（guide estimates），这些线是智能体根据采样证据推断出的道路方向或路径。此外，每个子图的顶部和底部都有黑色的条带，显示了智能体自身的滚动诊断信息，包括时间步（t）、奖励（r）、分数（s）、以及一些参数（如g和b）。这些条带还可能包含动作条（action bars），总结了智能体的动作决策。
- **数据流动**：智能体首先通过观察像素级的图像（赛道场景）来采样道路证据（黄色点）。然后，它使用这些证据来估计道路的几何形状（青色/洋红色线）。最后，根据这些估计，智能体执行动作并在滚动诊断条中记录相关信息。

**面板B：Road-geometry controller（道路几何控制器）**
这个面板展示了另一种“结构合成”编辑的结果，提交编号为001，同样标记为“新的最佳”。它也由多个子图组成，每个子图都显示了智能体在赛道上的行驶轨迹和诊断信息。
- **子图内容**：与面板A类似，每个子图都包含赛道场景、黄色采样点、青色/洋红色引导线以及滚动诊断条。这些子图展示了智能体在不同时间步或不同阶段的行驶情况。
- **数据流动**：与面板A类似，智能体通过采样道路证据、估计道路几何形状并执行动作来导航赛道。这个面板可能展示了智能体在调整其道路几何控制器后的行为变化。

**面板C：Candidate comparison（候选比较）**
这个面板展示了在一次“参数调整”编辑后的可见候选比较，提交编号为004，并标记为“新的最佳”。它是一个更长的子图，显示了智能体在赛道上的连续行驶轨迹和诊断信息。
- **子图内容**：这个子图包含四个时间步（t=200, t=250, t=300, t=350）的快照，每个快照都显示了智能体在赛道上的位置和方向。每个快照的顶部都有黑色的条带，显示了时间步（t）、奖励（r）、分数（s）、以及参数（如g和b）。智能体的位置用红色汽车表示，黄色点表示采样道路证据，青色/洋红色线表示引导估计。
- **数据流动**：在这个面板中，智能体在参数调整后继续导航赛道。我们可以看到智能体在不同时间步的位置变化，以及它如何根据采样证据和引导估计来调整其行驶轨迹。

**方法运作的具体说明**
从这张图中，我们可以看到智能体如何通过迭代地编辑其策略系统来改进性能。具体来说：
1. **结构合成编辑**：智能体通过采样道路证据（黄色点）来感知赛道，并估计道路的几何形状（青色/洋红色线）。这些估计帮助智能体规划其行驶路径。
2. **参数调整编辑**：智能体调整其策略的参数（如g和b），以优化其性能。这可以通过比较不同时间步的行驶轨迹和诊断信息来观察。
3. **反馈循环**：智能体在每次编辑后都会执行动作，并根据收到的反馈（如奖励和分数）来进一步调整其策略。这个过程是迭代的，直到达到预期的性能。

**结论**
这张图提供了定性证据，展示了智能体如何在EvoPolicyGym环境中迭代地改进其策略。通过分析智能体的可见诊断信息，我们可以理解其如何分配预算、将反馈转换为参数调整，并发现任务适当的机制。这些分析表明，强大的自主策略进化不仅依赖于孤立的任务胜利，还依赖于在有限反馈下发现任务适当的机制并优化策略。

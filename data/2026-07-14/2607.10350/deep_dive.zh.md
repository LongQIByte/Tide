# ABot-AgentOS: A General Robotic Agent OS with Lifelong Multi-modal Memory

[arXiv](https://arxiv.org/abs/2607.10350) · [HuggingFace](https://huggingface.co/papers/2607.10350) · ▲84

## 摘要（原文）

> Recent VLM and VLA systems have improved robotic perception and action prediction, yet long-horizon embodied agents still require a general runtime layer for reasoning, memory, tool use, verification, and cross-embodiment execution. We present ABot-AgentOS, a general robotic Agent Operating System that sits above low-level controllers and provides a deliberative agent layer for scene-conditioned planning, context-isolated skill execution, multi-stage verification, multi-modal memory, and edge-cloud collaboration. To evaluate such systems, we introduce EmbodiedWorldBench, an executable benchmark with 16 indoor, outdoor, and hybrid scenes, four difficulty levels, and over 200 tasks involving navigation, object search, NPC dialogue, dynamic events, and trace-grounded scoring. ABot-AgentOS further introduces Universal Multi-modal Graph Memory, a persistent source-grounded substrate that converts dialogue, visual observations, spatial context, temporal relations, and task traces into typed nodes and edges. A failure-driven self-evolution loop converts diagnosed memory failures into gated runtime evo-assets that are promoted only to later evaluation splits, preventing current-split ground-truth leakage while enabling continual improvement. On an initial EmbodiedWorldBench subset, ABot-AgentOS improves over a single-controller baseline in both task success and goal completion. Across memory benchmarks, ABot-AgentOS Static achieves 87.5 on LoCoMo, 59.9 on OpenEQA EM-EQA, 88.6 on Mem-Gallery, and 76.5 Acc@All on NExT-QA; self-evolution further improves LoCoMo to 88.7, OpenEQA to 60.4, and Mem-Gallery to 89.0. These results suggest that a general Agent OS layer can improve long-horizon embodied execution while providing persistent, auditable memory for continual interaction.

## 摘要（中译）

最近的视觉语言模型（VLM）和视觉-语言-动作模型（VLA）系统提升了机器人感知和动作预测能力，但长时程具身智能体仍需要一个通用的运行时层来实现推理、记忆、工具使用、验证和跨具身执行。我们提出了ABot-AgentOS，这是一个通用机器人智能体操作系统，位于低级控制器之上，为场景条件规划、上下文隔离的技能执行、多阶段验证、多模态记忆和边缘-云协作提供了一个慎思智能体层。为了评估此类系统，我们引入了EmbodiedWorldBench，这是一个可执行的基准测试，包含16个室内、室外和混合场景，四个难度级别，以及超过200个涉及导航、物体搜索、非玩家角色（NPC）对话、动态事件和基于轨迹评分的任务。ABot-AgentOS进一步引入了通用多模态图记忆，这是一个持久化的源基础基质，将对话、视觉观察、空间上下文、时间关系和任务轨迹转换为类型化的节点和边。一个由失败驱动的自我进化循环将诊断出的记忆故障转换为门控运行时进化资产，这些资产仅被提升到后续的评估分割中，防止当前分割的真实情况泄露，同时实现持续改进。在一个初始的EmbodiedWorldBench子集上，ABot-AgentOS在任务成功率和目标完成率上都优于单控制器基线。在记忆基准测试中，ABot-AgentOS静态版本在LoCoMo上得分为87.5，在OpenEQA EM-EQA上得分为59.9，在Mem-Gallery上得分为88.6，在NExT-QA上的Acc@All得分为76.5；自我进化进一步将LoCoMo提高到88.7，OpenEQA提高到60.4，Mem-Gallery提高到89.0。这些结果表明，一个通用的智能体操作系统层可以提高长时程具身执行，同时为持续交互提供持久、可审计的记忆。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
随着机器人技术的发展，人们希望AI不仅能处理数字任务（如聊天或图像识别），还能在物理世界中执行复杂、长期的任务——比如家庭服务、工业巡检或动态环境中的协作。这类“具身智能”需要解决三个核心问题：如何让机器人理解复杂指令并转化为可靠动作？如何让同一套系统适应不同形态的机器人（如人形、四足）？以及如何让机器人在长期互动中记住关键信息（比如“上次在这个房间找不到钥匙，这次应该检查抽屉”）？这些需求推动了从“单次任务执行”向“持续自主决策”的转变。  

**2. 先前方法的局限性**  
尽管视觉语言模型（VLM）和机器人控制技术取得了进展，现有系统仍存在三大瓶颈：  
- **推理与执行的脱节**：许多系统直接将AI模型的输出映射为动作，缺乏中间层来分解任务、验证步骤或处理错误（例如，机器人可能按指令拿起杯子，但没考虑杯子是否装满水）。  
- **形态泛化能力不足**：现有方案通常绑定特定硬件或环境（如只能用于实验室的机械臂），难以适应不同机器人（如从轮式机器人切换到人形机器人）。  
- **记忆的局限性**：传统记忆系统仅存储文本或短期数据，无法持久化关联多模态信息（如视觉观察、对话历史和空间关系），导致机器人无法从长期经验中学习（例如，忘记之前遇到的障碍物位置）。  

**3. 本文的解决思路**  
ABot-AgentOS通过三层创新突破这些限制：  
- **通用机器人操作系统架构**：在底层控制器（如运动控制）和高层AI模型之间插入一个“代理层”，负责任务规划、工具使用和错误恢复。这一层像一个“管家”，协调不同模块（如语音理解、视觉导航、技能调用），并支持多种机器人形态。  
- **动态基准测试**：设计了一个名为EmbodiedWorldBench的测试框架，包含室内、室外和混合场景的复杂任务（如与人对话、动态避障），评估机器人的长期自主能力。  
- **多模态记忆系统**：将机器人的经验（如对话、视觉观察、任务轨迹）存储为结构化的“图记忆”，并能通过失败分析自动优化（例如，如果机器人某次任务失败，系统会记录原因并在未来避免相同错误）。  

**4. 关键差异与创新点**  
与先前工作相比，ABot-AgentOS的核心突破在于：  
- **分层解耦**：将认知推理与物理执行分离，使系统更灵活且易于扩展；  
- **跨形态泛化**：通过插件式设计支持不同机器人硬件，而非针对单一设备优化；  
- **可进化记忆**：记忆不仅是存储，还能通过“失败驱动的学习”持续改进，让机器人在长期互动中变得更聪明。  

这一系统为具身智能从实验室原型走向实际应用提供了基础，让机器人能够像人类一样“思考、记忆、行动并从中学习”。

## 方法图解

![Figure 1 : System architecture of the proposed robot agent. Inputs from multiple](fig1_1.webp)

> Figure 1 : System architecture of the proposed robot agent. Inputs from multiple sources (microphone, APP, camera) to a dual-LLM core, where a Tiny LLM on the edge handles every turn and escalates to a cloud-based Large LLM on demand. The Agent Harness manages verification-aware ReAct loop, context, and skill evolvement, enabling an extensible skill library (Manipulation, Navigation, Motion, Vision, etc.). A hierarchical Memory System synchronizes private edge memory with shared cloud memory to support cross-robot knowledge transfer. Outputs are dispatched to the robot hardware for execution.

这张图展示了ABot - AgentOS的系统架构，我们可以从左到右、从上到下逐步解析每个组件及其信息流动：

首先看最左侧的“Input”部分，这里有三个输入源：麦克风（microphone）、应用程序（APP）和摄像头（camera）。这些输入源负责收集机器人的多模态输入，比如语音、应用指令、视觉图像等，然后将这些输入传递到中间的系统核心部分。

接下来是中间的几个主要模块：
1. **Skills & Tools（技能与工具）**：这个模块包含多个子模块，如Manipulation (Abot - M)、Navigation (Abot - N)、Motion、Vision等（还有省略号表示其他技能）。这些是机器人执行具体任务的工具，比如操作物体、导航、运动控制、视觉感知等。信息会从下方的模块传递到这里，然后输出到最右侧的“Robot Hardware（机器人硬件）”以执行任务。
2. **双LLM核心**：
    - **Tiny LLM (Edge)**：标注为“runs every turn”，意思是它在每一个交互回合都运行，位于边缘端（Edge）。它的作用是处理日常的、频繁的任务或决策，当遇到复杂问题时，会通过“help”箭头向“Large LLM (Cloud)”请求帮助。
    - **Large LLM (Cloud)**：标注为“runs on - demand”，即按需运行，位于云端（Cloud）。它处理更复杂、需要更多计算资源或知识的任务，当Tiny LLM无法处理时，会调用它来获取支持。
3. **Agent Harness（代理 harness）**：这个模块包含三个子部分：Verification - aware ReAct、Context Management、Skill Evolvement。Verification - aware ReAct负责带验证的ReAct循环（ReAct是一种结合推理和行动的框架），确保任务执行的正确性；Context Management管理上下文，让机器人在不同任务或场景中保持上下文的一致性；Skill Evolvement负责技能的进化，使机器人的技能能够不断改进。这个模块连接了LLM核心和Memory System，起到协调和管理的作用。
4. **Memory System（记忆系统）**：
    - **Private Memory (Edge)**：位于边缘端，包含Map as memory、Semantic memory、Multi - modal memory等。它存储机器人在本地（边缘）的记忆，比如地图信息、语义信息、多模态信息（结合视觉、语音等）。
    - **Common Memory (Cloud)**：位于云端，包含Map as memory等，存储共享的知识或跨机器人的记忆。
    - 这两个记忆部分之间有“upload”和“download”箭头，表示私有边缘内存和共享云内存之间的同步，支持跨机器人的知识转移。

信息的流动顺序大致是：输入源（麦克风、APP、摄像头）将输入传递到双LLM核心（Tiny LLM先处理，必要时调用Large LLM）；然后Agent Harness管理验证、上下文和技能进化，协调LLM核心和记忆系统的交互；记忆系统在边缘和云端之间同步记忆；最后，处理后的信息传递到Skills & Tools模块，再输出到机器人硬件执行任务。

这张图揭示了ABot - AgentOS的运作方式：它通过边缘端的Tiny LLM处理日常任务，按需调用云端的Large LLM处理复杂任务；Agent Harness负责验证、上下文管理和技能进化，确保任务执行的正确性和技能的改进；记忆系统在边缘和云端同步，支持多模态记忆和跨机器人知识转移；最终通过技能与工具模块驱动机器人硬件执行任务，形成一个从输入到输出的完整机器人代理系统，解决了长 horizon（长周期）具身智能体需要的推理、记忆、工具使用、验证和跨具身执行等问题。

---

![Figure 2 : Overview of the Agent Harness. The main LLM performs scene-conditione](fig2_1.webp)

> Figure 2 : Overview of the Agent Harness. The main LLM performs scene-conditioned planning with memory and context, delegates procedural subtasks to the Skill Runner, and receives corrective feedback from the Verifier to form a reasoning-execution-verification loop.

这张图（图2：Agent Harness概述）清晰地展示了ABot-AgentOS中代理执行任务的核心流程，它是一个“推理-执行-验证”的循环系统。

首先，流程从左侧的“Task”（任务）开始，用一个带有对勾和符号的黄色方框表示。这个任务被传递给中央的“LLM”（大型语言模型），用蓝色大脑图标表示。LLM是整个系统的核心推理组件，它接收来自“Memory”（记忆，数据库图标）和“Context”（上下文，日历/时钟图标）的信息输入，这些信息为LLM提供了场景条件和历史背景。LLM利用这些信息进行“Observation”（观察）、“Planning”（规划）、“Reasoning”（推理）和“Action”（行动），这些功能列在大脑图标的右侧。

接下来，LLM将规划好的程序性子任务委托给“Skill Runner”（技能运行器），用粉色的工人图标表示。Skill Runner负责执行具体的操作，它利用“Skills”（技能，卡片图标）和“Tools”（工具，扳手和螺丝刀图标）来完成这些子任务。

在执行过程中，系统的“Verifier”（验证器），用绿色盾牌图标表示，会进行监控。Verifier接收来自“Runtime”（运行时，播放按钮图标）和“Finish Call”（结束调用，电源按钮图标）的信息。它主要负责“Runtime Verification”（运行时验证）和“Finish Time Verification”（完成时间验证）。如果验证发现问题，会向LLM提供“corrective feedback”（纠正反馈），形成一个反馈回路，如图中从Verifier到LLM的虚线箭头所示。同时，Verifier也会进行“Runtime Verification”（运行时验证）并将信息反馈给LLM，以支持持续的推理和调整。

最后，当任务完成并通过验证后，流程到达最右侧的“Task Done?”（任务完成了吗？），用紫色旗帜图标表示，标志着任务的结束。

整个流程揭示了ABot-AgentOS的工作方式：任务由LLM驱动，结合记忆和上下文进行规划；具体操作由Skill Runner执行；整个过程受到Verifier的监控和验证，确保任务正确完成，并通过反馈回路实现持续改进和修正。这是一个典型的“思考-行动-检查-调整”循环在机器人代理系统中的体现。

数据或信息的流动顺序是：任务 -> LLM（结合记忆和上下文进行推理规划）-> Skill Runner（执行子任务）-> Verifier（监控和验证）-> （反馈给LLM进行调整，如果需要）-> 任务完成确认。

---

![Figure 3 : Overview of the multi-modal memory architecture. During online execut](fig3_1.webp)

> Figure 3 : Overview of the multi-modal memory architecture. During online execution, ABot-AgentOS writes observations and interactions into a source-grounded memory graph, retrieves task-relevant evidence, and records retrieval and answer traces. Offline, failure traces are diagnosed and converted into gated runtime evo-assets for later deployments.

这张图展示了ABot - AgentOS的多模态记忆架构，我们可以从在线执行和离线优化两个阶段来理解其工作流程：

### 在线执行阶段（数据流向与组件作用）
1. **感知（Perception）**：作为信息输入的起点，感知模块收集环境的多模态信息（如视觉、听觉等），然后将这些信息传递给**Agent Controller（智能体控制器）**。Agent Controller包含三个核心操作：Think（思考）、Act（行动）、Observe（观察），它负责协调整体的决策和执行流程。
2. **技能（Skills）**：上方的四个技能模块（Grounding：理解现实场景；Embeddings：语义知识；Face Embeddings：视觉身份识别；Tool - use / Prompt Skill：工具使用或提示技能）为Agent Controller提供支持，这些技能的知识或能力会被Agent Controller调用，以辅助其思考、行动或观察过程。
3. **记忆数据库（Memory DB）**：Agent Controller会与Memory DB进行交互。一方面，通过**Write Memory（写入记忆）**模块，将感知到的观察结果和交互信息（这些信息是“source - grounded”的，即有明确的来源依据）写入到Memory DB中，形成多模态的记忆图（包含对话、视觉观察、空间上下文、时间关系和任务轨迹等类型的节点和边）。另一方面，通过**Retrieve Memory（检索记忆）**模块，从Memory DB中检索与当前任务相关的证据，以支持决策或回答。
4. **VLM / LLM与回答、轨迹记录**：Agent Controller还会与**VLM / LLM（视觉语言模型/大语言模型）**交互，利用模型的能力生成**Answer（回答）**。同时，会记录**Trace Log（轨迹日志）**，如果出现失败情况，还会生成**Failure Trace（失败轨迹）**。

### 离线优化阶段（自我进化循环）
1. **失败轨迹的诊断与进化资产生成**：离线时，**Failure Trace（失败轨迹）**会被传递给**Diagnoser（诊断器）**子代理，诊断器分析失败的原因。然后，信息依次传递给**Hypothesis（假设）**子代理（生成关于失败的假设）、**Compiler（编译器）**子代理（将假设编译成可执行的改进方案）、**Gate Analyst（门分析器）**子代理（分析并决定是否将这些改进方案作为“gated runtime evo - assets（受控的运行时进化资产）”）。
2. **进化资产的部署**：这些进化资产会被“推广”到后续的评估分割（evaluation splits）中，用于以后的部署。这样做的目的是防止当前的“ground - truth（真实标签）”泄漏（即避免当前任务的解决方案影响未来任务的公平评估），同时实现持续的改进。

### 整体工作逻辑总结
在线执行时，ABot - AgentOS通过感知获取环境信息，由Agent Controller结合各种技能进行思考、行动和观察，同时将相关信息写入多模态记忆图（Memory DB），并从记忆中检索相关证据来支持决策和回答，同时记录轨迹和失败信息。离线时，通过对失败轨迹的诊断和分析，生成进化资产并部署到后续任务中，以实现系统的持续改进。这种架构使得ABot - AgentOS能够处理长周期的具身智能任务，具备场景条件规划、上下文隔离的技能执行、多阶段验证、多模态记忆和边缘 - 云协作等能力。

---

![Figure 4 : Concrete memory failure-to-evolution examples. Left: visual memory QA](fig4_1.webp)

> Figure 4 : Concrete memory failure-to-evolution examples. Left: visual memory QA retrieves image-grounded identity evidence but can expose missing breed-specific cues. Right: temporal text memory QA uses session metadata to resolve relative dates but can reveal temporal-normalization errors. In both cases, the failure trace is converted into targeted memory-writing, evidence-selection, frame-selection, or answering improvements.

这张图（图4）展示了**ABot-AgentOS**中“记忆失败到进化”的具体案例，分为**视觉记忆QA（左栏，A部分）**和**文本记忆QA（右栏，B部分）**两个模块，清晰呈现了“记忆写入→感知/检索→回答→失败分析→自我进化”的端到端流程，以及如何通过失败驱动的循环持续优化系统能力。  


### 左栏：视觉记忆QA（Image modality: visual memory QA）  
该模块展示**“图像-身份-相似性判断”**的记忆与推理流程，核心是“视觉线索匹配”与“失败后针对性优化”：  

1. **Memory Writer（记忆写入）**：  
   将图像转化为“带类型的记忆记录”。例如，D2:1记录（id=D2:1，modality=image，type=identity，entity=Lena，content=Maltese adopted）和D2:4记录（entity=Amy，content=Cairn / Pebble），并生成图像嵌入（img_emb）。这一步是“将视觉观察持久化为结构化记忆”，为后续检索提供依据。  

2. **Perception and retrieval action（感知与检索动作）**：  
   - 输入：查询问题（Q: “More similar to Amy or Lena?”）和待查询的图像（query图像，一只Cairn Terrier样貌的狗）。  
   - 感知线索（perception cues）：提取图像的视觉特征，如“shaggy coat（蓬松的毛）”“upright ear（直立的耳朵）”“terrier face（梗类狗的脸）”。  
   - 检索证据（retrieval evidence）：系统根据感知线索，从记忆中检索相关记录并打分。例如，Amy的记录（Cairn Terrier）得分0.82，Lena的记录（Maltese / Lumi）得分0.41。箭头表示“感知线索→检索证据”的匹配过程（得分高的线索优先匹配）。  

3. **Answer（回答）**：  
   根据检索证据的得分，得出结论：“Amy's Cairn Terrier”，并标注“gold answer（真实答案）”一致，说明这次回答正确？不，结合“Self-evo”部分，实际是**暴露了“缺失品种特异性线索”的问题**（后续进化解决）。这里回答正确但过程有隐患，需要优化。  

4. **Self-evo: concrete visual-cue improvement（自我进化：具体的视觉线索优化）**：  
   这是“失败驱动的优化循环”：  
   - failure trace（失败轨迹）：红色框显示“scene bias ranks Maltese too high（场景偏差导致Maltese的排名过高）”，即系统错误地认为待查询图像更像Maltese（Lena的品种），但实际应像Cairn Terrier（Amy的品种）。  
   - diagnoser（诊断器）：分析问题根源——“breed cues under-weighted（品种线索权重过低）”，即系统对“品种相关的视觉线索（如ear、coat）”重视不足。  
   - compiler patch（编译补丁）：针对诊断结果，调整“Cue Reranker（线索重排器）”，提升“ear”和“coat”线索的权重（蓝色条表示调整后权重变化）。  
   - gate analyst（门分析器）：验证优化效果——“0.52→0.82”（Amy的排名从0.52提升到0.82，超过Lena的0.41），且“Amy rank passes（Amy的排名通过验证）”。  
   - evo asset（进化资产）：将优化后的“Visual（视觉）”策略（如BreedCue Rerank）作为“进化资产”，仅在未来评估中使用（防止当前数据泄露，实现持续改进）。  


### 右栏：文本记忆QA（Text modality: temporal text memory QA）  
该模块展示**“文本-时间-日期解析”**的记忆与推理流程，核心是“时间归一化”与“失败后针对性优化”：  

1. **Memory Writer（记忆写入）**：  
   将文本转化为“带时间戳的记忆记录”。例如，输入文本“I adopted a Maltese dog yesterday!”（含时间词“yesterday”），系统先解析出日期（D2 date=2024-05-23），然后生成文本记录（id=D2:1，type=text，date=2024-05-23，content=Lena adopted dog yesterday），并生成文本嵌入（txt_emb）。这一步是“将文本对话持久化为带时间的结构化记忆”，为后续时间推理提供依据。  

2. **QA retrieval and answer process（问答检索与回答过程）**：  
   - 输入：问题（Q: “When did Lena adopt her dog?”，要求输出YYYY-MM-DD格式）。  
   - 检索相关记录：找到D2:1记录（内容含“yesterday”），需要解析“yesterday”的具体日期。  
   - 时间归一化：结合“session date anchors（会话日期锚点）”，假设会话日期是2024-05-23（因为D2 date=2024-05-23，“yesterday”对应2024-05-22）。箭头表示“问题→检索记录→时间解析”的流程。  

3. **Answer（回答）**：  
   得出结论：“2024-05-22”，并验证“gold answer（真实答案）”一致，说明这次回答正确？同样，结合“Self-evo”部分，实际是**暴露了“时间归一化错误”的隐患**（后续进化解决）。  

4. **Self-evo: concrete temporal-text improvement（自我进化：具体的时间-文本优化）**：  
   这是“失败驱动的优化循环”：  
   - failure trace（失败轨迹）：红色框显示“relative date not grounded（相对日期未归一化）”，即系统可能错误处理“yesterday”的时间（比如会话日期不是2024-05-23时，解析会出错）。  
   - diagnoser（诊断器）：分析问题根源——“D2 date missing（D2日期缺失）”或“yesterday的时间未正确锚定”。  
   - compiler patch（编译补丁）：针对诊断结果，调整“TemporalResolver（时间解析器）”，使用“session date - 1 day（会话日期减1天）”的策略。  
   - gate analyst（门分析器）：验证优化效果——“May 23 - 1d → 2024-05-22”（解析正确），并标记“√”表示通过验证。  
   - evo asset（进化资产）：将优化后的“Text（文本）”策略（如RelativeDate Resolver）作为“进化资产”，仅在未来评估中使用（防止当前数据泄露，实现持续改进）。  


### 整体逻辑：“失败→诊断→优化→进化”的闭环  
两个模块都遵循**“记忆写入（持久化多模态数据）→感知/检索（匹配记忆与当前任务）→回答（生成结果）→失败分析（识别问题）→自我进化（针对性优化，生成可复用的策略）”**的流程。  

- 视觉模块的问题是“视觉线索权重失衡（品种线索被低估）”，优化后提升了品种相关的线索权重，确保相似性判断更准确。  
- 文本模块的问题是“时间归一化依赖会话日期（可能泄露当前数据）”，优化后使用“会话日期-1天”的策略，确保时间解析更鲁棒（且仅在未来使用，避免当前split的答案泄露）。  

这种“失败驱动的自我进化”是ABot-AgentOS的核心：通过诊断记忆系统的失败点，生成针对性的优化策略（evo-assets），并将其“门控”到未来评估中，既解决了当前问题，又实现了**持续改进**（防止当前数据的答案泄露到未来任务中，保证评估的公平性）。  


这张图清晰展示了ABot-AgentOS如何通过“多模态记忆+失败进化”解决机器人代理中的长 horizon 推理问题：不仅完成当前任务，还能从失败中学习，逐步提升未来的性能。

---

![Figure 5 : Overview of EmbodiedWorldBench. EmbodiedWorldBench evaluates embodied](fig5_1.webp)

> Figure 5 : Overview of EmbodiedWorldBench. EmbodiedWorldBench evaluates embodied agents on compound tasks that span indoor and outdoor spaces and require tightly coupled navigation, NPC interaction, and environment perception across diverse scenes. The benchmark covers 16 scenes across four difficulty levels with over 200 tasks, revealing the challenges of achieving cross-scene generalization and adaptive replanning under dynamic events.

这张图（图5）是论文《ABot-AgentOS: A General Robotic Agent OS with Lifelong Multi-modal Memory》中用于展示 EmbodiedWorldBench 基准测试的概述图。它清晰地说明了一个典型的复合任务是如何在 EmbodiedWorldBench 中被定义和执行的，从而揭示了该方法（即通过 EmbodiedWorldBench 评估的代理）的具体运作方式。

首先，我们来看图的结构。这张图主要分为两个部分：下半部分是一个具体的场景示例（俯视图），上半部分是与该场景相关的四个任务步骤的特写。数据或信息的流动顺序遵循任务执行的逻辑顺序，从任务开始到任务结束。

在场景示例的俯视图中，我们可以看到一个住宅区的布局，包括几栋房子（如“Lily's House”和“Sam's House”）、街道、游泳池和车库。这个场景代表了 EmbodiedWorldBench 中的一个典型任务环境。图中标注了“START”点，表示代理的起始位置。

任务的执行流程通过四个编号的步骤来展示：

1.  **步骤1：Check Street（检查街道）** - 这个步骤的特写图显示了一条街道的景象。根据任务描述框中的文字：“Check if Tom is on the street.”（检查Tom是否在街上），这个步骤要求代理首先在街道上寻找一个名为Tom的NPC。箭头从“START”指向这个步骤的特写，表明这是任务的第一个行动。

2.  **步骤2：Inspect Pool（检查泳池）** - 如果在街上没有找到Tom（根据任务描述中的“If not”），代理需要执行此步骤。特写图显示了一个带有遮阳棚的游泳池。任务描述指出：“go to Lily's pool to see if everything is normal”（去Lily的泳池看看一切是否正常）。箭头从步骤1指向步骤2，表明这是一个条件分支后的行动。

3.  **步骤3：Verify Living TV（验证客厅电视）** - 如果泳池一切正常，代理需要执行此步骤。特写图显示了一个客厅内部的景象，其中有一台电视。任务描述指出：“then check if her TV is on”（然后检查她的电视是否开着）。箭头从步骤2指向步骤3，表明这是另一个条件分支后的行动。

4.  **步骤4：Return & Report（返回并报告）** - 完成所有检查后，代理需要返回。特写图显示了代理回到车库门前（或附近）的场景，可能是在向任务发布者报告结果。任务描述的最后部分指出：“and finally return to the garage door and report to me.”（最后回到车库门并向我报告）。箭头从步骤3指向步骤4，表明这是任务的最终阶段。

图中的箭头和任务描述框清晰地展示了任务的逻辑流程：代理首先检查街道上的Tom，如果找不到，则检查Lily的泳池，然后检查Lily家的电视，最后返回并报告。这个流程揭示了 EmbodiedWorldBench 如何评估代理在需要紧密耦合的导航、NPC互动和环境感知的复合任务中的表现。代理需要根据环境中的信息（如NPC的位置或物体的状态）进行自适应规划和决策。

此外，图的原始caption提到，EmbodiedWorldBench 评估的是在室内和室外空间中跨越的复合任务，这些任务需要紧密耦合的导航、NPC互动和环境感知，并且覆盖了16个场景、四个难度级别和超过200个任务，揭示了实现跨场景泛化和在动态事件下自适应重新规划的挑战。这张图通过一个具体的例子，生动地展示了这些挑战中的一个典型任务是如何构建的：它涉及多个地点的导航、与NPC相关的条件检查以及最终的报告。

总结来说，这张图通过一个具体的任务示例，详细说明了 EmbodiedWorldBench 如何设计复合任务来评估机器人代理的能力。任务的执行顺序是：首先在街道上寻找Tom，如果未找到则检查Lily的泳池，然后检查Lily家的电视，最后返回车库并报告结果。这展示了代理需要进行导航、条件判断、环境感知和交互的能力。

---

![Figure 6 : Overview of the training pipeline for a deployable ABot-AgentOS stude](fig6_1.webp)

> Figure 6 : Overview of the training pipeline for a deployable ABot-AgentOS student policy. The pipeline constructs controllable text-based environments, distills teacher trajectories for SFT initialization, and improves the policy through online RL with LLM-as-a-Judge rewards and GiGPO advantages.

这张图展示了可部署的ABot - AgentOS学生策略的训练管道，我们可以从三个主要部分来理解它的工作流程：

首先是(a)轨迹生成引擎部分：
- **EnvBuilder**：它是环境的构建器，有三个关键功能。“Difficulty Expansion”（难度扩展）可以将环境难度设置为简单、中等或困难；“Scenario Construction”（场景构建）涉及环境状态（env_state）、触发器（Triggers）和人物（Persona）的设置；“Executable Feedback”（可执行反馈）则是将工具调用（Tool - call）转换为观测（Obs）。这里还有一个指令示例：“Find Sam, and ask him to come over for dinner.”（找到山姆，请他过来吃晚饭）。在这个模块中，有一个“init”（初始化）步骤，然后环境中存在“blocked”（阻塞）的情况，比如Calvin的家到Sam的家的路径被阻挡，还有人物可以移除障碍物。
- **Text - based sandbox（基于文本的沙箱）**：包含“EnvController”（环境控制器）和“Agent”（智能体）以及“HumanAgent”（人类智能体）。“EnvController”有工具检查（如导航到Sam的家）、状态更新（如道路阻塞）和移除触发器等功能。“Agent”会进行工具调用（如nav）、当遇到失败（如道路阻塞）时请求帮助（speak:request），然后“HumanAgent”会根据人物设定接受请求并执行物理动作（如clear obstacle），之后将观测（obs）反馈给“Agent”。同时，“LLM - as - Judge Filter”（以大型语言模型为裁判的过滤器）会对教师轨迹进行评分，筛选出有用的轨迹用于后续步骤，“Retained Trajectories”（保留的轨迹）用于SFT（监督微调）初始化，而被拒绝的无用轨迹则被丢弃。

然后是(b)强化学习部分：
- **GiGPO**：它处理优势（advantage）计算，包括“Episode advantage”（回合优势）和“Step advantage”（步骤优势）。回合优势中考虑了“same scenario”（相同场景）等因素，步骤优势中涉及“anchor state”（锚定状态）等，最终得到动作的优势（如\(a^E\)和\(a^S\)）。
- **LLM - as - judge**：负责奖励计算，分为“Turn - level reward”（回合级奖励）和“Episode - level reward”（回合级奖励？不，是剧集级奖励）。回合级奖励涉及导航、操作、VOA（可能是视觉目标识别等）以及技能感知的路由；剧集级奖励考虑效率、一致性、完整性等因素。
- **Self - evolution（自我进化）**：包含“Cluster”（聚类）、“Analyzer”（分析器）、“Refiner”（优化器）和“Validator”（验证器），用于处理自我评估相关的操作，从轨迹中提取信息并优化。
- **Meta - judge（元裁判）**：进行5维度的验证，包括准确性、逻辑连贯性、清晰度、反馈价值和任务完成情况，将轨迹分为“Bad cases”（坏案例）和“Good cases”（好案例），并将这些反馈用于策略的改进。

最后是(c)轨迹示例部分：
- 这里展示了一个具体的任务执行轨迹，指令同样是“Find Sam, and ask him to come over for dinner.”。轨迹中的步骤包括：导航到Sam的家（nav('Sam's home')）、说话（speak('Can you help?')）、导航到棋盘俱乐部（nav('chess club')）、说话（speak(invitation)），并在每个步骤中标注了成功或失败的情况，比如“blocked road”（道路阻塞）被标记为失败，“obstacle remove”（障碍物移除）被标记为成功，“Sam found”（找到山姆）和“task completed”（任务完成）也被标记为成功。这个示例展示了整个策略在执行任务时的具体行为和结果。

整体来看，这个训练管道的流程是：首先通过EnvBuilder构建可控的基于文本的环境，在这个环境中生成轨迹，然后通过LLM - as - Judge Filter筛选出有用的轨迹用于SFT初始化；接着进入强化学习阶段，GiGPO计算优势，LLM - as - judge提供奖励，Self - evolution和Meta - judge对策略进行优化，不断迭代以提高策略的性能，最终得到一个能够在复杂场景中完成任务的学生策略。这个管道的关键在于结合了环境构建、监督微调、强化学习以及基于大型语言模型的裁判机制，来实现ABot - AgentOS学生策略的训练和优化，使其能够处理长 horizon（长时程）的具身智能任务，如导航、物体搜索、NPC对话等。

---

![Figure 7 : Lifelong memory self-evolution across sequential splits. Each split u](fig7_1.webp)

> Figure 7 : Lifelong memory self-evolution across sequential splits. Each split uses only evo-assets promoted from previous splits; failures from the current split are diagnosed and gated after evaluation, and accepted assets are used only by later splits.

这张图展示了ABot - AgentOS中终身多模态记忆的自我进化过程，按顺序分为多个“Split”（分割/阶段），从Split 1到Split n依次推进，数据或信息的流动以及方法运作方式如下：

### 组件与信息流动
1. **Split阶段（Split 1、Split 2、Split n）**：
    - 每个Split代表一个任务或场景的阶段，上方的小图片（如Split 1中的乐器、人物、花朵、鸟类等；Split 2中的数学、物理相关图片；Split n中的天文、自然现象等）表示该阶段的任务场景或输入数据类型。这些场景是后续处理的基础，每个Split会生成对应的“evo - assets”（进化资产，可理解为从任务中提取的有用信息或模型更新内容）。
    - 每个Split下方有“Self - Evo Subagents”（自我进化子代理），这些子代理负责处理当前Split的任务，同时与下方的“Evo”模块（如Evo 1、Evo 2、Evo n）交互。
2. **Evo模块（Evo 1、Evo 2、Evo n）**：
    - Evo模块是进化资产的管理和存储单元。Evo 1接收来自Split 1的“Self - Evo Subagents”的信息，经过处理后，将“evo state carried forward”（进化的状态被传递）到下一个Evo模块（Evo 2）。这里的“evo state”可以理解为从当前任务中学习到的知识、模型参数或任务执行的经验等。
    - 当处理到Split 2时，“Self - Evo Subagents”不仅处理当前Split的任务，还会接收来自Evo 1传递过来的进化状态（通过虚线箭头“evo state carried forward”），这样可以利用之前任务的经验来提升当前任务的处理能力。处理完Split 2后，生成的进化资产会被“accumulated evo state”（累积的进化状态）管理，并传递给下一个Evo模块（Evo n）。
    - 对于每个Split中的“Self - Evo Subagents”，它们会诊断当前Split中的失败情况（图中未明确画出失败诊断的具体过程，但根据caption可知），然后将诊断后的“gated runtime evo - assets”（门控运行时进化资产）进行处理：如果资产被接受，就会被用于后续的Split（如Split 2的资产用于Split n）；如果失败，则不会泄漏到当前的ground - truth（真实标签或任务评估标准）中，防止影响当前任务的评估。
3. **箭头与流程**：
    - 蓝色的实线箭头（从Split 1到Split 2，再到Split n）表示任务的顺序推进，即先处理Split 1的任务，再处理Split 2，最后处理Split n。
    - 橙色的虚线箭头（从Evo 1到Evo 2，再到Evo n，以及从“Self - Evo Subagents”到对应的Evo模块）表示进化状态的传递和反馈，即当前阶段的进化资产会被传递到下一个阶段，用于提升后续阶段的处理能力。
    - 虚线箭头（从“Self - Evo Subagents”到Evo模块）表示“Self - Evo Subagents”将处理后的信息（包括成功的经验和失败的教训）传递给Evo模块进行存储和管理。

### 方法运作方式
ABot - AgentOS通过以下步骤实现终身多模态记忆的自我进化：
1. **任务分割与处理**：将整个任务过程分为多个连续的Split（阶段），每个Split处理特定的任务场景或数据。在每个Split中，“Self - Evo Subagents”负责处理当前任务，同时利用之前Split传递过来的进化资产（通过Evo模块）来提升自身的处理能力。
2. **进化资产的生成与管理**：每个Split中的“Self - Evo Subagents”会生成进化资产（evo - assets），这些资产包含从当前任务中学习到的知识、模型更新或任务执行经验。然后，这些资产会被诊断，只有被接受的资产才会被传递到后续的Split（通过Evo模块的“evo state carried forward”和“accumulated evo state”机制），而被拒绝的资产（失败的）则不会影响当前任务的评估，防止了当前Split的ground - truth泄漏。
3. **持续改进**：通过将当前Split的成功进化资产传递到后续的Split，ABot - AgentOS能够实现持续改进，使得后续的任务处理能力不断提升，因为它可以利用之前任务的经验来优化当前和未来的任务执行。

### 结果相关（结合论文背景）
虽然这张图主要是展示方法的运作流程，但结合论文中的实验结果，在EmbodiedWorldBench的初始子集上，ABot - AgentOS在任务成功率和目标完成率上都优于单控制器基线。在记忆基准测试中，ABot - AgentOS Static在LoCoMo上得分为87.5，在OpenEQA EM - EQA上得分为59.9，在Mem - （论文中未完整显示，但可知有较好的表现）。这表明通过这种终身多模态记忆的自我进化方法，ABot - AgentOS能够有效提升机器人在长期任务中的表现。

总结来说，这张图清晰地展示了ABot - AgentOS中终身多模态记忆的自我进化过程：通过将任务分为多个Split，每个Split处理任务并生成进化资产，然后将成功的进化资产传递到后续Split，同时防止失败的资产泄漏到当前任务的评估中，从而实现持续的自我改进和任务处理能力的提升。

---

![Figure 8 : Self-evolution gains by benchmark and category. Bars show absolute sc](fig8_1.webp)

> Figure 8 : Self-evolution gains by benchmark and category. Bars show absolute score changes from Static to + Self-evo; hatched bars indicate the primary metric for each benchmark.

这张图（图8）的标题是“Self-evolution gains by benchmark and category”，即“按基准和类别划分的自我进化收益”。它清晰地展示了在不同基准测试（benchmark）和不同任务类别（category）下，引入“自我进化”（Self-evo）机制后，系统性能相对于“静态”（Static）版本的绝对提升。

首先，我们来看图的基本结构。横轴表示“Absolute gain Δ (+ Self-evo - Static)”，即绝对增益Δ，计算方式是“自我进化版本的性能减去静态版本的性能”。正值表示性能提升，负值表示性能下降。纵轴则列出了不同的基准测试及其下属的任务类别或具体指标。

每个基准测试（如LoCoMo, OpenEQA, Mem-Gallery, NExt-QA, EgoLife）都作为一个主要的分组。在每个分组下，有多个子条目，代表不同的任务类别或具体的评估指标。例如，在LoCoMo基准下，有Single-hop（单跳）、Temporal（时间）、Multi-hop（多跳）、Open-domain（开放域）、Adversarial（对抗）等类别，以及一个Overall（总体）指标。

图中的每个蓝色条形代表一个特定类别或指标的性能增益。条形的长度对应于增益的数值，数值标签直接标注在条形上。特别重要的是，图例指出“Hatched bars: primary metric”，即带有斜线填充的条形代表该基准测试的主要评估指标。例如，在LoCoMo基准下，Overall指标的条形是斜线填充的；在NExt-QA基准下，Acc@All指标的条形是斜线填充的。

现在，我们来分析这张图揭示的方法是如何运作的，以及它的结果：

1.  **方法运作机制的理解**：
    *   这张图展示的是“自我进化”机制带来的性能提升。根据论文摘要，ABot-AgentOS引入了一个“failure-driven self-evolution loop”（故障驱动的自我进化循环）。这个循环会将诊断出的“memory failures”（记忆故障）转化为“gated runtime evo-assets”（受控的运行时进化资产），并且这些资产只会在后续的评估阶段被启用。这样做的好处是“preventing current-split ground-truth leakage while enabling continual improvement”（防止当前评估集的真实标签泄露，同时实现持续改进）。
    *   因此，这张图通过比较“引入自我进化后的系统（+ Self-evo）”与“未引入自我进化的静态系统（Static）”之间的性能差异，来量化这种自我进化机制的有效性。每个条形代表一个特定任务或任务类别的性能提升量。

2.  **坐标与对比对象**：
    *   横轴（X轴）是“Absolute gain Δ”，范围从-2到6。这表示性能变化量。0点代表没有性能变化（即自我进化版本与静态版本性能相同）。
    *   对比对象是“Self-evo”版本和“Static”版本。每个条形都表示从“Static”到“+ Self-evo”的绝对增益。
    *   不同的基准测试（如LoCoMo, OpenEQA等）之间是相互独立的，用于评估系统在不同场景或任务类型下的表现。

3.  **结论与观察**：
    *   **总体趋势**：在大多数基准测试和任务类别中，引入自我进化机制后，系统性能都有显著的正向提升。这表明“自我进化”机制是有效的，能够帮助系统在长期任务中持续改进。
    *   **具体基准的性能提升**：
        *   **LoCoMo**：这是一个可能与语言或认知相关的基准。其主要的Overall指标提升了+1.2。各个类别如Temporal (+4.1)、Multi-hop (+1.9)、Open-domain (+2.1) 都有不错的提升，而Adversarial类别提升较小 (+1.0)，Single-hop (+1.9)。
        *   **OpenEQA**：这可能是一个开放环境问答基准。其Overall指标提升了+1.2。具体类别如HM3D (+1.3) 和 ScanNet (+1.1) 也有提升。
        *   **Mem-Gallery**：这可能是一个与记忆画廊或检索相关的基准。其主要的Overall指标提升了+0.4。虽然有些类别如TR (-1.5) 和 FR (-0.7) 表现不佳，但KR类别有非常大的提升 (+6.2)，MR (+1.5) 和 CD (+1.1) 也有积极表现。
        *   **NExt-QA**：这可能是一个下一事件预测或问答基准。其主要的Overall指标（Acc@All）提升了+4.1，这是一个非常显著的提升。其他指标如Acc@C (+4.5)、Acc@D (+3.4) 和 Acc@T (+1.6) 也都表现良好。
        *   **EgoLife**：这可能是一个与自我生活经验或日常活动相关的基准。其主要的Overall指标（Avg.）提升了+0.8。具体类别如TM (+2.0)、HI (+1.2) 和 ER (+0.8) 都有提升，而EL (-0.2) 略有下降。

总结来说，这张图通过直观的条形图展示了ABot-AgentOS中的自我进化机制在多个基准测试和任务类别上带来的显著性能提升。它证明了该方法能够有效地通过持续学习和改进来增强机器人的代理能力，特别是在处理复杂、长期和多模态的任务时。每个条形代表一个特定评估点的改进量，斜线填充的条形则突出了每个基准的核心性能指标。

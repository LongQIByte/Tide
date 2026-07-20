# SearchOS-V1: Towards Robust Open-Domain Information-Seeking Agent Collaboration

[arXiv](https://arxiv.org/abs/2607.15257) · [HuggingFace](https://huggingface.co/papers/2607.15257) · ▲60

## 摘要（原文）

> Recent advances in Tool-Integrated Large Language Models have made web search a core capability of information-seeking agents. However, as interaction histories grow, agents increasingly struggle to track task progress. When search attempts fail to yield useful evidence, current single- and multi-agent systems can become trapped in repetitive loops, wasting search budgets and ultimately compromising the quality and completeness of the final output. We introduce SearchOS, a system-level multi-agent framework that turns fragile, implicit search progress into explicit, persistent, and shared state. First, we formulate open-domain information seeking as relational schema completion with grounded citations, where agents discover entities, populate attributes across linked tables, and anchor each value to source evidence. Then we design Search-Oriented Context Management (SOCM), which externalizes the evolving state into Frontier Task, an Evidence Graph, a Coverage Map, and Failure Memory. Built on SOCM, SearchOS applies a pipeline-parallel scheduling mechanism that overlaps the execution of sub-agents and continuously refills freed slots with tasks targeting unresolved coverage gaps to improve utilization and throughput. To schedule and control the execution of search agents, SearchOS introduces a Search Tool Middleware Harness that intercepts model and tool interactions to record grounded evidence and react to stalls or budget exhaustion, and provides a reusable hierarchical skill system comprising strategy and access skills to augment the agents' search process and avoid repeating failed search patterns across runs. On WideSearch and GISA, SearchOS leads all metrics among the evaluated single- and multi-agent baselines, paving the way toward robust information-seeking collaboration.

## 摘要（中译）

最近，工具集成大型语言模型（Tool-Integrated Large Language Models）的进步使网络搜索成为信息寻求代理（information-seeking agents）的核心能力。然而，随着交互历史的增长，代理越来越难以跟踪任务进度。当搜索尝试未能产生有用的证据时，当前的单代理和多代理系统可能会陷入重复循环，浪费搜索预算，并最终损害最终输出的质量和完整性。我们引入了SearchOS，这是一个系统级多代理框架，它将脆弱的、隐式的搜索进度转变为明确的、持久的和共享的状态。首先，我们将开放域信息寻求（open-domain information seeking）表述为具有基于证据的引用的关系模式完成（relational schema completion），其中代理发现实体，填充链接表中的属性，并将每个值锚定到源证据。然后我们设计了面向搜索的上下文管理（Search-Oriented Context Management，SOCM），它将不断发展的状态外部化为前沿任务（Frontier Task）、证据图（Evidence Graph）、覆盖图（Coverage Map）和失败记忆（Failure Memory）。基于SOCM，SearchOS应用了管道并行调度机制，该机制重叠子代理的执行，并不断用针对未解决覆盖缺口的任务填充空闲插槽，以提高利用率和吞吐量。为了调度和控制搜索代理的执行，SearchOS引入了一个搜索工具中间件框架（Search Tool Middleware Harness），该框架拦截模型和工具交互以记录基于证据的引用，并对停滞或预算耗尽做出反应，并提供一个可重用的分层技能系统，包括策略和访问技能，以增强代理的搜索过程并避免在运行中重复失败的搜索模式。在WideSearch和GISA上，SearchOS在所有评估的单代理和多代理基线中引领了所有指标，为稳健的信息寻求协作铺平了道路。

## 背景剖析

### 背景剖析  

**技术背景**：随着工具集成大模型（LLM）的发展，信息检索代理已能通过网页搜索、浏览和推理来扩展知识边界，解决开放域的长任务（如结构化问答或事实核查）。这类技术广泛应用于需要整合多源信息的场景，例如学术研究、商业分析或智能助手。核心需求是让代理能可靠地跟踪任务进度、避免重复劳动，并生成可验证的答案。  

**之前的问题**：现有方法在处理复杂任务时面临两大挑战。首先，随着交互历史增长，代理难以跟踪已完成和待完成的部分，导致证据丢失、冗余收集或矛盾结论。例如，当搜索无果时，单一代理可能陷入重复无效搜索的循环，浪费资源。其次，简单增加代理数量并不能解决问题——并行工作可能导致重复劳动、意见分歧或资源闲置。根本原因在于传统方法将计划、进度和失败视为临时对话内容，而非系统级状态，导致长期任务缺乏可持续性和可追溯性。  

**本文的解法**：论文提出SearchOS框架，通过以下思路解决这些问题：  
1. **关系型搜索建模**：将开放域信息检索转化为“关系模式补全”任务，明确实体、属性和证据的关联，使进度可衡量。  
2. **显式状态管理**：引入“搜索导向上下文管理（SOCM）”，将执行状态（如未完成任务、证据图、覆盖地图）外部化，供所有代理共享。  
3. **流水线并行调度**：采用类似GPU训练的流水线机制，动态分配未完成的任务，提高资源利用率。  
4. **中间件控制**：通过“搜索工具中间件”监控和管理代理行为，避免重复错误并强制执行预算。  
5. **分层技能系统**：分离通用搜索策略和特定网站访问技能，提升跨任务的复用性。  

**切入角度**：与先前工作相比，SearchOS的关键差异在于：  
- **从隐式到显式状态**：将任务进度从对话历史中提取为系统级状态，避免依赖代理记忆。  
- **从单代理到多代理协作**：通过共享状态和动态调度实现高效协作，而非简单并行。  
- **从任务特定到可复用技能**：设计分层技能系统，支持跨场景复用，而非为每个任务重新学习。  

这些创新使SearchOS在实验中显著优于现有基线，为构建鲁棒的信息检索协作系统奠定了基础。

## 方法图解

![Figure 1 : SearchOS interface for a long-horizon information-seeking task. The w](fig1_1.webp)

> Figure 1 : SearchOS interface for a long-horizon information-seeking task. The workspace exposes the orchestration trace, pipeline parallel agent activity, and relational schema coverage.

这张图展示了SearchOS系统在处理一个长周期信息检索任务时的用户界面，清晰地呈现了系统的核心组件和工作流程。我们可以从三个主要区域来理解这张图：

首先，左侧是任务管理和项目导航区。这里列出了“所有研究”、“需要审核”、“收藏夹”等分类，以及具体的任务条目，如“我想去北京旅游，帮我梳理...”。这表明用户可以同时管理多个任务，并且当前选中的是这个北京旅游规划任务。下方还有按时间分类的任务列表，显示了任务的完成状态和更新时间。

中间区域是任务执行的核心视图，即“编排追踪”（Orchestration trace）。这个区域详细记录了任务执行的步骤和状态：
1.  顶部显示了任务的总览，包括使用了21个代理（agents）、346个步骤（steps），以及当前覆盖了189/189个单元格（cells），表明任务已全部完成。
2.  下方是具体的执行日志，按时间顺序展示了任务的进展：
    *   系统首先理解了用户的需求：“我来帮您规划北京五天四晚的旅行...”。
    *   然后，系统“探索任务已启动”，并“分派了1个代理”去执行“探索北京主要旅游景点”的子任务。
    *   接着，系统会“检查子代理的状态”，确认任务是否完成。
    *   当探索完成后，系统会总结已收集到的信息，例如“北京主要景点集中在东城、西城、海淀、朝阳、延庆等区”。
    *   随后，系统会“构建覆盖模式”（Built coverage schema），创建关系模式（如attractions、hotels、itinerary表），并为未解决的覆盖缺口分配新的任务。
    *   用户还可以在中间的对话框中与系统交互，例如补充需求“还有主题乐园的也帮我收集下”。

右侧区域分为上下两部分：
*   上半部分是“活动”（Activity）面板，显示了各个代理（Agent）的活动状态。每个代理卡片显示了其完成状态（如“Completed”）、执行的具体任务（如“搜索北京环球影城周边的五星级酒店”）、执行的步骤数以及一个“trace”链接以查看详细信息。这展示了系统如何并行调度多个代理来完成不同的子任务。
*   下半部分是“覆盖范围”（Coverage）面板，显示了关系模式的完成情况。以“北京主要景点”为例，它显示了覆盖率为91/91（100%），并列出了具体的景点、行政区和地址信息。这对应了论文中提到的“关系模式完成”（relational schema completion），表明系统成功地收集并组织了关于北京景点的信息。

这张图揭示了SearchOS的工作原理：
1.  **任务分解与调度**：系统将用户的长周期任务分解为多个子任务，并通过“管道并行调度机制”（pipeline-parallel scheduling mechanism）并行执行这些子任务。中间的“编排追踪”记录了这些子任务的执行顺序和状态。
2.  **状态显式化**：系统通过“前沿任务”（Frontier Task）、“证据图”（Evidence Graph）、“覆盖图”（Coverage Map）和“失败记忆”（Failure Memory）将搜索进度外部化。右侧的“活动”面板展示了代理的活动状态，而“覆盖范围”面板则展示了关系模式的完成情况。
3.  **信息收集与组织**：系统通过代理执行具体的搜索任务（如搜索景点、酒店），并将收集到的信息组织到预定义的关系模式中。右侧的“覆盖范围”面板中的表格就是这种组织方式的体现。
4.  **持续填充与优化**：当某些子任务完成并释放资源后，系统会持续填充未解决的覆盖缺口，以提高资源利用率和吞吐量。

总而言之，这张图展示了一个复杂的、多代理协作的信息检索系统如何通过显式化管理任务状态和进度，高效地完成一个长周期的开放域信息寻求任务。系统的各个组件协同工作，确保任务的每一步都得到跟踪和管理，最终成功构建出完整的关系模式。

---

![Figure 2 : SearchOS architecture.](fig2_1.webp)

> Figure 2 : SearchOS architecture.

这张图展示了SearchOS（SearchOS-V1）的架构，它是一个用于开放域信息寻求的多智能体协作系统。我们可以从几个主要部分来理解这个架构的工作流程和方法逻辑：

首先，最上方的“User Question”模块代表了用户的多类型信息查询任务，包括单事实查询、枚举、比较分析和开放域调查，最终目标是完成关系模式（Relational Schema）的填充。这些用户问题会进入中间的“Search Agents Collaboration Orchestrator”（搜索智能体协作协调器）模块。

在这个协调器中，首先会“Create Schema”（创建模式）、“Decompose tasks”（分解任务）和“Schedule Agents”（调度智能体）。然后，三种主要的智能体开始工作：
- “Explore Agent”（探索智能体）负责探索目标信息分布并构建任务先验知识；
- “Search Agent”（搜索智能体）执行并行子任务执行和中间任务总结；
- “Writer Agent”（写作智能体）读取累积的证据并起草结构化报告。
这些智能体的工作流程是协作的，探索智能体提供方向，搜索智能体执行具体搜索，写作智能体整合结果。

接下来，“Final Output”模块将合成发现并生成报告，包括答案/结果、引用/来源和提取的数据，最终生成有引文支撑的报告。

在协调器的下方是“Search Tool Middleware Harness”（搜索工具中间件套件），它包括三个中间件：
- “Context Middleware”（上下文中间件）管理搜索智能体的上下文，注册和管理预LLM调用包装器；
- “Sensor Middleware”（传感器中间件）监控进度并进行行为干预，是后工具调用包装器；
- “Evidence Extraction Middleware”（证据提取中间件）处理中间搜索和证据提取，也是后工具调用包装器。
这些中间件的作用是拦截模型和工具的交互，记录有根据的证据，并对停滞或预算耗尽做出反应。

再往下是“Search-Oriented Context Management”（面向搜索的上下文管理）模块，它包含四个部分：
- “Frontier Tasks”（前沿任务）是一个优先级调度的任务DAG（有向无环图），显示任务的并行、完成、运行和待处理状态；
- “Evidence Graph”（证据图）是一个模式绑定的证据图，包含来源、内容、质量和模式绑定，支持/部分支持/冲突的关系；
- “Coverage Map”（覆盖图）显示多模式填充状态，包括实体和属性的填充/不确定/缺失状态；
- “Failure Memory”（失败记忆）从失败中学习，改进未来的决策，记录无用查询、不可访问的网站和不可用的技能。

最右侧的“Toolset”（工具集）和“Search Agent Skills”（搜索智能体技能）模块提供了支持的工具和技能：
- “Schema Tools”（模式工具）可以创建、删除、更新和读取模式；
- “Schedule Tools”（调度工具）可以创建任务和检查智能体；
- “Simple Browser Tools”（简单浏览器工具）用于搜索、打开和查找；
- “Search Agent Skills”（搜索智能体技能）包括技能库、技能构建器和注册表/路由器，用于执行不同的技能。

数据或信息的流动顺序大致是：用户问题→协调器（创建模式、分解任务、调度智能体）→各智能体工作（探索、搜索、写作）→中间件处理（上下文、传感器、证据提取）→上下文管理（前沿任务、证据图、覆盖图、失败记忆）→最终输出报告。同时，工具集和技能模块为整个过程提供支持和工具。

这张图揭示了SearchOS的具体工作方式：它将脆弱、隐式的搜索进度转化为显式、持久和共享的状态，通过关系模式完成和有根据的引用来处理开放域信息寻求。它使用管道并行调度机制重叠子智能体的执行，并不断用针对未解决覆盖差距的任务填充空闲槽位，以提高利用率和吞吐量。搜索工具中间件套件拦截模型和工具的交互，记录有根据的证据，并对停滞或预算耗尽做出反应。面向搜索的上下文管理模块外部化了演进的状态，包括前沿任务、证据图、覆盖图和失败记忆，以跟踪任务进度和处理失败。

总之，SearchOS通过多智能体协作、显式状态管理和工具中间件，解决了当前单智能体和多智能体系统在搜索失败时陷入重复循环的问题，提高了信息寻求的质量和完整性。

---

![Figure 3 : Illustration of middleware interventions in the Search Agent loop.](fig3_1.webp)

> Figure 3 : Illustration of middleware interventions in the Search Agent loop.

这张图展示了搜索代理推理循环（Search Agent Reasoning Loop）与搜索工具中间件框架（Search Tool Middleware Harness）之间的交互流程，清晰地呈现了信息如何在各个组件之间流动以及中间件如何干预代理的决策过程。

首先，我们来看上方的“搜索代理推理循环”部分。这个循环由四个主要步骤组成，按顺序执行：

1. **Context Prepared（上下文准备）**：这一步接收任务和相关状态（task + relevant state），为后续的推理做准备。信息从这里开始流动，进入下一个组件。

2. **LLM Reasoning（大语言模型推理）**：在这个步骤中，大语言模型（LLM）根据准备好的上下文选择下一个动作（choose the next action）。这是代理做出决策的关键步骤。

3. **Tool Call（工具调用）**：根据LLM的决策，代理执行具体的工具调用，如搜索（search）、打开（open）或查找（find）。这一步是代理与外部工具交互的部分。

4. **Observation（观察）**：工具调用后，代理会收到页面（page）、结果（result）或证据（evidence）作为反馈。这些观察结果会被用于后续的决策。

接下来，我们看下方的“搜索工具中间件框架”部分，它包含三个关键组件，用于拦截和干预代理与工具的交互：

1. **Context（上下文）**：这个组件负责投影SOCCM状态（project SOCCM state）、检索技能和修剪历史（retrieve skills and trim history），并在每次模型调用前注入上下文（inject before each model call）。它的作用是确保代理在每次决策时都有最新的上下文信息。

2. **Evidence Extraction（证据提取）**：这个组件负责绑定和锚定证据（bind and anchor evidence）、更新证据图和覆盖范围（update Evidence Graph and Coverage），并为每次浏览器交互提供基础（ground every browser interaction）。它的作用是确保代理能够准确地跟踪和使用证据。

3. **Sensor（传感器）**：这个组件负责检测重复（detect repetition）、停滞（stalls）、低收益（low yield），并选择枢轴引导或硬停止（select pivot guidance or hard stop），仅在需要时进行干预（intervene only when needed）。它的作用是防止代理陷入无效的循环。

现在，我们来看信息在这些组件之间的流动和干预机制：

- 从“Context Prepared”到“LLM Reasoning”的箭头表示上下文信息的流动。
- 从“LLM Reasoning”到“Tool Call”的箭头表示决策信息的流动。
- 从“Tool Call”到“Observation”的箭头表示工具调用结果的流动。
- 从“Observation”到“LLM Reasoning”的虚线箭头表示观察结果的反馈，用于调整后续的决策。
- 中间件的干预通过虚线箭头表示，例如从“Context”到“LLM Reasoning”的虚线箭头表示上下文的注入，从“Evidence Extraction”到“LLM Reasoning”的虚线箭头表示证据的注入，从“Sensor”到“LLM Reasoning”的虚线箭头表示传感器的干预。

这张图揭示了SearchOS系统如何通过中间件框架来增强搜索代理的能力。具体来说，中间件通过拦截模型和工具的交互，记录锚定的证据，并对停滞或预算耗尽的情况做出反应，从而帮助代理避免陷入重复的循环，提高搜索的效率和效果。通过这种方式，SearchOS将脆弱的、隐式的搜索进度转化为明确的、持久的和共享的状态，从而提高了信息寻求代理的性能。

---

![(a) Frequent skill keywords. (b) Access-skill counts and functions. Figure 4 : P](fig4_1.webp)

> (a) Frequent skill keywords. (b) Access-skill counts and functions. Figure 4 : Pre-built skills: (a) weighted keyword frequency; (b) access-skill counts and mean functions by domain.

这张图（图4a）展示了预构建技能的关键词频率分布，以词云的形式呈现。词云中的每个单词代表一个与信息搜索相关的“技能”或功能，单词的大小反映了该技能在研究中被提及或使用的频率——字体越大，表示该技能出现的频率越高。

从词云中我们可以直观地看到，一些核心技能包括“query”（查询）、“entity”（实体）、“academic paper”（学术论文）、“data”（数据）、“web”（网络）、“search”（搜索）、“verification”（验证）、“evidence”（证据）和“news”（新闻）。这些关键词揭示了该方法主要关注如何通过各种技能来获取、验证和整合信息。例如，“entity”和“query”表明系统需要识别和查询特定实体；“academic paper”和“news”指出了信息来源的类型；而“verification”和“evidence”则强调了信息的可靠性和可追溯性。

这张图揭示了该方法的具体运作方式：它是一个多技能协作的框架。系统通过调用这些预构建的技能来完成开放域信息搜索任务。例如，当需要查找某个实体的信息时，系统可能会先使用“query”技能发起搜索，然后利用“entity”技能来识别和提取相关信息，再通过“verification”技能来验证信息的准确性，并可能使用“academic paper”或“news”技能来从特定来源获取更详细的数据。词云中的关键词频率分布表明，该方法特别强调实体识别、查询、证据验证和多源信息整合。

总而言之，这张词云图清晰地展示了该方法所依赖的核心技能集合，以及这些技能在信息搜索过程中的相对重要性。它表明该方法是一个高度模块化和技能驱动的系统，通过组合和协调不同的技能来解决复杂的开放域信息寻求任务。

---

![(a) Frequent skill keywords. (b) Access-skill counts and functions. Figure 4 : P](fig4_2.webp)

> (a) Frequent skill keywords. (b) Access-skill counts and functions. Figure 4 : Pre-built skills: (a) weighted keyword frequency; (b) access-skill counts and mean functions by domain.

这张图（图4b）展示了预构建技能的“访问技能计数”和“各技能的功能数量”，帮助我们理解不同领域中技能的使用情况和功能复杂度。

首先，我们来看图的左侧部分，标题为“Access skills”。这部分通过水平条形图展示了不同领域（如commercial、government、organization等）的技能访问次数。每个条形的长度代表了该领域的技能被访问的总次数，旁边的数字是具体的计数值。例如，“commercial”领域的技能被访问了138次，是所有领域中最多的；而“generic/API”领域的技能只被访问了7次，是最少的。这表明在预构建的技能中，商业领域的技能使用频率最高，而通用或API相关的技能使用最少。

接下来，我们看图的右侧部分，标题为“Functions per skill”。这部分同样使用水平条形图，但展示的是每个技能平均包含的功能数量。每个条形的长度代表了该领域技能的平均功能数，旁边的数字是具体的平均值。例如，“government”领域的技能平均包含4.5个功能，是所有领域中功能最丰富的；而“generic/API”领域的技能平均只有1.0个功能，功能最少。这说明政府领域的技能设计得更为复杂，包含更多的功能，而通用或API相关的技能功能较为单一。

通过对比左右两部分的数据，我们可以发现一些有趣的模式。例如，“commercial”领域虽然技能访问次数最多，但其平均功能数（3.7）却低于“government”和“organization”等领域。这可能意味着商业领域的技能更专注于特定的任务，而政府领域的技能则更全面，能够处理更多样化的需求。

此外，图中还列出了其他几个领域，如“organization”、“other domains”、“education”等，它们的技能访问次数和平均功能数介于上述两个极端之间。这些数据为我们提供了对预构建技能在不同领域中的使用情况和功能复杂度的全面了解。

总的来说，这张图揭示了预构建技能在不同领域中的分布情况，以及各领域技能的功能复杂度。通过分析这些数据，我们可以更好地理解如何设计和优化技能，以满足不同领域的信息寻求需求。

---

![Figure 5 : Middleware-governance trajectories on WideSearch.](fig5_1.webp)

> Figure 5 : Middleware-governance trajectories on WideSearch.

这张图（图5）展示了在WideSearch环境下，由中间件治理的搜索轨迹，重点比较了**早期干预**、**中期运行干预**和**晚期干预**三种不同阶段下，搜索代理的行为模式和任务完成情况。

我们可以将图分为上下两部分，上半部分（蓝色曲线）表示“Coverage”（覆盖率），即已探索或完成的任务比例，随“Cumulative tool calls”（累计工具调用次数）的变化；下半部分（橙色曲线）表示“Total entities”（实体总数），即在搜索过程中发现或处理的总实体数量，同样随累计工具调用次数的变化。每条曲线代表一个独立的实验案例，分别标记为(a) 早期干预（ws_zh_034）、(b) 中期运行干预（ws_zh_044）和(c) 晚期干预（ws_en_015）。

**核心组件与信息流动：**

1.  **X轴（横轴）：** “Cumulative tool calls”（累计工具调用次数）。这代表了搜索代理在执行任务过程中调用外部工具（如搜索引擎）的总次数。随着工具调用次数的增加，代理在逐步推进任务。
2.  **Y轴（纵轴）：**
    *   上半部分：“Coverage”（覆盖率），以百分比表示。这衡量了任务完成的程度，例如发现了多少比例的目标实体或信息。从0%到100%。
    *   下半部分：“Total entities”（实体总数），以绝对数值表示。这显示了在搜索过程中识别出的实体数量。随着搜索的进行，这个数字会增加，直到达到一个稳定值，表明所有相关实体已被发现。
3.  **关键事件标记：**
    *   **“Loop detected”（检测到循环）：** 图中虚线标记了代理检测到自身行为陷入重复模式的时刻。这通常发生在代理多次尝试相似的搜索策略但未获得新信息时。
    *   **“Strategy switch”（策略切换）：** 在检测到循环后，代理会调整其搜索策略。这可能涉及改变搜索关键词、尝试不同的信息源或采用新的推理方法。
    *   **“Loop detected Strategy switch”（检测到循环并策略切换）：** 这个标记明确指出了循环检测和策略调整的发生点。

**方法运作机制的揭示：**

这张图直观地展示了SearchOS系统如何通过中间件治理来应对搜索过程中的挑战：

*   **早期干预（图a）：** 在这个案例中，“Loop detected”和“Strategy switch”发生在累计工具调用次数较少（约20次）的时候。随后，覆盖率迅速上升，最终达到100%，实体总数稳定在5。这表明早期识别并解决循环问题可以有效地引导搜索过程，快速完成任务。
*   **中期运行干预（图b）：** 在此案例中，循环检测和策略切换发生在约300次工具调用时。在此之前，覆盖率增长较为缓慢，甚至出现停滞。策略切换后，覆盖率继续上升，最终也达到100%，实体总数稳定在15。这说明即使在搜索过程中较晚发现循环，系统仍然有能力调整策略并完成任务，但可能需要更多的工具调用。
*   **晚期干预（图c）：** 这个案例显示，在约150次工具调用时检测到循环并进行策略切换。之后，覆盖率继续增长，最终达到100%，实体总数稳定在50。这个案例的实体总数较高，可能意味着任务本身更复杂或需要探索更多实体。

**结论：**

这张图揭示了SearchOS系统中中间件治理的有效性。通过在搜索过程中监控代理的行为（如工具调用模式），并及时检测和应对陷入循环的情况，系统能够：

1.  **避免资源浪费：** 通过识别无效的重复行为（循环），防止代理在无用的搜索上浪费工具调用预算。
2.  **提高任务完成率：** 通过策略切换，代理能够摆脱困境，继续探索并最终达到较高的覆盖率（完成任务）。
3.  **适应不同任务阶段：** 无论是在早期、中期还是晚期发现循环，系统都能够做出响应，尽管早期干预可能更高效。

总而言之，这张图通过展示不同干预时机下的搜索轨迹，证明了SearchOS系统能够有效地管理搜索过程，克服循环陷阱，从而提高信息寻求任务的效率和效果。图中看不清或不确定的地方按caption处理或跳过，绝不要输出犹豫、自问自答或自我纠正的过程。

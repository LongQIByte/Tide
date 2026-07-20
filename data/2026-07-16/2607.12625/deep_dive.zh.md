# KnowAct-GUIClaw: Know Deeply, Act Perfectly, Personal GUI Assistant with Self-Evolving Memory and Skill

[arXiv](https://arxiv.org/abs/2607.12625) · [HuggingFace](https://huggingface.co/papers/2607.12625) · ▲56

## 摘要（原文）

> OpenClaw has emerged as a leading agent framework for complex task automation, yet it faces insufficient cross-platform GUI interaction support and a well-built self-evolution mechanism. These flaws limit its adaptation to diverse device ecosystems and prevent performance improvements through continuous learning from execution experience. To resolve these issues, we propose the Know Deeply, Act Perfectly paradigm for personal assistants, which holds that accumulated user interaction and task-running experience directly improve execution accuracy and efficiency, unifying cognitive comprehension and operational execution. Based on this paradigm, we introduce KnowAct-GUIClaw, a novel Know-Route-Act-Reflect framework designed to address OpenClaw's GUI manipulation deficits and break through its cross-platform and recursive self-improvement constraints. First, the host agent leverages accumulated interaction experience and task-relevant knowledge for long-horizon task decomposition and allocation (Know). Second, a pluggable GUI subagent with an experience-attributable memory system (Know) and self-evolving skill library (Act), enabling seamless cross-platform migration and fast-path integration. Especially, this framework continuously stores user profiles and feedback to improve the accuracy of task decomposition and tool calls. Extensive experiments across Android, iOS, HarmonyOS and Windows show that KnowAct-GUIClaw achieves superior efficiency, accuracy and cross-platform adaptability. Especially, the GUIClaw with open-source Kimi-2.6 models achieves the best performance (64.1%) on the long-horizon MobileWorld benchmark, beating all agentical frameworks and closed-source agentical models, e.g., Seed-2.0-Pro and GPT-5.5. Additionally, the knowledgeable memory and execution skills supported by our framework are transferable across diverse base models, improving by 8.5% with Kimi-2.6.

## 摘要（中译）

OpenClaw 已经成为复杂任务自动化的领先智能体框架，但它面临着跨平台图形用户界面（GUI）交互支持不足以及完善的自我进化机制缺失的问题。这些缺陷限制了它对多样化设备生态系统的适应能力，并且阻碍了通过从执行经验中持续学习来提升性能。为了解决这些问题，我们针对个人助理提出了“深度认知，完美行动”（Know Deeply, Act Perfectly）范式，该范式认为积累的用户交互和任务执行经验直接提高执行准确性和效率，将认知理解和操作执行统一起来。基于这一范式，我们引入了 KnowAct - GUIClaw，这是一种新颖的“认知 - 规划 - 行动 - 反思”（Know - Route - Act - Reflect）框架，旨在解决 OpenClaw 的 GUI 操作缺陷，并突破其跨平台和递归自我改进的限制。首先，宿主智能体利用积累的交互经验和与任务相关的知识进行长周期任务分解和分配（认知（Know））。其次，一个具有可归因于经验的记忆系统（认知（Know））和自我进化的技能库（行动（Act））的可插拔 GUI 子智能体，能够实现无缝的跨平台迁移和快速路径集成。特别是，该框架持续存储用户配置文件和反馈，以提高任务分解和工具调用的准确性。在安卓（Android）、苹果操作系统（iOS）、鸿蒙操作系统（HarmonyOS）和Windows 上的大量实验表明，KnowAct - GUIClaw 实现了卓越的效率、准确性和跨平台适应性。特别是，使用开源的金米 - 2.6（Kimi - 2.6）模型的 GUIClaw 在长周期的移动世界（MobileWorld）基准测试中取得了最佳性能（64.1%），击败了所有的智能体框架和闭源智能体模型，例如种子 - 2.0 - 专业版（Seed - 2.0 - Pro）和GPT - 5.5。此外，我们的框架支持的知识型记忆和执行技能可以在不同的基础模型之间转移，使用金米 - 2.6（Kimi - 2.6）时性能提高了8.5%。

## 背景剖析

### 背景剖析  

**1. 技术背景与真实需求**  
随着大语言模型（LLM）代理从简单对话工具发展为长期运行的个人助手，用户对其能力的需求已超越文本交互，延伸至图形用户界面（GUI）操作。例如，助手需要帮助用户在手机应用间迁移数据、处理权限弹窗、或在登录环境中执行多步骤工作流。这类任务无法通过标准化的API完成，必须依赖对动态GUI的理解与交互。然而，现有GUI代理（如AppAgent、Mobile-Agent等）仅能处理单一模态的视觉输入（如屏幕截图），难以应对跨应用、跨设备的复杂场景，更无法从历史经验中学习以提升效率。  

**2. 先前方法的局限性**  
传统GUI代理存在四大缺陷：首先，高阶指令常涉及多个应用，但自由文本描述无法保留跨应用所需的中间数据，导致任务中断；其次，GUI观察数据（如截图、操作轨迹）是碎片化的，主机代理需额外记录历史信息以指导轻量级GUI执行器；第三，任务完成后轨迹数据被丢弃，重复执行时需重新学习已知模式；最后，大多数GUI工作流未整合非视觉快捷方式（如系统意图、深度链接），且这些快捷方式无法安全复用为长期技能。  

**3. 本文的解决方案**  
KnowAct-GUIClaw通过“知深行准”（Know Deeply, Act Perfectly）范式解决上述问题。其核心设计是将任务分解为“主机代理-GUI执行器”协作模式：主机负责高层决策（如任务分配、工具调用），GUI执行器专注于视觉交互（如截图解析、动作执行）。具体创新包括：  
- **分层协作机制**：主机与执行器通过标准化接口交互，支持任务恢复和进度跟踪，避免重复探索；  
- **知识驱动的路由与信息传递**：根据任务类型（单应用/跨应用）动态分配资源，并通过共享数据板传递结构化信息；  
- **技能库与自进化**：将成功轨迹提炼为可复用的参数化技能（如点击-输入模式或系统意图），并通过反思机制持续优化；  
- **跨平台适应性**：通过经验归因记忆和技能验证机制，支持Android、iOS等多设备部署。  

**4. 与前人工作的关键差异**  
与传统单一GUI代理不同，KnowAct-GUIClaw强调“认知-执行”协同：主机代理利用全局上下文（如用户画像、历史任务）进行决策，而GUI执行器仅处理视觉层面的细节。此外，它首次将技能库与记忆系统结合，使代理能够从经验中学习并迭代优化，而非每次任务都从头开始。实验表明，该方法在MobileWorld基准测试中超越现有框架（如Seed-2.0-Pro），并支持跨模型迁移（如Kimi-2.6），证明了其通用性和高效性。

## 方法图解

![Figure 1: The success rate (SR) comparison on MobileWorld GUI-Only tasks. The ba](fig1_1.webp)

> Figure 1: The success rate (SR) comparison on MobileWorld GUI-Only tasks. The bars summarize Table 1 together with the additional Kimi-based KnowAct-GUIClaw runs; gray bars denote specialized GUI models, colored external bars denote general model families, and highlighted bars denote KnowAct-GUIClaw variants with memory and skills. The experimental results show that KnowAct-GUIClaw achieves SOTA performance and that the memory and skill are effective for different base models.

这张图（图1）展示了不同模型在**MobileWorld GUI-Only任务**上的**成功率（Success Rate, SR）**对比，核心是验证`KnowAct-GUIClaw`（结合记忆和技能的变体）的性能优势及有效性。以下分组件、逻辑和结论详细讲解：  


### 1. 图的组件与信息流动  
- **横轴（X轴）**：不同的模型/方法，按“基础模型类型→KnowAct-GUIClaw变体”的逻辑排列。包括：  
  - 灰色条：**专用GUI模型**（如“UI-Venue-72B”“Doubao-1.5-UI-TARS”等），仅针对GUI任务优化，无通用能力或自进化机制。  
  - 彩色外部条：**通用模型家族**（如“Qwen”“Claude”“GPT”等系列），具备通用任务能力，但原始GUI交互或自进化能力不足。  
  - 高亮条（蓝色/青绿色等）：**KnowAct-GUIClaw变体**（带“memory + skills”），是论文提出的方法，结合“认知（Know）-行动（Act）-反思（Reflect）”框架，通过经验积累和技能进化提升性能。  

- **纵轴（Y轴）**：成功率（%），数值越高表示任务完成越好。  

- **箭头与增量标注**：紫色/青绿色虚线箭头连接不同模型，标注的“+X”表示**性能提升量**（后一个模型比前一个模型的成功率高出X%）。例如：  
  - 从“Qwen3.5-32B-A10B”（34.5%）到“KnowAct GUIClaw + memory + skills”（37.9%），提升+13.1%；  
  - 从“KnowAct GUIClaw + memory + skills”（46.2%）到后续模型，进一步提升（如+3.5%、+5.9%、+8.5%等），体现“记忆+技能”的持续优化效果。  


### 2. 方法的运作逻辑（从图中推导）  
论文提出的`KnowAct-GUIClaw`遵循“**Know Deeply, Act Perfectly**”范式，通过以下步骤解决OpenClaw的缺陷（跨平台GUI支持不足、自进化机制缺失）：  

- **Know（认知）阶段**：  
  主代理利用**累积的用户交互经验**和**任务相关知识**，进行**长 horizon 任务分解与分配**（即把复杂GUI任务拆分为可执行的子步骤，并分配给合适的子代理）。例如，图中“KnowAct GUIClaw + memory + skills”的基础是“经验积累+知识驱动的任务规划”。  

- **Act（行动）阶段**：  
  采用**可插拔的GUI子代理**，结合：  
  - **经验可追溯的记忆系统**：存储用户画像、反馈和执行经验，用于优化任务分解和工具调用（如图中灰色条的“GUI”模型无此记忆，而KnowAct-GUIClaw的高亮条有）；  
  - **自进化技能库**：支持跨平台迁移（Android/iOS/HarmonyOS/Windows）和快速路径集成（即快速适配新GUI场景）。  

- **Reflect（反思）阶段**（隐含在“持续学习”中）：  
  框架**持续存储用户反馈和执行经验**，不断改进任务分解的准确性和工具调用的效率（如图中“+X”的增量体现了反思后的性能提升）。  


### 3. 对比对象与结论  
- **对比对象**：  
  - 专用GUI模型（灰色条）：性能普遍较低（如“UI-Venue-72B”仅16.4%），因为缺乏通用能力或自进化机制。  
  - 通用模型家族（彩色外部条）：性能优于专用GUI模型，但原始版本（如“Qwen3.5-122B-A10B”34.5%、“GPT-3.5”54.0%）仍低于KnowAct-GUIClaw变体。  
  - KnowAct-GUIClaw变体（高亮条）：通过“记忆+技能”显著提升性能，最终达到**64.1%**（最高值），且中间增量（如+13.1%、+3.5%、+8.5%）证明“记忆+技能”的有效性。  

- **结论**：  
  `KnowAct-GUIClaw`在MobileWorld GUI-Only任务上达到**SOTA（最先进）性能**，且“记忆+技能”的设计对不同基础模型（如Qwen、Claude、Kimi等）都有效——即无论基础模型如何，加入“经验记忆+自进化技能”都能提升GUI任务的成功率。  


这张图通过“成功率对比+增量箭头”，直观展示了`KnowAct-GUIClaw`如何通过“认知-行动-反思”的闭环，结合记忆和技能，突破传统GUI模型的局限，实现跨平台和自进化的任务自动化。

---

![Figure 2: Overview of the KnowAct-GUIClaw execution loop . Two persistent stores](fig2_1.webp)

> Figure 2: Overview of the KnowAct-GUIClaw execution loop . Two persistent stores—a memory and history store and a skill and shortcut store—supply advisory context to every stage. Know gathers evidence and assembles a reasoning context; Route ranks app candidates and turns the request into either a single GUI task or an ordered multi-app workflow whose subtasks exchange typed values through a blackboard; Act runs GUIClaw’s observe–reason–act loop over the hybrid action space of GUI primitives, skills, deeplink/intent shortcuts, and intervention actions; and Reflect distills each trajectory into updated skills and experience memory that feed back into the stores.

这张图展示了KnowAct - GUIClaw的执行循环概述，我们可以从四个主要阶段（Know、Route、Act、Reflect）以及两个持久化存储（Memory & History Store和Skill & Shortcut Store）来理解其工作流程：

### 持久化存储（顶部两个模块）
- **Memory & History Store**：包含Session Context（会话上下文）、Agent Memory（代理记忆）、History（历史记录）和GUI Policy（图形用户界面策略）。它为后续阶段提供与用户会话、代理自身记忆、历史交互和GUI策略相关的信息。
- **Skill & Shortcut Store**：包含Agent Skills（代理技能）和GUI Shortcuts（图形用户界面快捷方式）。它为后续阶段提供可用的代理技能和GUI快捷方式信息。
这两个存储通过箭头向下面的四个阶段（Know、Route、Act、Reflect）提供“建议性上下文”，即相关信息会被传递到这些阶段以支持其操作。

### 阶段1：Know（认知/知识获取）
这个阶段的目标是收集证据并组装推理上下文，分为三个子模块：
- **Evidence Gathering**：从Memory / Profile（记忆/配置文件）和Workspace Evidence（工作区证据）中收集信息，也就是从持久化存储和其他相关工作区数据中获取与任务相关的证据。
- **Indexing & Retrieval**：对Skills / Shortcuts Index（技能/快捷方式索引）进行操作，提供Top - k Hints（前k个提示）和Policies（策略），即从技能和快捷方式索引中检索出最相关的提示和策略。
- **Knowledge Package**：将上述收集和检索到的信息组装成Assembled Context for reasoning（用于推理的组装上下文），这个上下文将为后续的Route阶段提供支持。
信息流动顺序是：从Memory & History Store和Skill & Shortcut Store获取输入，经过Evidence Gathering、Indexing & Retrieval的处理，最终形成Knowledge Package。

### 阶段2：Route（路由/任务规划）
这个阶段的目标是对任务进行理解、规划，并将请求转化为单个GUI任务或多应用工作流，包含四个子模块：
- **Workflow Runner**：负责Task Understanding & Planning（任务理解和规划），即理解用户任务并规划如何执行。
- **App Candidates**：对Ranked Apps & Entry Points（排名应用和入口点）进行处理，也就是对可能的应用和它们的入口点进行排名，以确定执行任务的候选应用。
- **Multi - App Plan**：如果任务需要多个应用，就生成Multi - App Plan（多应用计划），并且子任务之间通过Blackboard（黑板）交换typed values（类型化值），黑板作为一个共享空间来传递信息。
- **Blackboard**：作为子任务之间信息交换的媒介，确保多应用工作流中的信息传递。
信息流动顺序是：从Know阶段的Knowledge Package获取输入，经过Workflow Runner、App Candidates的处理，生成Multi - App Plan，并且通过Blackboard进行信息交换。

### 阶段3：Act（行动/执行）
这个阶段的目标是在混合动作空间（GUI原语、技能、深度链接/意图快捷方式、干预动作）上运行GUIClaw的observe - reason - act循环，包含多个子模块：
- **Executor**：执行Observe - Reason - Act（观察 - 推理 - 行动）循环，这是执行的核心部分，负责实际的执行操作。
- **GUI Model**：与GUI相关的模型，可能用于理解GUI的结构和元素。
- **Canonical Action**：规范动作，即定义标准的动作形式。
- **Backend Dispatch**：后端调度，负责将动作发送到后端执行。
- **GUI Primitives**：图形用户界面原语，即基本的GUI操作，如点击、输入等。
- **Skill**：代理技能，即之前存储的代理技能，用于执行特定任务。
- **API**：应用程序接口，通过API调用执行任务。
- **Ask - User**：当需要时向用户询问信息，作为干预动作。
信息流动顺序是：从Route阶段的输出（如Multi - App Plan或单个GUI任务）获取输入，Executor通过GUI Model、Canonical Action、Backend Dispatch等模块，结合GUI Primitives、Skill、API、Ask - User等动作空间来执行任务。

### 阶段4：Reflect（反思/学习）
这个阶段的目标是将每个轨迹提炼成更新的技能和经验记忆，反馈到持久化存储中，包含三个子模块：
- **Trajectory Recorder**：记录任务的执行轨迹，即记录整个执行过程中的信息。
- **Skill Extraction**：从执行轨迹中提取技能，即从已有的执行经验中学习新的技能或改进现有技能。
- **GUI Memory Induction**：归纳图形用户界面记忆，即从执行轨迹中学习关于GUI的记忆，以改进未来的任务分解和工具调用。
信息流动顺序是：从Act阶段的执行结果获取输入，经过Trajectory Recorder、Skill Extraction、GUI Memory Induction的处理，将更新后的技能和记忆反馈到Memory & History Store和Skill & Shortcut Store中，从而实现自我进化和持续学习。

总体来说，KnowAct - GUIClaw的工作流程是：首先从两个持久化存储获取上下文信息，在Know阶段收集证据并组装推理上下文；然后在Route阶段规划任务，确定执行的候选应用或工作流；接着在Act阶段执行任务，利用混合动作空间完成任务；最后在Reflect阶段反思执行过程，更新技能和记忆，并反馈到持久化存储中，以实现自我进化和持续改进，从而解决OpenClaw在跨平台GUI交互和自我进化机制方面的不足。

---

![Figure 3: Experience memory improves a GUI task by changing the task context bef](fig3_1.webp)

> Figure 3: Experience memory improves a GUI task by changing the task context before low-level control begins . Without the retrieved memory (Top), GUIClawinvites continues through Mastodon’s mobile settings and reaches a nonproductive path for invite-link creation. With the retrieved memory (bottom), the Know stage supplies an advisory lesson that invite links with advanced settings that require the web administration panel; GUIClaw then opens the web interface, navigates to account settings, and reaches the invite-people page. The example shows that experience memory guides app choice, decomposition, and recovery while live screen observations still ground each action.

这张图（图3）来自论文《KnowAct-GUIClaw: Know Deeply, Act Perfectly, Personal GUI Assistant with Self-Evolving Memory and Skill》，它清晰地展示了“经验记忆”如何通过改变低级控制开始前的任务上下文来改进一个GUI任务的执行流程。该图通过上下两个并行的流程对比，直观地说明了有无“检索到的经验记忆”对任务执行路径的影响。

**图的总体结构与对比逻辑：**

*   **上半部分（标记为 "Step 1" 到 "Step n"）：** 这代表了**没有检索到经验记忆**时的任务执行路径。这个路径最终导向了一个“非生产性”的结果（由红色叉号标记）。箭头（主要是橙色虚线和实线）表示了在没有经验记忆指导下，GUI代理（GUIClawinvites）的行动顺序和界面跳转。
*   **下半部分（标记为 "Step 3" 到 "Step 6"，并带有“Experience Memory”框）：** 这代表了**检索到经验记忆**时的任务执行路径。这个路径最终成功到达了目标页面（由绿色对勾标记）。箭头（主要是绿色虚线和实线）表示了在经验记忆指导下，代理的行动顺序和界面跳转。
*   **左侧的“Experience Memory”框：** 这是整个图的核心信息来源之一。它提供了一个关于Mastodon邀请链接创建的关键知识：“Mastodon Invite Links Require Web Admin Panel When creating Mastodon invite links with custom settings (expiry, auto-follow), use the web or browser admin panel instead of the mobile app...”。这个知识是在“Know”阶段被检索并提供给代理的，用于指导后续的“Act”阶段。

**数据或信息的流动顺序：**

1.  **无经验记忆的流程（上半部分）：**
    *   **Step 1：** 从手机主屏幕开始，代理点击了“Mastodon”应用图标。
    *   **Step 2：** 进入Mastodon应用后，代理点击了右上角的菜单按钮（三个点）。
    *   **Step 3：** 在弹出的菜单中，代理点击了“Settings”（设置）。
    *   **Step 4：** 在设置页面中，代理点击了当前账户（@owner@10.0.2.2）。
    *   **Step 5：** 在账户设置页面中，代理点击了“about”（关于）。
    *   **Step n：** 随后，代理可能继续在设置中导航，但最终路径被标记为非生产性（红色叉号），暗示它没有找到创建高级邀请链接的正确方式，可能停留在了如“About Mastodon”这样的无关页面或无法完成任务的路径上。

2.  **有经验记忆的流程（下半部分）：**
    *   **“Experience Memory”框：** 首先，代理在“Know”阶段检索到了关于Mastodon邀请链接需要使用网页管理面板的经验。
    *   **Step 3：** 基于这个经验，代理在某个界面（可能是设置或菜单）中点击了“About Mastodon”。这个行动可能是为了确认当前环境或作为转向正确路径的一个步骤。
    *   **Step 4：** 接着，代理点击了“Even more settings”（更多设置），这可能是在寻找通往网页管理界面的入口。
    *   **Step 5：** 然后，代理点击了菜单图标（通常是三个点或横线），这可能打开了一个包含“Invite people”选项的菜单。
    *   **Step 6：** 最后，代理点击了“invite people”（邀请人），成功进入了邀请链接创建页面，并可以看到生成链接的选项（如“Generate invite link”按钮）。这个路径被标记为成功（绿色对勾）。

**方法的具体运作方式（如何做）：**

这张图揭示了KnowAct-GUIClaw方法的核心运作机制：

*   **“Know”阶段（认知）：** 代理首先利用其“经验记忆”系统检索与当前任务相关的历史经验和知识。在这个例子中，经验告诉我们，对于带有自定义设置（如过期时间、自动关注）的Mastodon邀请链接，应该使用网页管理面板而不是移动应用。
*   **“Act”阶段（行动）：** 基于“Know”阶段获取的知识，代理调整其行为策略。它不再盲目地在移动应用的设置中寻找，而是根据经验指引，导航到网页管理界面（通过Chrome浏览器）。
*   **任务分解与分配：** 经验记忆帮助代理进行更有效的长远任务分解。例如，它知道创建高级邀请链接需要多个步骤，包括打开网页管理面板、进入账户设置等。
*   **工具调用与跨平台迁移：** 方法中的“pluggable GUI subagent”（可插拔GUI子代理）和“self-evolving skill library”（自演进技能库）使得代理能够适应不同的平台（如图中提到的Android、iOS等）。在这个例子中，代理知道需要调用网页浏览器工具来完成特定任务。
*   **持续学习与改进：** 通过不断存储用户反馈和执行经验，方法能够提高任务分解的准确性和工具调用的效率。图中展示的就是这种机制如何避免错误路径并引导至正确路径的一个实例。
*   **实时屏幕观察与经验记忆的结合：** 尽管经验记忆提供了高阶的指导，但每个具体的动作（如点击按钮）仍然是基于实时的屏幕观察（grounded in live screen observations）。这意味着代理在执行时会根据当前界面的实际情况来执行预定的行动。

**结论：**

图中清晰地展示了KnowAct-GUIClaw方法的有效性。通过引入“经验记忆”，该方法能够显著改进GUI任务自动化。**结论是：经验记忆能够指导应用选择、任务分解和执行路径的恢复，从而避免进入非生产性路径，成功完成任务。** 上半部分的失败路径（无经验记忆）与下半部分的成功路径（有经验记忆）形成了鲜明对比，有力地证明了该方法的优势。这种方法解决了传统GUI自动化工具（如OpenClaw）在跨平台适应性和持续学习能力方面的不足。

---

![Figure 4: Blackboard-mediated execution in the Route stage . The short-lived bla](fig4_1.webp)

> Figure 4: Blackboard-mediated execution in the Route stage . The short-lived blackboard B B stores typed inputs and outputs known so far. Each subtask ( g i , h i , I i , O i ) (g_{i},h_{i},I_{i},O_{i}) checks its declared inputs I i I_{i} , reads their values from B B , runs GUIClaw’s observe–reason–act loop to produce a trajectory τ i \tau_{i} , and writes only its declared outputs O i O_{i} back to B B ( 2 ). A missing required input or output makes the workflow fail closed, so later subtasks consume observed typed values rather than free-form summaries.

这张图展示了KnowAct - GUIClaw框架中“Route阶段”基于黑板（Blackboard）的执行流程，清晰呈现了任务分解、子任务执行及结果输出的过程：

### 组件与信息流动
1. **左侧：Short - lived Blackboard B**：这是一个短期黑板，用于存储已声明的输入/输出和已知值（如`user.name`为Alice、`trip.from`为Beijing等）。它的作用是为后续子任务提供已知数据的存储和读取支持，箭头表示数据从黑板流向中间子任务处理流程（步骤2中“Append Known Values to Iᵢ”会从这里读取已知值补充到子任务的输入中），同时子任务的输出（步骤4）会写回黑板（如`flight.option`的最终值会从子任务输出提取后存入这里）。

2. **中间：Ordered Subtask执行流程**：
    - **步骤1：Check Declared Inputs Iᵢ**：每个子任务（如Subtask 1、Subtask 2、Subtask n，每个子任务有`gᵢ`（GUI代理）、`hᵢ`（可能为技能或策略）、`Iᵢ`（输入）、`Oᵢ`（输出））首先检查其声明的输入`Iᵢ`，明确需要哪些输入数据来执行任务。
    - **步骤2：Append Known Values to Iᵢ**：从左侧的Short - lived Blackboard B中读取已知的值，补充到子任务的输入`Iᵢ`中。例如，如果子任务需要`trip.from`的值，就会从黑板中获取Beijing并添加到`Iᵢ`里，确保子任务有足够的已知数据来执行。
    - **步骤3：Run GuiAgent (Observe - Reason - Act)**：每个子任务中的GuiAgent（如GuiAgent(g₁)、GuiAgent(g₂)等）执行“观察 - 推理 - 行动”循环。这个循环是KnowAct - GUIClaw的核心执行逻辑，通过观察界面、推理任务需求、执行操作来完成任务，产生轨迹τᵢ（图中未直接显示轨迹，但提到会记录轨迹用于后续分析或学习）。
    - **步骤4：Output Extractor (Write Oᵢ to B)**：子任务执行完成后，输出提取器会从子任务的输出中提取声明的输出`Oᵢ`（如Summary、Model Summary、Latest Trace等），并将其写回左侧的Short - lived Blackboard B中。例如，Subtask 1的输出`O₁`会被提取并写入黑板，供后续子任务（如Subtask 2）在步骤2中读取，或者供最终的“Structured Workflow Result”使用。

3. **右侧：Structured Workflow Result**：这是整个工作流的最终结果，包含Final State（最终状态）、Collected Outputs（收集的输出）、Evidence (Traces)（证据/轨迹）、Status (Success/Fail)（状态/成功/失败）、Next Suggestions（下一步建议）。这些结果是从各个子任务的输出中汇总而来的，例如子任务的输出会被整合到这里，以展示整个任务执行的最终情况。

### 方法运作方式
KnowAct - GUIClaw在“Route阶段”的运作遵循以下逻辑：
- **任务分解与输入处理**：首先将复杂任务分解为多个有序子任务（Subtask 1到Subtask n），每个子任务明确自己的输入`Iᵢ`、输出`Oᵢ`、执行的GUI代理`gᵢ`和相关策略`hᵢ`。然后通过黑板B来管理输入输出数据，确保子任务能获取到所需的已知值（步骤2），解决输入缺失的问题（如果输入缺失，工作流会“fail closed”，即后续子任务会使用观察到的类型化值而非自由形式摘要，保证执行的封闭性）。
- **子任务执行**：每个子任务通过GuiAgent执行“观察 - 推理 - 行动”循环，利用黑板中的已知数据和自身的能力（如跨平台GUI交互、自进化技能库等，虽然图中未直接显示这些能力，但根据论文背景可知）来完成任务，产生输出。
- **输出整合与结果生成**：子任务的输出被提取后写回黑板，最终所有子任务的输出被整合到“Structured Workflow Result”中，展示任务的最终状态、输出、轨迹、状态和建议等信息。

### 结果与结论（从图中逻辑推导）
从图中的流程可以看出，KnowAct - GUIClaw通过黑板介导的执行方式，实现了任务的分解、子任务的有序执行以及输出的整合，确保了任务的正确执行（如果输入输出都正确的话）。这种方法的优势在于：
- **数据管理**：通过黑板B集中管理输入输出数据，确保子任务能获取到所需的信息，解决输入缺失的问题，保证工作流的封闭性（fail closed）。
- **经验积累与自进化**：子任务的执行轨迹（Latest Trace）会被记录并写回黑板，后续可以用于改进任务分解和工具调用（根据论文背景），实现自进化。例如，用户反馈和交互经验会被存储在黑板或相关模块中，不断优化执行准确性。
- **跨平台适应性**：通过可插拔的GUI子代理和自进化的技能库（图中GuiAgent的设计暗示了这一点），可以实现无缝的跨平台迁移（如Android、iOS、HarmonyOS和Windows等，根据论文背景），解决OpenClaw的跨平台缺陷。

总之，这张图清晰地展示了KnowAct - GUIClaw在“Route阶段”如何通过黑板介导的执行流程，实现任务的分解、子任务的执行和结果的整合，解决了OpenClaw的GUI交互和自进化问题，提升了任务执行的效率、准确性和跨平台适应性。

---

![Figure 5: KnowAct-GUIClaw execution of a cross-app price comparison . The host s](fig5_1.webp)

> Figure 5: KnowAct-GUIClaw execution of a cross-app price comparison . The host supplies the product model from the user profile and routes two GUI tasks. A validated JD search shortcut lands directly on the results page, whereas Taobao requires five ordinary GUI steps. The blackboard carries both observed prices into the host’s recommendation, illustrating the step and token savings in Table 3 .

这张图展示了KnowAct - GUIClaw框架执行跨应用（京东和淘宝）价格比较任务的过程，我们可以从以下几个部分来理解它的运作机制：

### 1. 任务发起与信息输入
- **用户请求（User request）**：用户希望比较其在京东（JD）和淘宝（Taobao）上保存的固态硬盘（SSD）的价格，并得知哪个更值得购买。这里的任务需求被明确提出。
- **主机记忆（host memory / user profile）**：主机的用户配置文件中提供了SSD的型号（ssd_model = Samsung 990 EVO Plus），这个信息作为“已声明的黑板输入”被提供给路由（routing），这体现了框架利用用户积累的交互经验和任务相关知识（这里是产品型号）来进行任务处理的“Know”阶段，即认知理解阶段，明确任务所需的关键信息。

### 2. 路由与任务分配（Know阶段）
- **路由策略（routing policy）**：根据用户请求和用户配置文件中的信息，路由策略将任务分解为两个GUI任务，分别处理京东和淘宝的价格查询。这一步是任务的长 horizon 分解和分配，利用积累的经验和知识来确定如何执行任务，属于“Know”阶段的任务分配环节。

### 3. 京东（JD）的任务执行（Act阶段 - 快捷路径）
- **JD的界面与操作**：京东的任务使用了一个“已验证的JD搜索快捷方式（validated JD search shortcut）”，这个快捷方式直接将用户带到搜索结果页面。从图中可以看到，JD的界面显示了三星990 EVO Plus的相关商品，第一个商品的价格（first item ¥1399）被记录下来。这一步体现了框架的“Act”阶段中的快速路径集成，利用已有的快捷方式（可能是之前学习到的经验）来减少操作步骤，提高效率。这里的“blackboard”（黑板）系统记录了jd_price = ¥1399，将观察到的价格传递给主机的推荐环节。

### 4. 淘宝（Taobao）的任务执行（Act阶段 - 普通GUI步骤）
- **淘宝的界面与操作（5个普通GUI步骤）**：
    - **Step 1**：打开淘宝（Open Taobao），没有可用的快捷方式（no shortcut available），界面显示了一个618的促销弹窗。
    - **Step 2**：关闭搜索框上的618促销弹窗（Close the 618 promo popup over the search box），这样才能进行后续的搜索操作。
    - **Step 3**：点击搜索框（Tap the search box），激活搜索输入区域。
    - **Step 4**：输入产品型号（Type the product model），即Samsung 990 EVO Plus 1TB，通过键盘输入来完成搜索关键词的输入。
    - **Step 5**：点击搜索并读取第一个商品（Tap search; read the first item），淘宝的第一个商品价格为¥1271，这个价格被记录到黑板中（taobao_price = ¥1271）。
- 这一系列步骤展示了在没有快捷方式的情况下，框架如何通过模拟人类的GUI操作（点击、输入、关闭弹窗等）来完成任务的“Act”阶段，同时利用可归因于经验的记忆系统（这里记录了每一步的操作和观察到的价格）来确保操作的准确性，并且这些经验会被存储起来以改进未来的任务分解和工具调用。

### 5. 结果整合与推荐（Know阶段 - 反思与推荐）
- **黑板（blackboard）的信息流动**：黑板系统将京东的价格（jd_price = ¥1399）和淘宝的价格（taobao_price = ¥1271）都携带到主机的推荐环节（recommendation）。主机根据这些价格信息以及可能的售后服务和保修等因素（如图中主机的回复：“Taobao 1 TB is ¥128 cheaper; JD self - operated is preferable for after - sales and warranty.”），给出最终的购买建议。
- **效率与步骤节省**：从图中可以看出，京东使用了快捷方式，只需要较少的步骤（或直接的快捷方式）就完成了价格查询，而淘宝需要5个普通的GUI步骤。这在表3（文中提到的）中会体现出步骤和令牌（token）的节省，说明框架通过使用快捷方式和优化的任务执行路径，提高了执行效率和准确性。

### 整体运作机制总结
KnowAct - GUIClaw框架通过“Know - Route - Act - Reflect”的流程来完成任务：
- **Know（认知理解）**：利用用户配置文件中的信息（如产品型号）和积累的交互经验来分解任务，确定需要执行的操作（如使用快捷方式或模拟GUI操作）。
- **Route（路由分配）**：将任务分配给不同的应用（京东和淘宝），并为每个应用确定合适的执行路径（快捷方式或普通GUI步骤）。
- **Act（操作执行）**：对于京东，使用快捷方式快速获取价格；对于淘宝，模拟人类的GUI操作（点击、输入、关闭弹窗等）来获取价格，同时记录操作过程中的信息和观察到的结果（价格）到黑板中。
- **Reflect（反思与改进）**：将不同应用的价格信息整合到黑板中，主机根据这些信息和其他因素（如售后服务）给出推荐，并且将这次任务的经验（如快捷方式的有效性、GUI操作的步骤等）存储起来，用于改进未来的任务分解和工具调用，实现自我进化和跨平台适应。

通过这个例子，我们可以看到KnowAct - GUIClaw框架如何解决OpenClaw的不足，即通过积累的经验和知识来提高跨平台GUI交互的支持和自我进化能力，从而实现更高效、准确的任务自动化。

---

![Figure 6: Cases of our workflow with attribution experience. (a) Email-to-alarm ](fig6_1.webp)

> Figure 6: Cases of our workflow with attribution experience. (a) Email-to-alarm transfers the observed party time through the blackboard; the host subtracts one hour before the GUI subagent sets the alarm. (b) Failure-driven re-planning records a failed contact lookup, recovers the phone number from a resume, and delegates the final Messages GUI task.

这张图（图6）展示了我们的工作流案例，其中包含了归因经验（attribution experience）。它分为两个部分，(a) 和 (b)，分别展示了两种不同的任务处理流程，旨在说明我们的方法（KnowAct-GUIClaw）如何运作。

首先看(a)部分，标题是“Cross-app blackboard with host arithmetic”（跨应用黑板与主机算术）。这部分展示了一个从电子邮件中提取信息并设置闹钟的任务。
1.  **请求（Request）**：顶部的蓝色框显示了用户的原始请求：“Check my email for today's party time and set an alarm one hour before.”（检查我的电子邮件以获取今天的派对时间，并提前一小时设置闹钟。）
2.  **Email 应用界面**：左侧的手机界面模拟了电子邮件应用。邮件内容显示派对时间是晚上7点（“The annual Christmas party will start at 7:00 PM today.”）。在界面下方，有一个绿色的标签“party_time 7:00 PM”，并附有文字说明“Party time: 7:00 PM.”，这表示系统从邮件中成功提取了派对时间。
3.  **数据流动（箭头）**：一个蓝色的箭头从“Email”部分指向“Clock”部分，箭头上标有“host -1 h”。这表示主机代理（host agent）在接收到邮件中的派对时间后，执行了一个操作：将时间减去一小时。
4.  **Clock 应用界面**：右侧的手机界面模拟了时钟/闹钟应用。界面显示了一个设置为下午6点的闹钟（“Christmas Party”）。下方的绿色标签“alarm 6:00 PM”和文字说明“Set an enabled 6:00 PM alarm.”表明闹钟已成功设置。
5.  **黑板（blackboard）与数据存储**：在两个应用界面下方，有一个“blackboard”（黑板）的概念。这里展示了数据的存储和传递：“party_time = 7:00 PM” 然后 “→ alarm = 6:00 PM”。这说明提取到的派对时间被存储在黑板上，然后经过主机的计算（减一小时）后，生成了闹钟时间。
6.  **主机回复（Host reply）**：最下方的绿色对勾和文字“Host reply: the 6:00 PM alarm was created.”确认了任务成功完成。

这个案例揭示了方法的一部分：主机代理利用从GUI（电子邮件）中提取的信息（通过“blackboard”共享），进行必要的计算（如时间调整），然后指示另一个GUI子代理（闹钟应用）执行具体操作。这里的“host arithmetic”指的是主机进行的简单计算。

接下来看(b)部分，标题是“Failure-driven re-planning”（失败驱动的重新规划）。这部分展示了一个发送短信的任务，其中遇到了联系查找失败的情况，系统如何进行恢复。
1.  **请求（Request）**：顶部的蓝色框显示了用户的原始请求：“Text Kevin about the interview. He is not in Contacts, so recover the number from the resume.”（给Kevin发短信谈面试的事。他不在联系人中，所以从简历中恢复号码。）
2.  **Resume 应用界面**：左侧的手机界面模拟了简历应用。界面显示了一份简历，其中包含电话号码“(555) 123-4567”。下方的绿色标签“phone (555) 123-4567”和文字说明“Recover the number from the resume.”表明系统成功地从简历中恢复了电话号码。
3.  **数据流动（箭头）**：一个红色的箭头从“Resume”部分指向“Messages”部分，箭头上标有“re-plan”。这表示在之前的步骤（可能是查找联系人）失败后，系统进行了重新规划，将任务流程调整为从简历中获取号码，然后发送短信。
4.  **Messages 应用界面**：右侧的手机界面模拟了短信应用。界面显示了一条已发送的短信，内容是关于面试时间的安排。下方的绿色标签“SMS sent”和文字说明“Send the SMS to that number.”表明短信已成功发送到恢复的电话号码。
5.  **黑板（blackboard）与数据存储/状态更新**：在两个应用界面下方，有一个“blackboard”的概念。这里展示了任务的状态变化：“contact = failed”（表示查找联系人的尝试失败），然后“→ phone recovered”（表示成功从简历中恢复了电话号码），最后“→ sent”（表示短信已发送）。
6.  **主机回复（Host reply）**：最下方的绿色对勾和文字“Host reply: the number was recovered and the SMS sent.”确认了任务成功完成。

这个案例揭示了方法的另一部分：当任务执行过程中遇到失败（如“contact = failed”）时，系统能够进行失败驱动的重新规划。它从一个备用的信息源（简历）中恢复所需的数据（电话号码），然后继续执行最终的任务（发送短信）。这体现了系统的鲁棒性和自适应能力。

总结来说，这张图通过两个具体的案例，清晰地展示了KnowAct-GUIClaw框架的工作流程：
*   **(a) 跨应用协作与计算**：系统从一个应用（电子邮件）提取信息，通过主机进行计算，然后将结果传递给另一个应用（闹钟）执行操作。这依赖于“blackboard”进行信息共享和传递。
*   **(b) 失败恢复与重新规划**：当一个任务步骤失败时（如查找联系人），系统能够从一个备用的信息源（简历）恢复必要的数据，然后继续执行最终任务（发送短信）。这体现了系统的容错能力和动态调整任务计划的能力。

这两个案例共同说明了该方法如何通过积累的经验和知识来分解任务、分配给合适的子代理，并在遇到问题时进行自适应调整，从而实现高效、准确的个人助理服务。

---

![Figure 7: Host-mediated recovery in a conference-location task. The Email GUI ta](fig7_1.webp)

> Figure 7: Host-mediated recovery in a conference-location task. The Email GUI task returns only the hotel name, so the host resolves the full address through web search before delegating the Messages and Maps GUI tasks. Maps reports a 13 13 -minute walk. The workflow combines partial GUI evidence with external tools while preserving typed subtask boundaries.

这张图（图7）展示了在“会议地点”任务中，由宿主（Host）介导的恢复过程，清晰地说明了KnowAct-GUIClaw框架如何运作。

首先，我们来看**子任务1：在电子邮件中查找MCFT会议酒店的名称/地址**。
这个子任务的流程从左到右展开：
1.  最左侧的手机屏幕显示了一个典型的Android主屏幕，上面有各种应用图标。一个橙色箭头指向“邮件”应用图标，表示用户（或代理）首先打开了邮件应用。
2.  接下来的几个屏幕展示了邮件应用的界面：首先是“Inbox”（收件箱）视图，显示了多个邮件。一个橙色箭头指向其中一封主题为“MCFT conference”的邮件。
3.  点击该邮件后，进入邮件详情页面。另一个橙色箭头指向邮件正文中的一行文字，该行文字提到了酒店名称“Harvard Square Hotel”。
4.  流程的输出结果显示在右侧：“Output: Harvard Square Hotel”。这表明，通过交互邮件GUI，代理成功提取了酒店的名称。
5.  由于邮件只提供了酒店名称，宿主介入。宿主执行了一个工具调用：“Host: web_search('Harvard Square Hotel')”（用橙色框标出）。这表示宿主使用网络搜索来获取酒店的完整地址。
6.  工具反馈（Tool feedback）显示在下方：“Harvard Square Hotel, 110 Mount Auburn St, Cambridge, MA 02138”（用蓝色框标出）。这说明网络搜索成功返回了酒店的完整地址。
7.  随后，宿主委托另一个GUI任务：“Host: gui_task('Send a text message to Tom (4456547865) with the hotel address: Harvard Square Hotel, 110 Mount Auburn St, Cambridge, MA 02138')”（用橙色框标出）。这意味着宿主将“发送包含酒店地址的短信给Tom”这个子任务分配给了消息（Messages）GUI。

信息的流动顺序是：打开邮件应用 -> 查找并点击相关邮件 -> 提取酒店名称 -> 宿主进行网络搜索获取完整地址 -> 宿主委托消息任务。

接下来是**子任务2：向Tom (4456547865) 发送包含酒店地址的短信**。
这个子任务的流程同样从左到右：
1.  最左侧的屏幕显示了消息应用的界面，可能是联系人列表或对话列表。一个橙色箭头指向搜索栏或某个操作区域，表示开始查找联系人Tom。
2.  接下来的屏幕显示了联系人列表，其中包含多个联系人。一个橙色箭头指向名为“Tom”的联系人（或其电话号码4456547865）。
3.  然后，界面切换到新消息编辑界面。一个橙色箭头指向电话号码输入框，表示正在输入Tom的电话号码。
4.  接着，光标出现在消息文本输入框中，准备输入信息。一个橙色箭头指向输入框。
5.  然后，酒店地址“Harvard Square Hotel, 110 Mount Auburn St, Cambridge, MA 02138”被输入到消息文本中。
6.  最后一个屏幕显示了消息已发送的状态，右侧有一个绿色的对勾图标，表示短信发送成功。
信息的流动顺序是：打开消息应用 -> 查找并选择联系人Tom -> 输入电话号码 -> 输入包含酒店地址的消息 -> 发送短信。

最后是**子任务3：搜索从MIT Stata Center到哈佛广场酒店的步行路线，并提取步行时间（分钟）**。
这个子任务的流程：
1.  最左侧的屏幕显示了一个地图应用的初始界面，可能是一个“制作你的地图”或类似的功能。一个橙色箭头指向某个操作按钮，表示开始新的搜索。
2.  接下来的屏幕显示了地图应用的搜索界面，可能是一个世界地图视图。一个橙色箭头指向搜索框或某个操作区域，表示输入目的地。
3.  然后，界面显示了搜索结果或建议，可能是一个列表或地图标记。一个橙色箭头指向某个选项，可能是选择酒店或确认地点。
4.  接下来的屏幕显示了酒店的具体位置在地图上的标记，以及一些相关信息（如图片、评分等）。一个橙色箭头指向地图上的酒店标记。
5.  然后，界面切换到路线规划选项，可能显示了不同的出行方式（如步行、驾车）。一个橙色箭头指向“步行”选项或相关的路线规划按钮。
6.  接下来的屏幕显示了详细的步行路线图，包括起点（MIT Stata Center）和终点（Harvard Square Hotel），以及路线的可视化。一个橙色箭头指向路线或某个操作按钮。
7.  最后一个屏幕显示了步行路线的详细信息，包括总步行时间（图中显示为“13 min”）和距离（“3.3 mi”）。右侧有一个绿色的对勾图标，表示路线搜索成功并提取到了时间。
信息的流动顺序是：打开地图应用 -> 搜索目的地 -> 选择酒店 -> 查看酒店位置 -> 选择步行路线 -> 查看路线详情并获取步行时间。

这张图揭示了KnowAct-GUIClaw方法的具体运作方式：
1.  **任务分解与委托（Know）**：宿主代理首先将复杂任务（查找会议酒店并通知Tom，然后获取路线）分解为更小的子任务。例如，在子任务1中，它首先通过邮件GUI获取酒店名称，然后因为信息不足，宿主介入并调用外部工具（网络搜索）来获取完整地址。之后，宿主将“发送短信”和“搜索路线”这两个子任务分别委托给相应的GUI子代理（消息和地图）。
2.  **跨平台GUI交互与技能执行（Act）**：每个子任务都涉及到与特定平台的GUI进行交互。例如，邮件应用、消息应用和地图应用。代理能够理解GUI元素（如按钮、输入框、列表项），并进行相应的操作（点击、输入、选择）。图中橙色箭头指示了代理在GUI上的操作点和流程方向。
3.  **经验与工具集成**：当邮件GUI提供的信息不完整时（仅酒店名称），宿主利用外部工具（网络搜索）来补充信息。这体现了方法能够结合部分GUI证据与外部工具的能力。工具的反馈（完整地址）被用来进一步执行后续任务（发送短信、搜索路线）。
4.  **子任务边界的保留**：尽管使用了外部工具，但每个子任务的边界仍然清晰。例如，邮件检索、网络搜索、短信发送和路线搜索是四个逻辑上分离的步骤，但它们共同构成了一个更大的任务。
5.  **结果的提取与验证**：在最后一个子任务中，代理能够从地图应用的输出中提取具体的信息（步行时间13分钟），并用绿色对勾图标表示任务成功完成。

总而言之，这张图通过一个具体的例子（会议地点任务），详细展示了KnowAct-GUIClaw框架如何通过宿主介导，将复杂任务分解为一系列子任务，利用GUI交互和外部工具来解决信息不足的问题，并最终成功完成任务。信息的流动是线性的，从一个子任务到下一个子任务，每个步骤都有明确的输入和输出。

如果是结果图，我们可以看到：
*   **坐标**：图中没有明确的坐标系统，但流程是从左到右，从上到下组织的。
*   **对比对象**：这张图展示了一个成功的任务执行案例，对比的是如果没有宿主介导或没有外部工具辅助，任务可能无法完成或需要更多的人工干预。
*   **结论**：KnowAct-GUIClaw框架能够有效地处理需要跨多个GUI应用和外部工具的复杂任务。它能够通过任务分解、工具集成和结果提取来实现自动化。图中绿色对勾图标表明每个子任务都成功完成，最终得到了所需的步行时间（13分钟）。图中提到的“Maps reports a 13-minute walk”与caption中的信息一致。

---

![Figure 8: Cart-to-SMS cross-app execution. The TaoDian GUI task extracts the pro](fig8_1.webp)

> Figure 8: Cart-to-SMS cross-app execution. The TaoDian GUI task extracts the product names, order number, and recipient phone number and transfers them to the downstream messaging task. A validated messaging shortcut opens the SMS compose view with the recipient and message body already populated, illustrating both blackboard information transfer and navigation compression.

这张图（图8）展示了KnowAct-GUIClaw框架中一个典型的跨应用任务执行流程，具体为“购物车到短信”（Cart-to-SMS）的任务链。该图清晰地揭示了方法的核心运作机制，即通过任务分解、信息提取与传递、以及下游任务执行来完成复杂操作。

首先，我们来看图的上半部分，这部分描述了第一个子任务（Subtask 1）：在名为“TaoDian”的应用程序中查找待发货的商品，并提取产品名称、订单号和收件人电话号码。

*   **流程起始**：最左侧的图像显示了一个手机桌面，上面有多个应用图标。一个箭头指向其中一个图标（看起来像一个购物车或商店的图标），这代表了任务的起点——启动TaoDian应用。
*   **应用内导航**：接下来的几个图像展示了在TaoDian应用内部的操作步骤。箭头指示了用户的操作路径，例如点击屏幕上的某个区域（可能是菜单或特定按钮），然后进入“个人中心”或“我的订单”页面。
*   **信息定位与提取**：随后，箭头指向一个“订单列表”页面，其中显示了具体的订单详情。再下一步，箭头指向一个“订单详情”页面，这里包含了所需的关键信息：产品名称（如“经典白色T恤”、“保湿面霜套装”）、订单号（如“639281475036294”）和收件人电话号码（如“13800138888”）。这些信息是后续任务所必需的。

数据的流动顺序是：从启动TaoDian应用开始，经过一系列的界面导航和交互，最终在订单详情页面提取出目标信息。

接下来，我们看图的下半部分，这部分描述了第二个子任务（Subtask 2）：使用提取到的信息发送一条短信提醒。

*   **信息传递**：从上半部分的“订单详情”页面，信息被传递到短信/消息应用。图中显示了一个箭头，象征着信息（产品名称和订单号）从TaoDian应用被转移到短信应用的输入框中。
*   **短信应用操作**：接下来的图像展示了短信应用的界面。一个箭头指向短信应用的“新消息”创建界面，其中收件人电话号码（13800138888）已经被自动填充。
*   **消息内容填充与发送**：在短信编辑框中，产品名称和订单号（如“经典白色T恤 保湿面霜套装 639281475036294”）已经被自动填入。最后一个图像显示了短信发送成功的确认状态（例如，一个绿色的对勾或“已发送”的提示）。

这张图揭示了KnowAct-GUIClaw方法的具体运作方式：
1.  **任务分解（Know）**：主代理（host agent）利用积累的交互经验和任务相关知识，将复杂任务（如“发送订单提醒”）分解为更小的、可管理的子任务（如“从TaoDian提取信息”和“发送短信”）。
2.  **跨平台GUI交互（Act）**：一个可插拔的GUI子代理负责执行具体的界面操作。它利用经验可追溯的记忆系统（experience-attributable memory system）来自我学习和改进，实现跨平台的无缝迁移和快速路径集成。在这个例子中，它能够识别并在TaoDian应用中找到正确的信息，在短信应用中填写并发送消息。
3.  **信息传递与导航压缩**：图中特别指出了“黑板信息传递”（blackboard information transfer）和“导航压缩”（navigation compression）。这意味着提取的信息（如产品名称、订单号、电话号码）被存储在一个共享的“黑板”上，供后续任务直接使用，避免了重复的手动输入。同时，“导航压缩”可能指的是优化了在不同应用间切换和操作的路径，提高了效率。
4.  **验证与反馈**：整个过程的结果被验证（如图中的绿色对勾所示），确保任务成功完成。这种验证和反馈机制是KnowAct-GUIClaw自进化能力的一部分，用于持续改进任务分解和工具调用的准确性。

总而言之，这张图通过一个具体的“购物车到短信”任务示例，生动地展示了KnowAct-GUIClaw框架如何通过智能的任务分解、高效的信息提取与传递，以及跨平台的应用交互，来实现复杂的自动化任务。它强调了经验的积累和利用对于提高执行效率和准确性的重要性。

---

![Figure 9: Chinese annotated companion for the host-mediated recovery case in Fig](fig9_1.webp)

> Figure 9: Chinese annotated companion for the host-mediated recovery case in Figure 7 . The panel highlights the same control flow in which an underspecified GUI output is routed back to the host, grounded through web search, and then consumed by downstream Messages and Maps GUI tasks.

这张图（图9）是一个详细的用户界面交互流程图，用于展示一个名为“KnowAct-GUIClaw”的个人GUI助手框架如何执行一个具体的多步骤任务。该任务是根据Mastodon上用户“jack”分享的商品信息，在淘宝APP中下单购买2双同款商品。

我们可以将图分为两个主要部分，对应任务的两个子任务（Subtask），每个部分都由一系列手机屏幕截图和连接它们的箭头组成，清晰地展示了操作的顺序和信息的流向：

1.  **Subtask 1: 在Mastodon中获取商品信息**
    *   **起始点**：最左侧的手机屏幕截图显示了一个Android设备的主屏幕，上面有各种应用图标。这代表了任务的起点，即用户设备上的操作环境。
    *   **信息流**：黄色箭头指示了操作的顺序。首先，用户打开Mastodon应用（从主屏幕点击Mastodon图标开始）。随后的截图展示了用户在Mastodon应用内的操作，包括浏览帖子、找到用户“jack”分享的商品帖子，并最终获取到商品的关键信息。
    *   **输出（Output）**：在Subtask 1的右侧，有一个绿色边框的框，标注为“Output”，内容是：“已获取jack分享的淘店商品信息：一双棕色/卡其色休闲鞋（Nike风格），白色鞋底。图片已保存。” 这表明Subtask 1成功完成了，提取到了商品的核心描述信息。
    *   **知识传递（Stack In Blackboard）**：紧接着是一个橙色边框的框，标注为“Stack In Blackboard”，内容是：“棕色/卡其色休闲鞋（Nike风格），白色鞋底”。这表示从Subtask 1获得的信息被存储到一个“黑板”（Blackboard）结构中，这个结构可能是一个共享的记忆或上下文存储区域，供后续任务使用。
    *   **下一步指引（Next Subtask Append）**：最后是一个蓝色边框的框，标注为“Next Subtask Append”，提供了Subtask 2需要使用的已知值（known values），包括商品信息（product_info）、价格、描述、图片和搜索关键词。这明确指出了Subtask 2的输入数据来源。

2.  **Subtask 2: 在淘宝APP中搜索并购买商品**
    *   **起始点**：Subtask 2的左侧第一个截图显示了淘宝APP的界面，可能是一个搜索页面或首页。黄色箭头指示了接下来的操作流程。
    *   **信息流**：操作流程包括在淘宝中搜索商品（使用从Subtask 1获取的关键词，如“休闲鞋”）、浏览搜索结果、选择与目标商品匹配的选项、进入商品详情页、选择规格（如购买2双）、填写收货地址（广东省广州市天河区华景新城，收货人李四，电话13800139999）、确认订单信息并提交支付。
    *   **关键操作点**：图中的黄色箭头和手形光标图标清晰地标示了用户需要点击或操作的具体UI元素，例如搜索框、商品图片、规格选择按钮、地址填写字段和提交按钮。
    *   **完成标志**：Subtask 2流程的最右侧有一个绿色的对勾（✔️）图标，表示任务成功完成。最后的截图显示了支付成功的页面，确认了订单金额为598.00元（2双，每双299.00元）。

**方法运作的揭示**：
这张图揭示了KnowAct-GUIClaw框架的具体运作方式：
*   **任务分解与分配（Know）**：主机代理（host agent）首先将复杂任务（如在Mastodon获取信息并在淘宝购买）分解为更小的子任务（Subtask 1和Subtask 2）。它利用积累的交互经验和任务相关知识来指导这些子任务的执行。
*   **跨平台GUI交互（Act）**：一个可插拔的GUI子代理负责执行具体的GUI操作。它通过一个具有经验可追溯记忆系统（experience-attributable memory system）和自进化技能库（self-evolving skill library）来实现在不同平台（如Mastodon和淘宝）之间的无缝迁移和快速路径集成。
*   **信息传递与反馈循环**：Subtask 1的结果（商品信息）被存储到“黑板”中，并作为Subtask 2的输入。这体现了认知理解（Know）和操作执行（Act）的统一。框架通过持续存储用户资料和反馈来改进任务分解和工具调用的准确性，形成一个递归的自我改进机制。
*   **处理不明确的GUI输出**：如图的原始caption所述，这个框架能够处理“未充分指定的GUI输出”（underspecified GUI output），将其路由回主机代理，通过网页搜索等方式进行“接地”（grounded），然后再用于下游的GUI任务（如Messages和Maps）。虽然这张图主要展示了一个成功的流程，但其设计理念支持这种灵活性。

总而言之，这张图通过一个具体的案例，详细展示了KnowAct-GUIClaw框架如何通过深度认知（Know Deeply）和完美执行（Act Perfectly）来自动化复杂的个人GUI任务，特别是如何在不同平台间迁移并利用经验进行自我改进。

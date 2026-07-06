# Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming

[arXiv](https://arxiv.org/abs/2606.31227) · [HuggingFace](https://huggingface.co/papers/2606.31227) · ▲2

## 摘要（原文）

> The fast growth of open-source AI infrastructure, from model serving engines and agent platforms to the Model Context Protocol (MCP) ecosystem and the language models themselves, has outpaced the security tooling available to defend it. We present AI-Infra-Guard, an open-source framework that organizes AI red teaming around a single observation: the attack surface of an AI agent is stratified across layers (infrastructure, protocol/tool, agent behavior, and model), and no single detection paradigm fits all of them. The framework therefore matches a paradigm to each layer, from deterministic rule matching over 75+ AI components and 1{,}400+ vulnerability rules, through LLM-driven agentic auditing of MCP servers and agent-skill packages and multi-turn black-box agent red teaming, to a jailbreak harness with 26+ attack operators over sixteen datasets. To our knowledge it is the only open-source framework to span all of these, including supply-chain auditing of the agent skills that increasingly extend AI agents. We release AI-Infra-Guard as open source so that layer-paradigm matching can serve as a practical foundation for agent security and a shared base for the community to build on.

## 摘要（中译）

开源人工智能基础设施的快速发展，从模型服务引擎和代理平台到模型上下文协议（Model Context Protocol，MCP）生态系统以及语言模型本身，其速度已经超过了可用于保护它的安全工具的发展速度。我们提出了AI - Infra - Guard，这是一个开源框架，它围绕一个单一的观察结果来组织人工智能红队（red teaming）工作：人工智能代理的攻击面是分层分布的（基础设施层、协议/工具层、代理行为层和模型层），并且没有一种单一的检测范式适用于所有这些层。因此，该框架为每一层匹配一种范式，从对75多个人工智能组件和1400多个漏洞规则的确定性规则匹配，到MCP服务器和代理技能包的由大型语言模型（LLM）驱动的代理审计以及多轮黑盒代理红队测试，再到一个在十六个数据集上具有26多个攻击操作器的越狱测试框架。据我们所知，它是唯一一个涵盖所有这些方面的开源框架，包括对越来越多地扩展人工智能代理的代理技能的供应链审计。我们将AI - Infra - Guard作为开源项目发布，以便层 - 范式匹配能够作为代理安全的一个实用基础以及社区在此基础上构建的一个共享基础。

## 背景剖析

### 背景剖析  

**1. 技术背景**  
近年来，开源AI基础设施（如模型服务器、智能体平台、Model Context Protocol生态等）的快速发展催生了一类新型网络暴露软件。这些系统被个人或小团队部署在不受信任的网络中，用于构建对话机器人、自动化工作流甚至工具调用能力。然而，它们的安全需求与传统软件截然不同：需要防范未授权访问昂贵算力、API凭证泄露、提示注入劫持目标、工具滥用导致“困惑代理人”攻击，以及模型对齐性被对抗性提示破坏等问题。  

**2. 之前的问题**  
传统安全工具无法应对这些挑战，主要因为三个核心缺陷：首先，AI组件太新，现有漏洞数据库（如CVE）缺乏相关签名；其次，AI软件的版本管理不规范（如滚动更新、开发标签），导致依赖语义化版本比较的工具失效；最后，也是最关键的，AI的威胁模型已发生转变——高风险漏洞不再是传统的注入或脚本缺陷，而是需要多层级的检测方法（如基础设施暴露、协议漏洞、行为逻辑缺陷、模型对齐问题），而单一技术无法覆盖所有场景。  

**3. 本文的解法**  
论文提出“AI-Infra-Guard”框架，其核心思想是**分层匹配检测范式**：针对不同层级的攻击面（基础设施、协议/工具、智能体行为、模型），使用不同的检测方法。例如，基础设施层用规则匹配和版本归一化；协议层用LLM驱动的动态审计；行为层用对话式红队测试；模型层用多轮越狱评估。这种方法确保每个层级都能获得最适合的检测手段，而非强行套用单一技术。  

**4. 切入角度**  
与前人工作的关键差异在于，AI-Infra-Guard首次将AI安全评估视为一个**跨层级的统一问题**，并通过开源框架实现分层检测的标准化。它不仅覆盖从底层基础设施到高层模型对齐的全栈，还引入了“Prompt-as-Rule”等创新范式，允许社区扩展规则库和攻击算子，以适应快速演变的AI生态。这种设计既解决了当前工具的局限性，也为未来的AI安全研究提供了可扩展的基础。

## 方法图解

![Figure 5: The distributed server-agent architecture. A user interface (Web UI, C](fig4_1.webp)

> Figure 5: The distributed server-agent architecture. A user interface (Web UI, CLI, or HTTP API) drives backend services (Gin web server, plugin management, storage, and LLM providers), which in turn invoke the core engines (AI infra scan, MCP server scan, and LLM jailbreak evaluation). The engines draw on an AI-agents layer and a shared knowledge base of fingerprints, CVEs, MCP plugins, and jailbreak datasets.

这张图展示了一个名为“AI-Infra-Guard”的框架的分布式服务器-代理架构，该框架用于多层AI代理红队评估。下面我将详细解释图中的各个组件、板块、箭头以及信息和数据的流动顺序，以帮助您理解这个方法是如何运作的。

首先，我们从最顶层的“用户界面 (User Interface)”开始。这一层是用户与系统交互的入口，提供了三种不同的方式：
1.  **Web UI (Web用户界面)**：用户可以通过图形化界面进行操作。
2.  **CLI (命令行界面)**：用户可以通过命令行进行操作，适合熟悉命令行的用户或自动化脚本。
3.  **HTTP API (HTTP应用程序接口)**：允许其他软件系统通过HTTP协议与该框架进行交互，提供了程序化的访问方式。
这些用户界面的输入会流向下一层，即“后端服务 (Backend Services)”。

接下来是“后端服务 (Backend Services)”层。这一层负责处理来自用户界面的请求，并协调框架的核心功能。它包含以下几个关键组件：
1.  **Gin Web Server**：这是一个Web服务器，可能用于处理来自Web UI或HTTP API的请求。
2.  **Plugin Management (插件管理)**：负责管理和加载各种插件，这些插件可能扩展了框架的功能，例如支持新的扫描器或评估工具。
3.  **Storage (存储)**：用于存储系统运行所需的数据，如配置信息、扫描结果、知识库内容等。
4.  **LLM Providers (大语言模型提供者)**：这一组件与大型语言模型交互，可能用于生成报告、提供自然语言解释或支持某些类型的评估。
后端服务层处理完请求后，会调用“核心引擎 (Core Engines)”层来执行具体的任务。

然后是“核心引擎 (Core Engines)”层。这一层是框架的核心，包含了针对不同攻击层面的扫描和评估引擎：
1.  **AI Infra Scan (AI基础设施扫描)**：这个引擎负责扫描AI基础设施的安全性，例如模型服务引擎、代理平台等。它会利用下方的“AI Agents Layer”来执行具体的扫描任务。
2.  **MCP Server Scan (MCP服务器扫描)**：这个引擎专门针对Model Context Protocol (MCP)服务器进行扫描，评估其安全性。MCP是一个用于连接AI代理和工具的协议。
3.  **LLM Jailbreak Evaluation (大语言模型越狱评估)**：这个引擎用于评估大语言模型的安全性，特别是针对越狱攻击的抵御能力。它会利用下方的“Knowledge Base”来获取攻击方法和数据集。
这些核心引擎在执行任务时，会从下方的两个关键部分获取支持：

左边是“AI Agents Layer (AI代理层)”。这一层提供了一组代理，用于执行具体的扫描和红队任务：
1.  **Infra Scan Agent (基础设施扫描代理)**：专门用于执行AI基础设施的扫描任务，与“AI Infra Scan”引擎配合工作。
2.  **Scan Agent (扫描代理)**：一个通用的扫描代理，可能用于多种类型的扫描任务。
3.  **Red Teaming Agent (红队代理)**：专门用于执行红队攻击模拟，测试系统的安全性。
这些代理为“AI Infra Scan”引擎提供了执行能力。

右边是“Knowledge Base (知识库)”。这一层存储了框架运行所需的各种知识和数据：
1.  **Fingerprints (指纹)**：可能包含各种AI组件、漏洞或攻击的指纹信息，用于识别和匹配。
2.  **CVEs (常见漏洞和披露)**：存储已知的常见漏洞信息，用于检测和评估系统风险。
3.  **MCP Plugins (MCP插件)**：存储与MCP协议相关的插件信息，可能用于扩展MCP服务器的功能或进行安全评估。
4.  **Jailbreak Datasets (越狱数据集)**：存储用于评估大语言模型越狱攻击的数据集，包含各种攻击方法和示例。
“Knowledge Base”为“LLM Jailbreak Evaluation”引擎提供了必要的攻击方法和数据。

信息的流动顺序总结如下：
1.  用户通过“用户界面”发起请求或操作。
2.  请求被传递到“后端服务”进行处理和协调。
3.  “后端服务”调用“核心引擎”执行具体的扫描或评估任务。
4.  “AI Infra Scan”引擎利用“AI Agents Layer”中的代理来执行AI基础设施的扫描。
5.  “LLM Jailbreak Evaluation”引擎利用“Knowledge Base”中的数据和数据集来评估大语言模型的越狱风险。
6.  整个过程中，“Plugin Management”、“Storage”和“LLM Providers”等组件提供必要的支持和资源。

这张图清晰地展示了AI-Infra-Guard框架的分层架构和各组件之间的协作关系。它揭示了该方法的核心思想：将AI代理的攻击面分层，并为每一层匹配合适的检测范式。例如，对于AI基础设施层，使用基于规则的匹配（可能利用“Fingerprints”和“CVEs”）；对于MCP服务器和代理技能包，使用LLM驱动的代理审计；对于大语言模型本身，使用多轮黑盒红队评估和越狱测试。这种分层的方法使得框架能够全面地评估AI系统的安全性，并针对不同的攻击层面采用最有效的检测手段。

---

![Figure 2: The infrastructure-scanning pipeline (M1). Targets (IP lists, ranges, ](fig1_1.webp)

> Figure 2: The infrastructure-scanning pipeline (M1). Targets (IP lists, ranges, domains, or URLs) flow through fingerprint analysis (scanning-engine initialization, AI-framework identification, CVE matching, and framework risk analysis) and an infrastructure-scan agent (dynamic page rendering, visual asset capture, and multimodal risk assessment), producing a security score, an asset inventory, vulnerability details, and a business-impact summary.

这张图（图2）展示了AI-Infra-Guard框架中的基础设施扫描管道（M1），它详细描述了从确定扫描目标到生成最终安全报告的整个流程。

首先，我们来看最左边的“Scan Targets”（扫描目标）部分。这个模块列出了四种可能的输入类型，它们是整个扫描流程的起点：
*   **IP List**（IP列表）：用户可以提供一个具体的IP地址列表作为扫描目标。
*   **IP Range**（IP范围）：用户也可以指定一个IP地址范围，例如192.168.1.0/24。
*   **Domain List**（域名列表）：用户可以提供一个域名列表，例如["example.com", "test.org"]。
*   **URL List**（URL列表）：用户还可以提供一个URL列表，例如["https://example.com/api", "https://test.org/service"]。
这些目标数据通过虚线箭头流向中间的“Fingerprint Analysis”（指纹分析）模块，表示数据的输入。

接下来是中间的“Fingerprint Analysis”（指纹分析）模块。这个模块负责对输入的目标进行初步的分析和识别，它包含四个按顺序执行的步骤：
1.  **Scanning Engine Init**（扫描引擎初始化）：这是指纹分析的第一步，负责初始化扫描工具或引擎，为后续的分析做准备。
2.  **AI Framework Identification**（AI框架识别）：在引擎初始化后，系统会尝试识别目标中使用的AI框架。这一步是关键，因为它决定了后续分析的重点。
3.  **CVE Matching**（CVE匹配）：识别出AI框架后，系统会将其与已知的CVE（通用漏洞披露）数据库进行匹配，查找是否存在已知的安全漏洞。
4.  **Framework Risk Analysis**（框架风险分析）：基于CVE匹配的结果以及其他可能的风险因素，系统会对识别出的AI框架进行风险评估。
这四个步骤通过实线箭头连接，表示数据或控制流从一个步骤流向下一个步骤。完成指纹分析后，结果通过虚线箭头流向右侧的“Infra Scan Agent”（基础设施扫描代理）模块。

然后是“Infra Scan Agent”（基础设施扫描代理）模块。这个模块负责执行更深入的动态分析和风险评估，它包含四个步骤：
1.  **Dynamic Page Rendering**（动态页面渲染）：这一步可能涉及模拟用户交互，渲染目标网站的动态内容，以便进行更全面的分析。
2.  **Visual Asset Capture**（视觉资产捕获）：系统会捕获目标网站的视觉元素，如图标、图像等，这些信息可能用于进一步的分析或作为资产清单的一部分。
3.  **Multimodal Analysis**（多模态分析）：这一步可能结合多种数据源（如文本、图像、结构化数据）进行分析，以提供更全面的风险评估。
4.  **AI Infra Risk Assessment**（AI基础设施风险评估）：这是基础设施扫描代理的最后一步，它会综合前面的分析结果，对AI基础设施的整体风险进行评估。
这四个步骤同样通过实线箭头连接，表示数据的流动。完成基础设施扫描后，结果通过虚线箭头流向最右边的“Output”（输出）模块。

最后是“Output”（输出）模块。这个模块展示了扫描流程的最终结果，包括：
*   **Security Score**（安全评分）：一个综合评分，表示目标AI基础设施的整体安全状况。
*   **Asset Inventory**（资产清单）：扫描过程中发现的所有资产的列表，包括IP、域名、服务等。
*   **Vuln Details**（漏洞详情）：发现的漏洞的具体信息，包括CVE编号、描述、严重程度等。
*   **Business Impact**（业务影响）：评估这些漏洞对业务可能造成的潜在影响。
这些输出结果是整个扫描管道的最终产物，为用户提供了关于目标AI基础设施安全状况的全面视图。

总结来说，这张图揭示了AI-Infra-Guard框架中基础设施扫描管道的工作流程：首先确定扫描目标，然后对这些目标进行指纹分析和漏洞识别，接着进行更深入的动态扫描和风险评估，最后生成详细的安全报告。这个流程是分层的、逐步深入的，旨在全面评估AI基础设施的安全风险。

---

![Figure 3: The MCP-auditing pipeline (M2). From a target (local source, a remote ](fig2_1.webp)

> Figure 3: The MCP-auditing pipeline (M2). From a target (local source, a remote repository, or a live MCP URL), a recon agent builds project understanding, an MCP-scan agent performs static analysis and runtime interaction to find vulnerabilities and malicious behavior, and a vulnerability-review agent validates findings through dependency checks, sandboxed deployment, and dynamic risk validation, yielding a security score, risk details, and fix suggestions.

这张图展示了MCP审计管道（M2）的工作流程，它清晰地描绘了一个多层次的安全审计过程，旨在评估AI代理或其相关组件的安全性。整个流程从左侧的“扫描目标”（Scan Targets）开始，经过三个主要的代理模块，最终在右侧生成“输出”（Output）。

首先，我们来看“扫描目标”部分。这里列出了三种可能的审计对象：本地源代码（Local Source Code）、远程代码仓库（Remote Repository）或远程MCP URL（Remote MCP URL）。这些是审计的起点，系统将从这些来源获取待分析的项目信息。

接下来是第一个主要模块：“侦察代理”（Recon Agent）。这个模块负责对目标项目进行初步的信息收集和理解。它的处理流程依次是：
1.  **项目结构分析**（Project Structure Analysis）：分析项目的目录结构、文件组织等。
2.  **配置与环境解析**（Config & Env Parsing）：解析项目的配置文件和环境变量，了解其运行时设置。
3.  **API端点发现**（API Endpoint Discovery）：识别项目中暴露的API接口。
4.  **依赖映射**（Dependency Mapping）：梳理项目所依赖的库、框架或其他组件。
经过这些步骤后，“侦察代理”会生成一份“项目分析报告”（Project Analysis Report）。这份报告是后续分析的基础，它包含了关于目标项目的全面信息。

然后，信息流向第二个主要模块：“MCP扫描代理”（MCP Scan Agent）。这个模块接收“侦察代理”生成的“项目分析报告”，并进行更深入的安全检测。它的处理流程包括：
1.  **静态分析与运行时交互**（Static Analysis & Runtime Interaction）：结合静态代码分析和动态运行时行为观察来检查项目。
2.  **漏洞模式匹配**（Vuln Pattern Matching）：将项目中的代码或行为与已知的漏洞模式进行比对。
3.  **恶意行为检测**（Malicious Behavior Detection）：识别可能存在的恶意代码或行为。
4.  **错误配置检测**（Misconfiguration Detection）：检查项目是否存在安全相关的错误配置。
经过这些检测后，“MCP扫描代理”会生成一个“潜在风险列表”（Potential Risk List），其中包含了所有被识别出的潜在安全问题。

随后，信息流向第三个主要模块：“漏洞审查代理”（Vuln Review Agent）。这个模块负责对“潜在风险列表”中的条目进行验证和进一步分析。它的处理流程是：
1.  **依赖检查**（Dependency Check）：检查项目依赖的库是否存在已知漏洞。
2.  **沙箱部署**（Sandbox Deployment）：在隔离的沙箱环境中部署或模拟项目，以进行更安全的测试。
3.  **攻击载荷生成**（Exploit Payload Generation）：尝试生成针对已识别漏洞的攻击载荷，以验证其有效性。
4.  **动态风险验证**（Dynamic Risk Validation）：在运行时动态验证风险的真实性和严重程度。
这个模块最终会产出“验证结果”（Validation Results），这些结果是确定风险是否真实存在以及其严重程度的关键。

最后，在最右侧的“输出”部分，汇总了整个审计过程的结果，包括：
*   **安全评分**（Security Score）：一个综合评分，反映目标项目的整体安全状况。
*   **风险详情**（Risk Details）：关于已识别风险的详细描述，包括类型、位置和影响。
*   **修复建议**（Fix Suggestions）：针对已识别风险提供的具体修复建议或缓解措施。

数据或信息的流动顺序是：从“扫描目标”选择一个或多个对象，然后由“侦察代理”进行分析并生成报告，该报告被传递给“MCP扫描代理”进行漏洞检测并生成潜在风险列表，接着该列表被传递给“漏洞审查代理”进行验证并生成验证结果，最终所有这些信息被汇总到“输出”部分，提供最终的安全评估结果。这个流程揭示了该方法的具体运作方式：它通过分层的、多阶段的代理来处理不同的安全审计任务，从初步的信息收集到深入的漏洞检测，再到最终的验证和报告，形成一个完整的审计管道。

---

![Figure 4: The jailbreak-evaluation harness (M4). Given test cases, a target mode](fig3_1.webp)

> Figure 4: The jailbreak-evaluation harness (M4). Given test cases, a target model, and a judge model, a red-teaming agent initializes an attack strategy and applies a library of enhanced jailbreak attacks (role-play/DAN, cipher and encoding, context forcing, and more), verifying attack success through the judge. The output is a safety rating together with the successful jailbreak prompts and their evaluation basis.

这张图（图4）展示了论文中提出的“越狱评估 harness（M4）”的工作流程，它是一个用于测试目标模型安全性的系统框架。我们可以将其分为三个主要部分：输入、红队代理（Red Teaming Agent）和输出，信息按照从左到右的顺序流动。

首先，在最左侧的“输入”部分，包含了三个关键元素：
1.  **测试用例（Test Cases）**：这些是用于评估目标模型的具体问题或指令集，它们构成了红队代理进行攻击的基础。
2.  **判断模型（Judge Model）**：这个模型负责评估目标模型对测试用例的响应是否成功“越狱”，即是否绕过了其应有的安全限制或行为准则。
3.  **目标模型（Target Model）**：这是被测试的对象，即我们想要评估其安全性的AI模型。

接下来是中间的“红队代理”部分，这是整个流程的核心执行者，它包含几个关键步骤：
1.  **攻击策略初始化（Attack Strategy Initialization）**：红队代理首先根据输入的测试用例等信息，制定一个初始的攻击策略。这个策略指导后续的攻击行为。
2.  **增强型越狱攻击（Enhanced Jailbreak Attacks）**：这是红队代理执行的核心攻击手段。图中列出了几种具体的攻击方法，包括：
    *   **DAN / 角色扮演（Role-Play）**：通过让模型扮演特定角色或使用特定身份来尝试绕过限制。
    *   **密码/编码（Cipher / Encoding）**：使用加密或编码技术来隐藏恶意指令或请求。
    *   **上下文强制（Context Forcing）**：通过构造特定的上下文环境来诱导模型产生违规行为。
    *   **...**：表示还有其他未列出的攻击算子。
    这些攻击方法构成了一个攻击库，红队代理会从中选择并应用合适的攻击来挑战目标模型。
3.  **攻击成功验证（Attack Success Verification）**：在红队代理应用了攻击之后，会使用之前输入的“判断模型”来验证攻击是否成功。判断模型会评估目标模型的响应是否符合“越狱”的标准。

最后，在最右侧的“输出”部分，展示了评估的结果：
1.  **安全评级（Safety Rating）**：根据攻击测试的结果，给出目标模型的安全等级，表明其抵御越狱攻击的能力。
2.  **成功的越狱提示（Successful Jailbreak Prompts）**：记录下那些成功导致目标模型“越狱”的具体输入提示或指令。
3.  **评估依据（Evaluation Basis）**：提供判断攻击是否成功的标准和理由，通常由判断模型给出。

数据的流动顺序是：输入的测试用例、判断模型和目标模型被提供给红队代理。红队代理首先初始化攻击策略，然后应用增强型越狱攻击来挑战目标模型。攻击的结果随后被送回判断模型进行攻击成功验证。最终，验证的结果（包括安全评级、成功的越狱提示和评估依据）作为输出呈现出来。这个流程清晰地展示了如何系统地评估一个AI模型的安全性，特别是其抵御越狱攻击的能力。

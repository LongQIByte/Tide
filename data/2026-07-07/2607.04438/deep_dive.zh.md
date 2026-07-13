# ResearchStudio-Reel: Automate the Last Mile of Research from Paper to Poster, Video, and Blog

[arXiv](https://arxiv.org/abs/2607.04438) · [HuggingFace](https://huggingface.co/papers/2607.04438) · ▲61

## 摘要（原文）

> Research dissemination, turning a paper into a poster, a talk video, and a blog post, is still a manual last mile. Prior automation treats each artifact in isolation that each re-extract the paper from scratch, usually ship one-way renders the author cannot reopen in PowerPoint or Word, and gates quality on soft VLM-preference scores that plateau while load-bearing sections still read as empty. We argue this last mile is best built as a composition of skills: thin agent-readable contracts that share one upstream extractor and wrap deterministic primitives in a measured-fill loop whose exits are hard pass/fail render gates. We instantiate this as ResearchStudio-Reel, five Claude Code and Codex skills organized into one shared extractor (Paper2Assets), three editable generators (Paper2Poster, Paper2Video, Paper2Blog), and one interactive convergence layer (Paper2Reel). Paper2Assets extracts each paper once into a shared bundle that can be reused by every downstream skill; The three generators produce a print-ready poster, a synchronized talk video, and a bilingual blog that stay factually consistent and round-trip through PowerPoint or Word; Paper2Reel then binds all three into a self-contained HTML viewer whose section-level clicks jump the video, slides, captions, and blog to matching content. On the Paper2Poster benchmark, our posters lead every aesthetic and information sub-criterion against both prior automated systems and single-shot frontier LLMs, surpassing the authors' own on aesthetics under two held-out VLM judges and winning overall on 84% to 93% of papers; capability audits further show that, by uniquely pairing narration-aligned on-slide highlights with a bilingual blog gated by layout-aware DOCX repair, ResearchStudio-Reel is the only pipeline to ship all three editable artifacts. Project is available at https://aka.ms/ResearchStudio

## 摘要（中译）

研究传播（Research dissemination），即将一篇论文转化为海报（poster）、演讲视频（talk video）和博客文章（blog post），目前仍是一个需要人工完成的“最后一公里”工作。先前的自动化方法将每个成果孤立处理，每个成果都从零开始重新提取论文内容，通常只能单向生成作者无法在PowerPoint或Word中重新打开的文件，并且将质量评估基于软视觉语言模型（VLM）偏好分数，而这些分数在关键部分仍有空白时就会达到瓶颈。我们认为，这“最后一公里”最好被构建为一组技能的组合：轻量级的、智能体可读的契约（thin agent-readable contracts），它们共享一个上游提取器（upstream extractor），并在一个受控填充循环（measured-fill loop）中包装确定性原语（deterministic primitives），其出口是严格的通过/失败渲染门（hard pass/fail render gates）。我们将这一理念具体化为ResearchStudio - Reel，它由五个Claude Code和Codex技能组成，组织成一个共享提取器（Paper2Assets）、三个可编辑的生成器（Paper2Poster、Paper2Video、Paper2Blog）和一个交互式收敛层（Paper2Reel）。Paper2Assets将每篇论文提取一次到一个共享包（shared bundle）中，该包可被每个下游技能重复使用；这三个生成器生成一份可打印的海报、一个同步的演讲视频和一篇双语博客，它们在事实内容上保持一致，并且可以通过PowerPoint或Word双向转换；然后，Paper2Reel将这三者绑定到一个独立的HTML查看器（HTML viewer）中，其中章节级别的点击可以将视频、幻灯片、字幕和博客跳转到匹配的内容。在Paper2Poster基准测试（Paper2Poster benchmark）中，我们的海报在每个美学和信息子标准上都领先于先前的自动化系统和单次前沿大型语言模型（LLMs），在两位保留的视觉语言模型评审员（VLM judges）的美学评估中超过了作者自己的成果，并且在84%到93%的论文上整体获胜；能力审计（capability audits）进一步表明，通过独特地将与叙述对齐的幻灯片亮点（on - slide highlights）与受布局感知的DOCX修复（layout - aware DOCX repair）控制的双语博客相结合，ResearchStudio - Reel是唯一能够交付所有三个可编辑成果的流程。该项目可在https://aka.ms/ResearchStudio获取。

## 背景剖析

**背景剖析**

研究传播的最后环节——将学术论文转化为会议海报、演讲视频和科普博客——长期依赖人工完成，而这正是研究者最忙碌的阶段。这些成果需要面向不同受众：会议海报用于现场展示，视频用于线上分享，博客则面向非专业读者。当前自动化方案存在三个核心缺陷：首先，每个成果都需单独提取论文信息，导致跨媒介的事实一致性（如图表编号与引用）需要手动校对；其次，生成的文件多为不可编辑的PDF或视频，作者无法用PowerPoint或Word进行后续修改；最后，质量评估依赖模糊的视觉评分，可能忽略关键内容的完整性。

本文提出的ResearchStudio-Reel通过模块化架构解决这些问题。其核心思路是构建一个共享的知识提取层（Paper2Assets），一次性处理论文中的图表、元数据和关键主张，然后通过三个可编辑生成器（海报、视频、博客）复用这些信息。例如，视频生成器直接基于可编辑的PowerPoint幻灯片制作，确保叙事与视觉高亮同步。更关键的是，系统引入了“确定性循环”机制，只有在内容完全符合标准时才会结束生成，而非依赖机器学习模型的主观评分。

该方案与前人工作的本质区别在于：1）首次实现跨媒介的事实一致性，避免重复劳动；2）所有输出均为原生可编辑格式，支持后续调整；3）通过统一的交互式界面（Paper2Reel）将三个成果关联，读者可点击海报章节跳转至对应视频片段和博客内容。实验表明，其生成的海报在美学和信息完整性上超越现有系统和人类作者，视频则实现了字幕与旁白的精确对齐。这种将分散任务整合为协同工作流的方法，标志着研究传播自动化从“单点工具”向“系统级解决方案”的转变。

## 方法图解

![Figure 2: The ResearchStudio-Reel pipeline. One PDF in, three editor-ready artif](fig2_1.webp)

> Figure 2: The ResearchStudio-Reel pipeline. One PDF in, three editor-ready artifacts out, with one shared extraction stage in the middle. A single Paper2Assets pass produces the bundle that Paper2Poster, Paper2Video, and Paper2Blog each consume verbatim, and Paper2Reel binds the three into one navigable surface. Sharing the same section identifiers, figure handles, and claim anchors keeps the artifacts mutually cross-referenced rather than disjoint.

这张图展示了ResearchStudio - Reel的完整工作流程，我们可以从左到右、按数据/信息的流动顺序来拆解每个部分：

首先，最左侧的输入是“Paper (pdf / link)”，也就是一篇论文的PDF文件或者链接，这是整个流程的起始点，箭头指向第一个模块“Paper2Assets”。

“Paper2Assets”模块的作用是提取论文的资产，它的操作是“/paper2assets 'Convert my paper to asset'”。这个模块输出的“Reusable Assets（可复用资产）”包括几种格式的文件：JSON格式的文件（如narration.json、captions.json、metadata.json）、TXT格式的文件（paper.txt）和JPEG格式的文件（figures/ logos/）。这些资产是后续所有下游技能（生成器）的共同输入，也就是说，Paper2Poster、Paper2Video和Paper2Blog都会使用这个模块提取的资产，并且是“verbatim（逐字逐句，原样）”消费这些资产，这保证了后续生成的内容基于同一份提取的信息。

接下来，从“Reusable Assets”出发，有三个并行的生成器模块：“Paper2Poster”、“Paper2Video”和“Paper2Blog”，它们的操作都是“/paper2[poster/video/blog] Create ...”。这三个生成器属于“Editable Artifacts（可编辑工件）”阶段，它们分别生成不同的可编辑输出：Paper2Poster生成打印就绪的海报，Paper2Video生成同步的演讲视频，Paper2Blog生成双语博客。并且这些生成器生成的工件可以在PowerPoint或Word中往返（即可以导入导出而不丢失一致性），因为它们共享相同的章节标识符、图形句柄和声明锚点，这使得不同工件之间是相互交叉引用的，而不是孤立的。

然后，这三个可编辑工件会被传递到最右侧的“Paper2Reel”模块，它的操作是“/paper2reel Create ...”，并且使用了Claude和Codex工具。Paper2Reel的作用是将这三个工件绑定成一个自包含的HTML查看器，在这个查看器中，章节级别的点击可以将视频、幻灯片、字幕和博客跳转到匹配的内容，这实现了不同工件之间的导航和内容关联，属于“Interactive Artifacts（交互式工件）”阶段。

总结整个流程的逻辑：首先通过Paper2Assets提取论文的一次性资产，这些资产被三个可编辑生成器（海报、视频、博客）共享使用，保证内容的一致性和可交叉引用性；然后这三个生成器产出的可编辑工件被Paper2Reel整合成一个交互式的HTML查看器，实现多工件的导航关联。这样的设计解决了之前研究传播手动化、重复提取、不可编辑和内容孤立的问题，通过技能的组合（共享提取器和确定性原语的包装）来实现从论文到多种传播工件的自动化流程。

从结果的角度（结合论文摘要的基准测试），在Paper2Poster基准测试中，该方法生成的海报在每个美学和信息子标准上都领先于之前的自动化系统和单次前沿LLMs，甚至超过了作者自己的手动成果（不过图中主要展示的是流程，结果的具体坐标或对比对象的可视化在图中未详细呈现，但流程设计支撑了这样的结果）。

---

![Figure 3: The Paper2Poster pipeline. A Paper2Assets bundle (paper spec, cleaned ](fig3_1.webp)

> Figure 3: The Paper2Poster pipeline. A Paper2Assets bundle (paper spec, cleaned figures, logos, QR) drives an agent that picks the Method plus secondary figures and composes a self-contained poster.html along four axes: column layout, visual style, title-band header, and the Scan-to-Read block. A staged-fill loop then measures each section (slack + polish) and edits one section per round until every panel reads FULL (90–98%) and every figure is large enough on one axis. Narration audio and header logos are packed in, and the converged page is rendered to PDF and PNG and to an editable, native-shape PowerPoint, released only through a mandatory deliverables gate.

这张图展示了Paper2Poster的完整工作流程，从输入到最终交付成果，清晰呈现了各组件的功能和数据流向：

1. **输入阶段（INPUT）**：  
   首先，`Paper2Assets`模块处理输入，它接收来自Claude或Codex的`paper_spec.md`文件，输出`figures.json`（包含清理后的图表信息）、`logos/`（机构标志）和`qrr/`（二维码资源）。这一步是整个流程的基础，确保后续步骤有统一的资产包。

2. **选择图表（Pick figures）**：  
   该模块从`Paper2Assets`的输出中选择“Method”（方法部分）加上次要图表（目标数量≥2），确定需要展示的核心内容，为后续海报生成提供内容基础。

3. **组合海报（Compose poster.html）**：  
   此模块负责构建海报的HTML结构，从四个维度进行设计：  
   - 布局：支持全栏（full）、半栏（half）或三栏（3-col）；  
   - 视觉风格：提供11种样式选择；  
   - 标题带（Headers）：有5种变体；  
   - 扫描阅读块（Scan - to - Read）：可选择1 - OR或2 - OR模式。  
   这一步将选定的内容和设计参数整合，生成初步的`poster.html`。

4. **分阶段填充循环（Staged - fill loop）**：  
   这是核心的优化循环，包含三个关键步骤：  
   - `Measure`：测量每个部分的“slack”（空白空间）和“polish”（润色程度），评估是否达到“FULL”（目标范围90% - 98%）且每个图表在至少一个轴上足够大；  
   - `Edit ONE section`：如果测量未通过（fail），则编辑一个部分并重新测量；如果通过（pass），则进入下一个环节；  
   - 循环控制：最多进行12轮循环，或通过“circuit breaker”（断路器）终止，确保每个部分都达到“FULL”状态，图表显示充分。  
   循环的状态通过颜色标识：`OVERFLOW`（溢出，红色）、`SPILLAGE`（溢出，橙色）、`FULL`（目标，绿色）、`SPARSE`（稀疏，蓝色）、`EMPTY`（空，灰色）。

5. **资源打包（Audio、Logo）**：  
   在循环收敛后，添加旁白音频（支持Edge TTS、Azure Speech，输出为mp3）和机构标志（如pack header、institute logos），丰富海报的多媒体和视觉元素。

6. **渲染与交付（FINISHING & ARTIFACTS）**：  
   - `Render Poster`：将处理后的`poster.html`渲染为`Finetune HTML`、`Playwright`（可能用于自动化测试或渲染）、`Headless Chromium`（无头浏览器渲染），最终输出PDF和PNG格式；  
   - `PPTX Editable`：生成可编辑的PowerPoint文件，包含原生形状、方程式、文本，并保持1 - 1映射（确保内容可追溯）；  
   - `Deliverable gate Mandatory`：所有成果必须通过这个强制交付门，确保质量符合要求。

7. **最终成果（ARTIFACTS）**：  
   最终交付的成果包括HTML、PPT、PDF、PNG格式的文件，以及可编辑的PowerPoint，这些成果在`Reel`中被整合（图中右侧`Reel`部分提示这是多格式输出的集合）。

整个流程的核心逻辑是：通过`Paper2Assets`共享资产包，`Compose`生成初步海报，`Staged - fill loop`迭代优化每个部分的内容填充，最后打包资源和渲染输出，确保海报在信息完整性（每个部分达到FULL）和视觉呈现（图表足够大）上都满足要求，并且成果可交付、可编辑。

---

![Figure 4: The staged-fill loop, visualized on the Latent Diffusion Models poster](fig4_1.webp)

> Figure 4: The staged-fill loop, visualized on the Latent Diffusion Models poster. A debug overlay boxes every section and colors it by fill verdict (red / amber for EMPTY / SPARSE , green for FULL , orange / magenta for SPILLAGE / OVERFLOW ), annotated with its fill percentage. (a) Initial explorations: the freshly composed draft is uneven, with several underfilled sections and small figures. (b) Fill-loop in progress: the loop measures each section and edits one per round, so cards pass through OVERFLOW and SPARSE as content is added or trimmed. (c) Poster completed: the loop stops once every section reads FULL (90–98%) and every figure is large enough, yielding the shipped poster.

这张图展示了ResearchStudio - Reel中“staged - fill loop”（分阶段填充循环）在生成Latent Diffusion Models（潜在扩散模型）相关学术海报时的工作过程，通过三个阶段（初始探索、填充循环进行中、海报完成）的可视化，解释了该方法如何运作：

### 各组件与信息流动
- **阶段（a）：Initial explorations（初始探索）**：
    - 这个阶段的海报是刚组合好的草稿，各部分的填充情况不均匀。可以看到一些板块（如“Problem”“Motivation”等）的内容较少（标注为EMPTY/SPARSE，对应红色/琥珀色），还有小的图表。信息流动是从初始的草稿状态开始，此时各部分的填充百分比低，需要后续的填充循环来优化。
- **阶段（b）：Fill - loop in progress（填充循环进行中）**：
    - 这个阶段展示了填充循环的工作方式。循环会测量每个板块（section）的填充情况，然后每一轮编辑一个板块。内容会被添加或修剪，所以卡片（板块）会经历OVERFLOW（溢出，可能内容过多）和SPARSE（稀疏，内容不足）的状态，直到达到合适的填充程度。箭头可能表示信息的流动方向，即从一个板块的处理流向另一个板块的处理，或者从测量到编辑的流程。例如，“Method”“Dataset/Benchmark”等板块在这个阶段被逐步优化，内容的丰富度和大小在调整。
- **阶段（c）：Poster completed（海报完成）**：
    - 当每个板块的填充率达到FULL（90 - 98%）且每个图表足够大时，填充循环停止，生成最终的海报。此时所有板块的内容都足够充实，信息完整且视觉上协调。

### 方法的具体运作方式
- 首先，系统会生成一个初始的海报草稿（阶段a），这个草稿的各部分填充不均匀，有些部分内容不足（EMPTY/SPARSE），有些图表较小。
- 然后，进入填充循环（阶段b），系统会逐个测量每个板块的填充情况，然后针对每个板块进行编辑：如果内容不足（SPARSE），就添加内容；如果内容过多（OVERFLOW），就修剪内容。这个过程是迭代的，每一轮处理一个板块，直到所有板块的填充率达到要求（FULL），并且图表的大小合适。
- 最后，当所有板块都满足填充要求（阶段c），填充循环停止，生成最终的海报，这个海报在美学和信息传递方面都达到了较好的效果。

### 结果相关（结合基准测试）
- 在Paper2Poster基准测试中，这种方法生成的海报在每个美学和信息子标准上都领先于之前的自动化系统和单次前沿LLMs（大型语言模型），甚至超过了作者自己的手动制作的海报（从图中“Poster completed”的状态可以看出，最终的海报各部分都填充充分，信息完整，视觉效果良好）。例如，在“Key Results”板块中，新的SOTA（最先进技术）FID（Frechet Inception Distance，用于评估图像质量的指标）值等结果表明，这种方法生成的内容质量更高。

---

![Figure 5: Paper2Video overview. The skill reuses the Paper2Assets bundle, plans ](fig5_1.webp)

> Figure 5: Paper2Video overview. The skill reuses the Paper2Assets bundle, plans narration and duration, delegates deck authoring to the full ppt-master workflow, synthesizes aligned audio and captions, renders visual attention cues, and packages the editable deck with captioned and no-subtitle videos. The root deliverables are video.pptx , video.mp4 , and video_no_subtitles.mp4 , while timelines, captions, audio clips, and visual cues stay under assets/ , the auditable intermediates directory.

这张图展示了ResearchStudio - Reel中Paper2Video的工作流程，我们可以按数据/信息的流动顺序来拆解每个组件和板块：

首先看最左侧的“Assets”区域，这里包含了论文相关的资产文件，比如`paper_spec.md`（论文规范文件）、`narration.json`（叙述相关的JSON文件），还有`logos/`（logo文件夹）和`qr/`（二维码文件夹），这些是整个流程的基础输入资产。

接下来是“Pace narration”部分，这里有目标时长（target duration）、章节ID（section ids）、脚本JSON（script.json）和笔记（notes），它的作用是规划叙述的节奏和内容结构，为后续的音频生成和幻灯片制作提供时间线和内容指引。

然后进入“Run pipeline ppt - master”模块，这个模块的工作流程（Workflow）是使用`ppt - master`工具来处理幻灯片，输出的幻灯片格式是SVG和PPTX（即`Slides: SVG + PPTX`）。这个模块会利用左侧“Assets”和“Pace narration”的输入，来生成幻灯片的结构和内容，同时还会处理音频部分：将叙述（narration）转换为MP3格式的音频文件（`word_timings`可能是与单词时间相关的信息），也就是“Audio”部分的输出是`narration → *.mp3`（word_timings）。

之后是“ANCHOR VISUAL CUES”部分，这里展示了两张幻灯片（Slide 1和Slide 2）的处理情况。对于每张幻灯片，都有对应的脚本行（Script line），比如Slide 1的脚本行是“The figure shows ...”，Slide 2的是“The explains ...”。同时，这里还有相关性（correlation）的计算，比如Slide 1中有30%和26%的相关性，Slide 2中有42%和92%的相关性，这些相关性可能是用来对齐视觉提示（比如图片、文本框等）和脚本内容的，红色和绿色的箭头可能表示不同的对齐或关联方式，目的是合成对齐的视觉注意力提示（visual attention cues）。

再往后是“RENDER”模块，这个模块的作用是渲染视频。它会添加字幕（Add subtitles），字幕内容来自之前的脚本行（比如“The figure shows ...”）；还会“Burn highlights”（烧录高亮，可能是指在视频中突出显示某些内容）和使用“Laser cursor”（激光指针，可能是模拟演示时的指针效果）。渲染的输出是视频（Video），同时还有一些可审计的中间文件，比如时间线（timelines）、字幕（captions）、音频片段（audio clips）和视觉提示（visual cues），这些文件会存放在`assets/`目录下。

最后是“Runtime Fit Gate”和“Re - run Pipeline”部分，“Runtime Fit Gate”是一个质量检查的关卡，如果通过（Pass），就会输出最终的交付物，包括`video.pptx`（可编辑的幻灯片）、`video.mp4`（带字幕的视频）和`video_no_subtitles.mp4`（无字幕的视频）；如果没通过（Off by 30 seconds，可能是时间上的偏差），就会重新运行管道（Re - run Pipeline），直到通过质量检查。

整个流程的核心逻辑是：复用Paper2Assets提取的资产包，规划叙述和时长，将幻灯片制作委托给`ppt - master`工作流，合成语音和对齐的字幕，渲染视觉注意力提示，最后将可编辑的幻灯片和不同版本的视频打包输出。这样生成的幻灯片和视频在事实一致性上保持一致，并且可以在PowerPoint或Word中来回切换（round - trip）。

从图中的组件和箭头流动可以看出，数据的流动是从资产输入开始，经过叙述节奏规划、幻灯片和音频生成、视觉提示合成，再到视频渲染和质量检查，最终输出最终的交付物。如果中间某一步不符合要求（比如时间偏差），就会重新运行管道，确保最终结果的质量。

---

![Figure 8: Paper2Blog DOCX showcase. The figure shows the two required Word deliv](fig8_1.webp)

> Figure 8: Paper2Blog DOCX showcase. The figure shows the two required Word deliverables, the English article and the Chinese article, together with the layout checks discussed in the text: typography balance, figure fit, caption placement, and pagination risk.

这张图（图8）是ResearchStudio-Reel方法中Paper2Blog功能的DOCX输出展示，核心是呈现两个必需的Word交付物（英文文章和中文文章），以及文本中讨论的布局检查（排版平衡、图像适配、标题放置和分页风险）。我们逐部分解析：

首先，图的左侧列出了四个关键的“gate”（检查点），这些是确保博客文档质量的布局检查标准：
1.  **Typography gate (排版平衡)**：由蓝色箭头和文字标注，指向英文博客文档（blog_en.docx）的标题区域。这表示该检查点确保文章的行间距、字体大小等排版元素平衡，使文本看起来整齐易读。
2.  **Figure-fit gate (图像适配)**：由绿色箭头和文字标注，指向英文博客文档中的图表（Figure 1: The Transformer architecture...）。这表示该检查点确保插入的图像（如图表）在文档流中尺寸合适，不会过大或过小，与周围文本协调。
3.  **Caption gate (标题放置)**：由橙色箭头和文字标注，指向英文博客文档中图表下方的标题（Figure 1. The Transformer architecture...）。这表示该检查点确保图像的标题紧随图像之后，位置正确，便于读者理解。
4.  **Pagination gate (分页风险)**：由紫色箭头和文字标注，指向英文博客文档的底部区域。这表示该检查点确保文档分页时不会出现内容断裂或空白页，保证阅读的连续性。

接下来，图中展示了两个主要的Word文档：
-   **blog_en.docx (英文博客文档)**：位于图的左侧，是Paper2Blog生成的一个交付物。文档内容包括：
    -   标题：“NeurIPS 2017 | Attention Is All You Need: Making Attention the Backbone”，以及副标题解释了Transformer模型如何用自注意力机制替代循环和卷积。
    -   正文段落：解释了Transformer模型的背景和创新点。
    -   图表（Figure 1）：展示了Transformer的架构图，包括编码器和解码器的结构。
    -   图表标题和说明：位于图表下方，解释了图表内容。
    -   后续章节标题：“Why attention changes the path length”，以及相关的正文内容。
    -   底部区域：可能涉及分页检查的部分。

-   **blog_zh.docx (中文博客文档)**：位于图的右侧，是Paper2Blog生成的另一个交付物，与英文博客文档内容对应但语言不同。文档内容包括：
    -   标题：“为什么是attention”，以及后续的章节标题如“结果说明了什么”。
    -   正文段落：用中文解释了Transformer模型的动机、多头部注意力的设计以及实验结果。
    -   表格（表1：论文中的关键数字摘要）：展示了实验的关键数据，如BLEU分数。
    -   图表（图2：attention visualization）：展示了注意力机制的可视化结果。
    -   后续章节标题和内容：继续解释模型的细节和优势。

这两个文档（blog_en.docx和blog_zh.docx）是Paper2Blog生成的两个必需的Word交付物。方法的运作方式是：首先通过Paper2Assets提取器从原始论文中提取信息，然后使用Paper2Blog生成器生成这两个双语博客文档。在生成过程中，会应用上述四个“gate”检查点来确保文档的质量：
-   排版平衡（Typography gate）确保文本排版美观。
-   图像适配（Figure-fit gate）确保图像尺寸合适。
-   标题放置（Caption gate）确保图像标题正确。
-   分页风险（Pagination gate）确保分页合理。

通过这种方式，Paper2Blog能够生成高质量的双语博客文档，这些文档在事实一致性、格式和可读性方面都得到了保证。图中展示的这两个文档就是这种方法运作的结果，它们通过了所有的布局检查，展示了方法的有效性。

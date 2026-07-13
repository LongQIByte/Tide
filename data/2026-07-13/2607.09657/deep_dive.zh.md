# Scalable Visual Pretraining for Language Intelligence

[arXiv](https://arxiv.org/abs/2607.09657) · [HuggingFace](https://huggingface.co/papers/2607.09657) · ▲15

## 摘要（原文）

> The rapid progress of large foundation models has been driven predominantly by pretraining on large-scale text corpora. However, many forms of knowledge are conveyed through visual representations, where figures, typeset equations, and page layouts carry rich information that cannot be faithfully or completely captured by text alone. Yet current pretraining approaches discard these visual cues by converting visually rich sources, such as documents and web pages, into plain text for learning language intelligence. This paper challenges the default assumption that language models must be trained on text-only representations and shows that Visual Pretraining is a scalable learner for foundation model intelligence. To this end, we conduct a systematic study of unsupervised visual pretraining paradigms that directly leverage visual documents without text extraction. Across multiple backbones and benchmarks, visual pretraining on the same underlying corpora consistently outperforms text-only pretraining, offering an efficient pathway to scalable language intelligence.

## 摘要（中译）

大型基础模型的快速发展主要由大规模文本语料库的预训练推动。然而，许多形式的知识是通过视觉表示传达的，其中图形、排版方程和页面布局携带了仅通过文本无法忠实或完全捕获的丰富信息。然而，当前的预训练方法通过将视觉丰富的来源（如文档和网页）转换为纯文本以学习语言智能来丢弃这些视觉线索。本文挑战了语言模型必须仅在文本表示上训练的默认假设，并表明视觉预训练是基础模型智能的可扩展学习器。为此，我们对直接利用视觉文档而不进行文本提取的无监督视觉预训练范式进行了系统研究。在多个骨干网络和基准测试中，在相同的基础语料库上进行视觉预训练始终优于仅文本预训练，为可扩展的语言智能提供了一条有效的途径。

## 背景剖析

### 背景剖析  

近年来，大规模基础模型（如GPT、BERT等）的爆发式发展主要依赖于对海量文本数据的预训练。这类技术广泛应用于自然语言处理任务（如问答、翻译、文本生成），旨在让机器理解人类语言并生成有意义的回应。然而，现实世界中大量知识并非仅以文本形式存在——学术论文中的公式、技术文档中的图表、网页中的布局结构等视觉信息，往往包含文本无法完整表达的细节（例如数学符号的排版会影响其语义）。当前的问题在于，大多数预训练方法会将这些视觉丰富的资料（如PDF文档或网页）转换为纯文本后再进行学习，导致视觉线索被丢弃，从而限制了模型对复杂场景的理解能力。  

此前的方法之所以不够理想，主要有两点原因：首先，传统文本预训练忽略了视觉信息与语言的关联性，例如公式中的符号位置可能改变其数学含义；其次，现有视觉-语言模型通常需要额外的标注数据或复杂的对齐机制，难以扩展到大规模无标注场景。例如，将图像中的物体与文本描述配对需要大量人工标注，而直接从原始视觉文档中学习则更为高效。  

本文提出的解决方案是**无监督视觉预训练**，即让模型直接从原始视觉文档（如带公式的论文、多栏布局的网页）中学习，而不依赖文本提取或人工标注。通过设计专门的预训练任务（如预测视觉元素的位置关系或语义关联），模型可以同时理解视觉和语言信息。实验表明，这种视觉预训练在多个基准测试中优于纯文本预训练，证明视觉线索能显著提升语言模型的泛化能力。  

与前人工作的关键差异在于，本文不将视觉信息视为文本的辅助补充，而是将其作为独立的预训练信号。以往研究要么单独处理视觉或语言任务，要么通过复杂的多模态对齐技术结合两者，而本文直接利用视觉文档的原始结构，避免了转换过程中的信息损失。这种方法为构建更强大的基础模型提供了新方向：通过扩展预训练的数据类型（从纯文本到视觉文档），实现更高效、更全面的语言智能。

## 方法图解

（本文无可讲解的插图）

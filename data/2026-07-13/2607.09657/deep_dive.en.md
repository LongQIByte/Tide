# Scalable Visual Pretraining for Language Intelligence

[arXiv](https://arxiv.org/abs/2607.09657) · [HuggingFace](https://huggingface.co/papers/2607.09657) · ▲15

## Abstract (verbatim)

> The rapid progress of large foundation models has been driven predominantly by pretraining on large-scale text corpora. However, many forms of knowledge are conveyed through visual representations, where figures, typeset equations, and page layouts carry rich information that cannot be faithfully or completely captured by text alone. Yet current pretraining approaches discard these visual cues by converting visually rich sources, such as documents and web pages, into plain text for learning language intelligence. This paper challenges the default assumption that language models must be trained on text-only representations and shows that Visual Pretraining is a scalable learner for foundation model intelligence. To this end, we conduct a systematic study of unsupervised visual pretraining paradigms that directly leverage visual documents without text extraction. Across multiple backbones and benchmarks, visual pretraining on the same underlying corpora consistently outperforms text-only pretraining, offering an efficient pathway to scalable language intelligence.

## Background

### Background Analysis  

Recent advances in large foundation models (e.g., GPT, BERT) have primarily relied on pretraining with massive text corpora, enabling applications like question answering, translation, and text generation. However, much real-world knowledge is conveyed through visual cues—such as mathematical equations in papers, diagrams in technical documents, or layouts in web pages—that text alone cannot fully capture. The core problem is that most pretraining methods convert visually rich sources (e.g., PDFs or web pages) into plain text, discarding critical visual information (e.g., the spatial arrangement of symbols in a formula). This limits models’ ability to understand complex, multimodal contexts.  

Previous approaches faced two key limitations: (1) They ignored the intrinsic link between visual and linguistic information (e.g., how layout affects meaning), and (2) Multimodal models often required expensive labeled data or complex alignment mechanisms, making scalability difficult. For instance, aligning objects in images with text descriptions demands manual annotation, whereas learning directly from raw visual documents is more efficient.  

This paper proposes **unsupervised visual pretraining**, where models learn directly from raw visual documents (e.g., papers with formulas, multi-column web layouts) without text extraction or annotations. By designing pretraining tasks (e.g., predicting spatial relationships or semantic associations in visuals), the model simultaneously learns visual and linguistic patterns. Experiments show that visual pretraining outperforms text-only approaches across benchmarks, proving that visual cues enhance language understanding.  

The key innovation lies in treating visual information not as a secondary supplement to text but as a primary pretraining signal. Unlike prior work that either processed vision and language separately or used complex alignment techniques, this approach leverages the raw structure of visual documents, preserving information lost in text conversion. This provides a scalable path to more powerful language intelligence by expanding pretraining beyond text to include visual contexts.

## Method, Figure by Figure

(No figures to walk through.)

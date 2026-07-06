# Does VLA Even Know the Basics? Measuring Commonsense and World Knowledge Retention in Vision-Language-Action Models

[arXiv](https://arxiv.org/abs/2606.19297) · [HuggingFace](https://huggingface.co/papers/2606.19297) · ▲71

## Abstract (verbatim)

> Embodied Vision-Language-Action (VLA) models are typically obtained by fine-tuning powerful pretrained VLMs on robotics data, yet it is unclear how much commonsense and factual knowledge they retain after adaptation. Failures on knowledge-sensitive tasks are ambiguous, conflating missing knowledge with poor generalization of low-level control. We introduce Act2Answer, a lightweight protocol that adapts VLM knowledge benchmarks to VLA evaluation by requiring agents to answer through action. Each question becomes a short tabletop episode where the agent performs a single object-placement action to select among candidate answers, yielding an action-grounded success rate with reduced control confounds. We curate a test suite of such environments across diverse commonsense and world-knowledge categories and introduce layerwise intent probing to localize answer-relevant information across the VLM backbone and action head. In a large-scale study of 7 VLA models and 9 VLM baselines, we systematically rank models across categories, finding that VLAs show solid performance on simple concepts while exhibiting larger gaps on richer semantic categories relative to their source VLMs, that VQA co-training is associated with better knowledge retention, and that answer-relevant signals peak in middle VLA layers but attenuate in upper layers. Act2Answer is available at https://tttonyalpha.github.io/act2answer/.

## Background

### Background Analysis  

#### 1. Technical Context  
With the advancement of AI, embodied agents (e.g., home service robots, automated systems in retail) are being developed for everyday environments. These agents require a rich understanding of commonsense and factual knowledge (e.g., object usage, behavioral appropriateness) to make reasonable decisions in complex scenarios. Vision-Language-Action (VLA) models are proposed as the foundation for such agents, aiming to integrate visual perception, language understanding, and action execution for open-world interaction. However, while VLAs excel in manipulation tasks, it remains unclear whether they retain basic commonsense and world knowledge after robotics fine-tuning.  

#### 2. Previous Limitations  
Existing research focuses on task success rates (e.g., object manipulation or navigation) but overlooks a critical question: Can VLAs still reason based on commonsense after training? For example, a fine-tuned VLA might move a cup successfully but fail to judge that "cups are for holding water, not throwing." Additionally, traditional evaluations rely on task success metrics, making it hard to distinguish between "knowledge gaps" and "control deficiencies." Moreover, while VLM (Vision-Language Model) benchmarks are well-developed, they are text-based and unsuitable for action-oriented embodied agents.  

#### 3. Proposed Solution  
To address this, the paper introduces Act2Answer, a framework that adapts VLM knowledge benchmarks into action-based evaluations for VLAs. Each knowledge question is transformed into a simulated scenario where the agent selects an answer through a single action (e.g., placing an object). This reduces confounding factors from long-horizon planning and control, focusing evaluation on knowledge retention. The authors also introduce layered intent probing, using linear classifiers to analyze knowledge distribution across model layers, revealing how knowledge is retained or lost during fine-tuning.  

#### 4. Unique Approach  
Compared to prior work, Act2Answer’s key innovations are:  
- **Action-oriented evaluation**: Transforms text QA into actionable tasks, aligning with embodied agents’ needs.  
- **Diverse knowledge coverage**: Evaluates VLAs across multiple categories (e.g., attributes, states, emotions).  
- **Layerwise analysis**: Identifies where knowledge is retained or forgotten within the model.  
This approach fills gaps in existing research, providing a principled way to assess VLA knowledge retention.

## Method, Figure by Figure

![Figure 3: Overview of the data curation pipeline used to construct the Act2Answe](fig3_1.webp)

> Figure 3: Overview of the data curation pipeline used to construct the Act2Answer task suite from VLM benchmarks, including selection, filtering and normalization, and conversion

This figure (Figure 3) illustrates the **data curation pipeline** used to construct the Act2Answer task suite from Vision-Language Model (VLM) benchmarks, clarifying how generic VLM knowledge assessment is adapted for evaluating Vision-Language-Action (VLA) models.

The process begins with the "Diverse VLM Benchmarks" on the left. This dashed box contains different knowledge domains, such as "Temporal," "Cultural," "Social," "Normative," "Biological," "Quantitative," and "Physical." Different colored shapes (e.g., triangles, stars, circles, squares) under each category represent specific questions or knowledge points within that domain, indicating that the input data is diverse, covering various types of common sense and world knowledge.

Next, this benchmark data is fed into the "LLM" (Large Language Model) module. This module represents the original VLM or large language model, not yet optimized for action tasks. Additionally, there is an "LLM Prompt" module with the content "Convert into binary QA ...," which converts the original VLM benchmark questions into a binary question-answer format suitable for subsequent processing, likely to simplify the questions and make them easier to convert into action tasks.

Then, the data and prompts flow to the "Human review & edits" stage via a blue arrow. This stage, represented by three human figures with hard hats, indicates a human-in-the-loop step to review and edit the converted data, ensuring data quality and relevance. At this stage, the data is processed in a document format (with icons of images and text), which may mean that human reviewers check the matching between questions and related images (if any) and whether the question phrasing is suitable for action execution.

After human review, the data flows to the "Act2Answer Environment" on the right via a purple arrow. This environment shows a real-world robot manipulation scenario: a robotic arm is placing a cube on a mat with a fish, with the goal "Put cube on fish with more yellow fins." This scene intuitively demonstrates the core idea of Act2Answer: converting knowledge questions into a specific action task, i.e., selecting the correct answer through an object-placement action. In this environment, different regions (e.g., Z⁻, Z⁰, Z⁺) may represent different positions or conditions to evaluate whether the model's action selection is correct.

The information flow order of the entire process is: **Diverse VLM benchmark data → Conversion to binary QA format (via LLM and prompt) → Human review and editing → Conversion to an action-oriented Act2Answer environment**. The purpose of this process is to adapt the generic VLM knowledge assessment to the evaluation of VLA models, measuring the model's knowledge retention more accurately by requiring the model to answer questions through actions, thus reducing confusion from low-level control.

From the method's perspective, this figure reveals how Act2Answer works:
1. **Data Source**: Existing VLM benchmarks are used, covering multiple knowledge categories to ensure comprehensive evaluation.
2. **Data Conversion**: VLM benchmark questions are converted into a binary QA format to simplify the question structure, making it more suitable for action tasks.
3. **Human Review**: Human intervention ensures data quality and relevance, reducing noise.
4. **Action-Oriented Evaluation**: Questions are converted into specific action tasks (e.g., object placement), and the model's knowledge level is evaluated by its action selection. This approach can more directly measure whether the model has the knowledge required to answer the question, rather than just evaluating its language generation ability.

The advantage of this method is that it evaluates knowledge retention through the success of action execution, thus reducing potential control confusions (e.g., insufficient generalization of low-level control) present in traditional language evaluations. In this way, Act2Answer can more accurately measure the knowledge retention of VLA models in common sense and world knowledge and compare them with their source VLMs.

---

![Figure 4: Probing results for internal representations of VLA models on four tas](fig4_1.webp)

> Figure 4: Probing results for internal representations of VLA models on four tasks from the Act2Answer task suite. In the legend, Prefix labels indicate representations from the VLM component, whereas Action labels indicate representations from the Action component.

This figure presents probing results for internal representations of Vision-Language-Action (VLA) models on four tasks from the Act2Answer task suite. Each subplot corresponds to a task category (Attribute, State, Emotion, Quantity), with the x-axis representing the layer index of the model (ranging from 0 to 36) and the y-axis showing the validation accuracy (in percentage). The legend indicates different VLA models using various colors, including SmolVLA, π₀, OpenVLA, SpatialVLA, Magma, and Xiaomi-Robotics-R0. The line types (solid and dashed) represent representations from the VLM component (Prefix) and the Action component, respectively.

Specifically, this figure illustrates how the Act2Answer method operates:
1. **Task Design**: Act2Answer adapts VLM knowledge benchmarks to VLA evaluation by requiring agents to answer through actions. Each question becomes a short tabletop episode where the agent performs a single object-placement action to select among candidate answers, yielding an action-grounded success rate with reduced control confounds.
2. **Layerwise Intent Probing**: By conducting layerwise intent probing in the VLM backbone and action head of VLAs, it localizes answer-relevant information. This helps understand which information in different layers is most important for answering specific types of questions.
3. **Result Analysis**: The figure shows the performance of different models across the four task categories. For instance, in the "Attribute" task, the Magma model exhibits higher accuracy in the middle layers (around layers 12 to 24), while in the "State" task, both Magma and Xiaomi-Robotics-R0 models perform well in the middle layers.

In terms of coordinates, the x-axis represents the layer index of the model, and the y-axis represents the validation accuracy. The comparison objects are different VLA models and their performances in the VLM component and Action component. The conclusions are that VLAs show solid performance on simple concepts but exhibit larger gaps on richer semantic categories relative to their source VLMs. VQA co-training is associated with better knowledge retention, and answer-relevant signals peak in middle VLA layers but attenuate in upper layers.

This figure clearly demonstrates the performance of different models across various task categories, helping us understand the internal mechanisms of VLA models when handling different types of knowledge.

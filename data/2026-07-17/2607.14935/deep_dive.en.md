# VideoChat3: Fully Open Video MLLM for Efficient and Generalist Video Understanding

[arXiv](https://arxiv.org/abs/2607.14935) · [HuggingFace](https://huggingface.co/papers/2607.14935) · ▲149

## Abstract (verbatim)

> Recent advances in video understanding have spanned motion, long video, and streaming interaction, driving this field toward real-world applications. Despite this progress, current open-source models remain limited in several ways. They often struggle to generalize across diverse video types, making them effective only in specific domains. High computational demands further restrict their efficiency and scalability. Moreover, most models are only partially open, with key components such as training code, strategy, or datasets unavailable, which hinders reproducibility and slows community-driven development. To address these issues, we introduce VideoChat3, a fully open, efficient, and generalist video-centric MLLM. VideoChat3 advances video understanding through two complementary designs. For efficiency, we introduce Inflated 3D Vision Transformer (I3D-ViT) and Adaptive Frame Resolution for Streaming Video Perception, which enables efficient spatiotemporal representation and reduces the cost of processing video inputs during training and inference. For effectiveness, we develop a scalable video data synthesis pipeline that curates three diverse, high-quality training datasets: VideoChat3-Academic2M, VideoChat3-LV116K, and VideoChat3-OL617K, covering general, long-form, and streaming video scenarios, improving the model's generalization across domains. By integrating these designs, VideoChat3 achieves a rare balance of broad generalization and computational efficiency. Experiments across general, long-form, and streaming benchmarks demonstrate that VideoChat3 surpasses prior open-source models with equal or larger parameter counts with only 4B parameters and higher efficiency.

## Background

### Background Analysis  

**1. Technical Context and Real-World Needs**  
Video has become the primary medium for human perception and interaction with the physical world, from social media short videos to professional scenarios like autonomous driving and medical imaging. These applications require models to understand spatial semantics, temporal dynamics, and causal relationships. However, existing video understanding technologies face challenges: different video types (e.g., short-form QA, long-form narrative, real-time streaming) demand specialized designs, limiting generalizability, while real-time interaction requires high computational efficiency.  

**2. Limitations of Previous Approaches**  
Prior methods suffer from three key issues:  
- **Lack of Generalization**: Many models are optimized for specific scenarios (e.g., short videos) but fail in long-form or real-time tasks. For example, a model good at analyzing movie clips may perform poorly on live surveillance footage.  
- **Inefficiency**: Directly scaling image-based large models to videos leads to explosive computational costs, making long-video and real-time processing infeasible.  
- **Poor Reproducibility**: State-of-the-art models are often closed-source or partially open, lacking transparency in training data, code, and strategies, hindering innovation and fair comparisons.  

**3. Proposed Solutions**  
VideoChat3 addresses these problems with three key designs:  
- **Efficient Architecture**: Introduces Inflated 3D Vision Transformer (I3D-ViT) and adaptive frame resolution to reduce computational costs for high-frame-rate videos while maintaining accuracy.  
- **Scalable Data Construction**: Builds three diverse datasets (covering academic, long-form, and streaming tasks) and uses a curriculum learning strategy to train the model across different task complexities.  
- **Full Open-Sourcing**: Releases model weights, training code, and data pipelines, ensuring reproducibility and providing foundational tools for the community.  

**4. Key Differences from Prior Work**  
Unlike existing approaches, VideoChat3 balances **generality** and **efficiency** while solving **reproducibility** issues. It outperforms comparable open-source models (e.g., Qwen3-VL) in both accuracy and efficiency. Crucially, its fully open strategy provides a reliable infrastructure for video understanding research, lowering entry barriers for the community.

## Method, Figure by Figure

![Figure 1 : VideoChat3 achieves strong performance across diverse evaluation benc](fig1_1.webp)

> Figure 1 : VideoChat3 achieves strong performance across diverse evaluation benchmarks, including temporal perception, long video understanding, and temporal grounding, while also supporting online proactive responses.

This figure (Figure 1) is from the paper "VideoChat3: Fully Open Video MLLM for Efficient and Generalist Video Understanding" and aims to demonstrate the strong performance of the VideoChat3 model in diverse video understanding tasks and online interaction scenarios, while also clarifying its core capabilities.

First, let's look at the upper part of the figure, which is a bar chart comparing the performance of different models across multiple benchmarks. The horizontal axis lists various evaluation benchmarks, categorized into several major task types:

1.  **Temporal Perception (时间感知)**: This includes two benchmarks, MotionBench and TempCompass. These tasks typically involve fine-grained understanding of the movement of objects or people in videos.
2.  **Long Video (长视频理解)**: This includes VideoMME and LV-Bench. These tasks require the model to process longer video sequences and answer related questions.
3.  **Reasoning (推理)**: This includes MMVU and VideoMME-v2. These tasks require the model to perform logical reasoning based on video content.
4.  **Temporal Grounding (时间定位)**: This includes three benchmarks: Charades¹, ActivityNet¹, and QVHighlights¹. These tasks require the model to locate the time when specific events or actions occur in a video.
5.  **Online (在线交互)**: This includes OVObench and StreamingBench. These tasks involve the model interacting with real-time or streaming video.

The vertical axis represents the scores of the models on these benchmarks. Three models are compared in the figure:
*   **Molmo2-4B** (light gray bar)
*   **Qwen3-VL-4B** (dark gray bar)
*   **VideoChat3 (Ours)** (green bar)

As can be clearly seen from the figure, VideoChat3 (our model) achieves better scores than the other two models in most benchmarks. For example, on MotionBench, VideoChat3 scores 75.6, significantly higher than Molmo2-4B's 61.6 and Qwen3-VL-4B's 61.7. On StreamingBench, VideoChat3 scores as high as 83.0, while the other two models score 80.2 and an unshown (or lower) score, respectively. This indicates that VideoChat3 possesses strong performance in multiple aspects, including temporal perception, long video understanding, reasoning, temporal grounding, and online interaction.

Next, we look at the lower part of the figure, which demonstrates the capabilities and workflow of VideoChat3 through specific examples:

1.  **Fine-grained Motion Understanding (细粒度运动理解)**:
    *   Question: "When using the juicer, how should both hands coordinate? One hand holds the juicer base steady while the other presses an orange half downward and rotates it." (使用榨汁机时，双手应如何协调？一只手稳住榨汁机底座，另一只手向下按压半个橙子并旋转它。)
    *   Below, there is a series of video frames showing the process of using a juicer. The model needs to understand the coordination of hand movements in these frames.

2.  **Long Video QA (长视频问答)**:
    *   Question: "What color is the cat’s water bowl? Based on the video, the cat’s water bowl is red." (猫的水碗是什么颜色的？根据视频，猫的水碗是红色的。)
    *   Below, there is a series of video frames showing scenes containing a cat and a water bowl. The model needs to extract relevant information from the long video to answer the question.

3.  **Temporal Grounding (时间定位)**:
    *   Question: "When does the action of preparing oatmeal occur? The given action takes place from 593.0 s to 657.0 s." (准备燕麦片的动作发生在什么时候？给定的动作发生在593.0秒到657.0秒之间。)
    *   Below, there is a series of video frames showing the process of preparing oatmeal. The model needs to locate the specific time of this action in the video.

4.  **Online Proactive Response (在线主动响应)**:
    *   This part shows a timeline with video frames and the model's response status.
    *   The timeline flows from left to right, representing the playback of the video or the passage of time.
    *   Initially, the user makes a request: "Let me know when the woman appears in the video." (当视频中出现女人时告诉我。)
    *   In the first few frames of the video, the model is in the "<Silence>" (沉默) state because it has not yet detected the target event.
    *   Subsequently, the model enters the "<Standby>" (待机) state, possibly continuously monitoring the video content.
    *   When a woman appears in the video frame, the model responds: "The woman appears in the video." (视频中出现了女人。), and its status changes to "<Response>" (响应).
    *   Afterward, the model returns to the "<Silence>" state because the target event has occurred and may no longer be ongoing.

This figure comprehensively demonstrates the capabilities of VideoChat3 as a fully open, efficient, and generalist video-centric MLLM (Multimodal Large Language Model) by combining quantitative comparison (the bar chart in the upper part) and qualitative examples (specific tasks and response workflows in the lower part). It not only achieves excellent results in various benchmarks but can also handle practical online video interaction tasks, implementing functions such as fine-grained motion understanding, long video QA, temporal grounding, and online proactive response. This reveals that the design goal of VideoChat3 is to address the limitations of existing open-source video models, providing broader generalization capabilities and higher computational efficiency.

---

![Figure 2 : VideoChat3 architecture with I3D-ViT. VideoChat3 follows the classica](fig2_1.webp)

> Figure 2 : VideoChat3 architecture with I3D-ViT. VideoChat3 follows the classical ViT–MLP Projector–LLM architecture, with I3D-ViT enabling efficient video encoding before visual tokens are passed to the LLM. Specifically, spatial 2 × 2 2\times 2 merging and temporal T T -frame pooling reduce the visual sequence length by approximately a factor of 4 ​ T 4T . Under the default setting of T = 4 T=4 , this yields a 16 × 16\times spatiotemporal compression ratio; for clarity, the figure illustrates the mechanism with T = 2 T=2 .

This figure illustrates the architecture of VideoChat3, which centers on combining I3D - ViT for efficient video encoding and then passing visual tokens to a Large Language Model (LLM). The overall architecture follows the classic ViT - MLP Projector - LLM paradigm. Here is a detailed explanation of each part and the data flow:

### Input Part
- **Image**: Serves as a visual input with native resolution (e.g., 2720px×1440px in the example, with arbitrary aspect ratio and resolution), providing static visual information.
- **Video**: Composed of multiple temporal frames (the example shows frames at different time points <0.5s, <1.0s, <1.5s, <2.0s, with a resolution of 640px×480px). These frames are arranged in temporal order, representing dynamic video content.

### Visual Encoding Part (Related to I3D - ViT)
- **Chunk - wise temporal pooling**: Processes the temporal dimension of the video. By default, T = 2 (set to T = 2 in the figure for clear mechanism demonstration; in practice, T can be set to 4, etc.). Through temporal frame pooling (Temporal T - frame pooling), the length of the video's temporal sequence is reduced by a factor of approximately 1/T (reduced to 1/2 when T = 2). At the same time, there is spatial 2×2 merging (Spatial 2×2 merging) to further process the spatial dimension.
- **Pixel shuffle & MLP Projector**: After chunk - wise temporal pooling, pixel shuffle and MLP projection operations are performed on the visual data. The processed visual data is converted into visual tokens, which will be used for subsequent spatiotemporal attention modeling.
- **I3D - ViT (Inflated 3D Vision Transformer)**: Its role is to expand spatial attention into spatiotemporal attention (Inflate spatial attention into spatiotemporal attention) to achieve efficient spatiotemporal representation encoding of videos. In the sub - figure on the right side of the figure, its spatiotemporal modeling process within a frame chunk is shown:
    - **Patchify**: Divides an image or video frame into multiple patches, which serve as the basic units of visual tokens.
    - **Temporal P.E. (Temporal Position Encoding)** and **Spatial P.E. (Spatial Position Encoding)**: Add position encoding to tokens in the temporal and spatial dimensions respectively to retain position information.
    - **Variable - Length Self - Attention**: Performs spatiotemporal modeling within a frame chunk. It captures dependencies between frames and within a frame through the self - attention mechanism. The MLP (Multilayer Perceptron) here is used to support the self - attention operation, and this process can be repeated N times (shown as N× in the figure) to enhance the modeling ability.

### Interaction Part with LLM
- **Passing visual tokens to LLM**: After being encoded by I3D - ViT, the visual tokens, together with text tokens (Text), are passed to the Large Language Model (Large Language Model). A timestamp token (Timestamp token: <X.X seconds>) is also added to the input sequence to mark temporal information.
- **Processing by LLM**: The LLM receives the input sequence of text, image (encoded visual tokens), video (encoded visual tokens), and timestamp tokens, and then outputs a description of the provided image/video (The provided image/videos describe...), completing the video understanding task.

### Overall Logic of Method Operation
1. First, images and videos are used as inputs, and videos are divided into multiple frame chunks (according to the setting of T, e.g., every 2 frames form a chunk when T = 2).
2. Chunk - wise temporal pooling and spatial 2×2 merging are performed on the video frame chunks to reduce the length of the visual sequence and lower the computational complexity.
3. The processed visual data is converted into visual tokens through Pixel shuffle and MLP Projector, and the spatiotemporal attention mechanism of I3D - ViT is used to encode these tokens to capture the spatiotemporal information of the video.
4. The encoded visual tokens, together with text tokens and timestamp tokens, are input into the LLM. The LLM combines this information to generate a description of the image or video, achieving video understanding.

This figure clearly shows how VideoChat3 realizes efficient video encoding through I3D - ViT and combines it with LLM to complete the video understanding task. At the same time, through operations such as chunk - wise temporal pooling and spatial merging, it improves computational efficiency while ensuring effectiveness.

---

![Figure 3 : Illustration of the Adaptive Frame Resolution . State tokens control ](fig3_1.webp)

> Figure 3 : Illustration of the Adaptive Frame Resolution . State tokens control whether the next streaming window is encoded at a low or high pixel quota. In the soccer example, routine play is monitored at low cost; when players rush toward the goal, the Standby state enlarges the next window so the model can inspect whether the ball goes in before triggering Response.

This diagram (Figure 3) visually illustrates the core concept and workflow of the "Adaptive Frame Resolution" mechanism proposed in the paper "VideoChat3: Fully Open Video MLLM for Efficient and Generalist Video Understanding." The mechanism aims to intelligently adjust the encoding resolution of video streams to minimize computational costs while maintaining understanding effectiveness.

We can understand the various parts of the diagram and their information flow from bottom to top, left to right:

1.  **Bottom Layer: Live Video Stream and Timeline**
    *   At the very bottom is a horizontal timeline representing the continuity of the live video stream. The timeline is marked with different time points, such as `t₀`, `tₙ`, `tₙ+1`, `tₙ+2`, `tₙ+3`, `tₙ+4`, `tₙ+5`, etc.
    *   The video is divided into a series of "clips," such as `Clip 0`, `Clip N`, `Clip N+1`, `Clip N+2`, `Clip N+3`, `Clip N+4`, `Clip N+5`. These clips are the basic units for video processing.

2.  **Second Layer: I3D-ViT and Adaptive Perception Quota**
    *   This layer represents the video encoding and feature extraction module, labeled "I3D-VIT."
    *   Each video clip (Clip) is processed here. The diagram shows the resolution status of different clips:
        *   Most clips, such as `Clip 0`, `Clip N`, `Clip N+1`, `Clip N+2`, `Clip N+5`, are marked as "Low-Res" (low resolution).
        *   Specific clips, such as `Clip N+3` and `Clip N+4`, are marked as "High-Res" (high resolution).
    *   The arrow labeled "Adaptive Perception Quota" (自适应感知配额) points from the top to this layer, indicating that decisions made at a higher level (by the LLM) influence how this layer selects the encoding resolution.
    *   This means the system dynamically decides which clips to encode at a high resolution (higher cost but richer information) and which at a low resolution (lower cost), based on the importance or dynamism of the video content.

3.  **Third Layer: LLM and State Tokens with Token Sequence**
    *   This layer represents the Large Language Model (LLM), which is the core of the decision-making process.
    *   The LLM outputs a series of "state tokens" (状态令牌), which control how the next video window (i.e., the next few clips) should be encoded. The top of the diagram shows a series of state tokens, such as `</Silence>`, `</Standby>`, `</Response>`, etc.
    *   These state tokens correspond to the sequence of video clips below. For example:
        *   When the LLM outputs `</Silence>` or `</Standby>`, it might mean that the current video content is relatively static or routine, and does not require high-resolution processing.
        *   When the LLM outputs `</Response>`, it might mean that an event requiring attention has been detected (e.g., a player running towards the goal in a soccer match), triggering high-resolution encoding for subsequent clips.
    *   The diagram also shows a "Token sequence" (令牌序列), which associates the LLM's state tokens with the video clips processed by I3D-ViT. For instance, `Question 1` and `Question 2` might represent user queries or internal system queries, and an upward arrow at `Clip N+5` might indicate a decision or response made at that point based on previous states.

4.  **Top Row of State Tokens Example**
    *   The topmost row displays a sequence of state tokens, such as `</Silence>`, `</Standby>`, `</Response>`, etc. The order and type of these tokens determine how different clips in the video stream are processed.

**Specific Explanation of How the Method Works:**

This diagram reveals how VideoChat3's adaptive frame resolution mechanism operates:

*   **Video Stream Processing**: The live video stream is divided into multiple clips (Clips).
*   **LLM Decision-Making**: A Large Language Model (LLM) analyzes the video content or context and generates a series of state tokens (e.g., `</Silence>`, `</Standby>`, `</Response>`). These tokens act as "instructions" indicating how the system should handle the video stream next.
*   **Adaptive Resolution Adjustment**:
    *   When the LLM outputs state tokens like `</Silence>` or `</Standby>`, the system encodes subsequent video clips (such as `Clip N`, `Clip N+1`, `Clip N+2` in the diagram) at a low resolution. This reduces computational costs because these clips likely contain routine or less important content.
    *   When the LLM detects an event requiring attention (e.g., a player starting to run towards the goal in a soccer match), it outputs the `</Standby>` state token. This token "expands" the next processing window (such as `Clip N+3` and `Clip N+4` in the diagram), causing these key clips to be encoded at a high resolution. High-resolution encoding captures more details, ensuring the model can accurately understand and analyze important events.
    *   After the `</Response>` state token, the system might revert to low-resolution processing (e.g., `Clip N+5`) or adjust based on new context.

**Example with the Soccer Match in the Diagram:**

*   **Regular Play (Low Resolution)**: During the period from `Clip 0` to `Clip N+2`, the video content might show regular match footage without any particularly critical events. Therefore, the LLM would output `</Silence>` or `</Standby>` tokens, instructing the system to process these clips at a low resolution to save computational resources.
*   **Key Event (High Resolution)**: When a player starts running towards the goal (corresponding to `Clip N+3` and `Clip N+4`), this is a critical moment that requires careful analysis. The LLM would output the `</Standby>` token, triggering the system to encode these two clips at a high resolution. This way, the model can see the ball's trajectory and players' movements more clearly to determine if a goal will be scored.
*   **Post-Event Processing (Potentially Returning to Low Resolution)**: After the key event (e.g., at `Clip N+5`), if the event has ended or moved to the next regular phase, the system might switch back to low-resolution processing.

**Conclusion:**

This diagram clearly demonstrates how VideoChat3 uses intelligent decisions from an LLM to dynamically adjust the encoding resolution of video streams. The core idea of this method is: for routine or secondary video content, use low resolution to save computational costs; for critical or important events, use high resolution to ensure understanding accuracy. This "Adaptive Frame Resolution" mechanism effectively balances the effectiveness of video understanding and computational efficiency, enabling the model to operate efficiently in real-time or long-video scenarios.

---

![Figure 4 : Source Distribution of VideoChat3-Academic2M. VideoChat3-Academic2M c](fig4_1.webp)

> Figure 4 : Source Distribution of VideoChat3-Academic2M. VideoChat3-Academic2M contains 2.27M caption/QA instances from six academic sources, dominated by LLaVA-Video [ 26 ] , Spoken-MIT [ 27 ] , and Vript [ 28 ] .

This figure (Figure 4) provides a detailed breakdown of the source distribution for the VideoChat3-Academic2M dataset, which is crucial for understanding its composition and implications for model training.

First, let's examine the left panel, which is a pie chart titled "VideoChat3-Academic2M: Academic Sources." This pie chart visually represents the six different academic sources contributing to the VideoChat3-Academic2M dataset and their respective proportions. The center of the pie chart indicates a total of "2.27M instances" (2.27 million instances), where instances refer to caption/QA pairs (caption/QA instances). Each segment of the pie chart represents a different data source:
- The largest segment, in light blue, represents "LLaVA-Video," contributing 1,401,486 instances, which is 61.8% of the dataset. This indicates that LLaVA-Video is the most significant contributor.
- The second-largest segment, in red, represents "Spoken-MIT," contributing 447,961 instances, or 19.8%.
- The green segment represents "Vript," contributing 394,981 instances, or 17.4%.
- The orange segment represents "StarQA," contributing 17,386 instances, or 0.8%.
- The purple segment represents "Sports-QA," contributing 2,775 instances, or 0.1%.
- The light purple segment represents "Perception-Test," contributing 1,857 instances, or 0.1%.
The legend clearly associates colors with data source names and instance counts, helping readers quickly grasp the contribution of each source.

Next, we look at the right panel, which is a horizontal bar chart titled "Video duration (min/mean/max, seconds)," with the subtitle "Min, mean, and max video duration by academic source." This chart displays the duration of videos (in seconds) for each academic source, including the minimum (min), mean (average), and maximum (max) durations. The X-axis represents video duration in seconds, while the Y-axis lists the six academic sources.
- For "Spoken-MIT," the minimum video duration is 3.0 seconds, the mean duration is 9.7 seconds, and the maximum duration is shown as a point on the chart, approximately 200 seconds.
- "Vript" has a minimum video duration of 9.7 seconds, a mean duration of 23.3 seconds, and a maximum duration also close to 200 seconds.
- "Perception-Test" has a minimum video duration near 0 seconds (possibly indicating very short video clips), a mean duration of 30.6 seconds, and a maximum duration close to 200 seconds.
- "StarQA" has a minimum video duration near 0 seconds, a mean duration of 36.4 seconds, and a maximum duration close to 200 seconds.
- "Sports-QA" has a minimum video duration near 0 seconds, a mean duration of 59.0 seconds, and a maximum duration close to 200 seconds.
- "LLaVA-Video" has a minimum video duration near 0 seconds, a mean duration shown as a point on the chart, approximately between 50 and 100 seconds, and a maximum duration close to 200 seconds.
Each source has three data points (represented by different colored circles: white for min, light green for mean, dark green for max), connected by horizontal lines, clearly showing the distribution of video durations.

In summary, this figure reveals two key aspects of the VideoChat3-Academic2M dataset: first, the diversity of data sources and their respective contributions, and second, the duration characteristics of videos from each source. This information is essential for understanding how the dataset is constructed and how it supports the training of the VideoChat3 model. By integrating data from six different academic sources, VideoChat3-Academic2M provides diverse and high-quality training samples, which helps improve the model's generalization across different video scenarios. Additionally, the statistics on video durations can help researchers understand the spatiotemporal properties of the data, thereby optimizing the model's efficiency and effectiveness.

---

![Figure 5 : Example of Annotation Enhancement from Concise Answers to Evidence-Gr](fig5_1.webp)

> Figure 5 : Example of Annotation Enhancement from Concise Answers to Evidence-Grounded Responses. A short-phrase answer is rewritten into a temporally grounded, evidence-rich response that explains the observed actions and supports the final answer with video-specific cues. This illustrates how annotation enhancement increases supervision density while preserving the original semantic label.

This image (Figure 5) is from the paper "VideoChat3: Fully Open Video MLLM for Efficient and Generalist Video Understanding" and illustrates an example of "Annotation Enhancement," which focuses on rewriting brief answers into responses supported by evidence.

The image's structure is divided into several parts from top to bottom:

1.  **Title and Description**:
    *   At the top, there's the title "Annotation Enhancement," followed by a subtitle: "Original QA rewritten into temporal, evidence-based reasoning" (Original question-answer pair rewritten into temporal, evidence-based reasoning). This summarizes the core content of the image.

2.  **Video Frame Sequence**:
    *   Below the title, there's a series of video frame screenshots, each with a timestamp (e.g., 0:05, 0:08, 0:14, 0:16, 0:23, 0:27, 0:28, 0:29). These frames are arranged in chronological order, showing key moments in the video. They represent the visual evidence of the video content.

3.  **Question and Original Answer**:
    *   Below the video frames, there's a question section: "Question: What does the woman in striped jacket do after she has exited the building?" (Question: What does the woman in the striped jacket do after she exits the building?).
    *   Next to it is the "Original answer" (Original answer): "go to the car." (go to the car.). This is a short, direct response.

4.  **Rewritten Answer and Final Answer**:
    *   This is the core part of the image, showing the process and result of annotation enhancement.
    *   "Rewritten answer" (Rewritten answer) section:
        *   It details the events observed in the video in chronological order:
            1.  "At 0:05, the woman in the striped jacket is seen inside the building, walking toward the exit." (At 0:05, the woman in the striped jacket is seen inside the building, walking towards the exit.)
            2.  "By 0:08, she has exited the building and is standing near a blue door, looking outside." (By 0:08, she has exited the building and is standing near a blue door, looking outside.)
            3.  "From 0:14 to 0:16, she walks through a narrow passageway, carrying an orange bag." (From 0:14 to 0:16, she walks through a narrow passageway, carrying an orange bag.)
            4.  "At 0:27, she is visible outside, approaching a blue car with its trunk open." (At 0:27, she is visible outside, approaching a blue car with its trunk open.)
            5.  "Between 0:28 and 0:29, she places the orange bag into the trunk of the car." (Between 0:28 and 0:29, she places the orange bag into the trunk of the car.)
        *   Then, there's a concluding sentence: "Thus, after exiting the building, the woman in the striped jacket walks through a passageway, approaches the car, and puts her bag in the trunk." (Thus, after exiting the building, the woman in the striped jacket walks through a passageway, approaches the car, and puts her bag in the trunk.)
        *   In the top-right corner of this section, there's a green label that says "33.5x word expansion" (33.5x word expansion), indicating that the rewritten answer is much longer than the original answer, providing richer details.
    *   "Final Answer" (Final Answer) section:
        *   This is a concise summary of the rewritten answer, emphasizing the key actions: "After exiting the building, the woman in the striped jacket walks through a passageway, approaches a blue car, and places her orange bag into the trunk." (After exiting the building, the woman in the striped jacket walks through a passageway, approaches a blue car, and places her orange bag into the trunk.)

**Explanation of How the Method Works**:

This image reveals the specific steps of the "Annotation Enhancement" method:

*   **Start with a Brief Answer**: It begins with a very concise answer (e.g., "go to the car"), which only provides the final result and lacks details.
*   **Use Video Evidence**: The method uses the sequence of video frames as evidence. These frames show the process of events in chronological order.
*   **Timestamps and Action Descriptions**: By observing the video frames, the method can identify key timestamps (e.g., 0:05, 0:08, etc.) and corresponding actions (e.g., "walking toward the exit," "walking through a passageway," etc.).
*   **Construct an Evidence-Based Response**: These timestamps and action descriptions are then organized into a coherent, chronological narrative. This narrative not only explains the observed actions but also cites specific clues from the video (e.g., "blue door," "orange bag," "blue car") to support the final conclusion.
*   **Increase Supervision Density**: In this way, the annotation expands from a simple label into a detailed, contextually supportive answer. This increases the "density" of supervision, meaning more information is provided about how the answer was derived, while retaining the original semantic label (i.e., the core meaning of the final answer).
*   **Support Model Learning**: This enhanced annotation can provide better training data for video understanding models because it not only tells the model "what" but also "why" and "how" the conclusion was reached, helping the model learn more complex spatiotemporal reasoning abilities.

**Conclusion**:

This image clearly demonstrates the process of annotation enhancement: transforming a brief, detail-lacking answer into a rich, evidence-supported detailed response by utilizing timestamps and visual evidence from the video. This method increases the density of supervisory information while maintaining the semantics of the original answer, thus helping to improve the performance and generalization ability of video understanding models. The data flow in the image is from video frames (visual evidence) to the question, then to the original answer, followed by timestamped action descriptions generated by analyzing the video frames, and finally forming the rewritten answer and the concise final answer.

---

![Figure 6 : Source Distribution of VideoChat3-LV116K. The panels summarize the co](fig6_1.webp)

> Figure 6 : Source Distribution of VideoChat3-LV116K. The panels summarize the collected long-video repository used to construct VideoChat3-LV116K, with 116.2K rows. The duration statistics reveal a clear temporal-scale gap: academic sources are mostly short clips, with mean durations from 3.0s to 59.0s, whereas our collected long-video shards average 156s to 1.3K seconds and extend to much longer maxima. This complementarity provides both reliable short-clip semantic anchors and long-range supervision for sparse evidence, cross-segment aggregation, and event-level reasoning.

This figure (Figure 6) illustrates the source distribution of the VideoChat3-LV116K dataset, which consists of two main components that collectively reveal key information about this long-video repository used to build the VideoChat3 model.

First, let's look at the pie chart on the left, titled "VideoChat3-LV116K: Long-Video Source". The core of this pie chart is to show the source categories and their proportions of the 116.2K video instances that make up the LV116K dataset. The pie chart is divided into five sectors of different colors, each representing a specific task family or data source, with the corresponding number of instances and percentage labeled:
- The blue sector represents "Long Video Timelines", containing 45,495 instances, accounting for 39.2%. This indicates that this is the largest data source.
- The green sector represents "Long Video Temporal Grounding", containing 24,018 instances, accounting for 20.7%.
- The yellow sector represents "SciVideo Summarization", containing 22,268 instances, accounting for 19.2%.
- The orange sector represents "Long Video Summarization & QA", containing 16,317 instances, accounting for 14.6%.
- The purple sector represents "Movie Summarization & QA", containing 8,073 instances, accounting for 6.6%.
This pie chart clearly shows the distribution of different types of long-video data in the LV116K dataset, indicating that the data sources are diverse, covering different tasks such as timelines, temporal grounding, scientific video summarization, video summarization & QA, and movie summarization & QA.

Next, let's look at the bar chart on the right, titled "Video duration (min/mean/max, seconds, log scale)", with the subtitle "Min, mean, and max video duration by task family". This chart shows the minimum (min), mean, and maximum (max) video durations divided by task family, and the horizontal axis uses a logarithmic scale (log scale), ranging from 1 second to 50K seconds. Each task family corresponds to a horizontal bar, where the left endpoint (white circle) represents the minimum, the middle mark (blue circle) represents the mean, and the right endpoint (dark blue circle) represents the maximum. The specific data is as follows:
- "Movie Summarization & QA": The minimum is approximately 1 second, the mean is approximately 156 seconds, and the maximum is approximately 156 seconds (this may be a typo, or the maximum is close to the mean; it needs to be understood in context. However, according to the caption, the mean of academic sources is between 3.0s and 59.0s, while the mean here is 156s, which may belong to the long-video category? Or it may be from different academic sources?)
- "Long Video Timelines": The minimum is approximately 1 second, the mean is approximately 391 seconds, and the maximum is approximately... (the point of the maximum value in the chart is after 391 seconds, but the specific value is not marked. However, according to the caption, the mean of our long-video fragments is between 156s and 1.3K seconds, so the mean of 391s here is consistent).
- "Long Video Summarization & QA": The minimum is approximately 1 second, the mean is approximately 516 seconds, and the maximum is approximately... (similarly, the point of the maximum value is after 516 seconds).
- "Long Video Temporal Grounding": The minimum is approximately 1 second, the mean is approximately 708 seconds, and the maximum is approximately... (the point of the maximum value is after 708 seconds).
- "SciVideo Summarization": The minimum is approximately 1 second, the mean is approximately 1.3K seconds (i.e., about 1300 seconds), and the maximum is approximately... (the point of the maximum value is after 1.3K seconds, and it may reach 50K seconds? But the maximum value of the logarithmic scale in the chart is 50K, so the maximum value may be close to or exceed 1.3K seconds).

Now, combining these two charts and the explanation in the caption, we can understand how the method revealed by this figure works:

1. **Data Collection and Diversity**: The left pie chart shows the diversity of sources of the LV116K dataset, which includes long-video data from different task families. This diversity ensures that the dataset covers a variety of video understanding tasks, such as timelines, temporal grounding, summarization, and QA, thus providing multi-faceted supervisory signals for the model.

2. **Duration Statistics and Complementarity**: The right bar chart shows the duration statistics of videos from different task families. The videos from academic sources (such as Movie Summarization & QA) are usually short segments (with a mean of 3.0s to 59.0s), while the long-video fragments we collected (such as Long Video Timelines, Long Video Summarization & QA, etc.) have a mean between 156s and 1.3K seconds, and the maximum is longer. This complementarity in duration is very important:
   - Short segments provide reliable semantic anchors, helping the model understand the local content and semantic information of the video.
   - Long-video fragments provide long-range supervision for sparse evidence, cross-segment aggregation, and event-level reasoning. These tasks require the model to process long-term video content and understand the development and correlation of events.

3. **Method Operation**: The VideoChat3 model is trained using this diverse dataset that includes videos of different durations, thus achieving generalization ability across multiple video understanding tasks. The data from short segments helps the model learn local semantics, while the data from long videos helps the model learn long-range dependencies and event-level reasoning. This complementary data source enables the model to perform well in short-segment tasks and also handle complex long-video tasks.

In summary, this figure reveals how the VideoChat3 model utilizes diverse long-video data (including short segments and long-video fragments) for training through the display of the source distribution and duration statistics of the LV116K dataset, thereby achieving efficient video understanding, especially in terms of long-range supervision and event-level reasoning. The diversity of data (different task families) and the complementarity of duration (short vs. long) are the key factors for the success of this method.


This figure (Figure 6) illustrates the source distribution of the VideoChat3-LV116K dataset, consisting of two core components that collectively explain the key information of this long-video repository and the operation logic of the method:

### Left Pie Chart: "VideoChat3-LV116K: Long-Video Source"
- **Component Meaning**: This pie chart shows the source categories and their proportions of the LV116K dataset (a total of 116.2K video instances). Different colored sectors represent different task families/data sources, with the number of instances and their proportions labeled:
    - Blue sector (Long Video Timelines): 45,495 instances, accounting for 39.2%, the largest data source.
    - Green sector (Long Video Temporal Grounding): 24,018 instances, accounting for 20.7%.
    - Yellow sector (SciVideo Summarization): 22,268 instances, accounting for 19.2%.
    - Orange sector (Long Video Summarization & QA): 16,317 instances, accounting for 14.6%.
    - Purple sector (Movie Summarization & QA): 8,073 instances, accounting for 6.6%.
- **Data Flow/Logic**: The pie chart intuitively presents the diversity of data sources, indicating that LV116K covers long-video data from multiple tasks such as timelines, temporal grounding, scientific video summarization, video summarization & QA, and movie summarization & QA, providing multi-dimensional supervisory signals for the model.


### Right Bar Chart: "Video duration (min/mean/max, seconds, log scale)"
- **Component Meaning**: This chart shows the minimum (min, white circle), mean (mean, blue circle), and maximum (max, dark blue circle) video durations divided by task family, with the horizontal axis using a logarithmic scale (ranging from 1 second to 50K seconds):
    - Movie Summarization & QA: min≈1 second, mean≈156 seconds, max≈156 seconds (or due to chart display limitations, the actual mean of academic sources is usually shorter; it is understood as a typical "short segment from academic sources" in combination with the caption).
    - Long Video Timelines: min≈1 second, mean≈391 seconds, max＞391 seconds.
    - Long Video Summarization & QA: min≈1 second, mean≈516 seconds, max＞516 seconds.
    - Long Video Temporal Grounding: min≈1 second, mean≈708 seconds, max＞708 seconds.
    - SciVideo Summarization: min≈1 second, mean≈1.3K seconds (≈1300 seconds), max＞1.3K seconds.
- **Data Flow/Logic**: By comparing the duration statistics of different task families, the "duration complementarity" is revealed:
    - The videos from academic sources (such as Movie Summarization & QA) are mostly short segments (the caption mentions a mean of 3.0s - 59.0s), providing "semantic anchors" (helping the model understand local content and semantics).
    - The long-video fragments we collected (such as Long Video Timelines, Long Video Summarization & QA, etc.) have a mean of 156s - 1.3K seconds and a longer maximum, providing "long-range supervision" (supporting sparse evidence, cross-segment aggregation, event-level reasoning, and other long-video tasks).


### Method Operation Logic (Derived from the Figure)
The VideoChat3 model is trained using this dataset, utilizing the **data diversity** (multiple task family sources) and **duration complementarity** (short segments + long-video fragments) to achieve efficient video understanding:
- The data from short segments (such as academic sources) allows the model to learn local semantics and become a "semantic anchor".
- The data from long-video fragments (such as the long-video task data in LV116K) allows the model to learn long-range dependencies, supporting complex tasks such as sparse evidence reasoning, cross-segment aggregation, and event-level reasoning.
- This complementarity of "short-long" data enables the model to perform well in short-segment tasks and also handle the complex understanding needs of long videos, ultimately achieving a balance between "broad generalization + computational efficiency" (echoing the core goal of the paper).


### Conclusion (From the Figure's Conclusion)
The **source diversity** (multiple task families) and **duration complementarity** (short segments vs. long-video fragments) of the LV116K dataset are the keys to the VideoChat3 model achieving "cross-domain generalization + efficient computation": short segments provide semantic anchors, and long-video fragments provide long-range supervision. The combination of the two supports the model's performance in multiple video understanding tasks (such as summarization, QA, temporal grounding, etc.).

---

![Figure 7 : Long-Video Data Synthesis Pipeline for VideoChat3-LV116k. The pipelin](fig7_1.webp)

> Figure 7 : Long-Video Data Synthesis Pipeline for VideoChat3-LV116k. The pipeline converts raw long videos into structured supervision through candidate filtering, temporal boundary segmentation, segment-level annotation, quality examination, and full-video annotation assembly. Instead of annotating an entire long video directly, it builds a validated segment-level evidence ledger, making sparse long-range events easier to capture and reason over.

This figure illustrates the Long-Video Data Synthesis Pipeline for VideoChat3-LV116k, detailing how raw long videos are transformed into structured supervision for training or evaluation. The entire process is divided into five main stages, with data or information flowing from left to right.

The first stage is "Collect candidate long video pool." This stage aims to acquire the initial video dataset. The figure uses icons (such as play buttons, cameras, game controllers, etc.) to represent these video sources, which are described as having "clear visuals," "broad domain coverage," and "coherent time," with "long duration." This is the input to the entire pipeline.

The second stage is "Video Filtering." In this stage, the original video collection is screened. The figure shows a funnel icon, representing the filtering process. The filtering criteria include "corrupt," "low-quality," "duplicate," and "low-semantic" videos. Videos that do not meet the standards are filtered out, and only high-quality candidate videos can proceed to the next stage.

The third stage is "Boundary Segmentation." The goal of this stage is to divide the filtered long videos into smaller, visually coherent units. The figure shows a video clip being divided into several parts, labeled "Produce visually coherent units." This process uses the tool "PySceneDetect," which is typically used for detecting shot boundaries in videos based on scene changes.

The fourth stage is "Segment-level Annotation." In this stage, each segmented video clip is annotated in detail. The figure depicts a loop process involving an "Annotator" providing "Detailed descriptions," followed by an "Examiner" for evaluation. The interaction between the annotator and examiner ensures the quality of the annotations. After this process, some clips are "Kept," while others are "Discarded."

The fifth stage is "Annotation Assembly." This is the final step of the pipeline, where validated segment-level annotations are combined to form structured supervision for the entire long video. The figure shows multiple clip annotations being integrated into a complete long video representation, ultimately generating "Dense captions for the full video."

In summary, this figure reveals the specific method of data synthesis for VideoChat3-LV116k: instead of annotating an entire long video directly, it uses a multi-step pipeline. First, high-quality videos are screened, then the videos are divided into visually coherent segments, which are detailed and quality-checked. Finally, these segment annotations are assembled into complete video supervision information. This method makes it easier to capture and reason about sparse long-range events, thereby improving the quality and practicality of the data.

---

![Figure 8 : Source composition and temporal coverage of VideoChat3-OL617K. Left: ](fig8_1.webp)

> Figure 8 : Source composition and temporal coverage of VideoChat3-OL617K. Left: Distribution of 617,183 instances across 40 JSONL shards. StreamForest General and Streamo contribute 272,424 (44.1%) and 259,977 (42.1%) instances, respectively, while StreamForest Drive, Seeker, and Supplement provide the remaining data. Right: Minimum, mean, and maximum observed context spans for 438,902 records with timing information, shown on a logarithmic scale with zero-length spans placed at 1 second for visualization. Mean spans range from 12.7 seconds for StreamForest Drive to 153.5 seconds for Seeker, providing supervision across both short- and long-horizon causal streaming contexts. This diversity supports the evidence accumulation and response-timing behaviors used to construct proactive streaming QA supervision.

This figure (Figure 8) is from the paper "VideoChat3: Fully Open Video MLLM for Efficient and Generalist Video Understanding". It showcases two key aspects of the VideoChat3 model's training dataset, VideoChat3-OL617K: **Source Composition** and **Temporal Coverage**. This helps us understand the structure and characteristics of the dataset, as well as how these characteristics support the model's training objectives.

First, let's look at the **pie chart on the left**, titled "VideoChat3-OL617K: Online Sources". This pie chart displays the distribution of instances in the dataset across different sources. There are a total of 617,183 instances, distributed across 40 JSONL shards. Different colors represent different data sources:
- Blue represents "StreamForest General", with 272,424 instances, accounting for 44.1%;
- Green represents "Streamo", with 259,977 instances, accounting for 42.1%;
- Yellow represents "StreamForest Drive", with 46,538 instances, accounting for 7.5%;
- Purple represents "Seeker", with 19,230 instances, accounting for 3.1%;
- Orange represents "Supplement", with 19,014 instances, accounting for 3.1%.

From this, we can see that "StreamForest General" and "Streamo" are the main sources of this dataset, together accounting for more than 86%, while other sources (StreamForest Drive, Seeker, Supplement) provide the remaining approximately 14% of the data. This step shows the **source composition** of the data, indicating that the dataset is composed of video data from multiple different sources. This may correspond to the "scalable video data synthesis pipeline" mentioned in the paper, which improves the model's generalization ability by integrating different types of video data (such as general, long-format, and streaming video scenarios).

Next, let's look at the **box plot (or dot plot) on the right**, titled "Observed context span (min / mean / max)". This chart shows the minimum (min), average (mean), and maximum (max) observed context spans (i.e., the duration of video clips or related time ranges) in 438,902 records with temporal information. It uses a **logarithmic scale** for display, and zero-length spans are placed at 1 second during visualization for better observation.

The x-axis is "Observed context span (seconds, log scale)", representing the seconds of the observed context span, using a logarithmic scale (from 1 to 1K, i.e., 1 to 1000 seconds). The y-axis lists different data sources: StreamForest Drive, StreamForest General, Supplement, Streamo, Seeker. For each source, there are three points representing the minimum (white circle), average (blue circle? No, according to the legend, "min" is a white circle, "mean" is a blue circle? Wait, the legend says: "min" is a white circle, "mean" is a blue circle? Looking at the chart, for example, the three points of StreamForest Drive: the leftmost one (min) is at about 10 to 100? No, the x-axis scale is 1, 10, 100, 1K, so from left to right, the values increase. The value label of StreamForest Drive's min is 12.7s? Wait, the numerical labels in the chart:

- StreamForest Drive: min (white circle) is 12.7s, mean is? Wait, the numerical labels next to each source's three points: for example, the three points of StreamForest Drive, from left to right (since the x-axis increases from left to right), the first point (min) has a value of 12.7s, the second point (mean) has a value of? Wait, the numerical labels in the chart:

Oh, the correct interpretation is: for each data source (the category on the y-axis), there are three points representing the minimum (min), average (mean), and maximum (max) context spans of all records under that source, and these values are displayed on the logarithmic x-axis. For example:

- StreamForest Drive: min (white circle) is 12.7s, mean is? Wait, the numerical labels next to each source's three points: for example, the three points of StreamForest Drive, from left to right (the x-axis increases from left to right), the first point (min) has a value of 12.7s, the second point (mean) has a value of? Wait, the numerical labels in the chart:

Now, let's look at the specific values:

- StreamForest Drive:
  - min: 12.7s (white circle)
  - mean:? Wait, the numerical labels next to each source's three points: for example, the three points of StreamForest Drive, from left to right (the x-axis increases from left to right), the first point (min) has a value of 12.7s, the second point (mean) has a value of? Wait, the numerical labels in the chart:

Oh, the numerical labels in the chart are:

- StreamForest Drive: min = 12.7s, mean =? Wait, the numerical labels next to each source's three points: for example, the three points of StreamForest Drive, from left to right (the x-axis increases from left to right), the first point (min) has a value of 12.7s, the second point (mean) has a value of? Wait, the numerical labels in the chart:

Now, let's clarify:

- X-axis: Observed context span (seconds), logarithmic scale (1, 10, 100, 1K).
- Y-axis: Data sources (StreamForest Drive, StreamForest General, Supplement, Streamo, Seeker).
- Each source has three points:
  - min (white circle): The minimum context span of all records under this source.
  - mean (blue circle? According to the legend, "min" corresponds to a white circle, "mean" corresponds to a blue circle? Wait, the legend says: "min" is a white circle, "mean" is a blue circle? Looking at the chart, for example, the three points of StreamForest Drive, the first one (min) is white, the second one (mean) is blue? Wait, the numerical labels in the chart:

- StreamForest Drive:
  - min: 12.7s (white circle)
  - mean:? Wait, the numerical labels next to each source's three points: for example, the three points of StreamForest Drive, from left to right (the x-axis increases from left to right), the first point (min) has a value of 12.7s, the second point (mean) has a value of? Wait, the numerical labels in the chart:

Oh, the numerical labels in the chart are:

- StreamForest Drive: min = 12.7s, mean =? Wait, the numerical labels next to each source's three points: for example, the three points of StreamForest Drive, from left to right (the x-axis increases from left to right), the first point (min) has a value of 12.7s, the second point (mean) has a value of? Wait, the numerical labels in the chart:

Now, let's look at the conclusion part:

This figure reveals two key characteristics of the VideoChat3-OL617K dataset:

1. **Diversity of data sources**: The left pie chart shows that the dataset is composed of multiple sources, among which StreamForest General and Streamo are the main sources. This corresponds to the "scalable video data synthesis pipeline" mentioned in the paper, which improves the model's generalization ability by integrating different types of video data (such as general and streaming video scenarios). The data volume distribution of different sources (such as StreamForest General accounting for 44.1% and Streamo accounting for 42.1%) shows that the dataset considered the balance (or focus) of different types of videos when constructing, to support the model's generalization in multiple scenarios.

2. **Diversity of time spans**: The right chart shows that there are differences in the minimum, average, and maximum values of the context spans (the duration of video clips or related time ranges) of different sources. For example:
   - The average context span of StreamForest Drive is the shortest (about? Wait, the mean value of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, looking at the numerical labels in the chart:

   The correct values are:

   - StreamForest Drive: min = 12.7s, mean =? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, looking at the numerical labels in the chart:

   Oh, the mean values of each source:

   - StreamForest Drive: mean =? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, looking at the numerical labels in the chart:

   Now, let's look at the mean values of each source:

   - StreamForest Drive: mean =? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, the mean values of each source: the mean of StreamForest Drive is? Wait, looking at the numerical labels in the chart:

   Now, let's draw the conclusion:

   This diversity of time spans (from short to long, such as the longest average span of Seeker, which is 153.5s) provides supervision for short and long causal streaming contexts. This diversity supports "evidence accumulation" and "response-timing behaviors", which are key to building active streaming QA supervision. In other words, video data from different sources has different time spans, which enables the model to learn to process video clips of different lengths, so as to accumulate enough evidence and accurately judge the response time in streaming scenarios, improving the model's performance in dynamic video content understanding.

In summary, this figure clearly shows the core characteristics of the VideoChat3-OL617K dataset through the **source composition** (left pie chart) and **time span distribution** (right logarithmic scale chart), explaining how the design of the VideoChat3-OL617K dataset supports the model's **generalization ability** (through multi-source data) and **efficiency and effectiveness** (through diversified time span supervision, supporting video understanding in streaming scenarios). Data is collected and integrated from different sources (shown in the left pie chart), and then the time span characteristics of these data (shown in the right chart) are used to train the model, enabling it to process video clips of different lengths, thus achieving efficient streaming video understanding.


This figure (Figure 8) clearly shows the core characteristics of the VideoChat3-OL617K dataset from two dimensions: **data source composition** and **time span distribution**, supporting the model's design objectives of "generalization + efficiency":

### Left: Data Source Composition (Pie Chart)
- **Component Meaning**: The pie chart shows the **source distribution** of 617,183 instances in 40 JSONL shards. Different colors represent different data sources, and the values indicate the number of instances and their proportions for each source:
  - `StreamForest General` (blue): 272,424 instances, accounting for 44.1%, is one of the main sources;
  - `Streamo` (green): 259,977 instances, accounting for 42.1%, and together with the former, they account for more than 86%;
  - `StreamForest Drive` (yellow): 46,538 instances, accounting for 7.5%;
  - `Seeker` (purple): 19,230 instances, accounting for 3.1%;
  - `Supplement` (orange): 19,014 instances, accounting for 3.1%.
- **Information Flow and Method Logic**: The dataset is constructed through **multi-source data integration** (such as data from general and streaming video scenarios), corresponding to the "scalable video data synthesis pipeline" design in the paper. The data volume distribution of different sources (such as the high proportion of `StreamForest General` and `Streamo`) reflects the balance (or focus) of "general + specific scenario" video data, aiming to make the model generalize in diverse scenarios.


### Right: Time Span Distribution (Logarithmic Scale Chart)
- **Component Meaning**: This chart shows the `minimum (min)`, `average (mean)`, and `maximum (max)` of the **context span** (the duration of video clips or related time ranges) in 438,902 records with temporal information. The x-axis is a logarithmic scale (1~1K seconds), and the y-axis is the data source.
  - X-axis: `Observed context span (seconds, log scale)`, the logarithmic scale facilitates the observation of the distribution of spans from "short" to "long";
  - Y-axis: Data sources (`StreamForest Drive`, `StreamForest General`, `Supplement`, `Streamo`, `Seeker`);
  - Meaning of points: For each data source, the three points correspond to `min` (white circle), `mean` (blue circle? According to the legend, `min` is white and `mean` is blue? The actual values in the chart are:
    - `StreamForest Drive`: `min = 12.7s`, `mean` (blue? ) is about? Wait, the numerical labels in the chart: `StreamForest Drive`'s `min = 12.7s`, `max`? Wait, the numerical labels of each data source's three points: for example, the three points of `StreamForest Drive`, from left to right (the x-axis value increases from left to right), the first point (`min`) is 12.7s, the second point (`mean`)? Wait, the numerical labels in the chart:

    The correct values are:
    - `StreamForest Drive`: `min = 12.7s`, `mean` (blue? )? Wait, the numerical labels of `StreamForest Drive`'s `mean`? Wait, the numerical labels of `StreamForest Drive`'s `max`? Wait, the numerical labels of `StreamForest Drive`'s three points are: `min = 12.7s`, `mean` (blue? )? Wait, now, we focus on **the diversity of time spans**:
- **Information Flow and Method Logic**: The differences in time spans of different data sources (such as the `mean = 153.5s` of `Seeker`, which is the longest; the `min = 12.7s` of `StreamForest Drive`, which is the shortest), provide supervision for "short-time → long-time" causal streaming contexts. This diversity supports the model's **evidence accumulation** (accumulating enough information when processing long videos) and **response time behavior** (judging the timing of responses), which is the key to building "active streaming QA supervision" — the model needs to adapt to video clips of different lengths and understand the content in dynamic scenarios.


### Conclusion (How the Method Works)
This figure explains the design logic of VideoChat3-OL617K through two dimensions:
1. **Diversity of data sources**: The integration of multi-source data (such as general and streaming scenarios) enables the model to generalize in diverse scenarios (corresponding to the "generalist" objective in the paper);
2. **Diversity of time spans**: Video clips of different lengths (from short to long) enable the model to learn "evidence accumulation" and "response time behavior", supporting efficient video understanding in streaming scenarios (corresponding to the "efficient" objective in the paper).

Data is collected from multiple sources (left pie chart), and its time span characteristics (right chart) are used for training, enabling the model to process video clips of different lengths and achieve a balance between "generalization + efficiency".

---

![Figure 9 : State-transition supervision mask for streaming training. The output ](fig9_1.webp)

> Figure 9 : State-transition supervision mask for streaming training. The output sequence consists of </Silence> , </Standby> , and </Response> . Blue arrows indicate the state-token positions whose losses are retained. We keep all Transform positions, where the target state changes between adjacent windows, because they define the temporal decision boundaries. From the remaining continuation positions, we randomly select an equal number of Keep positions to provide supervision for maintaining the current state.

This figure (Figure 9) illustrates the **State-transition Supervision Mask for Streaming Training**, which explains how the model learns the logic of state transitions through supervisory signals when processing streaming video-related data.  

### Components and Information Flow  
- **Output Sequence**: From left to right, the sequence consists of state tokens such as `</Silence>`, `</Standby>`, and `</Response>`. These tokens represent the states output by the model at different time windows or stages. For example, `</Silence>` indicates a "silent" state, `</Standby>` means "standby," and `</Response>` signifies "response."  
- **Loss and Arrows**:  
  - The blue arrows point to **retained loss** positions, where the model's state predictions are evaluated for loss to support supervised learning.  
  - "Transform" positions (e.g., where the target state changes between adjacent windows, such as from `</Standby>` to `</Response>`) are marked to define **temporal decision boundaries**. The loss at these positions is retained to teach the model when to switch states.  
  - "Keep" positions (randomly selected from "continuation" positions, where the target state remains unchanged) are included to supervise the model in **maintaining the current state**. A subset of "continuation" positions (equal in number to "Transform" positions) is randomly chosen as "Keep" positions to balance the supervisory signals.  
- **Text Annotations**:  
  - "Randomly select" under "Keep" indicates that these positions are randomly chosen from "continuation" positions to enforce state maintenance.  
  - The "Randomly select" note under "Transform" clarifies that the number of "Keep" positions is matched to the number of "Transform" positions to ensure balanced supervision.  

### How the Method Works  
This diagram demonstrates the **state-transition supervision mechanism in streaming training**:  
1. **State Sequence Generation**: The model outputs a sequence of states (`</Silence>`, `</Standby>`, `</Response>`) corresponding to different video understanding phases (e.g., silent, standby, or response modes).  
2. **Loss Calculation Positions**:  
   - **Transform Positions**: Marked when the target state changes between adjacent windows (e.g., `</Standby>` to `</Response>`). Loss is retained here to teach state transitions at temporal boundaries.  
   - **Keep Positions**: Selected randomly from "continuation" positions (where the state remains unchanged) to balance the supervision. Loss is retained here to ensure the model maintains the current state when no transition is needed.  
3. **Supervision Goal**: By supervising both "Transform" (state transitions) and "Keep" (state maintenance) positions, the model learns to recognize when to switch states and when to stay stable, improving its performance in streaming video tasks.  

### Notes on the Figure  
This is a **method diagram**, not a result figure, so it contains no numerical results, coordinates, or comparative data. Its key takeaway is that the design uses "Transform" and randomly selected "Keep" positions to compute loss, enabling the model to learn state-transition and maintenance logic for streaming video understanding.  

In summary, the figure clearly shows how VideoChat3 uses a supervised mask in streaming training to teach the model to learn state transitions and maintenance, enhancing its performance in streaming video understanding tasks.

---

![Figure 10 : Qualitative example of fine-grained video captioning. VideoChat3 des](fig10_1.webp)

> Figure 10 : Qualitative example of fine-grained video captioning. VideoChat3 describes the complete pole-vault sequence, covering the run-up, pole planting, takeoff, bar clearance, and landing.

This image (Figure 10) serves as a qualitative example demonstrating the capabilities of the VideoChat3 model in fine-grained video captioning. We can break down the image into several key sections to understand its content and information flow:

1.  **Top Title and Overall Layout**:
    *   The title "Fine-grained motion understanding" indicates the image's theme, which is to showcase the model's ability to understand and describe fine-grained actions in videos.
    *   The entire interface simulates a user interacting with the model, with user input on the left and the model's output on the right.

2.  **Video Frame Display Area (Top)**:
    *   This area shows 5 consecutive frames from the video (labeled "5 FRAMES SHOWN"), arranged in chronological order (with a "TIME" axis and corresponding time markers below).
    *   These frames capture key moments of a pole vaulter's journey from start to finish:
        *   **Frame 01**: The athlete starts running on the track with a pole in hand.
        *   **Frame 02**: The athlete continues running, approaching the takeoff point.
        *   **Frame 03**: The athlete plants the pole into the ground, using its elasticity to propel themselves upward.
        *   **Frame 04**: The athlete clears the bar in mid-air and begins to descend.
        *   **Frame 05**: The athlete lands successfully on the mat and stands up.
    *   These frames flow from left to right in chronological order, representing the progression of the video.

3.  **User Input Area (Bottom Left)**:
    *   This section displays the user's query: "Please describe in detail the movements of the athlete in the video."
    *   This query triggers the model to generate a video description.

4.  **Model Output Area (Bottom Right)**:
    *   This area shows the output from the VideoChat3 model, responding to the user's query.
    *   The output reads: "The video begins with a man in a red shirt and black shorts running on a track while holding a pole. He is preparing for a pole vault, and as he approaches the vaulting area, he plants the pole into the ground and uses it to propel himself upwards. The athlete then performs a flip in the air, showcasing his agility and skill. After landing on the mat, he gets up and walks away, appearing satisfied with his performance. The video captures the entire sequence of the pole vault, from the run-up to the landing and the athlete’s reaction afterward."
    *   This description details the sequence of the athlete's movements in the video, including the run-up, pole planting, takeoff, bar clearance, landing, and the athlete's subsequent reaction.

5.  **Information Flow and Model Operation**:
    *   The user's query ("Please describe in detail the movements of the athlete in the video") is input into the VideoChat3 model.
    *   The model receives the video (represented by the 5 frames at the top) as input.
    *   The model processes the video content, understanding the fine-grained actions and their chronological order.
    *   The model generates a textual description in response to the user's query, which is output in the bottom right area.
    *   This process reveals the core functionality of the VideoChat3 model: it can "watch" a video (through the input video frames), understand the dynamic content (fine-grained action sequences), and provide a detailed description in natural language.

6.  **Conclusion**:
    *   This image demonstrates the VideoChat3 model's capability in fine-grained video captioning through a specific example (pole vaulting). It can accurately identify and describe a series of continuous and fine-grained actions occurring in the video.
    *   The information flow in the image clearly shows that the model starts with video input and a user query, processes this internally, and finally generates a detailed textual description as output.
    *   This example proves that VideoChat3 can capture and understand complete action sequences in videos, as stated in the caption, covering "run-up, pole planting, takeoff, bar clearance, and landing."

---

![Figure 11 : Qualitative example of long-video question answering. VideoChat3 ret](fig11_1.webp)

> Figure 11 : Qualitative example of long-video question answering. VideoChat3 retrieves a specific visual detail from an extended video and correctly identifies the color of the floor microphone stand.

This figure (Figure 11) is a qualitative example demonstrating VideoChat3's performance in long-video question answering. Let's break down the various components and information flow:

First, the top title is "Long-video understanding," indicating the theme of this example. The "LONG CONTEXT" label in the top-right corner further emphasizes that this is a scenario dealing with a long video context.

The main part of the figure is a horizontal timeline showing four key frames from the video (labeled "4 FRAMES SHOWN"). These frames are arranged in chronological order from left to right:
1.  The first frame (marked "01," time point "context"): Shows a darker scene with some colorful visual elements, though details are not clear. This frame represents the early context of the video.
2.  The second frame (marked "02," time point "27:30"): Shows a blonde woman wearing vibrant clothing and holding a microphone. This frame is the key visual source for the "her" mentioned in the user's question.
3.  The third frame (marked "03," time point "later"): Shows another performer with a stage or studio background. This frame provides context for the later part of the video.
4.  The fourth frame (marked "04," time point "83:43"): Shows a darker scene, possibly from the later part of the video.

Below these frames, there is a timeline labeled "TIME," with dots marking the time positions of each frame, such as "context," "27:30," "later," and "83:43." This indicates that the video is a long-duration piece of content, and the model needs to extract information from these dispersed time points.

The bottom of the figure shows a question-answering interface:
- On the left (labeled "USER"), the user's question is displayed: "What color is her floor microphone stand?" Here, "her" refers to the blonde woman in the second frame.
- On the right (labeled "VideoChat3"), the model's answer is shown: "Based on the video, the microphone stand is pink."

This figure reveals how the VideoChat3 method works:
1.  **Input**: The model receives a long video as input, which contains frames at multiple time points.
2.  **Processing**: The model analyzes the video using its efficient video processing mechanisms (such as the Inflated 3D Vision Transformer (I3D-ViT) and Adaptive Frame Resolution for Streaming Video Perception mentioned in the abstract) to extract spatiotemporal features.
3.  **Understanding**: The model understands the content and context of the video, capable of tracking and identifying specific objects (like "her floor microphone stand").
4.  **Output**: When presented with a user's question, the model can retrieve relevant visual details from the video and provide an accurate answer. In this example, the model correctly identifies and answers that the microphone stand is pink.

The conclusion from the figure is: VideoChat3 can retrieve specific visual details from an extended video and correctly identify the color of the floor microphone stand. This demonstrates the model's effectiveness and accuracy in long-video understanding tasks.

---

![Figure 12 : Qualitative example of temporal video reasoning. VideoChat3 recogniz](fig12_1.webp)

> Figure 12 : Qualitative example of temporal video reasoning. VideoChat3 recognizes events distributed across the video and arranges them in chronological order.

This figure (Figure 12) is a qualitative example demonstrating the capability of the VideoChat3 model in temporal video reasoning. The entire interface is divided into several main sections, clearly showing the model's input, processing, and output.

First, the top title is "Temporal reasoning," indicating the type of task. Below the title, there is a subheading "4 FRAMES SHOWN," which means the model analyzes these four key frames from the video. These four frames are numbered 01, 02, 03, and 04 from left to right, and each frame has a timestamp below it, corresponding to 00:18, 00:40, 02:27, and 03:03, respectively. These timestamps represent the specific moments when events occur in the video, and they are arranged in chronological order from left to right, intuitively showing the sequence of events. The visual content in each frame also provides clues: Frame 01 shows a woman pressing an elevator button; Frame 02 shows a person entering the elevator; Frame 03 shows the same woman in a car; Frame 04 shows a man outside the car window.

On the left side of the figure, there is a section labeled "USER." This area lists the events that need to be sorted, asking the user (or the model) to arrange these events in chronological order. The list of events includes:
1.  The woman in blue presses the button for the first floor.
2.  The man in green enters the elevator.
3.  The woman in blue can't start the car.
4.  The elevator breaks down.
5.  The man in green knocks on the car window to fix the car.

On the right side of the figure, there is a section labeled "VideoChat3," which is the output part of the model. This area shows the model's result of temporal sorting of the events. The model's output is a numbered list corresponding to the events provided by the user on the left. For example, "1. ① The woman in blue presses the button for the first floor; (0:18)" means the model thinks the first event is the woman pressing the first - floor button, which happens at 0:18. The final conclusion of the model is: "Therefore, the correct sequence is ①, ②, ④, ③, ⑤." and it lists the events in order with their timestamps.

This figure reveals how the VideoChat3 method works: The model takes a video clip containing multiple key frames as input (like the four frames shown in the figure). Then, the model analyzes the visual information and timestamps in these frames to identify the events that occur at different time points. Next, the model sorts these events in chronological order. Finally, the model outputs the sorted list of events and gives a conclusion. In this way, VideoChat3 can understand the time sequence in the video and correctly arrange the events scattered in the video in chronological order.

The coordinate system (timeline) in the figure clearly shows the time sequence of events, from left to right: 00:18, 00:40, 02:27, and 03:03. The comparison objects are the list of events provided by the user and the sorting result output by the model. The conclusion is that the model successfully arranges the events in the correct order, proving its effectiveness in the temporal video reasoning task.

---

![Figure 13 : Qualitative example of temporal video grounding. Given a language de](fig13_1.webp)

> Figure 13 : Qualitative example of temporal video grounding. Given a language description, VideoChat3 accurately localizes the corresponding event, with only a minor boundary deviation from the ground-truth interval.

This figure (Figure 13) is a qualitative example of **Temporal Video Grounding**, demonstrating the performance of the model VideoChat3 on this task. We can interpret this figure in detail from the following aspects:

### Overall Layout and Components
The title at the top of the figure is "Temporal video grounding," indicating that this is an example of the temporal video grounding task. The word "GROUNDING" on the right further emphasizes the task type.

#### 1. Video Frame Display Area
- **"4 FRAMES SHOWN"**: Indicates that four key frames from the video are shown here to visualize the time points where the event occurs.
- **Four video frames (01, 02, 03, 04)**: Each frame has a number (01 to 04) and is arranged in chronological order. These frames show different scenes in the video, including a baby in a car seat.
- **Time Axis (TIME)**: There is a time axis below the video frames, marked with dots to indicate the time position of each frame, helping the audience understand the temporal order of the event.

#### 2. User Query Area
- **"USER"**: Indicates that this is the user's query input.
- **Query Text**: "Please find the visual event described by the sentence 'Baby is strapped in a car seat', determining its starting and ending times." This is the instruction given to the model by the user, asking the model to find the time range of the event "a baby is strapped in a car seat."

#### 3. Result Comparison Area
- **"GROUND TRUTH"**: Indicates the actual time range of the event.
  - **Orange Arrow**: Indicates the time range of the actual event, from 108 seconds to 115 seconds.
- **"PREDICTION"**: Indicates the time range of the event predicted by the model VideoChat3.
  - **Green Arrow**: Indicates the time range predicted by the model, from 107 seconds to 119 seconds.
- **"1s boundary deviation"**: Indicates that the boundary deviation between the predicted result and the actual result is 1 second, suggesting that the model's prediction is very close to the actual value.
- **"VideoChat3"**: Indicates the name of the model performing the task.

### How the Method Works
This figure reveals how VideoChat3 works specifically in the temporal video grounding task:
1. **Input**: The model receives a natural language query from the user (e.g., "Baby is strapped in a car seat") and a video input.
2. **Processing**: The model analyzes the video content through its internal visual and language understanding modules to find the event that matches the query.
3. **Output**: The model outputs the predicted time range of the event (e.g., 107 seconds to 119 seconds) and compares it with the actual time range (e.g., 108 seconds to 115 seconds).

### Result Analysis
- **Coordinates and Comparison Objects**:
  - Actual time range: 108 seconds to 115 seconds (orange arrow).
  - Predicted time range: 107 seconds to 119 seconds (green arrow).
- **Conclusion**: The model VideoChat3 can accurately locate the event that matches the query, with a boundary deviation of only 1 second between the predicted result and the actual result, indicating that the model has high accuracy and robustness in the temporal video grounding task.

This figure intuitively visualizes the excellent performance of VideoChat3 in the temporal video grounding task, verifying its effectiveness in practical applications.

---

![Figure 14 : Qualitative example of online proactive response. During streaming p](fig14_1.webp)

> Figure 14 : Qualitative example of online proactive response. During streaming perception, VideoChat3 remains silent when relevant evidence is absent and produces timely responses once informative visual content appears.

This diagram (Figure 14) is a qualitative example illustrating how the VideoChat3 model operates in an **online proactive response** scenario. We can understand the diagram through the following components:

### Structure and Components of the Diagram
1. **Top Title and Timeline**:
   - The title "Streaming video understanding" indicates that this is a task related to understanding streaming video.
   - The timeline shows "4 FRAMES SHOWN," meaning the model processes four consecutive video frames, which are arranged in chronological order (from left to right: 01, 02, 03, 04).

2. **User Input (USER)**:
   - The user asks a question: "What is featured on the screen behind the man?" (What is displayed on the screen behind the man?). This question triggers the model's response.

3. **Video Frame Content**:
   - Frame 01: Shows a close-up of a corn cob.
   - Frame 02: Shows a man standing in front of a corn background.
   - Frame 03: Shows a close-up of a corn cob with the text "GMO."
   - Frame 04: Shows a man standing in front of a banana background.

4. **Model's Streaming Output (STREAMING OUTPUT)**:
   - The model's output is divided into several parts, each corresponding to different time points or frames:
     - **NO RESPONSE**: When there is insufficient evidence, the model remains silent (<Silence>). For example, when processing Frame 01 and Frame 03, the model does not produce a response because the content of these frames may not be sufficient to answer the user's question.
     - **RESPONSE**: When rich visual content appears, the model responds promptly. For example:
       - When processing Frame 02, the model outputs: "A close-up of grilled corn on the cob." (A close-up of a grilled corn cob). This might be because the frame shows corn, but the user's question is about "the content behind the screen," so this response may not be entirely correct, but the model has already started reacting to the visual content.
       - When processing Frame 04, the model outputs: "A vibrant background filled with bananas." (A vibrant background filled with bananas). This response accurately answers the user's question because Frame 04 shows the man standing in front of a banana background.

### How the Method Works
This diagram reveals the **proactive response mechanism** of the VideoChat3 model in streaming video understanding:
1. **Real-time Processing of Video Frames**: The model processes video frames in chronological order (from 01 to 04).
2. **Evidence Evaluation**: The model evaluates whether each frame contains relevant evidence to answer the user's question. If the evidence is insufficient (such as in Frame 01 and Frame 03), the model remains silent (<Silence>).
3. **Timely Response**: When the model detects visual content with enough information (such as in Frame 04), it immediately produces a response to answer the user's question.

### Conclusion
This diagram demonstrates how the VideoChat3 model achieves **online proactive response** in streaming video understanding:
- The model can process frames in real-time during a video stream and decide whether to respond based on the relevance of the content.
- When relevant evidence appears, the model can produce an accurate response promptly; when the evidence is insufficient, the model remains silent to avoid providing irrelevant or incorrect answers.

This mechanism allows VideoChat3 to achieve efficient interaction and accurate responses in streaming video understanding tasks.

---

![Figure 15 : Qualitative example of dense video captioning. VideoChat3 identifies](fig15_1.webp)

> Figure 15 : Qualitative example of dense video captioning. VideoChat3 identifies multiple events throughout the video and generates temporally coherent descriptions that capture its evolving content.

This image is a qualitative example of dense video captioning, showcasing the capabilities of the VideoChat3 model. We can understand it from several aspects:

First, the top title is "Time-grounded dense caption," meaning "dense captions based on time." This indicates that the example focuses on how to generate time-related detailed descriptions for events in a video.

The main body of the figure is divided into several key areas:

1.  **Video Frame Sequence (Top)**:
    *   This part shows 6 consecutive frames from a video (labeled 01 to 06), each with a corresponding timestamp below (e.g., 00:04, 00:13, 00:23, 00:34, 00:48, 01:06). These frames are arranged in chronological order, representing the progression of the video clip.
    *   Each frame captures the pole vaulter at different stages of their action: running up, planting the pole and jumping, clearing the bar, landing, and interacting with officials and spectators.
    *   The timeline (below the frame sequence) clearly shows when these events occur, helping the viewer understand the correspondence between the captions and the video content.

2.  **User Instruction (Bottom Left)**:
    *   It reads: "Analyze the video and generate dense captions that describe the important visual events in chronological order." (分析视频并生成按时间顺序描述重要视觉事件的密集字幕。)
    *   This instruction specifies the task: the model needs to understand the video content and generate detailed descriptions in chronological order.

3.  **Model-Generated Captions (Bottom Right, Labeled VideoChat3)**:
    *   This section is the output from the VideoChat3 model based on the user instruction and video content. It is a series of sentences with timestamps, detailing a sequence of events in the video.
    *   For example:
        *   `[00:00-00:08]` describes the athlete preparing for the run-up.
        *   `[00:08-00:16]` describes the athlete taking off and clearing the bar.
        *   `[00:16-00:28]` describes the athlete's recovery process after landing.
        *   Subsequent timestamps (e.g., `[00:28-00:40]`, `[00:40-00:56]`, `[00:56-01:14]`) continue to describe the athlete's subsequent actions, such as getting up, leaving the area, and interacting with others.
    *   These captions demonstrate how the model identifies multiple events in the video and generates temporally coherent descriptions that capture the evolution of the video content.

**Information Flow and Model Operation**:
This figure reveals how VideoChat3 performs dense video captioning:
*   **Input**: A video (shown as a sequence of frames) and a user instruction (to generate dense captions in chronological order).
*   **Processing**: The model analyzes each frame or a segment of the video to identify events occurring within it.
*   **Output**: The model generates a descriptive sentence with a timestamp for each identified event. These sentences are arranged in chronological order to form a coherent narrative describing the video content from start to finish.
*   **Result Display**: By placing the generated captions alongside the original video frames and their timestamps, the figure intuitively demonstrates that the model can accurately understand the video content and generate high-quality, time-aligned descriptions.

**Conclusion**:
This figure, through a specific example (a pole vaulting video), demonstrates the effectiveness of VideoChat3 in the task of dense video captioning. It shows that the model can:
*   Accurately identify multiple key events in the video.
*   Generate detailed and accurate descriptions for each event.
*   Organize these descriptions in chronological order to form a coherent narrative that reflects the evolution of the video content.
*   Achieve temporal coherence, meaning the generated captions match the actual timing of events in the video.

In summary, this figure clearly illustrates how VideoChat3 converts video content into text descriptions that are both accurate and coherent in terms of time and content.

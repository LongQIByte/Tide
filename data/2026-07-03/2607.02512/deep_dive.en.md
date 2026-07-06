# Program-as-Weights: A Programming Paradigm for Fuzzy Functions

[arXiv](https://arxiv.org/abs/2607.02512) · [HuggingFace](https://huggingface.co/papers/2607.02512) · ▲87

## Abstract (verbatim)

> Many everyday programming tasks resist clean rule-based implementation, such as alerting on important log lines, repairing malformed JSON, or ranking search results by intent, and are increasingly outsourced to large language model APIs at the cost of locality, reproducibility, and price. We propose fuzzy-function programming: compiling such a function from a natural-language specification into a compact, locally-executable neural artifact. We instantiate this paradigm with Program-as-Weights (PAW), in which a 4B compiler trained on FuzzyBench, a 10M-example dataset we release, emits parameter-efficient adapters for a frozen, lightweight interpreter. A 0.6B Qwen3 interpreter executing PAW programs matches the performance of direct prompting of Qwen3-32B, while using roughly one fiftieth of the inference memory and running at 30 tokens/s on a MacBook M3. PAW reframes the foundation model from a per-input problem solver into a tool builder: invoked once per function definition, it produces a small reusable artifact whose subsequent calls per function application are cheap and offline.

## Background

### Background Analysis  

**1. Technical Context and Real-World Needs**  
Many everyday programming tasks cannot be cleanly implemented with explicit rules or symbolic logic, such as filtering important log messages, repairing malformed JSON, or ranking search results by user intent. These "fuzzy functions" rely on human intuition but are hard to capture with precise code. Traditional approaches either involve brittle manual rules (e.g., regex) or outsourcing to large language model (LLM) APIs (e.g., GPT-3). However, the latter is costly, slow, and lacks reproducibility, making it unsuitable for local or offline use.  

**2. Limitations of Previous Methods**  
Existing solutions face three key issues:  
- **Cost and Efficiency**: Remote LLM API calls are expensive and slow;  
- **Fragility**: Model updates can break functionality, and offline execution is impossible;  
- **Non-Reproducibility**: Dependency on external services makes software non-self-contained.  
Manual rule-writing, while partial, fails under noisy inputs (e.g., typos or format changes).  

**3. Proposed Solution**  
The paper introduces "Program-as-Weights" (PAW), a paradigm that compiles fuzzy tasks into locally executable neural modules. The core idea is:  
- **Natural Language to Neural Program Compilation**: Developers describe tasks in natural language (e.g., "extract error lines from logs"), which a compiler converts into a lightweight parameter-efficient adapter (e.g., LoRA) embedded in a frozen interpreter (e.g., Qwen3-0.6B);  
- **Two-Stage Compilation**: A pre-trained model generates a clean pseudo-program (with examples), then a trained LoRA compiler produces the adapter;  
- **Local Execution**: Compiled programs run offline on user devices, using 1/50th the memory of direct LLM calls and running at 30 tokens/s on a MacBook M3.  

**4. Key Differences from Prior Work**  
PAW’s innovation lies in shifting the foundation model from "solving each input anew" to "compile once, reuse many times." Unlike rigid rules or direct API calls, PAW uses parameter-efficient fine-tuning (PEFT) to solidify fuzzy tasks into reusable neural modules, balancing flexibility (natural language input) and efficiency (local execution). Additionally, PAW’s compiler is trained on a large-scale fuzzy task dataset (FuzzyBench, 10M examples), unlike prior work limited to single tasks or small data.  

This paradigm paves the way for a "small-model future," where heavy computation happens only at compile time, and daily execution is local, resolving trade-offs between cost, efficiency, and reproducibility.

## Method, Figure by Figure

![Figure 1 : Overview of the Program-as-Weights paradigm. Top: compile once in the](fig1_1.webp)

> Figure 1 : Overview of the Program-as-Weights paradigm. Top: compile once in the cloud. A natural-language description of a fuzzy function (here, “classify if this is urgent”) is fed to a neural compiler, which produces a neural program. Bottom: run locally. A small frozen neural interpreter loads the compiled program and runs the user’s input (“Need your signature by EOD!”) to produce the output (“urgent”). The compiled program is a single file that can be cached, version-controlled, and called offline like any other library function.

This figure clearly illustrates the core workflow of the "Program-as-Weights" (PAW) paradigm, divided into two main phases: "compile once in the cloud" and "run locally."

First, let's look at the upper part of the figure, titled "Compile Once in the Cloud." This phase describes how a neural program is generated from a natural language description.
- The leftmost box is "Description," which contains a natural language function specification, for example, "Classify if this is urgent" in the figure. This description defines a fuzzy functional requirement.
- The middle box is "Neural Compiler," which takes the description above as input. This compiler is a trained model (according to the paper abstract, a 4B-parameter compiler trained on the FuzzyBench dataset), and its role is to convert the natural language description into a "Neural Program."
- The rightmost box is "Neural Program," which is the output of the compiler. This neural program consists of two parts:
    - "Discrete Text": This may represent some structured or symbolic instruction part of the program.
    - "Continuous LoRA": LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning technique, here indicating the trainable parameter part of the program, which is continuous and relatively small in size, allowing the program to be executed locally.
The information flow order is: from "Description" through an arrow to "Neural Compiler," and then from "Neural Compiler" through an arrow to "Neural Program."

Next, we look at the lower part of the figure, titled "Run Locally." This phase describes how to use the neural program compiled in the cloud to process user input and generate output.
- The leftmost box is "Input," which contains the user's actual input data, for example, "Need your signature by EOD!" in the figure. This is the raw data that needs to be processed.
- The middle box is "Neural Interpreter," which receives the input data above and the "Neural Program" compiled in the cloud (indicated by a dashed arrow, meaning the program is preloaded). According to the paper abstract, this interpreter is a frozen, lightweight model (e.g., a 0.6B-parameter Qwen3 interpreter) designed to execute PAW programs.
- The rightmost box is "Output," which shows the processed result, for example, "Urgent" with a warning icon in the figure. This is the final result generated by the neural interpreter based on the input and the compiled program.
The information flow order is: from "Input" through an arrow to "Neural Interpreter," and then from "Neural Interpreter" through an arrow to "Output." At the same time, "Neural Program" flows to "Neural Interpreter" through a dashed arrow, indicating that the program is one of the inputs to the interpreter.

This figure reveals the specific operation of the PAW method:
1. **Compilation Phase**: The user provides a natural language description that defines a fuzzy function (e.g., "determine if it is urgent"). This description is fed into a trained neural compiler, which converts it into a compact neural program. This program consists of discrete text and continuous LoRA parameters, is small in size, and can be executed locally.
2. **Execution Phase**: When actual data needs to be processed, the user feeds the input data (such as a log or a piece of text) into a lightweight neural interpreter. The interpreter loads the precompiled neural program and uses it to process the input data to generate the output result (e.g., "urgent").
The key to this method is that the compiler is only called once when defining the function, and the generated executable program can be cached, version-controlled, and used offline without a network connection. This makes subsequent function calls inexpensive and fast, solving the problems of locality, reproducibility, and cost when directly using large language model APIs.

In summary, this figure shows how the PAW paradigm compiles a fuzzy function described in natural language into a neural program that can be efficiently executed locally, thus implementing a new programming paradigm where the foundation model transitions from a per-input problem solver to a tool builder.

---

![Figure 2 : Text-to-LoRA instantiation of PAW ( Section ˜ 3.2 ). Left. The traine](fig2_1.webp)

> Figure 2 : Text-to-LoRA instantiation of PAW ( Section ˜ 3.2 ). Left. The trained LoRA compiler reads the function specification, the pseudo-program produced by an off-the-shelf prompted pseudo compiler C p C_{p} (not depicted), and a fixed sequence of learned prefix tokens; it emits prefix-position hidden states H H . Middle. The LoRA mapper mean-pools H H , passes it through an MLP, and projects into mixing coefficients that compose LoRA matrices ( A ex , B ex ) (A^{\text{ex}},B^{\text{ex}}) over shared learnable bases ( eq. ˜ 3 ). Right. The frozen interpreter ingests p discrete p_{\text{discrete}} prepended to the user input x x , with the LoRA hot-attached, and generates the output autoregressively. The same pipeline holds for the prefix-tuning precursor ( Section ˜ 3.3 , with architecture in Figure ˜ 18 ); only the mapping from compiler hidden states to PEFT module changes (LoRA → \to KV-cache mapper).

This figure (Figure 2) illustrates the "Text - to - LoRA" implementation of the PAW (Program - as - Weights) method proposed in the paper "Program - as - Weights: A Programming Paradigm for Fuzzy Functions". It is divided into three main parts: the left - hand LoRA Compiler, the middle - hand LoRA Mapper, and the right - hand Interpreter. The flow of data or information and the functions of each component are as follows:

### Left: LoRA Compiler
- **Input**: It consists of three parts, namely `Func Spec` (function specification, blue squares), `Pseudo Program` (generated by an off - the - shelf prompted pseudo - compiler \( C_p \), not shown, green squares), and a fixed sequence of learned prefix tokens `Prefix Tok` (red dotted squares). These inputs represent the information related to the fuzzy function that needs to be compiled into a neural artifact, such as the function description, the pseudocode - like structure, and the fixed prefix information.
- **Processing**: The trained LoRA Compiler reads these inputs and outputs the prefix - position hidden states \( H \) (the three dotted red squares at the top). The role of this compiler is to convert the text - form function specification and other information into a hidden - state representation that can be processed by the neural network, preparing for the subsequent LoRA mapping.

### Middle: LoRA Mapper
- **Input**: The hidden states \( H \) obtained from the LoRA Compiler.
- **Processing steps**:
    1. **Mean Pool**: Perform a mean - pooling operation on the hidden states \( H \). This step may be used to extract the statistical features of the hidden states, reduce the dimension of the data, or highlight the main features.
    2. **MLP**: Pass the result of the mean - pooling through a Multi - Layer Perceptron (MLP). The role of the MLP is to further transform and map the features to generate appropriate parameters.
    3. **LoRA Matrix Combination**: The output of the MLP is used to calculate the mixing coefficients. These mixing coefficients are used to combine the shared learnable bases (`LoRA A Bases` and `LoRA B Bases`, represented by trapezoids of different colors in the figure, those with flame marks may represent different types of bases) to obtain the LoRA matrices (\( A^{\text{ex}}, B^{\text{ex}} \)). Specifically, by multiplying the mixing coefficients with the matrices in `LoRA A Bases` and `LoRA B Bases` (the cross marks in the figure) and then adding them (the plus marks in the figure), the final LoRA parameters are obtained. These parameters will be applied to the Interpreter.

### Right: Interpreter
- **Input**: The user input \( x \) (blue squares, marked as `{x}`) and the predefined discrete tokens \( p_{\text{discrete}} \) (green squares, related to the input of the `Pseudo Program`? Or maybe the discrete representation of the pseudo - program? According to the caption, it should be that \( p_{\text{discrete}} \) is prepended to the user input \( x \)), and at the same time, the LoRA parameters obtained from the LoRA Mapper are hot - attached to the Interpreter.
- **Processing**: The Interpreter (here it is a frozen lightweight interpreter, such as Qwen3) generates the output autoregressively (the blue squares at the top, marked as `Output`). Autoregressive means that it generates the output token by token, based on the previous generation results, the current input, and the LoRA parameters.

### Summary of the Overall Operation Process of the Method
1. **Compilation Stage**: The LoRA Compiler converts the function specification, pseudo - program, and prefix tokens into the hidden states \( H \). This step is to convert the text - form fuzzy function definition into a neural representation.
2. **Mapping Stage**: The LoRA Mapper processes the hidden states \( H \) to generate the LoRA parameters for adjusting the Interpreter. These parameters are obtained through mean - pooling, MLP, and LoRA matrix combination.
3. **Execution Stage**: The Interpreter uses these LoRA parameters and the user input to generate the output autoregressively. The advantage of this method is that the foundation model only needs to be called once for each function definition (the role of the Compiler and the Mapper), and each subsequent function application call is cheap and can be done offline. At the same time, it reduces the memory usage for inference and improves the running speed.

This figure shows the Text - to - LoRA instance of the PAW method. Compared with the predecessor method of prefix - tuning, the main difference is that the mapping from the compiler's hidden states to the PEFT (Parameter - Efficient Fine - Tuning) module changes from LoRA to KV - cache mapping, but the overall process structure is similar, only the way of parameter adjustment is different. Through this method, the method in the paper can transform the large language model from a tool that solves problems for each input into a tool builder. The generated neural artifact can be reused, which improves efficiency and reproducibility.

---

![Figure 5 : Step 1: Compile a program from natural language. The user specifies a](fig4_1.webp)

> Figure 5 : Step 1: Compile a program from natural language. The user specifies a fuzzy function in natural language. Image inputs are also supported.

This figure illustrates the first step of the "Program-as-Weights" (PAW) paradigm proposed in the paper "Program-as-Weights: A Programming Paradigm for Fuzzy Functions": compiling a program from a natural language specification.

The interface is titled "Program Specification," indicating that this step involves defining the desired functionality of the program. The accompanying text, "Describe what your program should do. It can accept text or images as input and will produce text output," further clarifies the type of information the user needs to provide.

There are two main buttons: "New Program" and "Load Existing." Currently, "New Program" is selected, signifying that the user is creating a new program.

Below these buttons is a text input field containing an example: "Extract all email addresses from text and return them as a JSON list." This input field is where the user provides a natural language description of the desired program behavior. The camera icon to the left of the input field indicates that image input is also supported, as mentioned in the original figure caption.

Under the input field is a section labeled "Input/Output Examples," which is currently collapsed (indicated by the arrow on the left). This section is optional (as indicated by the word "Optional" on the right), allowing users to provide specific input-output examples to more precisely define the program's behavior.

At the bottom of the interface, there are two main action buttons. On the left is a prominent blue button labeled "Compile Program" with a star-like icon. This button is the key to triggering the compilation process after the program specification is complete. On the right is a smaller button labeled "Models >" with a gear icon, which likely allows the user to select the underlying model for executing the compiled program.

The flow of data is as follows: the user starts by using the "New Program" or "Load Existing" button. Then, they provide a natural language description of the program's functionality in the text input field, or they can use the camera icon for image input. Optionally, they can provide specific input-output examples in the "Input/Output Examples" section. Finally, the user clicks the "Compile Program" button to compile the natural language-described fuzzy function into a compact, locally executable neural artifact (i.e., a PAW program).

This figure reveals how the method works: a user describes a fuzzy function they want to implement using natural language (e.g., extracting email addresses from text) through a simple interface. This description is fed into a trained compiler (a 4B-parameter compiler mentioned in the paper), which converts this natural language specification into a parameter-efficient adapter for a frozen, lightweight interpreter (like Qwen3). Once compiled, this generated program (the PAW program) can be executed locally without needing to call large language model APIs for each input. This approach reframes the foundation model from a per-input problem solver to a tool builder, thereby improving efficiency, reducing costs, and enhancing reproducibility and locality.

In summary, this figure demonstrates the initial phase of the fuzzy-function programming paradigm, showing how a fuzzy task described in natural language is converted into a compilable program specification. The user provides a functional description, and the system (by clicking the "Compile Program" button) compiles it into an efficient, locally executable program.

---

![Figure 7 : Step 3: Execute the program locally via Python. Once compiled, the pr](fig6_1.webp)

> Figure 7 : Step 3: Execute the program locally via Python. Once compiled, the program can be loaded and invoked through a simple Python API; subsequent execution requires no internet access.

This figure illustrates the third step in the "Program-as-Weights" (PAW) paradigm, as proposed in the paper "Program-as-Weights: A Programming Paradigm for Fuzzy Functions": how to execute a compiled neural program locally using Python.

At the top, a green checkmark and the title "Program Ready!" indicate that the neural program has been successfully compiled and is now ready for deployment. The accompanying text, "Your neural program is compiled. Add it to your Python code:", guides the user on integrating this compiled program into their Python environment.

The process is divided into two main steps:

1.  **Install ProgramAsWeights Library**:
    *   The first section, titled "1. Install ProgramAsWeights," instructs the user to install a Python library named `programasweights`. It provides a command-line instruction: `pip install programasweights`, which the user can execute to install the necessary dependency. A "Copy" button is available to facilitate copying this command.

2.  **Use Your Program**:
    *   The second section, titled "2. Use Your Program," includes a note: "Runs 100% locally—no API calls or internet needed (after initial model download)." This highlights the core advantage of the method: once the initial model is downloaded, subsequent executions occur entirely locally, ensuring data privacy, reproducibility, and reduced operational costs.
    *   Below this note is a code example displayed in a dark-themed box with light text, demonstrating how to use the compiled program in Python:
        *   The first line is an import statement: `import programasweights as paw`, which imports the `programasweights` library and aliases it as `paw` for convenience.
        *   Next, the compiled neural program is loaded: `fn = paw.function("d8837e679e5a")`. Here, `paw.function()` is the API provided by PAW. The user passes a unique identifier (in this case, the string "d8837e679e5a") to load a specific compiled neural program. This function is assigned to the variable `fn`, allowing it to be called like a regular Python function.
        *   The loaded function is then used: `output = fn("Hi team,\n\nPlease contact the following people for assistance:\n- Alice Walker: alic...")`. The function `fn` is called with a specific input (a piece of text containing contact information, partially truncated). The result of this call is stored in the variable `output`.
        *   Finally, the output is printed: `print(output)` to display the result of the function execution.
        *   Below the code example, expected output is commented: `# Expected output: # "[\"alice.w.cur@example.com\",\"bob-sales@shop.co.uk\",\"support@company.org\",\"john.doe+perso..."`, showing the format of the result (a JSON array of email addresses) that the function should return after processing the input.

The flow of data is as follows: the user first installs the `programasweights` library, then uses the API provided by this library to load a compiled neural program (via its unique ID). Subsequently, the loaded function is called with input data, similar to a regular Python function, and the processed output is obtained. The entire process emphasizes local execution: once the program is compiled and loaded, subsequent calls are local and efficient, without requiring further access to cloud APIs.

This figure reveals how the PAW method operates: it compiles a fuzzy function, described in natural language, into a compact neural artifact that can be executed locally. Users interact with this artifact through a simple Python API, treating it like a regular function. This approach reframes the foundation model (e.g., Qwen) from a per-input problem solver to a tool builder: the model is invoked once per function definition to generate this small, reusable artifact. Subsequent function applications are inexpensive and can be performed offline. The example in the figure demonstrates how a fuzzy task, such as information extraction (e.g., extracting email addresses from text), can be compiled and executed locally and efficiently using PAW.

---

![Figure 19 : A library of compiled PAW programs. Three example natural-language f](fig8_1.webp)

> Figure 19 : A library of compiled PAW programs. Three example natural-language function specifications (“Classify message urgency”, “Fix malformed JSON”, “Remove personal information”; left) are each compiled into a separate neural program (middle): a discrete pseudo-program in a fixed format plus a continuous per-example LoRA (depicted as red, blue, green adapters). At deployment time (right), all three programs are served by a single device-resident interpreter ( LM ) with the appropriate LoRA hot-attached per call — the “one runtime, many programs” picture that motivates compile-once-run-locally.

This figure (Figure 19) illustrates the core workflow of the "Program-as-Weights" (PAW) method, which compiles natural language-described functional specifications into locally executable neural programs and deploys them through a shared interpreter.

First, we look at the leftmost panel, "Function Specification." It lists three example natural language task descriptions:
1.  "Classify message urgency" (分类消息紧急程度), represented by a red envelope icon.
2.  "Fix malformed JSON" (修复格式错误的JSON), represented by a blue wrench icon.
3.  "Remove personal information" (移除个人信息), represented by a green lock icon.
These are non-structured user-provided functional requirements.

Next, an arrow points from the "Function Specification" panel to the middle "Neural Programs" panel, labeled "Compile" at the bottom. This represents the compilation process: a pre-trained "compiler" (indicated by the robot icon at the bottom of the figure, noted in the paper as a 4B-parameter compiler) converts these natural language specifications into neural programs. The middle "Neural Programs" panel shows the compiled results, one for each input functional specification:
1.  The first neural program contains a red pseudocode window icon, with adjacent text describing the task: "[PSEUDO_PROGRAM] Task: Classify a message as 'immediate' ..." (伪程序：任务是将消息分类为“紧急”...). Next to it is a red funnel-shaped icon labeled "LoRA 1," representing a parameter-efficient adapter (Low-Rank Adaptation).
2.  The second neural program contains a blue pseudocode window icon, with a task description: "[PSEUDO_PROGRAM] Task: Fix malformed JSON by adding missing ..." (伪程序：任务是通过添加缺失部分来修复格式错误的JSON...). Next to it is a blue funnel-shaped icon labeled "LoRA 2."
3.  The third neural program contains a green pseudocode window icon, with a task description: "[PSEUDO_PROGRAM] Task: Remove all names, addresses, email addresses ..." (伪程序：任务是移除所有姓名、地址、电子邮件地址...). Next to it is a green funnel-shaped icon labeled "LoRA 3."
This process indicates that each natural language functional specification is compiled into a "discrete pseudo-program" (fixed-format pseudocode) and a "continuous, example-specific LoRA adapter" (learnable weight adjustments).

Then, an arrow points from the "Neural Programs" panel to the rightmost "Local Deployment" panel, labeled "Interpret" at the bottom. This represents the deployment and execution phase. The rightmost "Local Deployment" panel shows a shared "LM" (Large Language Model) interpreter (represented by a black paw print icon) as the runtime environment. Each neural program, when called, has its corresponding LoRA adapter "hot-attached" to this shared LM interpreter:
1.  For "PAW Email Triage" (PAW邮件分诊), the input is various email icons (e.g., spam, regular emails), and after processing by the LM with "LoRA 1," the output is classification results (e.g., hourglass, checkmark, warning triangle icons).
2.  For "PAW Json Fixer" (PAW JSON修复器), the input is malformed JSON snippets (e.g., {} with missing brackets), and after processing by the LM with "LoRA 2," the output is fixed JSON snippets.
3.  For "PAW PII Redactor" (PAW个人信息编辑器), the input is documents containing personal information (e.g., locked files, passwords), and after processing by the LM with "LoRA 3," the output is documents with personal information removed.
This "one runtime, many programs" picture is precisely the embodiment of the "compile-once-run-locally" philosophy. The shared LM interpreter is fixed, while different LoRA adapters provide specific functionalities for different tasks.

In summary, this figure clearly demonstrates the PAW method's workflow: starting from natural language functional specifications, compiling them into neural programs containing pseudo-programs and LoRA adapters, and then, during deployment, executing these neural programs through a shared lightweight interpreter, loading the appropriate LoRA adapter as needed. This method reframes the foundation model from a per-input problem solver to a tool builder, invoked once per function definition to produce a reusable artifact, with subsequent function calls being inexpensive and offline.

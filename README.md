# Methods of Synthetic Data Generation for Combinatorial Problems with Large Language Models

This repository contains the code and data used for a research experiment evaluating the capabilities of large language models (LLMs) in processing and generating mathematical texts. The research introduces new problem variations and a metric that captures the performance rate and correlation between baseline problems and generated variations.

**Note:** The filtered dataset and code will be released upon paper approval.

## Project Stages

- **Stage 1: Filtering**
  - Filter 1,000 problems from [NuminaMath-COT](https://huggingface.co/datasets/AI-MO/NuminaMath-COT).

- **Stage 2: Answer Extraction**
  - Apply LLM along with regex functions for answer extraction.

- **Stage 3: Variation Generation**
  - Use LLM to generate three new variations of the original problems: *fictional* *adversarial* and *contextual disguise*.

- **Stage 4: Results Comparison**
  - Run permutation tests and correlation tests to assess the quality of the generated data and LLM performance.

## Models Used in the Experiment

The open-source models tested during experimentation have been quantized using K-means quantization with the help of the [llama.cpp](https://github.com/ggerganov/llama.cpp) library.

| Model                  | Quant. | Quant. Method | Access      | Model Creator |
|------------------------|--------|---------------|-------------|---------------|
| LLaMA-2-7B-Chat        | ✓      | Q4_K_M        | Open-source | Meta          |
| Llama-3-8B-Instruct    | ✓      | Q4_K_M        | Open-source | Meta          |
| Mathstral-7B           | ✓      | Q4_K_M        | Open-source | Mistral AI    |
| Mixtral-8x7B-Instruct  | ✓      | Q4_K_M        | Open-source | Mistral AI    |
| Qwen2-7B-Instruct      | ✓      | Q4_K_M        | Open-source | Qwen          |
| Qwen2-Math-7B          | ✓      | Q4_K_M        | Open-source | Qwen          |
| GPT-4o-mini-2024-07-18 | ✗      | N/A           | API         | OpenAI        |

## Installation

To set up the environment and run the scripts, install the necessary Python libraries using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Dataset Information

### NuminaMath-CoT Data (the Baseline)

| Column Name | Description                          |
|-------------|--------------------------------------|
| problem_id  | Unique identifier for each problem.  |
| source      | Problem origin.                      |
| problem     | Problem statement.                   |
| solution    | Problem solution.                    |
| messages    | Chain-of-Thought data.               |
| answer      | Problem answer extracted (expected). |

### Synthetically Generated Data

| Column Name     | Description                                    |
|-----------------|------------------------------------------------|
| fictional       | Fictional variation of the problem.            |
| adversarial     | Adversarial variation of the problem.          |
| contdis         | Contextual disguise variation of the problem.  |
| original_sol    | Original variation solution generated by model.|
| fictional_sol   | Fictional variation solution.                  |
| adversarial_sol | Adversarial variation solution.                |
| contdis_sol     | Contextual disguise variation solution.        |
| original_ans    | Original variation answer extracted.           |
| fictional_ans   | Fictional variation answer extracted.          |
| adversarial_ans | Adversarial variation answer extracted.        |
| contdis_ans     | Contextual disguise answer extracted.          |



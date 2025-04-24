# Prompt-Engineering-Project

- [1. Introduction](#1-introduction)
- [2. Getting Started](#2-getting-started)
  - [2.1 Preparations](#21-preparations)
  - [2.2 Install Packages](#22-install-packages)
- [3. Evaluation](#3-evaluation)
- [4. Results](#4-results)

---

# **1. Introduction**

This project examined different prompting techniques such as **Zero-shot**, **Few-shot**, and **Chain-of-Thought** prompting. The goal was to evaluate the performance of these techniques in generating code snippets for a given task. For each problem and prompt type, output data was taken from the GPT-4o model and the Gemini 2.0 Flash model.

# **2. Getting Started**

This project is implemented in **Python 3.12+** and is compatible with **macOS, Linux, and Windows**.

## **2.1 Preparations**

(1) Clone the repository to your workspace:

```shell
~ $ git clone https://github.com/LynSChen04/in-context_prompt_engineering
```

(2) Navigate into the project repository:

```
~ $ cd in-context_prompt_engineering
~/in-context_prompt_engineering $
```

(3) Set up a virtual environment and activate it:

For macOS/Linux:

```
~/in-context_prompt_engineering $ python -m venv ./venv/
~/in-context_prompt_engineering $ source venv/bin/activate
(venv) ~/in-context_prompt_engineering $
```

For Windows:

```
~/in-context_prompt_engineering $ python -m venv ./venv/
~/in-context_prompt_engineering $ ./venv/Scripts/activate
```

To deactivate the virtual environment, use the command:

```
(venv) $ deactivate
```

## **2.2 Install Packages**

Install the required dependencies:

```shell
(venv) ~/in-context_prompt_engineering $ pip install -r requirements.txt
```

---

# **3. Evaluation**

We used BLEU in order to evaluate the similarity between the two inputs. However we also implemented the ability to use METEOR as an evaluation metric as well. The user can switch between the two by passing either a `B` for BLEU or `M` for METEOR. We decided to use BLEU as our metric as it gave us high level evaluation which is what we deemed to be the best.

# **4. Results**

The raw data consisting of 88 outputs, 2 types of prompts from the 2 models for each of the 22 problems. This data is stored in `complete_outputs.json`. The script `main.py` was used to automate the process of generating outputs. The script generated 76 total prompt outputs, skipping prompts 18, 21, and 22 which were done manually.  The output of the prompts is the `prompts_output.json` file. We also used the script to obtain BLEU evaluations of the generated code. Our PDF report containing our analysis and outputs of notable problems as well as BLEU scores for all the problems with code outputs is the `Assignment Three.pdf` file. The BLEU evaluation scores for the outputs is the `BLEU_evaluation.json` file. The METEOR evaluation scores for the output is in `prompt_eval.json`.

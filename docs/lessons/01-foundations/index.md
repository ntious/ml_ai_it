# Module 1: ML and AI foundations for practical decisions

Begin here if you are new to ML, AI, or Python. You will compare ways to solve a service problem, run a small program, change its input, and save an explained result. No prior programming, paid account, GPU, or AI service is required. Estimated effort: 60–90 minutes plus installation; this estimate needs learner piloting.

## Learning outcomes

- **M01.1:** Distinguish AI, ML, deep learning, and generative AI using an IT example.
- **M01.2:** Identify a problem's stakeholder, input, output, and reason for choosing a rule or learned model.
- **M01.3:** Execute and save a supplied Python example; in the notebook route, launch the interface, run a cell, and save the notebook. Explain the installation route.
- **M01.4:** Change an input, predict the result, and explain what happened.

The script route supplies the same programming evidence when a notebook interface is a barrier. It does not demonstrate notebook-interface operation. An instructor assessing that particular skill should arrange an accessible interface and support with the learner.

## Understand the methods

**Artificial intelligence (AI)** is a broad field of systems that perform tasks associated with intelligence, such as reasoning, perception, or language use. **Machine learning (ML)** develops models using patterns in data. **Deep learning** is ML using neural networks with multiple layers. **Generative AI** produces content such as text, images, or code; many current generative systems use deep learning. These terms describe different aspects of systems and are not four interchangeable labels.

A **feature** is an input representation, such as recent request count. A **target** is a value the model is intended to predict, such as next-hour workload. **Training** fits a model using data; **inference** applies a trained model to inputs. A function that compares a measurement to a threshold has not learned that threshold from data.

| Learning approach | Feedback during learning | IT example to reason about |
| --- | --- | --- |
| Supervised | Examples with target values | Predict next-hour ticket volume from past workload and calendar features |
| Unsupervised | No supplied target labels | Group devices by similar traffic patterns; investigate the groups before naming them |
| Reinforcement | Rewards from actions and interactions | Learn a resource-allocation policy in a simulator; unsafe exploration would be inappropriate on live servers |

Generating text is an output capability, not a fourth mutually exclusive learning paradigm. An LLM may be trained in several stages using different feedback. A fluent response can still contain unsupported claims.

## Compare three service decisions

A fictional service team wants fewer interruptions. The following are design sketches, not three implemented systems.

| Approach | Inputs and output | What evidence is needed? |
| --- | --- | --- |
| Human-written rule | Current storage usage → review above 80% | Boundary checks and an operational reason for the chosen threshold |
| Learned workload predictor | Historical workload/features → future count | Representative data, a simple baseline, and held-out evaluation; implementation begins in later modules |
| Generated draft reply | A ticket and approved facts → proposed response text | Factual checks, privacy controls, and human review before sending |

For the first program, choose the rule: its behavior is small enough to inspect completely. The stakeholder is an IT operator. Its output requests review; it neither deletes files nor changes a server. The 80% threshold is an arbitrary teaching choice, not industry guidance. A rule may be sufficient when the requirement is explicit. ML becomes a candidate when learning from examples is useful and its errors can be evaluated.

## Run and save the first example

Download and extract the [complete source archive](../../downloads/ml_ai_it-source.zip), or use your repository checkout. Open a terminal in its `ml_ai_it` folder. Install Python if needed using the [first-run guide](../../../QUICKSTART.md). For Modules 1 and 2, Python's standard library is sufficient; no package installation is needed.

On Windows PowerShell:

```powershell
py examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

On macOS or Linux:

```sh
python3 examples/first-run/scripts/first_run.py --storage-percent 85 --output runs/module01/first-run.txt
```

The named text result says storage used is 85 percent, the review threshold is 80 percent, and the decision is `Review storage`. It explicitly says no model was trained and no AI service was called. Open `runs/module01/first-run.txt` in a text editor. The file preserves the same explanation. Rerunning with the same output path replaces that file; use a different name to keep a comparison.

Read `src/practical_ml_ai/foundations.py`. The central expression is `storage_percent > threshold`. `>` means strictly greater than. The function returns a Boolean: `True` or `False`. The script imports this shared function; it does not contain a separate algorithm.

## Notebook route

The [first-steps notebook](../../downloads/module01/first_steps.ipynb) calls the same functions. Keep the source archive's folder structure and open `notebooks/lessons/01-foundations/first_steps.ipynb` using the [notebook setup instructions](../../../QUICKSTART.md#notebook-option).

A notebook contains text cells and code cells. Its kernel is the Python process holding variables. Open the notebook, select the first code cell, and use your interface's Run command. Run subsequent cells in order. Use File → Save (or the interface's documented keyboard command), then close, reopen, restart the kernel, and run all cells to check that saved work does not depend on hidden state. A downloaded notebook is a file, not an installed interface. Installation and screen-reader usability are separate checks; see [current accessibility status](../../accessibility/index.md).

## Read selectively

- **Core concepts:** [Google's Introduction to ML](https://developers.google.com/machine-learning/intro-to-ml): read the introduction and types of ML sections. No full external course is required.
- **Setup reference:** [Python downloads](https://www.python.org/downloads/), only if Python is missing. Our recorded checks use Python 3.12; the examples require 3.11 or newer.
- **Optional foundation support:** [Python foundations OER](https://ntious.github.io/python_foundation/): getting started, variables, and output as needed.

## Practice and continue

Complete [practice and reflection](practice.md), then use [worked feedback](feedback.md). If using GenAI, ask it to explain why 80 and 81 give different results. Verify the explanation by reading `>` and running both values; you should be able to explain the result yourself. No AI account is required: the feedback supplies a sample explanation.

Next: [Module 2, Python for reproducible ML workflows](../02-python-workflows/index.md). A learner arriving directly at a later module can use this page as a short setup and terminology bridge.

## Support and teaching

Use the [foundation bridge](foundation.md) for the rule/model distinction and first trace. [Instructor guidance](instructor.md) provides adaptation and outcome-evidence notes.

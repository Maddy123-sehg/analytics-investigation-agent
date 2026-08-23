# Analytics Investigation Agent

A small, interview-explainable Python agent that investigates a daily revenue change. It uses a visible decision loop and two analytics tools to identify the likely driver from sample sales data.

## What makes it agentic?

The agent has a goal, chooses which business dimensions to inspect, calls tools, observes their results, and synthesizes an evidence-backed conclusion. Version 1 uses a deterministic policy instead of an LLM, making every decision easy to trace, test, and explain.

```text
question -> headline metrics -> category/region/channel tools -> rank drivers -> conclusion
```

## Project structure

```text
analytics_agent/agent.py   decision loop and final explanation
analytics_agent/tools.py   reusable analytics tools
data/sales.csv             intentionally small sample dataset
tests/test_agent.py        behavior checks
main.py                    command-line entry point
```

## Run it

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The requirements file is intentionally empty in version 1; the install command is included so the setup remains familiar when dependencies are added later.

Run the tests:

```bash
python -m unittest discover -s tests
```

No API key is needed. To customize the data location, copy `.env.example` to `.env`; `.env` is ignored by Git so local settings and future secrets stay out of the repository.

## How to explain it in an interview

1. **Goal:** explain a revenue change with evidence.
2. **Tools:** one tool calculates headline metrics; another groups them by a chosen dimension.
3. **Agent loop:** decide what to inspect, call a tool, observe, repeat, then synthesize.
4. **Guardrails:** allowed dimensions are explicit, the dataset is read-only, and tests cover the expected driver.
5. **Tradeoff:** the deterministic policy is transparent and cheap, but less flexible than an LLM planner.

## Good version-2 extensions

- Accept natural-language questions and dates.
- Put the data in SQLite and add a read-only SQL tool.
- Add an LLM planner while retaining tool validation and the trace.
- Add charts or a small Streamlit interface.

## Publish to GitHub

Create an empty GitHub repository named `analytics-investigation-agent` (do not initialize it with a README, `.gitignore`, or license), then run:

```bash
git init
git add README.md .gitignore .env.example requirements.txt main.py analytics_agent data tests
git commit -m "Initial analytics investigation agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/analytics-investigation-agent.git
git push -u origin main
```

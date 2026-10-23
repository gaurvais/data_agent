# DataAgent

DataAgent is a Python application that uses LangGraph and Google Gemini to route
natural-language requests to either a PostgreSQL SQL analyst or an ETL analyst.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Features](#2-features)
3. [Architecture](#3-architecture)
4. [Prerequisites](#4-prerequisites)
5. [Installation](#5-installation)
6. [Configuration](#6-configuration)
7. [Usage](#7-usage)
8. [Agent Descriptions](#8-agent-descriptions)
9. [Project Structure](#9-project-structure)
10. [Examples](#10-examples)

---

## 1. Overview

DataAgent accepts a single natural-language message and automatically routes it
to the correct specialist agent:

- **SQL Analyst** — answers questions about data in a PostgreSQL database.
- **ETL Analyst** — extracts data from API endpoints or transforms local files.

A lightweight **Streamlit dashboard** (`app.py`) provides a browser-based
interface to the same pipeline.

---

## 2. Features

- Answers natural-language questions about a PostgreSQL database.
- Extracts data from an API endpoint and saves it as CSV, JSON Lines, or Parquet.
- Transforms local CSV, JSON Lines, or Parquet files based on a natural-language
  instruction.
- Judges generated SQL for safety before execution (read-only guard).
- Streamlit dashboard for interactive use without editing Python files.
- Includes LangGraph architecture diagrams for all three agents.

---

## 3. Architecture

```
User Question
      │
      ▼
 Data Agent (LangGraph)
      │
  [Router Node] ─── decides: "sql" or "etl"
      │
      ├── sql ──▶ SQL Analyst Graph
      │               curate_ques → prompt_query_context → generate_sql
      │               → is_safe_sql → execute_sql → represent_final_answer
      │
      └── etl ──▶ ETL Analyst Graph
                      llm_node ⇄ tool_node
                      (extract_load_tool | transform_load_tool)
```

Architecture diagram images:

- [Data agent](./data_agent_graph.png)
- [SQL analyst](./sql_analyst_graph.png)
- [ETL analyst](./etl_analyst_graph.png)

---

## 4. Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key (`GOOGLE_API_KEY`)
- A PostgreSQL database (required only for SQL analyst queries)

---

## 5. Installation

1. Clone the repository and enter the project directory.
2. Install all dependencies (including Streamlit):

   ```powershell
   uv sync
   ```

---

## 6. Configuration

Create a `.env` file in the project root:

```dotenv
GOOGLE_API_KEY=your-google-api-key

# Required for SQL analyst queries
host=localhost
port=5432
database=your-database
user=your-database-user
password=your-database-password
```

Keep `.env` private — it is excluded from Git.

---

## 7. Usage

### Streamlit Dashboard (recommended)

```powershell
uv run streamlit run app.py
```

Open the URL shown in the terminal (default: `http://localhost:8501`), type your
question or ETL instruction, and click **Run Agent**.

### Command-line

Edit the `HumanMessage` content in `main.py` and run:

```powershell
uv run python main.py
```

The data agent routes the request automatically to the SQL or ETL analyst.

---

## 8. Agent Descriptions

### Data Agent (`agents/data_agent.py`)

The top-level orchestrator. Accepts `{"messages": [HumanMessage(...)], "route_response": ""}`.
A router LLM classifies the request as `"sql"` or `"etl"` and delegates to the
appropriate sub-graph. The final result is returned in the same state object.

### SQL Analyst (`agents/sql_analyst.py`)

Handles database questions. Pipeline:

1. **curate_ques** — rewrites the user's question for SQL generation.
2. **prompt_query_context** — fetches the live database schema and builds a prompt.
3. **generate_sql** — generates a PostgreSQL query.
4. **is_safe_sql** — a judge LLM checks that the query is read-only.
5. **execute_sql** — runs the query against PostgreSQL.
6. **represent_final_answer** — converts the result rows to a plain-English answer.

The final answer is stored in `state.final_answer`.

### ETL Analyst (`agents/etl_analyst.py`)

Handles data extraction and transformation. Uses two LangChain tools:

- **extract_load_tool** — calls an API endpoint and saves the response as
  CSV, JSON Lines, or Parquet.
- **transform_load_tool** — reads a local file, generates Pandas code with an
  LLM, executes it, and saves the output.

The agent loops between `llm_node` and `tool_node` until no more tool calls are
needed.

---

## 9. Project Structure

```
DataAgent/
├── app.py                  # Streamlit dashboard
├── main.py                 # CLI entry point
├── pyproject.toml          # Project metadata and dependencies
├── agents/
│   ├── data_agent.py       # Top-level routing agent
│   ├── sql_analyst.py      # PostgreSQL analyst sub-graph
│   └── etl_analyst.py      # ETL analyst sub-graph
├── Models/
│   └── schema.py           # Pydantic state schemas for all agents
├── utils/
│   ├── database.py         # PostgreSQL connection and query utilities
│   ├── etl_tools.py        # Extract, transform, and code-execution helpers
│   └── llm_pick.py         # LLM factory (low / medium / high tiers)
├── data/
│   ├── extract/            # Output folder for extracted data
│   ├── transform/          # Output folder for transformed data
│   └── *.csv               # Sample data files (excluded from Git)
├── src/dataagent/          # Installable package entry point
├── data_agent_graph.png    # LangGraph diagram — data agent
├── sql_analyst_graph.png   # LangGraph diagram — SQL analyst
└── etl_analyst_graph.png   # LangGraph diagram — ETL analyst
```

---

## 10. Examples

### SQL question

> "What are the different types of Payment Methods we have in our database?"

The router classifies this as `sql`. The SQL analyst fetches the schema, generates
`SELECT DISTINCT payment_method FROM payments LIMIT 10;`, verifies it is
read-only, executes it, and returns a natural-language summary.

### ETL — extract

> "Extract data from `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd` and save it to data/extract in csv format."

The router classifies this as `etl`. The ETL analyst calls `extract_load_tool`,
which fetches the JSON response and writes `data/extract/extracted_data.csv`.

### ETL — transform

> "Transform `data/extract/extracted_data.csv` — filter to show bitcoin and ethereum only — save to `data/transform` as parquet."

The router classifies this as `etl`. The ETL analyst calls `transform_load_tool`,
which reads the file, generates Pandas code, executes it, and saves the result.

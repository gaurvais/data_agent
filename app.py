"""
DataAgent Streamlit Dashboard
==============================
A minimal dashboard that exposes the existing data_agent LangGraph pipeline.
The agent automatically routes natural-language requests to either the
SQL analyst (database questions) or the ETL analyst (extract/transform tasks).
"""

import sys
import os

# Ensure the project root is on the path so agent imports resolve correctly
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from langchain_core.messages import HumanMessage

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataAgent Dashboard",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Color palette ─────────────────────────────────────────────────────────────
NAVY     = "#123B65"
BLUE     = "#1F5A94"
LIGHT_BG = "#EAF2F8"
BG       = "#F5F7FA"
WHITE    = "#FFFFFF"
TEXT     = "#243447"
MUTED    = "#64748B"
BORDER   = "#D9E2EC"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
        /* Page background */
        .stApp {{
            background-color: {BG};
        }}

        /* Hide default Streamlit header/footer */
        #MainMenu, footer, header {{ visibility: hidden; }}

        /* ── Dashboard header ── */
        .da-header {{
            background: linear-gradient(135deg, {NAVY} 0%, {BLUE} 100%);
            color: {WHITE};
            padding: 2rem 2.5rem 1.8rem;
            border-radius: 10px;
            margin-bottom: 1.75rem;
        }}
        .da-header h1 {{
            margin: 0 0 0.3rem 0;
            font-size: 1.9rem;
            font-weight: 700;
            letter-spacing: 0.02em;
        }}
        .da-header p {{
            margin: 0;
            font-size: 0.95rem;
            opacity: 0.85;
        }}

        /* ── Info pill ── */
        .da-pill {{
            display: inline-block;
            background: {LIGHT_BG};
            color: {BLUE};
            border: 1px solid {BORDER};
            border-radius: 20px;
            padding: 0.25rem 0.85rem;
            font-size: 0.8rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }}

        /* ── Card ── */
        .da-card {{
            background: {WHITE};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 1.5rem 1.75rem;
            margin-bottom: 1.25rem;
        }}
        .da-card h3 {{
            color: {NAVY};
            margin: 0 0 0.75rem 0;
            font-size: 1rem;
            font-weight: 600;
        }}

        /* ── Output box ── */
        .da-output {{
            background: {LIGHT_BG};
            border: 1px solid {BORDER};
            border-left: 4px solid {BLUE};
            border-radius: 6px;
            padding: 1rem 1.25rem;
            color: {TEXT};
            font-size: 0.93rem;
            line-height: 1.65;
            white-space: pre-wrap;
            word-break: break-word;
        }}

        /* ── Route badge ── */
        .da-badge-sql {{
            display: inline-block;
            background: #E3F0FB;
            color: {BLUE};
            border: 1px solid #B6D4EE;
            border-radius: 4px;
            padding: 0.1rem 0.6rem;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.6rem;
        }}
        .da-badge-etl {{
            display: inline-block;
            background: #E8F5E9;
            color: #2E7D32;
            border: 1px solid #A5D6A7;
            border-radius: 4px;
            padding: 0.1rem 0.6rem;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.6rem;
        }}

        /* ── Button styling ── */
        .stButton > button {{
            background-color: {NAVY};
            color: {WHITE};
            border: none;
            border-radius: 6px;
            padding: 0.55rem 1.6rem;
            font-weight: 600;
            font-size: 0.92rem;
            transition: background-color 0.2s;
        }}
        .stButton > button:hover {{
            background-color: {BLUE};
            color: {WHITE};
        }}

        /* ── Text area ── */
        .stTextArea textarea {{
            border: 1px solid {BORDER};
            border-radius: 6px;
            font-size: 0.92rem;
            color: {TEXT};
        }}
        .stTextArea textarea:focus {{
            border-color: {BLUE};
            box-shadow: 0 0 0 2px {LIGHT_BG};
        }}

        /* ── Divider ── */
        hr {{
            border: none;
            border-top: 1px solid {BORDER};
            margin: 1.25rem 0;
        }}

        /* ── Muted text ── */
        .muted {{
            color: {MUTED};
            font-size: 0.82rem;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="da-header">
        <h1>🤖 DataAgent Dashboard</h1>
        <p>
            Ask questions about your PostgreSQL database or request ETL operations
            on API data and local files — the agent routes your request automatically.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── How-it-works pill ─────────────────────────────────────────────────────────
st.markdown(
    f'<span class="da-pill">SQL Analyst &nbsp;·&nbsp; ETL Analyst &nbsp;·&nbsp; Auto-routed by LangGraph</span>',
    unsafe_allow_html=True,
)

# ── Agent guide card ──────────────────────────────────────────────────────────
with st.expander("ℹ️  How the agents work", expanded=False):
    st.markdown(
        f"""
        <div style="color:{TEXT}; font-size:0.9rem; line-height:1.7;">
            <b>SQL Analyst</b> — answers natural-language questions about data stored in your
            PostgreSQL database. It curates your question, generates a safe SQL query,
            evaluates its safety, executes it, and returns a plain-English answer.<br><br>
            <b>ETL Analyst</b> — extracts data from an API endpoint and saves it as
            <code>csv</code>, <code>json</code>, or <code>parquet</code>; or transforms a
            local file based on your instructions.<br><br>
            The <b>router</b> reads your question and automatically decides which analyst
            to invoke. You do not need to select one manually.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="margin-top:0.75rem; color:{MUTED}; font-size:0.82rem;">
            <b>SQL examples:</b><br>
            &nbsp;• "What are the different payment methods in our database?"<br>
            &nbsp;• "Show me the top 5 users by number of rides."<br><br>
            <b>ETL examples:</b><br>
            &nbsp;• "Extract data from https://api.example.com/data and save as CSV in data/extract"<br>
            &nbsp;• "Transform data/extract/extracted_data.csv — keep only rows where amount > 100 — save to data/transform as parquet"
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="da-card"><h3>💬 Your Question or Instruction</h3>', unsafe_allow_html=True)

user_input = st.text_area(
    label="Question",
    placeholder=(
        "e.g.  What are the different types of Payment Methods we have in our database?\n"
        "      Extract data from https://api.coingecko.com/... and save to data/extract in csv"
    ),
    height=110,
    label_visibility="collapsed",
)

run_col, _ = st.columns([1, 4])
with run_col:
    run_clicked = st.button("▶  Run Agent")

st.markdown("</div>", unsafe_allow_html=True)

# ── Run & display output ──────────────────────────────────────────────────────
if run_clicked:
    if not user_input.strip():
        st.warning("Please enter a question or instruction before running the agent.")
    else:
        with st.spinner("Agent is thinking…"):
            try:
                # Import here so loading errors surface as friendly messages
                from agents.data_agent import data_agent

                result = data_agent.invoke(
                    {
                        "messages": [HumanMessage(content=user_input.strip())],
                        "route_response": "",
                    }
                )

                # ── Determine which agent was invoked ──────────────────────
                route = result.get("route_response", "").lower()

                # ── Extract the answer ─────────────────────────────────────
                if route == "sql":
                    # SQL agent stores the final answer in result["final_answer"]
                    answer = result.get("final_answer", "").strip()
                    if not answer:
                        # Fall back to last AI message
                        msgs = result.get("messages", [])
                        answer = next(
                            (m.content for m in reversed(msgs) if hasattr(m, "content")),
                            "No answer returned.",
                        )
                    badge_html = '<span class="da-badge-sql">SQL Analyst</span>'

                elif route == "etl":
                    # ETL result is in the last message of the messages list
                    msgs = result.get("messages", [])
                    answer = next(
                        (m.content for m in reversed(msgs) if hasattr(m, "content")),
                        "ETL operation completed but returned no message.",
                    )
                    badge_html = '<span class="da-badge-etl">ETL Analyst</span>'

                else:
                    # Unexpected route — show whatever we received
                    msgs = result.get("messages", [])
                    answer = next(
                        (m.content for m in reversed(msgs) if hasattr(m, "content")),
                        str(result),
                    )
                    badge_html = '<span class="da-badge-sql">Unknown Route</span>'

                # ── Render output card ─────────────────────────────────────
                st.markdown(
                    f"""
                    <div class="da-card">
                        <h3>📋 Agent Response</h3>
                        {badge_html}
                        <div class="da-output">{answer}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            except ImportError as e:
                st.error(
                    f"**Import error:** {e}\n\n"
                    "Make sure all dependencies are installed (`uv sync`) and that your "
                    "`.env` file is present with a valid `GOOGLE_API_KEY`."
                )
            except KeyError as e:
                st.error(
                    f"**Environment variable missing:** {e}\n\n"
                    "Check that your `.env` file contains `host`, `port`, `database`, "
                    "`user`, and `password` for the SQL analyst."
                )
            except Exception as e:
                st.error(f"**Agent error:** {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f'<p class="muted" style="text-align:center;">DataAgent · Powered by LangGraph &amp; Google Gemini</p>',
    unsafe_allow_html=True,
)

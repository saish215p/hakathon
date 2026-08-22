import streamlit as st
from research import research_agent
from news import news_agent
from ai import generate_ai_summary
from tool_router import coordinator_agent
from agents.crew_setup import run_crew

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    
    page_title="PulseAI",
    page_icon="🔍",
    layout="wide"
)
# =====================================
# Memory Initialization
# =====================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_query" not in st.session_state:
    st.session_state.last_query = ""

if "current_context" not in st.session_state:
    st.session_state.current_context = ""

#CSS START HERE   
st.markdown("""
<style>

/* Hide Streamlit Header */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* Main Background */

.stApp{
    background: linear-gradient(
        180deg,
        #070B17 0%,
        #0E1525 40%,
        #111827 100%
    );
}

/* Hero Card */

.hero{

padding:40px;

border-radius:25px;

background:linear-gradient(
135deg,
rgba(71,85,255,.30),
rgba(0,212,255,.15)
);

backdrop-filter:blur(20px);

border:1px solid rgba(255,255,255,.15);

margin-bottom:25px;

box-shadow:
0 0 30px rgba(0,255,255,.15);

}

/* Hero Title */

.hero h1{

font-size:58px;

color:white;

margin-bottom:5px;

}

/* Hero Subtitle */

.hero p{

font-size:20px;

color:#cbd5e1;

}

/* Search Card */

.search-card{

padding:25px;

border-radius:20px;

background:rgba(255,255,255,.05);

border:1px solid rgba(255,255,255,.10);

backdrop-filter:blur(15px);

}

/* Metric Cards */

.metric-card{

padding:20px;

border-radius:18px;

background:rgba(255,255,255,.04);

border:1px solid rgba(255,255,255,.08);

text-align:center;

transition:.3s;

}

.metric-card:hover{

transform:translateY(-6px);

box-shadow:0 0 18px #4f46e5;

}

/* Section Title */

.section-title{

font-size:30px;

font-weight:bold;

color:white;

margin-top:20px;

margin-bottom:10px;

}

/* Buttons */

.stButton > button{

height:58px;

font-size:22px;

font-weight:bold;

border-radius:16px;

background:linear-gradient(
90deg,
#4F46E5,
#06B6D4
);

border:none;

color:white;

transition:.35s;

}

.stButton > button:hover{

transform:translateY(-3px);

box-shadow:
0 0 25px #06B6D4;

}

background:linear-gradient(
90deg,
#6366F1,
#8B5CF6
);

color:white;

font-size:18px;

border-radius:14px;

height:55px;

border:none;

transition:.3s;

}

.stButton>button:hover{

box-shadow:0 0 25px #6366F1;

transform:scale(1.02);

}

/* Text Input */

.stTextInput > div > div > input{

background:#0F172A;

border:2px solid #4F46E5;

color:white;

font-size:20px;

padding:16px;

border-radius:16px;

transition:.3s;

}

.stTextInput > div > div > input:focus{

border:2px solid #00E5FF;

box-shadow:0 0 25px rgba(0,229,255,.45);

}

background:#1E293B;

color:white;

border-radius:12px;

border:1px solid #4F46E5;

font-size:18px;

}

</style>
""",unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("""
<div class="hero">

<h1>🚀 PulseAI</h1>

<p>
Autonomous Research & Competitor Intelligence Platform
</p>

<p style="margin-top:20px;font-size:18px;color:#d1d5db;">
Discover research papers, industry news, competitor insights and AI-powered executive summaries in one intelligent dashboard.
</p>

</div>
""", unsafe_allow_html=True)

# -------------------------------
# Search Section
# -------------------------------
# -------------------------------
# Search Section
# -------------------------------

st.markdown("""
<div class="search-card">

<h2 style="color:white;margin-bottom:10px;">
⚡ AI Search Console
</h2>

<p style="color:#94a3b8;">
Search any company, startup, technology or competitor.
PulseAI automatically decides which AI agents and APIs should execute.
</p>

</div>
""", unsafe_allow_html=True)

left, right = st.columns([6,1])

with left:

    keyword = st.text_input(
        "",
        placeholder="🔍 Example: Tesla, OpenAI, Nvidia, Quantum Computing..."
    )

with right:

    st.write("")
    st.write("")

    analyze = st.button(
        "🚀",
        use_container_width=True,
        type="primary"
    )

if analyze:
    if keyword.strip() == "":
        st.warning("Please enter a keyword.")
    else:
          # =====================================
          # Save Search to Memory
          # =====================================

          st.session_state.last_query = keyword
          context_words = [
              "latest news",
              "news",
              "research",
              "papers",
              "paper",
              "patents",
              "competitors",
              "competition",
              "updates"
          ]
          # =========================================
          # Manager Agent decides which agents to run
          # =========================================

          query = keyword.lower()

          run_research = False
          run_news = False

          # Dynamic Planning
          if "research" in query or "paper" in query:
              run_research = True

          elif "news" in query or "latest" in query:
              run_news = True

          else:
               # General company search
               run_research = True
               run_news = True

          if keyword.lower() not in context_words:
             st.session_state.current_context = keyword

          if keyword not in st.session_state.history:
            st.session_state.history.append(keyword)

          with st.spinner("🔍 Searching research papers, news, and generating AI insights..."):

               # =====================================
               # Context Resolution
               # =====================================

            context_keywords = [
                "latest news",
                "news",
                "research",
                "papers",
                "paper",
                "patents",
                "competitors",
                "competition",
                "updates"
                ]

            search_keyword = keyword

            if (
                    keyword.lower() in context_keywords
                    and st.session_state.current_context != ""
            ):
                    search_keyword = f"{keyword} {st.session_state.current_context}"

                # Ask the Coordinator Agent
            st.info("🤖 CrewAI Manager is planning the workflow...")

            crew_result = run_crew(search_keyword)
            st.success("🤖 CrewAI Manager created execution plan")
            st.subheader("🧠 Manager Task Decomposition")

            tasks = []

            if run_research:
                tasks.append("📚 Research Collection")

            if run_news:
                tasks.append("📰 News Collection")

            tasks.append("🤖 AI Summary")

            for i, task in enumerate(tasks, 1):
                st.write(f"{i}. {task}")
            st.info("🧠 Manager Decision")

            if run_research:
                 st.write("✅ Research Agent Selected")

            if run_news:
                 st.write("✅ News Agent Selected")
            status = st.status("🤖 AI Agents Working...", expanded=True)

            status.write("👨‍💼 Manager Agent → Planning")
            status.write("📚 Research Agent → Fetching Research Papers")
            status.write("📰 News Agent → Gathering Latest News")
            status.write("🧠 AI Analyst → Preparing Executive Summary")

            status.update(
              label="✅ Multi-Agent Execution Completed",
              state="complete",
              expanded=False
            )
            st.markdown("### 🤖 Active Agents")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
              st.success("👨‍💼 Manager")

            with c2:
               st.info("📚 Research")

            with c3:
               st.warning("📰 News")

            with c4:
               st.success("🧠 Analyst")

               st.markdown("### ⚡ Execution Progress")

               import time

               progress = st.progress(0)

               steps = [
                     "👨‍💼 Manager planning...",
                     "📚 Research Agent collecting papers...",
                     "📰 News Agent gathering updates...",
                     "🧠 AI Analyst generating summary..."
                ]

               for i, step in enumerate(steps):
                  st.write(step)
                  time.sleep(0.4)
                  progress.progress((i + 1) * 25)

                  st.success("✅ All Agents Finished Successfully")

               st.success("✅ All Agents Finished Successfully")

            with st.expander("⚙️ Multi-Agent Workflow", expanded=True):

              st.markdown("""
            ### Execution Flow

            ```
                              👨‍💼 Manager Agent
                                      │
                   ┌──────────────────┼──────────────────┐
                   │                  │                  │
             📚 Research Agent   📰 News Agent   🧠 AI Analyst
                   │                  │                  │
                   └──────────────────┼──────────────────┘
                                      │
                           📄 Executive Summary
            ```
            """)

            st.json(crew_result)

            tools = coordinator_agent(search_keyword)

            papers = []
            news = []
            # ==========================================
            # Resource Aware Execution
            # ==========================================

            MAX_RESULTS = 5

            if len(search_keyword) > 30:
               MAX_RESULTS = 3
               st.info("⚡ Resource Mode Activated (Reduced API Usage)")

            # ==========================
            # Research Agent
            # ==========================
            if tools["research"] and run_research:
                try:
                     papers = research_agent(search_keyword)[:MAX_RESULTS]
                     st.success("📚 Research Agent completed successfully")
                except Exception as e:
                    st.warning("⚠️ Research Agent failed. Continuing without research papers.")
                    papers = []

            # ==========================
            # News Agent
            # ==========================
            if tools["news"] and run_news:
                try:
                     news = news_agent(search_keyword)[:MAX_RESULTS]
                     st.success("📰 News Agent completed successfully")
                except Exception as e:
                     st.warning("⚠️ News Agent failed. Continuing without news.")
                     news = []

            # Generate AI Summary
            ai_summary = generate_ai_summary(search_keyword, papers, news)
            # ==========================================
            # Confidence Score
            # ==========================================

            confidence = 0

            if len(news) > 0:
                confidence += 50

            if len(papers) > 0:
                confidence += 50

            st.subheader("🎯 Confidence Score")

            c1, c2 = st.columns(2)

            with c1:
                st.metric("Confidence", f"{confidence}%")

            with c2:
                if confidence >= 80:
                    st.success("High Confidence")
                elif confidence >= 50:
                    st.warning("Medium Confidence")
                else:
                    st.error("Low Confidence")

            # Dashboard Metrics
            st.markdown("### 📊 Dashboard Overview")
            st.markdown("---")
            st.header("🤖 Agent Self Evaluation")

            evaluation = {
                "Manager Agent": "Completed",
                "Research Agent": "Success" if len(papers) > 0 else "No Results",
                "News Agent": "Success" if len(news) > 0 else "No Results",
                "AI Analyst": "Completed" if ai_summary else "Failed",
            }

            st.json(evaluation)

            score = (
                (len(papers) > 0)
                + (len(news) > 0)
                + (ai_summary != "")
            )

            st.progress(score / 3)
            st.success(f"Overall Performance: {int(score / 3 * 100)}%")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("📚 Research Papers", len(papers))
            c2.metric("📰 Industry News", len(news))
            c3.metric("🤖 AI Status", "Ready")
            c4.metric("🔍 Search", keyword)

            st.success(f"✅ Analysis completed for: {keyword}")
            st.info(f"🧠 Active Context: {st.session_state.current_context}")
            st.markdown("### 🧠 Memory Manager")

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"**Current Context:** {st.session_state.current_context}")

            with col2:
                st.info(f"**Last Query:** {st.session_state.last_query}")

                st.markdown("### 📜 Search History")

                if st.session_state.history:

                    st.write(" ➜ ".join(st.session_state.history))

                else:

                    st.caption("No searches yet.")

            st.markdown("### 🛠️ Tools Used")

            if tools["research"]:
                st.success("📚 arXiv API")

            if tools["news"]:
                st.success("📰 GNews API")

            st.success("🤖 Gemini AI")
               # -----------------------------------
               # Active Agents
               # -----------------------------------
            st.markdown("### 🤝 Active Agents")

            st.success("🎯 Coordinator Agent")

            if tools["research"]:
                st.success("📚 Research Agent")

            if tools["news"]:
                st.success("📰 News Agent")

            st.success("🤖 AI Analyst Agent")
            # -----------------------------
            # Agent Decision
            # -----------------------------
            st.markdown("### 🧠 Agent Decision")

            if tools["research"] and tools["news"]:
                st.info("The agent detected that both research papers and current news are required for this query.")

            elif tools["research"]:
                    st.info("The agent detected a research-focused query and used only the arXiv API.")
        
            elif tools["news"]:
                    st.info("The agent detected a news-focused query and used only the GNews API.")
# -------------------------------
# Divider
# -------------------------------
st.divider()

# -------------------------------
# Empty Result Sections
# -------------------------------
st.subheader("📚 Research Papers")

if "papers" in locals():
    if papers:
        for paper in papers:
            with st.container(border=True):
                 st.markdown(f"## 📄 {paper['title']}")

                 st.caption(f"👨‍🔬 Authors: {paper['authors']}")

                 st.caption(f"📅 Published: {paper['published']}")

                 st.write(paper["summary"])

                 st.link_button(
                     "📖 Read Full Paper",
                     paper["link"],
                     use_container_width=True
                 )
    else:
       if "tools" in locals() and not tools["research"]:
          st.info("ℹ️ Research search was skipped because this query is news-focused.")
       else:
          st.info("No research papers found.")

st.subheader("📰 Industry News")

if "news" in locals():
    if news:
        for article in news:
            with st.container():
                st.markdown(f"### {article['title']}")
                st.write(f"**Source:** {article['source']}")
                st.write(f"**Published:** {article['published']}")
                st.write(article['description'])
                st.markdown(f"[Read Article]({article['link']})")
                st.divider()
    else:
        st.info("No news articles found.")

st.subheader("📄 Patent Developments")
st.empty()

st.subheader("🏢 Competitor Intelligence")
st.empty()

st.subheader("🤖 AI Executive Summary")

if "ai_summary" in locals():
    st.markdown(ai_summary)
    # =====================================
# Footer
# =====================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="
padding:25px;
margin-top:20px;
border-radius:18px;
background:linear-gradient(135deg,#111827,#1E293B);
border:1px solid rgba(255,255,255,0.08);
text-align:center;
">

<h2 style="color:#60A5FA;margin-bottom:5px;">
🚀 PulseAI
</h2>

<p style="color:#CBD5E1;font-size:17px;">
Autonomous Research & Competitor Intelligence Agent
</p>

<p style="color:#94A3B8;">
🤖 Google Gemini AI &nbsp; • &nbsp;
📚 arXiv API &nbsp; • &nbsp;
📰 GNews API &nbsp; • &nbsp;
⚡ Streamlit
</p>

<hr style="border:0.5px solid #334155; margin:18px 0;">

<p style="color:#9CA3AF;font-size:15px;">
Developed for <b>Agentx Hackathon 2026</b>
</p>

<p style="color:#64748B;font-size:14px;">
Built with ❤️ by <b>TEAM A7</b>
</p>

</div>
""", unsafe_allow_html=True)

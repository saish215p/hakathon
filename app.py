import streamlit as st
from research import research_agent
from news import news_agent
from ai import generate_ai_summary
from tool_router import coordinator_agent

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
            tools = coordinator_agent(search_keyword)

            papers = []
            news = []

            # Call Research API only if needed
            if tools["research"]:
                papers = research_agent(search_keyword)

            # Call News API only if needed
            if tools["news"]:
                news = news_agent(search_keyword)

            # Generate AI Summary
            ai_summary = generate_ai_summary(search_keyword, papers, news)

            # Dashboard Metrics
            st.markdown("### 📊 Dashboard Overview")

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
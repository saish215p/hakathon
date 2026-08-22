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

# -------------------------------
# Header
# -------------------------------
st.title("🔍 PulseAI")

st.caption("Autonomous Research & Competitor Intelligence Dashboard")

st.markdown("""
### Stay ahead with AI-powered research and competitor intelligence.

Search any company, startup, or technology to instantly receive:

- 📚 Latest Research Papers
- 📰 Industry News
- 🤖 AI Executive Summary
- 📈 Research Trends
- 🏢 Competitor Insights
""")

st.divider()

# -------------------------------
# Search Section
# -------------------------------
with st.container(border=True):

     st.info("💡 Search any company, startup, competitor, or technology.")

keyword = st.text_input(
    "",
    placeholder="🔍 Search Tesla, OpenAI, Quantum Computing..."
)

analyze = st.button(
    "🚀 Analyze",
    type="primary",
    use_container_width=True
)

if analyze:
    if keyword.strip() == "":
        st.warning("Please enter a keyword.")
    else:

          with st.spinner("🔍 Searching research papers, news, and generating AI insights..."):

               # Ask the AI router which tools to use
               tools = coordinator_agent(keyword)

               papers = []
               news = []

               # Call Research API only if needed
               if tools["research"]:
                   papers = research_agent(keyword)

               # Call News API only if needed
               if tools["news"]:
                   news = news_agent(keyword)

               # Generate AI Summary
               ai_summary = generate_ai_summary(keyword, papers, news)

               # Dashboard Metrics
               st.markdown("### 📊 Dashboard Overview")

               c1, c2, c3, c4 = st.columns(4)

               c1.metric("📚 Research Papers", len(papers))
               c2.metric("📰 Industry News", len(news))
               c3.metric("🤖 AI Status", "Ready")
               c4.metric("🔍 Search", keyword)

               st.success(f"✅ Analysis completed for: {keyword}")

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
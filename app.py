import streamlit as st
from research import search_research
from news import search_news

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
st.subheader("Autonomous Research & Competitor Intelligence Agent")

st.write(
    "Track research papers, industry news, patent developments, "
    "and competitor insights using AI."
)

# -------------------------------
# Search Section
# -------------------------------
keyword = st.text_input(
    "Enter Company, Startup, or Technology",
    placeholder="Example: Tesla, OpenAI, Quantum Computing"
)

if st.button("Analyze", type="primary"):
    if keyword.strip() == "":
        st.warning("Please enter a keyword.")
    else:
        st.success(f"Searching for: {keyword}")

        papers = search_research(keyword)
        news = search_news(keyword)
# -------------------------------
# Divider
# -------------------------------
st.divider()

# -------------------------------
# Empty Result Sections
# -------------------------------
st.subheader("📚 Research Papers")
st.subheader("📚 Research Papers")

if "papers" in locals():
    if papers:
        for paper in papers:
            with st.container():
                st.markdown(f"### {paper['title']}")
                st.write(f"**Authors:** {paper['authors']}")
                st.write(f"**Published:** {paper['published']}")
                st.write(paper['summary'])
                st.markdown(f"[Read Paper]({paper['link']})")
                st.divider()
    else:
        st.info("No research papers found.")

st.subheader("📰 Industry News")
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
st.empty()
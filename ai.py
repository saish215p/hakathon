import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_summary(keyword, papers, news):
    """
    Generate an AI summary using Gemini.

    Args:
        keyword (str): Search keyword.
        papers (list): List of research papers.
        news (list): List of news articles.

    Returns:
        str: AI-generated summary.
    """

    if not GEMINI_API_KEY:
        return "❌ GEMINI_API_KEY not found in .env"

    # Format research papers
    paper_text = ""
    for i, paper in enumerate(papers, start=1):
        paper_text += f"""
Paper {i}
Title: {paper['title']}
Summary: {paper['summary']}
"""

    # Format news
    news_text = ""
    for i, article in enumerate(news, start=1):
        news_text += f"""
News {i}
Title: {article['title']}
Description: {article['description']}
"""

    prompt = f"""
You are an AI Research & Competitor Intelligence Agent.

Keyword:
{keyword}

Research Papers:
{paper_text}

Industry News:
{news_text}

Analyze all information and generate:

1. Executive Summary
2. Research Trends
3. Competitor Insights
4. Opportunities
5. Risks
6. Recommended Actions

Keep the report concise.
Use bullet points.
Maximum 300 words.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Gemini Error: {e}"
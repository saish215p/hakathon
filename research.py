"""
Research Agent

Responsibilities:
- Search research papers.
- Retrieve paper details from arXiv.
- Return structured research results.
"""
import requests
import feedparser
from urllib.parse import quote


ARXIV_API = "http://export.arxiv.org/api/query"


def research_agent(keyword):
    """
    Search arXiv for the latest 5 research papers.

    Returns:
        [
            {
                "title": "...",
                "authors": "...",
                "published": "...",
                "summary": "...",
                "link": "..."
            }
        ]
    """

    if not keyword.strip():
        return []

    try:
        url = (
            f"{ARXIV_API}"
            f"?search_query=all:{quote(keyword)}"
            f"&start=0"
            f"&max_results=5"
            f"&sortBy=submittedDate"
            f"&sortOrder=descending"
        )

        response = requests.get(url, timeout=15)
        response.raise_for_status()

        feed = feedparser.parse(response.text)

        papers = []

        for entry in feed.entries:
            papers.append({
                "title": entry.title,
                "authors": ", ".join(author.name for author in entry.authors),
                "published": entry.published,
                "summary": entry.summary.replace("\n", " "),
                "link": entry.link
            })

        return papers

    except Exception as e:
        print(f"arXiv Error: {e}")
        return []
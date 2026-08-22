"""
Coordinator Agent

Responsibilities:
- Analyze the user's query.
- Decide which specialized agents should run.
- Coordinate the workflow between agents.
"""

def coordinator_agent(query):
    """
    Decide which external tools should be used
    based on the user's query.
    """

    query = query.lower()

    use_research = False
    use_news = False

    research_keywords = [
        "research",
        "paper",
        "papers",
        "study",
        "journal",
        "arxiv"
    ]

    news_keywords = [
        "news",
        "latest",
        "today",
        "industry",
        "announcement",
        "launch"
    ]

    # Check for research-related keywords
    if any(word in query for word in research_keywords):
        use_research = True

    # Check for news-related keywords
    if any(word in query for word in news_keywords):
        use_news = True

    # If no specific intent is detected,
    # use both APIs (default behavior)
    if not use_research and not use_news:
        use_research = True
        use_news = True

    return {
        "research": use_research,
        "news": use_news
    }

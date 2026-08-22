from crewai import Agent

news_agent = Agent(
    role="News Analyst",
    goal="Collect the latest industry news.",
    backstory="Expert in monitoring technology news and market trends.",
    verbose=True,
    allow_delegation=False,
)
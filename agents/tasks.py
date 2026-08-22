from crewai import Task

from agents.manager import manager_agent
from agents.research_agent import research_agent
from agents.news_agent import news_agent
from agents.analyst_agent import analyst_agent


def create_tasks(query):

    research_task = Task(
        description=f"Find the latest research papers about {query}.",
        expected_output="List of relevant research papers.",
        agent=research_agent,
    )

    news_task = Task(
        description=f"Find the latest industry news about {query}.",
        expected_output="List of latest news articles.",
        agent=news_agent,
    )

    summary_task = Task(
        description=f"Generate an executive summary for {query} using research and news.",
        expected_output="Executive summary.",
        agent=analyst_agent,
    )

    return research_task, news_task, summary_task
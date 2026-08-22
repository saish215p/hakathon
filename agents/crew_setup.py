from crewai import Crew, Process

from agents.manager import manager_agent
from agents.research_agent import research_agent
from agents.news_agent import news_agent
from agents.analyst_agent import analyst_agent


def run_crew(query):

    execution_plan = {
        "manager": "Planning completed",
        "research": "Research Agent selected",
        "news": "News Agent selected",
        "analyst": "AI Analyst selected",
        "query": query
    }

    return execution_plan
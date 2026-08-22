from crewai import Agent

analyst_agent = Agent(
    role="AI Analyst",
    goal="Combine research and news into a concise executive summary.",
    backstory="Senior AI analyst capable of synthesizing multiple information sources.",
    verbose=True,
    allow_delegation=False,
)
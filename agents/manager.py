from crewai import Agent

manager_agent = Agent(
    role="Project Manager",
    goal="Plan which agents should work and coordinate their execution.",
    backstory="Experienced AI manager responsible for planning and task orchestration.",
    verbose=True,
    allow_delegation=True,
)
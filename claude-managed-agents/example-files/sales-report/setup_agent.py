import json
from anthropic import Anthropic

client = Anthropic()

# The agent: model, instructions and tools (created once)
agent = client.beta.agents.create(
    name="Sales Analyst",
    model="claude-sonnet-5-5",
    system=(
        "You are a data analyst for a small online shop. "
        "Analyze the data you get with Python, and save "
        "every output in /mnt/session/outputs/."
    ),
    tools=[{"type": "agent_toolset_20260401"}],
)

# The environment: where sessions run (a cloud sandbox)
environment = client.beta.environments.create(
    name="sales-report-env",
    config={
        "type": "cloud",
        "networking": {"type": "limited"},
    },
)

ids = {"agent": agent.id, "environment": environment.id}
with open("ids.json", "w") as f:
    json.dump(ids, f)
print("Agent:", agent.id)
print("Environment:", environment.id)

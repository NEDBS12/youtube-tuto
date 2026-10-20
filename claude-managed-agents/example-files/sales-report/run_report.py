import json
import time
from pathlib import Path
from anthropic import Anthropic

client = Anthropic()
ids = json.loads(Path("ids.json").read_text())

# 1. Upload the data, start a session with it mounted
data = client.files.upload(file=Path("orders.csv"))
session = client.beta.sessions.create(
    agent=ids["agent"],
    environment_id=ids["environment"],
    title="October sales report",
    resources=[{"type": "file", "file_id": data.id,
                "mount_path": "/orders.csv"}],
)

TASK = (
    "Analyze /mnt/session/uploads/orders.csv. Write "
    "report.md with the total revenue, revenue per week "
    "and the top 3 products, and save a chart of weekly "
    "revenue as weekly.png. Save both in "
    "/mnt/session/outputs/."
)

# 2. Send the task, then stream what the agent does
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(session.id, events=[
        {"type": "user.message",
         "content": [{"type": "text", "text": TASK}]},
    ])
    for event in stream:
        if event.type == "agent.tool_use":
            print(f"[tool] {event.name}")
        elif event.type == "agent.message":
            for block in event.content:
                if block.type == "text":
                    print(block.text)
        elif event.type == "session.status_idle":
            print("Idle:", event.stop_reason.type)
            break

# 3. Download what the agent saved in outputs/
time.sleep(5)  # outputs can appear a few seconds after idle
files = client.beta.files.list(
    scope_id=session.id,
    betas=["managed-agents-2026-04-01"],
)
for f in files:
    if f.id != data.id:
        client.files.download(f.id).write_to_file(f.filename)
        print("Downloaded", f.filename)

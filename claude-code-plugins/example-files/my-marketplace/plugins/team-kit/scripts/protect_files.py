import json, sys

# Files and folders Claude must never edit
PROTECTED = [".env", "secrets/"]

# Claude Code sends the tool call as JSON
data = json.load(sys.stdin)
path = data["tool_input"]["file_path"]
path = path.replace("\\", "/")

for pattern in PROTECTED:
    if pattern in path:
        print(f"Blocked: {path} is protected.", file=sys.stderr)
        sys.exit(2)

sys.exit(0)

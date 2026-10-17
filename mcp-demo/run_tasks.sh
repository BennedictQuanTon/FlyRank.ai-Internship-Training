#!/usr/bin/env bash
# Runs the three MCP evidence tasks with Claude Code as the MCP client.
# Built-in tools are disabled (--tools ""), so every file access must go through the filesystem MCP server.
set -u
cd "$(dirname "$0")/.."
FLAGS=(--mcp-config mcp-demo/mcp.json --strict-mcp-config --tools "" --allowedTools 'mcp__filesystem__*' --output-format stream-json --verbose)

claude -p "Read FL_04_WORKFLOW_PIPELINE.md in this repo and give me a markdown table of its 4 steps: step name, tool used, and the handoff contract it produces." \
  "${FLAGS[@]}" < /dev/null > mcp-demo/logs/task1_read_file.jsonl

claude -p "Find every Python file in this repo, then list all FastAPI endpoints (method + path) as a markdown table and mark which ones require auth via Depends(auth.get_current_user). End with one sentence on any security concern you notice." \
  "${FLAGS[@]}" < /dev/null > mcp-demo/logs/task2_endpoint_audit.jsonl

SID=$(grep -o '"session_id":"[^"]*"' mcp-demo/logs/task2_endpoint_audit.jsonl | head -1 | cut -d'"' -f4)
claude -p "Save the endpoint table and the security note from your previous answer as mcp-demo/endpoint_audit.md, then confirm with the file info." \
  --resume "$SID" "${FLAGS[@]}" < /dev/null > mcp-demo/logs/task3_write_file.jsonl

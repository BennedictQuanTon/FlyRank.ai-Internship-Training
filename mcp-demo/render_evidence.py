"""Render the stream-json MCP task logs into terminal-style HTML pages for screenshots.

Usage: python3 mcp-demo/render_evidence.py <out_dir>
Writes one HTML file per log plus a "connected" page built from the init event.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
REPO = str(ROOT.parent) + "/"

TASKS = {
    "task1_read_file": "Task 1 · Read a local file",
    "task2_endpoint_audit": "Task 2 · Search and audit local code",
    "task3_write_file": "Task 3 · Write a file to disk",
}
PROMPTS = {
    "task1_read_file": "Read FL_04_WORKFLOW_PIPELINE.md in this repo and give me a markdown table of its 4 steps: step name, tool used, and the handoff contract it produces.",
    "task2_endpoint_audit": "Find every Python file in this repo, then list all FastAPI endpoints (method + path) as a markdown table and mark which ones require auth via Depends(auth.get_current_user). End with one sentence on any security concern you notice.",
    "task3_write_file": "Save the endpoint table and the security note from your previous answer as mcp-demo/endpoint_audit.md, then confirm with the file info.",
}

CSS = """
body{margin:0;background:#0f172a;color:#e2e8f0;font:14px/1.5 'JetBrains Mono',Menlo,monospace}
.wrap{padding:24px 28px;max-width:1140px}
h1{font:600 18px/1.3 -apple-system,sans-serif;color:#f8fafc;margin:0 0 4px}
.meta{color:#94a3b8;margin-bottom:18px}
.badge{display:inline-block;background:#064e3b;color:#6ee7b7;border-radius:4px;padding:0 6px;margin-right:6px}
.block{border-left:3px solid #334155;padding:6px 12px;margin:10px 0;white-space:pre-wrap;word-break:break-word}
.user{border-color:#38bdf8}.user b{color:#38bdf8}
.tool{border-color:#059669;background:#052e2b}.tool b{color:#34d399}
.res{border-color:#475569;color:#cbd5e1;background:#111c33}
.text{border-color:#a78bfa}.text b{color:#c4b5fd}
.final{color:#94a3b8;margin-top:14px}
"""


def short(s, n):
    s = s.replace(REPO, "./")
    return s if len(s) <= n else s[:n] + f" … [+{len(s) - n} chars]"


def events(name):
    return [json.loads(l) for l in (LOGS / f"{name}.jsonl").read_text().splitlines() if l.strip()]


def page(title, body):
    return f"<!doctype html><meta charset=utf-8><title>{html.escape(title)}</title><style>{CSS}</style><div class=wrap>{body}</div>"


def header(init, title):
    servers = ", ".join(f"{s['name']} ({s['status']})" for s in init["mcp_servers"])
    builtin = [t for t in init["tools"] if not t.startswith("mcp__")]
    return (f"<h1>{html.escape(title)}</h1><div class=meta>"
            f"<span class=badge>MCP client: Claude Code {init['claude_code_version']}</span>"
            f"<span class=badge>server: {html.escape(servers)}</span>"
            f"<span class=badge>built-in tools: {len(builtin) or 'none'}</span>"
            f"model: {init['model']}</div>")


def render_task(name):
    evs = events(name)
    init = next(e for e in evs if e.get("subtype") == "init")
    out = [header(init, TASKS[name]),
           f"<div class='block user'><b>&gt; user</b>\n{html.escape(PROMPTS[name])}</div>"]
    for e in evs:
        if e["type"] == "assistant":
            for c in e["message"]["content"]:
                if c["type"] == "tool_use":
                    args = short(json.dumps(c["input"], ensure_ascii=False), 260)
                    out.append(f"<div class='block tool'><b>⚙ tool_use → {c['name']}</b>\n{html.escape(args)}</div>")
                elif c["type"] == "text":
                    out.append(f"<div class='block text'><b>◆ assistant</b>\n{html.escape(c['text'])}</div>")
        elif e["type"] == "user":
            for c in e["message"].get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    r = c["content"]
                    r = "".join(x.get("text", "") for x in r) if isinstance(r, list) else r
                    out.append(f"<div class='block res'>↳ result: {html.escape(short(r, 320))}</div>")
        elif e["type"] == "result":
            out.append(f"<div class=final>✔ {e['subtype']} · {e['num_turns']} turns · {e['duration_ms'] / 1000:.1f}s</div>")
    return page(TASKS[name], "".join(out))


def render_connected():
    init = next(e for e in events("task1_read_file") if e.get("subtype") == "init")
    tools = "\n".join(init["tools"])
    body = (header(init, "MCP server connected · filesystem")
            + f"<div class='block user'><b>mcp-demo/mcp.json</b>\n{html.escape((ROOT / 'mcp.json').read_text())}</div>"
            + f"<div class='block tool'><b>Tools exposed to the model (from the session init event)</b>\n{html.escape(tools)}</div>")
    return page("MCP connected", body)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "mcp_00_connected.html").write_text(render_connected())
    for i, name in enumerate(TASKS, 1):
        (out / f"mcp_0{i}_{name.split('_', 1)[1]}.html").write_text(render_task(name))

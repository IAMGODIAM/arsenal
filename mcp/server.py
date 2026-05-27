#!/usr/bin/env python3
"""
ARSENAL MCP Server — Sovereign OSINT Platform
Wraps all installed OSINT tools as MCP tools for Hermes Agent control.
Runs as stdio MCP server.
"""

import json
import subprocess
import sys
import os
import asyncio
from typing import Any

ARSENAL_HOME = "/home/user/arsenal"


def run_cmd(cmd: list[str], timeout: int = 120) -> dict:
    """Run a command and return structured output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=ARSENAL_HOME,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Command timed out after {timeout}s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════
# Tool definitions
# ═══════════════════════════════════════════

TOOLS = {
    "arsenal_username_sherlock": {
        "name": "arsenal_username_sherlock",
        "description": "Enumerate username across 400+ social networks using Sherlock. Returns found profile URLs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username to search"},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default 60)"},
            },
            "required": ["username"],
        },
        "handler": lambda args: run_cmd(
            ["sherlock", args["username"], "--timeout", str(args.get("timeout", 60)), "--print-found"],
            timeout=args.get("timeout", 60) + 10,
        ),
    },
    "arsenal_username_naminter": {
        "name": "arsenal_username_naminter",
        "description": "Async username enumeration across 600+ sites using WhatsMyName dataset (Naminter).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username to search"},
            },
            "required": ["username"],
        },
        "handler": lambda args: run_cmd(
            ["naminter", args["username"]],
            timeout=180,
        ),
    },
    "arsenal_email_holehe": {
        "name": "arsenal_email_holehe",
        "description": "Check email account existence across 100+ sites using Holehe.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Email address to check"},
            },
            "required": ["email"],
        },
        "handler": lambda args: run_cmd(
            ["holehe", "--email", args["email"]],
            timeout=180,
        ),
    },
    "arsenal_email_breach": {
        "name": "arsenal_email_breach",
        "description": "Check email against breach databases using h8mail.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Email address to check"},
            },
            "required": ["email"],
        },
        "handler": lambda args: run_cmd(
            ["h8mail", "-t", args["email"]],
            timeout=120,
        ),
    },
    "arsenal_phone_infoga": {
        "name": "arsenal_phone_infoga",
        "description": "Gather phone number information (carrier, location, type) using PhoneInfoga.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "Phone number in international format"},
            },
            "required": ["phone"],
        },
        "handler": lambda args: run_cmd(
            ["phoneinfoga", "scan", "-n", args["phone"]],
            timeout=60,
        ),
    },
    "arsenal_domain_dnstwist": {
        "name": "arsenal_domain_dnstwist",
        "description": "Detect typosquatted/squatted domains using DNSTwist.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain name to check"},
            },
            "required": ["domain"],
        },
        "handler": lambda args: run_cmd(
            ["dnstwist", "--registered", args["domain"]],
            timeout=120,
        ),
    },
    "arsenal_domain_opensquat": {
        "name": "arsenal_domain_opensquat",
        "description": "Detect domain look-alikes and impersonations using openSquat.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain name to check"},
            },
            "required": ["domain"],
        },
        "handler": lambda args: run_cmd(
            ["opensquat", "-k", args["domain"]],
            timeout=120,
        ),
    },
    "arsenal_domain_subfinder": {
        "name": "arsenal_domain_subfinder",
        "description": "Discover subdomains using Subfinder.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "silent": {"type": "boolean", "description": "Silent mode (default true)"},
            },
            "required": ["domain"],
        },
        "handler": lambda args: run_cmd(
            ["subfinder", "-d", args["domain"], "-silent" if args.get("silent", True) else ""],
            timeout=120,
        ),
    },
    "arsenal_domain_amass": {
        "name": "arsenal_domain_amass",
        "description": "Map attack surface and enumerate subdomains using Amass.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
            },
            "required": ["domain"],
        },
        "handler": lambda args: run_cmd(
            ["amass", "enum", "-d", args["domain"]],
            timeout=180,
        ),
    },
    "arsenal_harvest": {
        "name": "arsenal_harvest",
        "description": "Harvest emails, subdomains, and more from public sources using theHarvester.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Target domain"},
                "source": {"type": "string", "description": "Search source (default: all)", "default": "all"},
            },
            "required": ["domain"],
        },
        "handler": lambda args: run_cmd(
            ["theHarvester", "-d", args["domain"], "-b", args.get("source", "all")],
            timeout=120,
        ),
    },
    "arsenal_scan_nuclei": {
        "name": "arsenal_scan_nuclei",
        "description": "Scan target for vulnerabilities using Nuclei.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target URL or IP"},
                "severity": {"type": "string", "description": "Filter by severity (critical,high,medium,low,info)"},
            },
            "required": ["target"],
        },
        "handler": lambda args: run_cmd(
            ["nuclei", "-u", args["target"]]
            + (["-severity", args["severity"]] if args.get("severity") else []),
            timeout=300,
        ),
    },
    "arsenal_probe_httpx": {
        "name": "arsenal_probe_httpx",
        "description": "Probe HTTP services and gather info using HTTPX.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target URL, IP, or file of targets"},
                "list_mode": {"type": "boolean", "description": "Treat target as file of targets"},
            },
            "required": ["target"],
        },
        "handler": lambda args: run_cmd(
            ["httpx", "-u", args["target"], "-silent", "-title", "-status-code", "-tech-detect"]
            + (["-l"] if args.get("list_mode") else []),
            timeout=120,
        ),
    },
    "arsenal_archive_page": {
        "name": "arsenal_archive_page",
        "description": "Archive a web page using SingleFile.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to archive"},
                "output": {"type": "string", "description": "Output file path (default: auto)"},
            },
            "required": ["url"],
        },
        "handler": lambda args: run_cmd(
            ["single-file", args["url"], args.get("output", f"{ARSENAL_HOME}/archive/page.html")],
            timeout=60,
        ),
    },
    "arsenal_archivebox_add": {
        "name": "arsenal_archivebox_add",
        "description": "Add a URL to ArchiveBox for archiving.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to add to archive"},
            },
            "required": ["url"],
        },
        "handler": lambda args: run_cmd(
            ["docker", "exec", "arsenal-archivebox", "archivebox", "add", args["url"]],
            timeout=60,
        ),
    },
    "arsenal_social_analyzer": {
        "name": "arsenal_social_analyzer",
        "description": "Analyze username across social platforms using Social Analyzer.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Username to analyze"},
            },
            "required": ["username"],
        },
        "handler": lambda args: run_cmd(
            ["social-analyzer", "-u", args["username"]],
            timeout=180,
        ),
    },
    "arsenal_status": {
        "name": "arsenal_status",
        "description": "Check ARSENAL platform status — all tools and services.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": lambda args: {
            "success": True,
            "platform": "ARSENAL",
            "home": ARSENAL_HOME,
            "tools": {
                cmd: "installed" if subprocess.run(
                    ["which", cmd], capture_output=True
                ).returncode == 0 else "not found"
                for cmd in [
                    "sherlock", "naminter", "holehe", "phoneinfoga",
                    "dnstwist", "opensquat", "theHarvester", "h8mail",
                    "ghunt", "social-analyzer", "subfinder", "nuclei",
                    "httpx", "amass", "single-file",
                ]
            },
            "services": {
                docker: "running" if subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Running}}", docker],
                    capture_output=True, text=True
                ).stdout.strip() == "true" else "stopped/not found"
                for docker in ["arsenal-spiderfoot", "arsenal-archivebox"]
            },
        },
    },
}


# ═══════════════════════════════════════════
# MCP Protocol implementation
# ═══════════════════════════════════════════

async def handle_request(request: dict) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "arsenal-osint", "version": "1.0.0"},
            },
        }

    elif method == "tools/list":
        tools_list = []
        for tid, tdef in TOOLS.items():
            tools_list.append({
                "name": tdef["name"],
                "description": tdef["description"],
                "inputSchema": tdef["inputSchema"],
            })
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": tools_list},
        }

    elif method == "tools/call":
        tool_name = request.get("params", {}).get("name", "")
        arguments = request.get("params", {}).get("arguments", {})

        if tool_name not in TOOLS:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Unknown tool: {tool_name}"},
            }

        result = TOOLS[tool_name]["handler"](arguments)

        if isinstance(result, dict) and "error" in result and not result.get("success"):
            content = [{"type": "text", "text": json.dumps(result, indent=2)}]
        else:
            content = [{"type": "text", "text": json.dumps(result, indent=2)}]

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": content},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


async def main():
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            if not line:
                break

            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                continue

            response = await handle_request(request)
            print(json.dumps(response), flush=True)

        except EOFError:
            break
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "error": {"code": -32603, "message": str(e)},
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    asyncio.run(main())

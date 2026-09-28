import sys
import json
from client import BDIAgent

agent = BDIAgent()

def handle_rpc(line):
    global agent
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-bdi-belief-desire-intention-agent-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "perceive_and_deliberate",
                    "description": "Update agent beliefs with percepts and deliberate next committed intention",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "percepts": {"type": "object"}
                        },
                        "required": ["percepts"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "perceive_and_deliberate":
            agent.update_beliefs(args.get("percepts", {}))
            plan = agent.filter_intentions()
            act = agent.step()
            res = {"content": [{"type": "text", "text": json.dumps({"desires": agent.desires, "intentions": plan, "action": act})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()

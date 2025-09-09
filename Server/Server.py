from fastmcp import FastMCP
import K8s_Client as k8s

mcp = FastMCP("My MCP Server")

@mcp.tool
async def  listar_pods(namespace: str) -> str:
    return await k8s.listar_pods(namespace)

@mcp.tool
async def listar_deployments(namespace: str) -> str:
    return await k8s.get_deployments(namespace)


if __name__ == "__main__":
    mcp.run(transport="http", port=8000 )
# main.py
import os
import tools
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("host info mcp")
mcp.add_tool(tools.get_host_info)


def main():
    # 通过环境变量控制传输方式及网络参数，便于容器/云部署
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    host = os.getenv("MCP_HOST")
    port_str = os.getenv("MCP_PORT")
    path = os.getenv("MCP_PATH")
    log_level = os.getenv("MCP_LOG_LEVEL")

    # FastMCP (mcp SDK) 某些版本的 run 不接受 host/port/path 等关键字参数
    # 仅按传输类型启动，使用库自身默认配置
    if transport in ("http", "streamable-http"):
        # 兼容旧版 SDK：统一使用 "streamable-http"
        mcp.run("streamable-http")
    elif transport == "sse":
        mcp.run("sse")
    else:
        mcp.run("stdio")


if __name__ == '__main__':
    main()
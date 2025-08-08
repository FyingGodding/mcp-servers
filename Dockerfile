FROM python:3.11-slim
WORKDIR /app

# 仅复制依赖清单，充分利用 Docker 层缓存
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# 复制项目源码
COPY . /app

# 默认以 HTTP 方式运行，避免依赖 fastmcp CLI
ENV MCP_TRANSPORT=http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8080 \
    MCP_PATH=/mcp \
    MCP_LOG_LEVEL=info

EXPOSE 8000
CMD ["python", "main.py"]
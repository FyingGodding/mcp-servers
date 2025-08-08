# mcp-servers

用于部署并运行一个示例 MCP 服务器（主机信息查询）。已适配 Linux 本机与 Docker 环境。

## 运行环境
- Linux（x86_64/arm64 均可）
- Python >= 3.11（本地运行）
- 或 Docker / Docker Compose（容器化运行）

## 本地运行（Linux）
### 使用 uv（推荐）
1. 安装 uv（若未安装）：参考 `https://docs.astral.sh/uv/`。
2. 在项目根目录执行：
   ```bash
   uv run python main.py
   ```
   - 默认使用 `stdio` 传输，可在集成到支持 MCP 的客户端时直接使用。

### 使用 pip
1. 准备 Python 3.11+ 与 venv：
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install -r requirement.txt  # 或使用 pyproject: pip install .
   ```
2. 运行：
   ```bash
   python main.py
   ```

### 以 HTTP 暴露（可选）
设置环境变量切换到 HTTP 传输：
```bash
export MCP_TRANSPORT=http
export MCP_HOST=0.0.0.0
export MCP_PORT=8080
export MCP_PATH=/mcp
python main.py
```

## Docker 运行
### 直接使用 Docker
```bash
docker build -t mcp-host-info .
docker run --name mcp-host-info -p 8080:8080 --rm mcp-host-info
```

镜像默认以 HTTP 方式启动，监听 `0.0.0.0:8080`，路径 `/mcp`。

### 使用 Docker Compose
```bash
docker compose up -d
```

## 备注
- `tools.py` 中的 CPU 信息探测已做跨平台处理；Linux 下通过读取 `/proc/cpuinfo` 等实现。
- `requirement.txt` 移除了仅 Windows 平台可用的 `pywin32`，避免在 Linux 下安装失败。
- `Dockerfile` 未固定平台架构，适配多架构 Linux。

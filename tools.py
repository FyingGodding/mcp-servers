import platform
import psutil
import subprocess
import json
import sys
from typing import Any, Dict

def _detect_cpu_model() -> str:
    """Best-effort cross-platform CPU model detection.

    Returns a human-readable CPU model string, or "Unknown" if not available.
    """
    try:
        current_platform = sys.platform

        # Windows
        if current_platform == "win32":
            # Try PowerShell CIM first (more reliable on modern Windows)
            try:
                result = subprocess.check_output(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        "(Get-CimInstance Win32_Processor | Select-Object -First 1 -ExpandProperty Name)"
                    ],
                    stderr=subprocess.DEVNULL,
                ).decode(errors="ignore").strip()
                if result:
                    return result
            except Exception:
                pass

            # Fallback to WMIC (deprecated but often present)
            try:
                result = subprocess.check_output(
                    ["wmic", "cpu", "get", "Name"],
                    stderr=subprocess.DEVNULL,
                ).decode(errors="ignore").splitlines()
                values = [line.strip() for line in result if line.strip() and line.strip().lower() != "name"]
                if values:
                    return values[0]
            except Exception:
                pass

            # Last resort
            return platform.processor() or "Unknown"

        # macOS
        if current_platform == "darwin":
            try:
                return subprocess.check_output(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    stderr=subprocess.DEVNULL,
                ).decode(errors="ignore").strip()
            except Exception:
                return platform.processor() or "Unknown"

        # Linux
        if current_platform.startswith("linux"):
            try:
                with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if "model name" in line:
                            return line.split(":", 1)[1].strip()
            except Exception:
                pass
            return platform.processor() or "Unknown"

        # Other/unknown platforms
        return platform.processor() or "Unknown"
    except Exception:
        return "Unknown"


def get_host_info() -> Dict[str, Any]:
    """获取主机信息并以结构化对象返回，便于 MCP 直接序列化。

    返回:
        Dict[str, Any]: 包含系统、CPU、内存等信息的字典
    """
    info: Dict[str, Any] = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    }

    cpu_count = psutil.cpu_count(logical=True)
    info["cpu_count"] = int(cpu_count) if cpu_count is not None else 0
    info["cpu_model"] = _detect_cpu_model()

    return info

if __name__ == '__main__':
    # 手动运行时打印 JSON，方便调试
    print(json.dumps(get_host_info(), indent=4, ensure_ascii=False))
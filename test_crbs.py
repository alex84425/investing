# Direct REST API call to Cerebras (no pydantic dependency)
# Python 3.14 beta breaks pydantic, so we use raw requests

import os
import json
import urllib.request

API_KEY = os.environ.get("CEREBRAS_API_KEY", "")  # 從環境變數讀取，勿硬編金鑰

payload = json.dumps({
    "model": "zai-glm-4.7",
    "messages": [{"role": "user", "content": "分析 nv rubin and cerebras 再推論市場優劣"}],
    "max_completion_tokens": 4096,
    "temperature": 0.2,
    "top_p": 1,
    "stream": False,
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.cerebras.ai/v1/chat/completions",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "cerebras-test/1.0",
    },
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    print("Model:", data["model"])
    print("Content:", data["choices"][0]["message"]["content"][:500])
    print("\nUsage:", json.dumps(data.get("usage", {}), indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.reason}")
    print("Response:", e.read().decode())

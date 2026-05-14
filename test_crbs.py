# !pip install cerebras-cloud-sdk

import os

from cerebras.cloud.sdk import Cerebras

client = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY", "csk-vw9w2prk846tyc8ymrh2t3yjtdfwpf5w594854kwdd3w4k4x"))

completion = client.chat.completions.create(
    messages=[{"role": "user", "content": "Why is fast inference important?"}],
    model="zai-glm-4.7",
    max_completion_tokens=4096,
    temperature=0.2,
    top_p=1,
    stream=False,
)

print("Content:", completion.choices[0].message.content)
print("Reasoning:", completion.choices[0].message.reasoning)

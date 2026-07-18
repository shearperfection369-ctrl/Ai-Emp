import json
import os
import urllib.request

base = os.environ["INTEGRATION_PROXY_URL"]
job_id = "4263ebe4-18d0-4265-8057-e386523560ce"
key = "sk-emergent-61221C576D1548a22C"
req = urllib.request.Request(
    base + "/stripe/sandboxes",
    data=json.dumps({"job_id": job_id}).encode(),
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req) as r:
    sandbox = json.load(r)

print(json.dumps(sandbox, indent=2))

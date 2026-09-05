import json
from urllib.request import Request, urlopen


payload = {
    "text": "This product is excellent",
}

prediction_request = Request(
    url="http://127.0.0.1:8000/predict",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
    },
    method="POST",
)

with urlopen(prediction_request) as response:
    response_body = response.read().decode("utf-8")

print(json.dumps(json.loads(response_body), indent=2))

health_request = Request(
    url="http://127.0.0.1:8000/health",
    method="GET",
)

with urlopen(health_request) as response:
    response_body = response.read().decode("utf-8")

print(json.dumps(json.loads(response_body), indent=2))


# Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:8000/predict" -ContentType "application/json" -Body '{"text":"This product is excellent"}'
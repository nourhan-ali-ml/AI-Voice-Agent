import requests

file_path = r"D:\projects\simple-voice-agent\test.wav"
url = "http://localhost:8000/api/voice-call"

with open(file_path, "rb") as f:
    files = {"audio": f}
    response = requests.post(url, files=files)

print(response.json())

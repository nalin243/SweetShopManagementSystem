import subprocess
import time
import os
import signal
import pytest
import requests
from pymongo import MongoClient

UVICORN_CMD = [
    "uvicorn",
    "app.main:app",
    "--host", "127.0.0.1",
    "--port", "8001",
    "--log-level", "warning",
]

@pytest.fixture(scope="session", autouse=True)
def start_test_server():
    #start the fastapi app via uvicorn in a background process for tets and shut it down later
    env = os.environ.copy()
    #dedicated test database to isolate the test data
    env["MONGO_DB"] = "test_auth"
    env["MONGO_URI"] = "mongodb://localhost:27017"

    proc = subprocess.Popen(UVICORN_CMD, env=env)

    #wait until server is responsive
    base_url = "http://127.0.0.1:8001/health"
    for _ in range(50):
        try:
            r = requests.get(base_url, timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.2)
    else:
        proc.terminate()
        raise RuntimeError("Server did not start in time")

    yield

    #emptying the test collection so as not cause conflicts in future tests
    client = MongoClient(env["MONGO_URI"])
    db = client["test_auth"]
    db["users"].delete_many({})
    client.close()

    #stop server
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

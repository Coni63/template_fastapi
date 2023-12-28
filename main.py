import uvicorn

from api.server import app


if __name__ == "__main__":
    # poetry run uvicorn main:app --reload --port 8000 --host 0.0.0.0
    uvicorn.run(app, host="0.0.0.0", port=8000)

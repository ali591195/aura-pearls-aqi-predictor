import os

from dotenv import load_dotenv
import uvicorn

load_dotenv()


if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=os.getenv("VITE_BACKEND_HOST", "127.0.0.1"),
        port=int(os.getenv("VITE_BACKEND_PORT", "8000")),
        reload=True,
    )
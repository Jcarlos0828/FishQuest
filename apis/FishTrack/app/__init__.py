from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="FishTrack API",
        description="Species checklist by aquarium.",
        version="0.1.0",
    )
    return app

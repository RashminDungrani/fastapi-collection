import uvicorn


def main() -> None:
    """Entrypoint of the application."""

    uvicorn.run(
        "app.routes.application:get_app",
        workers=1,
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True,
    )


if __name__ == "__main__":
    main()

import uvicorn

if __name__ == "__main__":
    print("Running in dev")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True, env_file=".env.dev")
    print("Running out")

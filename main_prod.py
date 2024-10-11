import uvicorn

if __name__ == "__main__":
    print("Running in prod")
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True, env_file=".env.prod")
    print("Running out")

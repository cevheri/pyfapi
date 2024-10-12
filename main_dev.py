import uvicorn
from app.config.app_settings import server_settings

if __name__ == "__main__":
    print("Running in dev")
    host = server_settings.HOST
    port = server_settings.PORT
    reload = server_settings.RELOAD
    env_file = ".env.dev"

    uvicorn.run("app.main:app", host=host, port=port, reload=reload, env_file=env_file)
    print("Running out")

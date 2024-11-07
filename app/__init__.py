from app.middleware import log_handler

print("app.__init__.py is running")

print("logger configuration")
log = log_handler.init_log()
print("logger configured")


from fastapi import FastAPI
from routes import items, clock_in

app = FastAPI()

# Register routes
app.include_router(items.router)
app.include_router(clock_in.router)

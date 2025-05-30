from fastapi import FastAPI
from contextlib import asynccontextmanager

from middleware import add_request_logging
from core.routers import registered_routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup

    yield 

    # on_shutdown
    print("Shutting down")

app = FastAPI(docs_url="/", lifespan=lifespan)
add_request_logging(app)

for route in registered_routers:
    app.include_router(route.router, tags=[route.tag])


# origins = [
#     "http://localhost:3000",
#     "http://localhost:8000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

import time

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .image.set_image import set_image_router
from .image.gnerate_image import generate_image_router


app = FastAPI()
app.add_middleware(CORSMiddleware)
app.get("/", include_in_schema=False)(lambda: RedirectResponse(url="/docs/"))


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)

    process_time = int((time.time() - start_time) * 1000)
    response.headers["X-Process-Time"] = f"{process_time}ms"

    return response


app.include_router(set_image_router)
app.include_router(generate_image_router)

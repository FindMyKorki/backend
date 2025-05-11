# middleware.py
from fastapi import Request, UploadFile
from starlette.datastructures import UploadFile, FormData
import json

async def receive_with_body(body: bytes):
    """Returns a receive function that feeds a fixed body"""
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}
    return receive

def add_request_logging(app):
    @app.middleware("http")
    async def log_request_body(request: Request, call_next):
        body = await request.body()
        content_type = request.headers.get("content-type", "")

        print("#######################################################")
        if "multipart/form-data" in content_type:
            request = Request(request.scope, receive=await receive_with_body(body))
            form: FormData = await request.form()
            log_data = {}
            for key in form:
                value = form.getlist(key)
                log_data[key] = []
                for item in value:
                    if isinstance(item, UploadFile):
                        log_data[key].append({
                            "filename": item.filename,
                            "content_type": item.content_type,
                        })
                    else:
                        log_data[key].append(item)
                if len(log_data[key]) == 1:
                    log_data[key] = log_data[key][0]  # simplify single-item lists
            print("Multipart Form Data:\n", json.dumps(log_data, indent=2))
        else:
            try:
                print("Request Body:\n", json.dumps(json.loads(body), indent=2))
            except Exception:
                print("Request Body (raw):\n", body.decode("utf-8", errors="ignore"))
        print("#######################################################")
        return await call_next(request)

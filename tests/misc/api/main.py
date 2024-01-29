# -*- coding: utf-8 -*-
from os import getenv
from uuid import uuid4
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse


app = FastAPI()
instance_id = None
report_num = 0

list_router = APIRouter(prefix="/list")
bunkernet_router = APIRouter(prefix="/bunkernet")


@list_router.get("/ip")
async def ip(_: Request):
    return PlainTextResponse("192.168.0.254\n10.0.0.0/8\n127.0.0.0/24")


@list_router.get("/rdns")
async def rdns(_: Request):
    return PlainTextResponse(".example.com\n.example.org\n.bw-services")


@list_router.get("/asn")
async def asn(_: Request):
    return PlainTextResponse(f"1234\n{getenv('AS_NUMBER', '3356')}\n5678")


@list_router.get("/user_agent")
async def user_agent(_: Request):
    return PlainTextResponse("BunkerBot\nCensysInspect\nShodanInspect\nZmEu\nmasscan")


@list_router.get("/uri")
async def uri(_: Request):
    return PlainTextResponse("/admin\n/login")


@bunkernet_router.get("/ping")
async def ping(_: Request):
    return JSONResponse(status_code=200, content={"result": "ok", "data": "pong"})


@bunkernet_router.post("/register")
async def register(_: Request):
    global instance_id
    if not instance_id:
        instance_id = str(uuid4())
    return JSONResponse(status_code=200, content={"result": "ok", "data": instance_id})


@bunkernet_router.post("/report")
async def report(_: Request):
    global report_num
    report_num += 1
    return JSONResponse(status_code=200, content={"result": "ok", "data": "Report acknowledged."})


@bunkernet_router.get("/db")
async def db(_: Request):
    return JSONResponse(status_code=200, content={"result": "ok", "data": []})


@bunkernet_router.get("/instance_id")
async def get_instance_id(_: Request):
    global instance_id
    if not instance_id:
        return JSONResponse(status_code=404, content={"result": "error", "data": "Instance ID not found."})
    return JSONResponse(status_code=200, content={"result": "ok", "data": instance_id})


@bunkernet_router.get("/report_num")
async def get_report_num(_: Request):
    global report_num
    return JSONResponse(status_code=200, content={"result": "ok", "data": report_num})


@bunkernet_router.post("/reset")
async def reset(_: Request):
    global instance_id, report_num
    instance_id = None
    report_num = 0
    return JSONResponse(status_code=200, content={"result": "ok", "data": "Reset done."})


app.include_router(list_router)
app.include_router(bunkernet_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import APIRouter, Request

ip_router = APIRouter()

@ip_router.get('/get-ip')
async def get_ip(request: Request):
    if request.headers.get("X-Forwarded-For"):
        ip = request.headers.get("X-Forwarded-For").split(',')[0].strip()
    else:
        ip = request.client.host
    return {'client_ip': ip}

@ip_router.get('/ip_addr')
async def ip_addr(request: Request):
    return request.client.host

from app import app
from asgiref.wsgi import WsgiToAsgi

asgi_app = WsgiToAsgi(app)

async def handler(scope, receive, send):
    await asgi_app(scope, receive, send)

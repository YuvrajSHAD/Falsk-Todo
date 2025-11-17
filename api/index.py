from app import app

async def handler(request, response):
    # Vercel serverless Python expects an async handler
    # Adapt Flask WSGI to ASGI using `asgiref`
    from asgiref.wsgi import WsgiToAsgi
    asgi_app = WsgiToAsgi(app)
    return await asgi_app(request.scope, request.receive, response.send)

import fastapi
import ssl
from tg_bot import startup_down
from app_routing import route
from tg_bot import WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV, DOMAIN, EXTERNAL_PORT
import uvicorn

app = fastapi.FastAPI(lifespan=startup_down)
app.include_router(route)

# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(certfile=WEBHOOK_SSL_CERT, keyfile=WEBHOOK_SSL_PRIV)

if __name__ == '__main__':
    uvicorn.run(app=app, host=DOMAIN, port=int(EXTERNAL_PORT), ssl_certfile=WEBHOOK_SSL_CERT, ssl_keyfile=WEBHOOK_SSL_PRIV)
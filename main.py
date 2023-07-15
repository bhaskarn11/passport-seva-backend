from fastapi import FastAPI, Request, Security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from settings import get_settings
from services import application_service, user_service, appointment_service, admin_service, payment_service
from schemas import CustomHTTPException
from datetime import datetime
from utils.auth_utils import read_current_user

config = get_settings()

app = FastAPI(version=config.version, title=config.app_name, description=config.app_description, docs_url="/")


origins = [
    'http://localhost:3000',
    'https://passportseva-demo.vercel.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(
    user_service.router,
    prefix="/users",
    tags=['User Service']
)

app.include_router(
    application_service.router,
    prefix="/applications",
    tags=['Applications Service'],
    dependencies=[Security(read_current_user, scopes=['application:read', 'application:write'])]

)

app.include_router(
    appointment_service.router,
    prefix="/appointments",
    tags=['Public Service'],
)

app.include_router(
    admin_service.router,
    prefix="/admin",
    tags=['Admin Service'],
    # dependencies=[Security(read_current_user, scopes=['user:admin'])]
)


app.include_router(
    payment_service.router,
    prefix="/payment",
    tags=['Payment Service']
)


# Custom Exception Handler

@app.exception_handler(CustomHTTPException)
def custom_error_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S %z")
        }
    )

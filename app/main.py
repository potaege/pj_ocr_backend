from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse
import traceback

from app.entities.users import User
from app.entities.thai_id import ThaiID
from app.entities.driving_licence import DrivingLicence
from app.entities.passport import Passport
from app.entities.house_registration import HouseRegistration
## api router
from app.api.test import router as router_test
from app.api.documents import router as router_documents
from app.api.ocr import router as router_ocr
from app.api.users import router as router_users
from app.api.login import router as router_login



app = FastAPI()

app.include_router(router_test)
app.include_router(router_documents)
app.include_router(router_ocr)
app.include_router(router_users)
app.include_router(router_login)



@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "traceback": traceback.format_exc(),
        },
    )

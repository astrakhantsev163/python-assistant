from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from db.cruds import crud_doctors
from db.models import models_doctors
from db.postgres import engine, get_postgres
from db.schemas import schema_doctors
from utils.decorators import render_doctors

templates_path = Path(__file__).parent / "../templates"
templates = Jinja2Templates(directory=templates_path.resolve())
router = APIRouter(prefix="/doctors", tags=["doctors"])
models_doctors.Base.metadata.create_all(bind=engine)


@router.get("/")
@render_doctors("doctors.html")
async def get_doctors(request: Request):
    return {"request": request}


@router.post("/add-doctor")
@render_doctors("doctors.html")
async def add_doctor(
    request: Request,
    full_name: str = Form(...),
    specialization: str = Form(...),
    price: str = Form(...),
    address: str = Form(...),
    db: Session = Depends(get_postgres),
):
    doctor = schema_doctors.DoctorCreate(
        full_name=full_name, specialization=specialization, price=price, address=address
    )
    crud_doctors.create_doctor(db=db, doctor=doctor)
    doctors_data = {"doctors_data": crud_doctors.get_doctors(db)}
    return doctors_data

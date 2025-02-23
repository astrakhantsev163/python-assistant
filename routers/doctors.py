from pathlib import Path

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from db.cruds import crud_doctors
from db.models import models_doctors
from db.postgres import engine, get_postgres
from db.schemas import schema_doctors

templates_path = Path(__file__).parent / "../templates"
templates = Jinja2Templates(directory=templates_path.resolve())
router = APIRouter(prefix="/doctors", tags=["doctors"])
models_doctors.Base.metadata.create_all(bind=engine)


@router.get("/", response_model=list[schema_doctors.Doctor])
def get_doctors(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_postgres),
):
    full_name, specialization, price, address = crud_doctors.get_doctors(
        db, skip=skip, limit=limit
    )
    doctors_data = list(zip(full_name, specialization, price, address))
    return templates.TemplateResponse(
        "doctors.html",
        context={
            "request": request,
            "doctors": doctors_data,
        },
    )


@router.post("/", response_model=schema_doctors.Doctor)
def create_doctor(
    doctor: schema_doctors.DoctorCreate, db: Session = Depends(get_postgres)
):
    return crud_doctors.create_doctor(db=db, doctor=doctor)

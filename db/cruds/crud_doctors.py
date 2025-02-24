from sqlalchemy.orm import Session

from db.models import models_doctors
from db.schemas import schema_doctors


def create_doctor(db: Session, doctor: schema_doctors.DoctorCreate):
    db_doctor = models_doctors.Doctor(
        full_name=doctor.full_name,
        specialization=doctor.specialization,
        price=doctor.price,
        address=doctor.address,
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    doctors = db.query(models_doctors.Doctor).offset(skip).limit(limit).all()
    doctors_list = []
    for doctor in doctors:
        doctors_dict = {key: value for key, value in doctor.__dict__.items()}
        doctors_list.append(doctors_dict)
    full_name = []
    specialization = []
    price = []
    address = []
    for doctor_data in doctors_list:
        full_name.append(doctor_data.get("full_name") or "Не заполнено")
        specialization.append(doctor_data.get("specialization") or "Не заполнено")
        price.append(doctor_data.get("price") or "Не заполнено")
        address.append(doctor_data.get("address") or "Не заполнено")
    return full_name, specialization, price, address


def get_doctor_by_id(db: Session, doctor_id: str):
    return (
        db.query(models_doctors.Doctor)
        .filter(models_doctors.Doctor.id == doctor_id)
        .first()
    )


def update_doctor(db: Session, doctor_id: str, doctor: schema_doctors.DoctorCreate):
    db_doctor = (
        db.query(models_doctors.Doctor)
        .filter(models_doctors.Doctor.id == doctor_id)
        .first()
    )
    if db_doctor:
        db_doctor.full_name = doctor.full_name
        db_doctor.specialization = doctor.specialization
        db_doctor.address = doctor.address
        db_doctor.price = doctor.price
        db.commit()
        db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: str):
    db_doctor = (
        db.query(models_doctors.Doctor)
        .filter(models_doctors.Doctor.id == doctor_id)
        .first()
    )
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
    return db_doctor

from pydantic import BaseModel


class DoctorBase(BaseModel):
    full_name: str
    specialization: str
    price: str
    address: str


class DoctorCreate(DoctorBase):
    full_name: str
    specialization: str
    price: str
    address: str


class Doctor(DoctorBase):
    id: str

    class Config:
        from_attributes = True

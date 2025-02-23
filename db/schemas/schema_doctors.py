from pydantic import BaseModel


class DoctorBase(BaseModel):
    full_name: str
    specialization: str
    address: str


class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase):
    id: str

    class Config:
        from_attributes = True

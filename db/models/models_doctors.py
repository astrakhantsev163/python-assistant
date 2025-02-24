from sqlalchemy import Column, Integer, String

from db.postgres import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    price = Column(String, nullable=False)
    address = Column(String, nullable=False)

    def to_dict(self):
        return {
            column.full_name: getattr(self, column.full_name)
            for column in self.__table__.columns
        }

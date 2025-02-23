from sqlalchemy import Column, String

from db.postgres import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(
        String, primary_key=True, index=True
    )  # Можно использовать UUID или автоинкремент
    full_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    price = Column(String, nullable=False)
    address = Column(String, nullable=False)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

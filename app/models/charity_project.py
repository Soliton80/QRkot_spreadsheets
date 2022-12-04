from sqlalchemy import Column, String, Text

from .common_model import CommonModel


class CharityProject(CommonModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return self.name

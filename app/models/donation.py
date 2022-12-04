from sqlalchemy import Column, ForeignKey, Integer, Text

from .common_model import CommonModel


class Donation(CommonModel):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

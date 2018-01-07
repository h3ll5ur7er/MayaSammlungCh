
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship, deferred
from sqlalchemy import Column, ForeignKey, Integer, String, Binary

Model = declarative_base()


class User(Model):
    """ Department data object """
    __tablename__ = 'ms_users'

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return "{}".format(self.name)

    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False)
    pw_hash = Column(String(50), nullable=False)

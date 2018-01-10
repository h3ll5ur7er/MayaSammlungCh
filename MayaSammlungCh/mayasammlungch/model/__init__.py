# -*- coding: utf-8 -*-
"""The application's model objects"""

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, create_session
from sqlalchemy.ext.declarative import declarative_base

maker = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

SQLITE_DATA_TARGET = "sqlite:///db__data_target.db"
DataDbEngine = create_engine(SQLITE_DATA_TARGET)
DataDbSession = create_session(DataDbEngine)
DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)

    return DBSession

from mayasammlungch.model.auth import User, Group, Permission
from mayasammlungch.model.data_model_lite import *
__all__ = ('User', 'Group', 'Permission')

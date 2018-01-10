# -*- coding: utf-8 -*-

""" Api controller for the katalog_py webservice """

from mayasammlungch.lib.base import BaseController
from tg import expose, response
from sqlalchemy.orm import Session, Load, joinedload_all
from mayasammlungch.model.data_model_lite import Department, LangGroup, Village, Category, Object,Picture
import logging

class ApiController(BaseController):

    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def _before(self):
        response.headers.update({'Access-Control-Allow-Origin': '*'})

    @expose('json')
    def home(self):
        """ /home """

        response_data = {
            'heading': "Willkommen",
            'content': "Lorem Ipsum"
        }

        return response_data

    @expose('json')
    def catalog(self, offset=0, limit=32, **kwargs):
        session = self.db
        obj_query = session.query(Object).options(joinedload_all("*"))

        slice_from = int(offset)
        slice_to = int(offset) + int(limit)

        objects = obj_query.order_by(Object.object_number)[slice_from:slice_to]

        response_data = {
            'items': objects,
            'title': "Katalog"
        }

        return response_data
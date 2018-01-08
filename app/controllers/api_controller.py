# -*- coding: utf-8 -*-

""" Api controller for the katalog_py webservice """

from tg import expose, TGController, response
from sqlalchemy.orm import Session
from model.data_model_lite import Department, LangGroup, Village, Category, Object


class ApiController(TGController):

    def __init__(self, engine):
        self.engine = engine

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
        session = Session(self.engine)
        query = session.query(Object)

        slice_from = int(offset)
        slice_to = int(offset) + int(limit)

        objects = [obj for obj in query.order_by(Object.object_number)][slice_from:slice_to]

        response_data = {
            'items': objects,
            'title': "Katalog"
        }

        return response_data
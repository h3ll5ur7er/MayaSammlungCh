# -*- coding: utf-8 -*-

""" Main controller for the katalog_py webservice """

from tg import expose, TGController
from sqlalchemy.orm import Session
from model.data_model_lite import Department, LangGroup, Village, Category, Object
from controllers.login_controller import LoginController

class RootController(TGController):
    """ Main controller for the katalog_py webservice """

    login = None

    def __init__(self, engine, login_engine):
        self.engine = engine
        self.login = LoginController(login_engine)

    @expose("templates/default.xhtml")
    def index(self):
        """ home page """
        content = {
            'active_nav_index':1,
            'body_header':"Willkommen",
            'body_content': self._lorem_ipsum()
        }
        return content


    @expose("templates/catalog.xhtml")
    def catalog(self, page=0, page_size=32, **kwargs):
        """ catalog page """

        session = Session(self.engine)
        query = session.query(Object)

        if 'category' in kwargs:
            query = query.join(Object.category)\
                         .filter(Category.name.like("%{}%".format(kwargs['category'])))

        if 'lang_group' in kwargs:
            query = query.join(Object.village)\
                         .join(Village.lang_group)\
                         .filter(LangGroup.name.like("%{}%".format(kwargs['lang_group'])))

        if 'department' in kwargs:
            query = query.join(Object.village)\
                         .join(Village.department)\
                         .filter(Department.name.like("%{}%".format(kwargs['department'])))

        if 'village' in kwargs:
            query = query.join(Object.village)\
                         .filter(Village.name.like("%{}%".format(kwargs['village'])))

        if 'object_number' in kwargs:
            query = query.filter(Object.object_number.like("%{}%".format(kwargs['object_number'])))

        print "{}:{}".format(page, page_size)
        slice_from = int(page)*int(page_size)
        slice_to = slice_from + page_size
        print "{}:{}".format(slice_from, slice_to)
        objects = [obj for obj in query.order_by(Object.object_number)][slice_from:slice_to]
        
        content={
            'active_nav_index':2,
            'objects': objects
        }
        return content


    @expose("templates/detail.xhtml")
    def detail(self, obj_id=-1):
        """ detail page """
        if obj_id == -1:
            return
        session = Session(self.engine)
        query = session.query(Object) \
                       .filter(Object.id == obj_id) \
                       .first()

        content={
            'active_nav_index':2,
            'obj': query
        }
        return content


    @expose("templates/nav_tree.xhtml")
    def about(self):
        """ about us page """

        
        session = Session(self.engine)

        categories = [category for category in session.query(Category).order_by(Category.name)]
        departments = [department for department in session.query(Department).order_by(Department.name)]
        langgroups = [langgroup for langgroup in session.query(LangGroup).order_by(LangGroup.name)]
        villages = [village for village in session.query(Village).order_by(Village.name)]


        content = {
            'active_nav_index':3,
            'body_header':"Über uns",
            'categories':categories,
            'departments': departments,
            'langgroups':langgroups,
            'villages':villages,
            'body_content': self._lorem_ipsum()
        }
        return content


    @expose("templates/default.xhtml")
    def contact(self):
        """ contacts page """
        content = {
            'active_nav_index':4,
            'body_header':"Kontakt",
            'body_content': self._lorem_ipsum()
        }
        return content


    def _lorem_ipsum(self):
        return "Lorem ipsum dolor sit amet, consetetur sadipscing elitr,\
        sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,\
        sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.\
        Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.\
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr,\
        sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,\
        sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.\
        Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."

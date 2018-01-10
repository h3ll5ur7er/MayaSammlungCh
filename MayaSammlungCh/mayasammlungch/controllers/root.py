# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from mayasammlungch import model
from mayasammlungch.controllers.secure import SecureController
from mayasammlungch.controllers.api_controller import ApiController
from mayasammlungch.model import DBSession, DataDbSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from mayasammlungch.lib.base import BaseController
from mayasammlungch.controllers.error import ErrorController

__all__ = ['RootController']

class RootController(BaseController):
    """
    The root controller for the MayaSammlungCh application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    api = ApiController(DataDbSession)
    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "Maya-Sammlung.ch"

    @expose('mayasammlungch.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')


    @expose("templates/nav_tree.xhtml")
    def about(self):
        """ about us page """

        
        session = DataDbSession

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

    @expose('mayasammlungch.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('mayasammlungch.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('mayasammlungch.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    # @expose('mayasammlungch.templates.register')
    # def register(self, came_from=lurl('/'), failure=None, login=''):
    #     """Start the user login."""
    #     print login
    #     print request
    #     if failure is not None:
    #         if failure == 'user-not-found':
    #             flash(_('User not found'), 'error')
    #         elif failure == 'invalid-password':
    #             flash(_('Invalid Password'), 'error')

    #     login_counter = request.environ.get('repoze.who.logins', 0)
    #     if failure is None and login_counter > 0:
    #         flash(_('Wrong credentials'), 'warning')

    #     return dict(page='login', login_counter=str(login_counter),
    #                 came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        print request
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    # @expose()
    # def post_register(self, came_from=lurl('/')):
    #     """
    #     Redirect the user to the initially requested page on successful
    #     authentication or redirect her back to the login page if login failed.

    #     """
    #     if not request.identity:
    #         login_counter = request.environ.get('repoze.who.logins', 0) + 1
    #         redirect('/login',
    #                  params=dict(came_from=came_from, __logins=login_counter))
    #     userid = request.identity['repoze.who.userid']
    #     flash(_('Welcome back, %s!') % userid)

    #     # Do not use tg.redirect with tg.url as it will add the mountpoint
    #     # of the application twice.
    #     return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)


    @expose("mayasammlungch.templates.catalog")
    @expose("json")
    @require(predicates.not_anonymous("You have to be logged in to search the catalog."))
    def catalog(self, page=0, page_size=32, **kwargs):
        """ catalog page """
        from mayasammlungch.model.data_model_lite import Object, Department, LangGroup, Village, Category, Picture

        session = DataDbSession
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


    @expose("mayasammlungch.templates.detail")
    def detail(self, obj_id=-1):
        """ detail page """
        if obj_id == -1:
            return

        from mayasammlungch.model.data_model_lite import Object, Department, LangGroup, Village, Category, Picture

        session = DataDbSession
        query = session.query(Object) \
                       .filter(Object.id == obj_id) \
                       .first()

        content={
            'active_nav_index':2,
            'obj': query
        }
        return content

    @expose("mayasammlungch.templates.default")
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

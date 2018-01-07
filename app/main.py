# -*- coding: utf-8 -*-

""" main entry for katalog_py """

from wsgiref.simple_server import make_server
from tg import AppConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from root_controller import RootController

DEFAULT_ACTION = 'run'
SQLITE_DATA_TARGET = "sqlite:///db__data_target.db"

def start_server():

    """ start webserver """

    engine = create_engine(SQLITE_DATA_TARGET)
    config = AppConfig(minimal=True, root_controller=RootController(engine))
    config.sa_auth.charset = 'utf-8'
    config.renderers = ['kajiki']
    config.default_renderer = 'kajiki'
    config.serve_static = True
    config.paths['static_files'] = 'public'

    application = config.make_wsgi_app()
    print "Serving on port 8080..."
    httpd = make_server('', 8080, application)
    httpd.serve_forever()


def test():

    """ debug testing function """

    from data_model_lite import Model, Department, LangGroup, Village, Category, Object, Picture
    engine = create_engine(SQLITE_DATA_TARGET)
    session = Session(engine)
    query = session.query(Object)

    obj_nr_l = []

    for obj in query:
        obj_nr_l.append(len(obj.object_number))

    print("min number length: {}".format(min(obj_nr_l)))
    print("max number length: {}".format(max(obj_nr_l)))


if __name__ == "__main__":
    import os
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    if 'test' in sys.argv[1:] \
        or os.getenv("PARAM") == "test" \
        or (os.getenv("PARAM") is None and len(sys.argv[1:]) == 0 and DEFAULT_ACTION == 'test'):
        print '>>>___test___<<<'
        test()
        print '<<<___test___>>>'

    if 'start' in sys.argv[1:] \
        or os.getenv("PARAM") == "run" \
        or (os.getenv("PARAM") is None and len(sys.argv[1:]) == 0 and DEFAULT_ACTION == 'run'):
        print '>>>___start___<<<'
        start_server()
        print '<<<___start___>>>'
        
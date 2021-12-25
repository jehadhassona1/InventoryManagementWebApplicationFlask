import os
#برجع مكان الفايل الي انا فيه 
basrdir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URL=os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basrdir,'app.db')
  
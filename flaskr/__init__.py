import os

from flask import Flask
from flaskr.db import init_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) #creates the Flask instance

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SECRET_KEY='dev', #should be overriden with a random value when deploying
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)
    '''
    mongodb using flask_mongoengine
    db = MongoEngine() #before define app:
    
    app = Flask(...)
    
    app.config['MONGODB_SETITNGS'] = {
    'db': dbname,
    'host': 'mongodb+srv://dbAdmin:insolar@cluster0.huuha.mongodb.net/insolar?retryWrites=true&w=majority"',
    }
    
    db.init_app(app)
    '''

    with app.app_context():
        init_db()

    from . import auth
    app.register_blueprint(auth.bp)

    # import and register the contacts bluepoint
    with app.app_context():
        from . import contact

        app.register_blueprint(contact.bp)
        app.add_url_rule('/', endpoint='index')

    return app
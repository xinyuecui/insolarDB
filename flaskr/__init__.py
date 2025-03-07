import os

from flask import Flask
from flask_pymongo import PyMongo


def create_app(test_config=None):
    '''
        create and configure the app
    '''

    app = Flask(__name__, instance_relative_config=True) #creates the Flask instance

    app.config.from_mapping(
        SECRET_KEY='dev', #should be overriden with a random value when deploying
    )

    app.config['MONGO_URI'] = 'mongodb+srv://dbAdmin:insolar@cluster0.huuha.mongodb.net/insolar?retryWrites=true&w=majority'
    mongo = PyMongo(app)

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


    # import and register the contacts bluepoint
    with app.app_context():
        from . import contact
        app.register_blueprint(contact.bp)
        app.add_url_rule('/', endpoint='index')

    return app
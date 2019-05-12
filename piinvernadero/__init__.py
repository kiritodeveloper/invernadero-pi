import os 
import atexit

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'invernadero.sqlite'),
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


    # Para ejecutar cada 5 segundos la lectura de sensores
    @app.before_first_request
    def init_scheduler():
        from . import sensorread
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=sensorread.read_sensors, trigger="interval", seconds=5)
        scheduler.start()
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #Para inicializar la DB
    from . import db
    db.init_app(app)



    #Para la autenticacion
    from . import auth
    app.register_blueprint(auth.bp)

    from . import grupo
    app.register_blueprint(grupo.bp)

    from . import site
    app.register_blueprint(site.bp)

    from . import sensor
    app.register_blueprint(sensor.bp)


    from . import dashboard
    app.register_blueprint(dashboard.bp)

    from . import actuator
    app.register_blueprint(actuator.bp)

    from . import sensorread


    return app



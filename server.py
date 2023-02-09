from flask import Flask


def create_app(config_class, *blueprints):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_errorhandlers(app)
    register_blueprints(app, *blueprints)
    register_extensions(app)
    return app


def register_blueprints(app: Flask, *args):
    for blueprint in args:
        app.register_blueprint(blueprint)


def register_extensions(app: Flask):
    from models import ma
    from models import db, create_database

    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        create_database()
        db.create_all()


def register_errorhandlers(app: Flask):
    from flask import jsonify
    from sqlalchemy.exc import SQLAlchemyError

    # * Errors in db
    @app.errorhandler(SQLAlchemyError)
    def sql_alchemy_error(err):
        app.logger.exception(err)
        return jsonify({"Request body error": f"{err}"}), 400

    @app.errorhandler(Exception)
    def exception(err):
        app.logger.exception(err)
        return jsonify({"error": f"{err}"}), 400

    # * Error 401
    @app.errorhandler(401)
    def method_not_unauthorized(err):
        app.logger.exception(err)
        return jsonify({"Authenticate": "Could not verify"}), 401

    # * Error 403
    @app.errorhandler(403)
    def access_denied(err):
        app.logger.exception(err)
        return jsonify({"Permission": "Acces denied for this resource"}), 403

    # * Error 404
    @app.errorhandler(404)
    def page_not_found(err):
        app.logger.exception(err)
        return jsonify({"Message": "This page could not be found"}), 404

    # * Error 405
    @app.errorhandler(405)
    def method_not_allowed(err):
        app.logger.exception(err)
        return (
            jsonify({"Message": "The method is not allowed for the requested URL"}),
            405,
        )

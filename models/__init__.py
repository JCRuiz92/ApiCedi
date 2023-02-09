from flask_sqlalchemy import SQLAlchemy, Model
from flask_marshmallow import Marshmallow
from flask import abort, current_app as app
from sqlalchemy import exc, event
from datetime import datetime
from werkzeug.security import generate_password_hash


class DBUtils(Model):
    """ Utils for database"""

    def save(self):
        """ Save new record """
        db.session.add(self)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError("Error trying to save or update resource")

    @classmethod
    def get_by_id(cls, id, *args):
        """get record for id

        Args:
            table(Model): table for search
            id: id for search
            args: other arguments
        Returns:
            object: requested data
            int: http error 404
        """
        return cls.query.get_or_404(id)

    @classmethod
    def all(cls, *args):
        """get all records

        Args:
            table(Model): table for search
            args: other arguments
        Returns:
            object: requested records
            int: http error 404
        """
        list_records = cls.query.all()
        return list_records if list_records else abort(404)

    @classmethod
    def paginate(cls, page: int, per_page: int, *args):
        """paginate all records

        Args:
            table(Model): table for search
            page(int): size to page
            per_page(int): page to show
            args: other arguments
        Returns:
            object: requested records
            int: http error 404
        """
        paginate = cls.query.paginate(page, per_page, False)
        return paginate if paginate.items else abort(404)

    def delete(self, *args):
        """ Delete record """
        db.session.delete(self)
        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError("Error trying to delete resource")


db = SQLAlchemy(model_class=DBUtils)
ma = Marshmallow()
Model = db.Model
Schema = ma.Schema


def create_database():
    """Crate database"""
    engine = db.create_engine(app.config["EGINE_URI"], {})
    engine.execute(f"CREATE DATABASE IF NOT EXISTS {app.config['DB_NAME']}")


from .table_example import TableExample


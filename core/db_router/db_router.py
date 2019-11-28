def _get_db_schema( model ):
    if hasattr( model._meta, "db_scheme" ) and model._meta.db_scheme is not None:
        return model._meta.db_scheme
    return None


class DBRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        return _get_db_schema( model )

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        return _get_db_schema( model )

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        return _get_db_schema( obj1 )

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        return db == 'default'

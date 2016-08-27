
from tornado.gen import coroutine
from database import DatabaseError
import logging


class Model(object):

    @coroutine
    def __setup_event__(self, event_name):
        events = yield self.get_setup_db().get(
            """
                SHOW EVENTS LIKE %s;
            """, event_name)

        if events:
            if event_name in events.values():
                return

        with (open("sql/{0}.sql".format(event_name))) as f:
            sql = f.read()

        try:
            yield self.get_setup_db().execute(sql)
        except DatabaseError as e:
            logging.error("Failed to create event '{0}': {1}".format(event_name, e.args[1]))
        else:
            logging.warn("Created event '{0}'".format(event_name))

            method_name = "setup_event_" + event_name

            if hasattr(self, method_name):
                yield getattr(self, method_name)()

    @coroutine
    def __setup_table__(self, table_name):
        tables = yield self.get_setup_db().get(
            """
                SHOW TABLES LIKE %s;
            """, table_name)

        if tables:
            if table_name in tables.values():
                return

        with (open("sql/{0}.sql".format(table_name))) as f:
            sql = f.read()

        try:
            yield self.get_setup_db().execute(sql)
        except DatabaseError as e:
            logging.error("Failed to create table '{0}': {1}".format(table_name, e.args[1]))
        else:
            logging.warn("Created table '{0}'".format(table_name))

            method_name = "setup_table_" + table_name

            if hasattr(self, method_name):
                yield getattr(self, method_name)()

    def get_setup_tables(self):
        return []

    def get_setup_events(self):
        return []

    def get_setup_db(self):
        raise NotImplementedError()

    @coroutine
    def started(self):
        for table in self.get_setup_tables():
            yield self.__setup_table__(table)

        for event in self.get_setup_events():
            yield self.__setup_event__(event)

    @coroutine
    def stopped(self):
        """
        Called when a server is about to shutdown.
        Please not that within 5 second the server will be shut down anyway.
        """
        pass

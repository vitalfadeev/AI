 # http://docs.python.org/howto/logging.html#configuring-logging
import logging
import socket
import traceback
from datetime import datetime
from sqlalchemy import create_engine


"""
DESCRIPTION:    Class for catching any kind of exceptions and store them in a data base
MAIN FUNCTION:  class Logger
USAGE:		    import Logger class in your module. Wrap your functions in try-except block
		and if call Logger passing the error inside:

		try:
		    1/0
		except Exception as error:
		    Logger(error)
"""


class GlobalLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

        self.PORT = 3306
        self.HOST = '192.168.1.146'
        self.USER = 'admin'
        self.PASSWORD = 'ixioo999'
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.max_lvl = 1

        self.levels = {
            1: ""'DEBUG'"",
            2: "'INFO'",
            3: "'WARNING'",
            4: "'ERROR'",
            5: "'CRITICAL'"
        }

        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.addHandler(ch)

        # Create connections to databases
        self.LOGGER_CURSOR = self.get_connection_to_database('globallogger')

    def get_connection_to_database(self, database_name):
        # Create database engine
        engine = create_engine("mysql://{user}:{pw}@{host}:{port}/{db}".format(user=self.USER,
                                                                               pw=self.PASSWORD,
                                                                               db=database_name,
                                                                               host=self.HOST,
                                                                               port=self.PORT))
        return engine

    def display_table(self):
        for i in self.LOGGER_CURSOR.execute("""SELECT * FROM globallogger""").fetchall():
            print(i)

    def clear_table(self):
        self.LOGGER_CURSOR.execute("DELETE FROM globallogger.globallogger")


    def add_log_to_sql(self, exception):
        traceback_values = traceback.format_exception(etype=type(exception),
                                                      value=exception,
                                                      tb=exception.__traceback__)
        tb = exception.__traceback__
        stk = traceback.extract_tb(tb)

        main_module = stk[0][0].split('/')[-1].replace('\n', '')
        main_func = stk[0][3].replace('\n', '')
        trace = ''.join(traceback_values)
        trace = repr(trace.split('\n')[1])
        message = str(exception)

        sql = """INSERT INTO globallogger.globallogger(DateTimeCreation, Level, TraceBack, MainModule, MainFunction, Message, HostName, IP)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""" % (
            f"'{datetime.now()}'",
            self.levels[self.level],
            trace,
            repr(main_module),
            repr(main_func),
            repr(message),
            repr(self.host_name),
            repr(self.host_ip)
        )
        self.LOGGER_CURSOR.execute(sql)

    def add_message_to_sql(self, message, module=None):
        import os
        cwd = os.path.dirname(os.path.abspath(__file__))
        # print(cwd)

        if module is None:
            sql = """INSERT INTO globallogger.globallogger(Level, Message, HostName, IP)
                     VALUES (%s, %s, %s, %s)""" % (self.levels[self.level], self.normalize_message(message), repr(self.host_name), repr(self.host_ip))
        else:
            sql = """INSERT INTO globallogger.globallogger(Level, Message, HostName, IP, MainModule)
                                 VALUES (%s, %s, %s, %s, %s)""" % (
            self.levels[self.level], self.normalize_message(message), repr(self.host_name), repr(self.host_ip), module)
        self.LOGGER_CURSOR.execute(sql)


    def debug(self, msg, *args, **kwargs):
        self.level = 1
        if self.max_lvl <= 1:
            super().debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.level = 2
        if self.max_lvl <= 2:
            super().info(msg, *args, **kwargs)

    def warning(self, msg, module=None, *args, **kwargs):
        self.level = 3
        if self.max_lvl <= 3:
            super().warning(msg, *args, **kwargs)

            if type(msg) is not str:
                self.add_log_to_sql(msg)
            else:
                if module is not None:
                    self.add_message_to_sql(msg, module=module)
                else:
                    self.add_message_to_sql(msg)

    def error(self, msg, module=None, *args, **kwargs):
        self.level = 4
        if self.max_lvl <= 4:
            super().error(msg, *args, **kwargs)

            if type(msg) is not str:
                self.add_log_to_sql(msg)
            else:
                if module is not None:
                    self.add_message_to_sql(msg, module=module)
                else:
                    self.add_message_to_sql(msg)

    def critical(self, msg, module=None, *args, **kwargs):
        self.level = 5
        if self.max_lvl <= 5:
            super().critical(msg, *args, **kwargs)

            if type(msg) is not str:
                self.add_log_to_sql(msg)
            else:
                if module is not None:
                    self.add_message_to_sql(msg, module=module)
                else:
                    self.add_message_to_sql(msg)

    def setLevel(self, level):
        super().setLevel(level)
        self.max_lvl = level

    @staticmethod
    def normalize_message(message:str):
        res = ''
        for c in message:
            if c != "'":
                res += c
            else:
                res += '"'
        return "'" + res + "'"


if __name__ == '__main__':
    # create logger
    logger = GlobalLogger('example')
    logger.display_table()

    # logger.setLevel(2)

    # create console handler and set level to debug
    # ch = logging.StreamHandler()
    #
    # # create formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #
    # # add formatter to ch
    # ch.setFormatter(formatter)
    #
    # # add ch to logger
    # logger.addHandler(ch)
    #
    # 'application' code
    try:
        a = 1
        b = 0
        c = a / b
    except Exception as ex:
        logger.critical(ex)
    logger.info("EVERYTHING IS WORKING!")


import sys

class Jlog:

    def __init__(self, *, name=None, email=None):
        self.__file = file
        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def file(self):
        return self.__file


    def debug(self, body):
        logging.debug(' %s : %s',self.thread_id, logtext)

    def info(self, logtext):
        logging.info(' %s : %s',self.thread_id, logtext)

    def warn(self, logtext):
        logging.warn(' %s : %s',self.thread_id, logtext)

    def error(self, logtext):
        logging.error(' %s : %s',self.thread_id, logtext)

    def logging(level,body):
        print('')

"""
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format=
            '{'
            ' "time":"%(asctime)s"'
            ' "type":""'
            ' "level":"%(levelname)s"'
            ' "file":"%(filename)s"'
            ' "line":"%(lineno)s"'
            ' "thread":""'
            ' "body":"%(message)s"'
            '},'
    )
    thread_id = ''

    def __init__( self, thread_id) :
        self.thread_id = thread_id

    def debug(self, logtext):
        logging.debug(' %s : %s',self.thread_id, logtext)

    def info(self, logtext):
        logging.info(' %s : %s',self.thread_id, logtext)

    def warn(self, logtext):
        logging.warn(' %s : %s',self.thread_id, logtext)

    def error(self, logtext):
        logging.error(' %s : %s',self.thread_id, logtext)
"""
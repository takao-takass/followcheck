
import logging

class ThreadLogging:

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(message)s')
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

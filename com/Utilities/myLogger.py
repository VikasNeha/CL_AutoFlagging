import logging
import CL_AutoFlagging

module_logger = logging.getLogger('main.logging')


def setupLogging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=CL_AutoFlagging.get_main_dir() + '/Resources/logger.log',
                        filemode='w', )
    #fh = logging.FileHandler('logger.log')
    logger = logging.getLogger('')
    #logger.addHandler(fh)
    #module_logger.info("abc1")
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    logger.addHandler(ch)
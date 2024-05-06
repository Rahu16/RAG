import logging

formatter = logging.Formatter("[%(levelname)s]: RAG_QNA : V1: %(asctime)s:"
                              "%(module)s: %(funcName)s: %(message)s:", "%Y-%m-%d %H:%M:%S")
"""to print message on console"""
handler = logging.StreamHandler()

'''to append in file remove comment'''
# handler = logging.FileHandler("logger.txt", mode='a', encoding=None, delay=False)

handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

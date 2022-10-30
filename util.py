import sys
import numpy as np
import random
import torch
import logging
import json
import time
from datetime import timedelta

def set_random_seed(args):
    if "torch" in sys.modules:
        torch.manual_seed(args["random_seed"])
    np.random.seed(int(args["random_seed"]))
    random.seed(args["random_seed"])

def setup_logging(args):
    
    level = {
        "info" : logging.INFO, 
        "debug" : logging.DEBUG,
        "critical" : logging.CRITICAL
    }
    
    msg_format = '%(asctime)s:%(levelname)s: %(message)s'
    formatter = logging.Formatter(msg_format, datefmt = '%H:%M:%S')
    args = args["logging"]

    file_handler = logging.FileHandler(args["filename"], mode = args["filemode"])
    file_handler.setLevel(level=level[args["level"]])
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    
    logger = logging.getLogger()
    logger.setLevel(level[args["level"]])

def load_dataset(path: str):
    
    logging.info("Load dataset {}!".format(path))
    path = str(path)
    
    if "json" in path:
        with open(path, encoding = "utf-8") as f:
            if ".jsonl" in path:
                data = [json.loads(line) for line in f]
            elif ".json" in path:
                data = json.loads(f.read())
    return data
def fcall(fun):
    """
    Convenience decorator used to measure the time spent while executing
    the decorated function.
    :param fun:
    :return:
    """
    def wrapper(*args, **kwargs):

        logging.info("[{}] ...".format(fun.__name__))

        start_time = time.perf_counter()
        res = fun(*args, **kwargs)
        end_time = time.perf_counter()
        runtime = end_time - start_time

        logging.info("[{}] Done! {}s\n".format(fun.__name__, timedelta(seconds=runtime)))
        return res

    return wrapper

@fcall
def parser_config(path):
    
    return load_dataset(path)
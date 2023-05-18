import argparse
import logging

from util import parser_config, setup_logging, set_random_seed
from model.utils import preprocess_dataset


from numba.core.errors import NumbaWarning
import warnings



def main():
    warnings.simplefilter('ignore', category=NumbaWarning)
    logging.getLogger('numba').setLevel(logging.WARNING)
    parser = argparse.ArgumentParser()
    arguments = [
        ("preprocess", preprocess_dataset, "Preprocess samples - cleaning/filtering of invalid data")
    ]

    for arg, _, description in arguments:
        parser.add_argument('--{}'.format(arg), action ='store_true', help=description)

    params = parser.parse_args()
    args = parser_config("config.json")
    
    setup_logging(args)
    set_random_seed(args)
    for arg, fun, _ in arguments:
        if hasattr(params, arg) and getattr(params, arg):
            print(1)
            logging.info("Performing {} operation..".format(arg))
            fun(args)

if __name__ == "__main__":
    main()
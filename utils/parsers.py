import argparse


def argument_parser_land_deformation():
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    parser = argparse.ArgumentParser(description="Experiment Args")
    parser.add_argument('-r', "--root-folder", dest='root_folder', required=True, help="path to root folder")
    parser.add_argument('-p', "--pilot", dest='pilot', required=True, help="pilot city")
    parser.add_argument('-s', "--s1-product", dest='s1_product', required=True, help="insar sentinel-1 product")
    parser.add_argument('-c', "--clipped", dest='clipped', required=True, help="whether the data has been clipped")

    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    return parser


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
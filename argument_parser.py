import argparse
from settings import config


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n', '--hostname', type=str, default=config.hostname,
        help=f'DNS hostname with port, default {config.hostname}'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=config.port,
        help=f'TCP port number. Default {config.port}'
    )
    parser.add_argument(
        '-s', '--storage', type=str, default=config.storage_path,
        help=f'Storage path. Default {config.storage_path}'
    )
    return parser.parse_args()

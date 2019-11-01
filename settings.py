DEFAULT_HOSTNAME = 'http://k4m454k.hldns.ru:19100'
# DEFAULT_HOSTNAME = 'http://localhost:8090'

FORBIDDEN_FILE_NAMES = [
    'CON', 'COM0', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10',
    'COM11', 'COM12', 'COM13', 'COM14', 'COM15', 'LPT0', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6',
    'LPT7', 'LPT8', 'LPT9', 'LPT10', 'LPT11', 'LPT12', 'LPT13', 'LPT14', 'LPT15', "AUX", "PRN", "NUL"
]

DEFAULT_STORAGE_PATH = './files'
DEFAULT_PORT = 8090


class Settings:
    def __init__(self, hostname, port, forbidden_filenames, storage_path):
        self.hostname = hostname
        self.port = port
        self.forbidden_filenames = forbidden_filenames
        self.storage_path = storage_path


config = Settings(
    hostname=DEFAULT_HOSTNAME,
    port=DEFAULT_PORT,
    forbidden_filenames=FORBIDDEN_FILE_NAMES,
    storage_path=DEFAULT_STORAGE_PATH
)

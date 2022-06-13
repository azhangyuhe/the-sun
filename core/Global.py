import signal
from config.auxiliary.common import get_banner
from config.auxiliary.common import create_log

ORIGINAL_SIGINT = signal.getsignal(signal.SIGINT)

# banner相关
BANNER = get_banner('C u i t  S c a n')

# 日志相关
LOGGER = create_log()

IP_PLUGIN = ['plugins/ip', 'plugins/os']
DOMAIN_PLUGIN = ['plugins/server', 'plugins/web']



BURP_SERVER_DICT="data/top20.txt"

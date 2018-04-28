from pkg_resources import get_distribution
try:
    __version__ = get_distribution('mpu').version
except:
    __version__ = 'Not installed'

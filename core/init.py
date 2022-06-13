import os
from importlib import import_module

from core.Global import IP_PLUGIN, DOMAIN_PLUGIN


def load_plugins(i):
    plug_tmp = {}
    for root, dirs, files in os.walk(i):
        files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)
        for file in files:

            # 'plugins/ip' ---> ['plugins', 'ip']
            tmp = [i for i in os.path.split(root) if i]
            if '/' in tmp[0]:
                tmp[0]=tmp[0].replace('/', '.')
            if not plug_tmp.get(tmp[-1], ''):
                plug_tmp[tmp[-1]] = []
            # ['plugins', 'ip'] ---> 'plugins.ip'
            package = '.'.join(tmp)
            # unauthorized.py ---> unauthorized
            file = os.path.splitext(file)[0]
            mod = import_module(f'{package}.{file}')
            mod = mod.Scan()
            plug_tmp[tmp[-1]].append((file, mod))
    return plug_tmp


def init():
    PLUGINS = dict()
    D_PLUGINS = dict()
    for i in IP_PLUGIN:
        PLUGINS.update(load_plugins(i))
    for i in DOMAIN_PLUGIN:
        D_PLUGINS.update(load_plugins(i))
    return PLUGINS,D_PLUGINS

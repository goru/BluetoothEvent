#!/usr/bin/env python

from setuptools import setup

APP = [ 'BluetoothEvent.py' ]
DATA_FILES = [
    'ic_phonelink_black_24dp.png',
    'ic_phonelink_white_24dp.png'
]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': [ 'rumps' ],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={
        'py2app': OPTIONS
    },
    setup_requires=[
        'py2app',
        'rumps'
    ],
    dependency_links=[
        'hg+https://bitbucket.org/ronaldoussoren/py2app@25ce18b#egg=py2app',
        'git+https://github.com/jaredks/rumps.git@ae11371#egg=rumps'
    ]
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

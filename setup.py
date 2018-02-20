import os
import sys
from distutils.core import setup
from distutils.sysconfig import get_python_lib

import py2exe  # NOQA

sys.argv.append('py2exe')

DATA = [
    ('imageformats', [
        os.path.join(
            get_python_lib(), 'PyQt4', 'plugins', 'imageformats', 'qico4.dll'
        ),
    ]),
]

setup(
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'includes': ['sip'],
            'optimize': 2,
        },
    },
    windows=[
        {
            'script': 'main.py',
            'dest_base': 'gatpy',
            'icon_resources': [(0, 'resources/icon.ico')],
        },
        {
            'script': 'manager.py',
            'dest_base': 'manager',
            'icon_resources': [(0, 'resources/icon.ico')],
        },
    ],
    data_files=DATA,
)

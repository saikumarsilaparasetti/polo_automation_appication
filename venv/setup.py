# from setuptools import setup
#
# APP = ["venv/main.py"]
# OPTIONS = {
#     "argv_emulation": True
# }
#
# setup(
#     app = APP,
#     options = { "py2app": OPTIONS},
#     setup_requires = ['py2app']
# )


from setuptools import setup
from PyInstaller.hooks import *
APP = ['venv/main.py']  # Replace with your main script

OPTIONS = {
    'argv_emulation': True
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
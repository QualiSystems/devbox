#!/usr/bin/env bash
pip uninstall devbox --yes
python setup.py build
python setup.py install

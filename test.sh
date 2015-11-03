#!/bin/bash
source install.sh > /dev/null
pylint -E rmrf_enter/*.py
echo "passed linting"
#python -m unittest discover --verbose --failfast --catch --start-directory rmrf_enter/test/ --pattern "*.py"

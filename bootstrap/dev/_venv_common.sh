#!/bin/sh -xe

VENV_NAME=${VENV_NAME:-venv}

# .egg-info directories tend to cause bizzaire problems (e.g. `pip -e
# .` might unexpectedly install letshelp-letsencrypt only, in case
# `python letshelp-letsencrypt/setup.py build` has been called
# earlier)
rm -rf *.egg-info

# virtualenv setup is NOT idempotent: shutil.Error:
# `/home/jakub/dev/letsencrypt/letsencrypt/venv/bin/python2` and
# `venv/bin/python2` are the same file
mv $VENV_NAME "$VENV_NAME.$(date +%s).bak" || true
virtualenv --no-site-packages $VENV_NAME $VENV_ARGS
. ./$VENV_NAME/bin/activate

# Separately install setuptools and pip to make sure following
# invocations use latest
pip install -U setuptools
pip install -U pip
pip install "$@"

echo "Please run the following command to activate developer environment:"
echo "source $VENV_NAME/bin/activate"

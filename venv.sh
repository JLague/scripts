#!/bin/sh

# Check if python module is loaded
if [ ! $(module is-loaded python) ]; then
    echo "Python is not loaded!" 1>&2
    echo "Loading latest version available..."
    module load python
fi

# Create and source venv
virtualenv --no-download $1 && source $1/bin/activate

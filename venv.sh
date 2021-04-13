#!/bin/sh


# Check if directory already exist
if [ -d "$1" ]; then
    echo "Directory $1 already exists!" 1>&2
    yes_or_no "Do you want to overwrite it?" || kill -INT $$ # SSH friendly :)
fi

# Check if python module is loaded
(module -v 2> /dev/null && ! module is-loaded python)
load_python=$?

echo $load_python

# Load python
if [ "$load_python" -eq "0" ]; then
    echo "Python is not loaded!" 1>&2
    echo "Loading latest version available..."
    module load python
fi

# Create and source venv
python -m venv $1 && source $1/bin/activate

# Unload python if necessary
if [ $load_python -eq "0" ]; then
    echo "Unloading python..."
    module unload python
fi

# Get a yes or no answer from user
function yes_or_no {
    while true; do
        read -p "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0  ;;
            [Nn]*) echo "Aborted" ; return  1 ;;
        esac
    done
}

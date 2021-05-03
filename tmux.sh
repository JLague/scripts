#!/bin/sh

if [ $# -eq 0 ]; then
    tmux
elif [ $# -eq 1 ]; then
    tmux has-session -t $1 && tmux attach-session -t $1 || tmux new-session -s $1
else
    echo "Usage: tmux [SESSION_NAME]"
fi

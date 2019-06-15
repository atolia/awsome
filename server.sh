#!/usr/bin/env bash

trap "kill %1; exit" SIGHUP SIGINT SIGTERM

./server.py &
while : ; do ./fetch.py out.json; sleep 20; done

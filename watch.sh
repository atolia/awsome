which fswatch || { echo please install fswatch; exit 1; }

trap "kill %1; exit" SIGHUP SIGINT SIGTERM

fswatch -o html.pug out.json docs/script.js docs/style.css |
  while read i; do   ./render.py html.pug out.json docs/index.html ; done &

open docs/index.html

while : ; do ./fetch.py out.json; sleep 20; done


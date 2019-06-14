which fswatch || { echo please install fswatch; exit 1; }

fswatch -o html.pug out.json | while read i; do   ./render.py html.pug < out.json > out.html ; done &
open out.html


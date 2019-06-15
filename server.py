#!/usr/bin/env python

from render import render
from livereload import Server
# , shell

def myRender():
  render('html.pug', 'out.json', 'docs/index.html') 

server = Server()
server.watch('*.json', myRender )
# server.watch('*.pug', myRender )
# server.watch('docs/*.js', myRender )
# server.watch('docs/*.css', myRender )
server.serve(root='docs/')

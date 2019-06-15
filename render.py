#!/usr/bin/env python

import pypugjs, json, sys
from jinja2 import Environment, FileSystemLoader
from util import eprint

def render( pugName, inJson, htmlOut ):

  env = Environment(
      loader=FileSystemLoader('.'),
      extensions=['pypugjs.ext.jinja.PyPugJSExtension']
  )

  with open(inJson) as file:  
    data = json.load(file)

  eprint(f'Rendering data using template:{ pugName }, input:{inJson}, output:{htmlOut}  ')
  template = env.get_template( pugName )

  with open(htmlOut, 'w', encoding='utf-8') as outfile:
    outfile.write( template.render(data=data, foo=1) )

if __name__ == '__main__':
  if len(sys.argv) < 4 :
    print( f'Usage: {sys.argv[0]} html.pug out.json docs/index.html\n')
    exit(1)
  render(sys.argv[1], sys.argv[2], sys.argv[3])

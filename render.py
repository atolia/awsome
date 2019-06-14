#!/usr/bin/env python

import pypugjs, json, sys
from jinja2 import Environment, FileSystemLoader
from util import eprint


env = Environment(
    loader=FileSystemLoader('.'),
    extensions=['pypugjs.ext.jinja.PyPugJSExtension']
)


# with open(sys.stdin) as json_file:  
data = json.load(sys.stdin)

eprint(f'Rendering data using { sys.argv[1] } ')
template = env.get_template( sys.argv[1] )

print( template.render(data=data, foo=1) )

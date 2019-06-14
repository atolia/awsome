import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def age(t, now):
  t=t.replace(tzinfo=None)
  d=(now-t).days
  h=(now-t).seconds//3600
  m=(now-t).seconds%3600//60
  mm=dd=''
  if d>0:
    dd=f'{d}d'
  else:
    mm=f'{m}m'
  return dd + f'{h}h' + mm
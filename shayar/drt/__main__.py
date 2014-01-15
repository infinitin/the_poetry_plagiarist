__author__ = 'Nitin'

import build

f = open('grammar.fcfg', 'r+')
f.truncate()
build.write_all_rules(f)
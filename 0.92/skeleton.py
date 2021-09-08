#!/usr/bin/env python 

# skeleton.py - the bare bone of an inkscape extension python file

import inkex
import sys
from lxml import etree

class Skeleton(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)

  def effect(self):
    svg = etree.Element('svg')
    svg.set('width', '5in')
    svg.set('height', '5in')
    layer = etree.SubElement(svg, 'g')
    layer.set(inkex.addNS('label', 'inkscape'), 'layer 1')
    layer.set(inkex.addNS('groupmode', 'inkscape'),'layer')

    self.f = etree.tostring(svg) #svg file in str format
    # inkex.debug(self.unittouu('1in'))
    inkex.debug(sys.version)

  def output(self):
    sys.stdout.write(self.f)  # or self.f.write(sys.stdout)

if __name__ == '__main__':
  e = Skeleton()
  e.affect()

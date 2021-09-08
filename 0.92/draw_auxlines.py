#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
# draw_auxlines.py
Draw the auxilary lines for the SignTool package

Copyright (C) February 2018, June 2018 George Zhang

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
'''
This program create auxilary lines on a new layer. 
'''

import re
import inkex
import simplestyle


class SignTool_AuxLines(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)

    self.OptionParser.add_option("-d", "--dimensions", action="store", 
            type="string", dest="dimensions", default="0" )
    self.OptionParser.add_option("-t", "--type", action="store", 
            type="string", dest="type", default="horizontal" )
    self.OptionParser.add_option("--fStrokeWidth", action="store", type="float", 
            dest="fStrokeWidth", default="0" )


  def effect(self):
    so = self.options
    # need to add code for irregular string input
    
    str_input = so.dimensions
    orient = so.type
    
    lstr = self.verify_str(str_input)
    elem = self.document.getroot()
    aux_layer = self.find_or_create_layer( elem, 'aux_lines')
    
    self.draw_alignment_lines(lstr, orient, aux_layer)

  
  def verify_str(self, str_input):    
    strlist_re = []
    str_r = str_input.replace(';', ',')
    str_r = str_input.replace(':', ',')
    str_remove = re.sub(r'[^\d\s,.]', '', str_r) # remove char
    str_l = str_remove.split(',')  
    for s in str_l:
      strlist_re.append(s.strip())
    return strlist_re


  def draw_alignment_lines(self, str_list, orientation, parent):
    
    style = {
      'stroke': '#000000',
      'stroke-width': self.unittouu(str(self.options.fStrokeWidth) + 'px'),
      'fill': 'none'}
    
    font_style = {
      'font-size' : '0.5in',
      'alignment-baseline' : 'middle',
      'text-anchor' : 'end' }

    height = self.unittouu('3in')
    offset = self.unittouu('1in')
    if orientation == 'horizontal' : 
      self.draw_SVG_line( (offset, -1 * offset), (offset, -1 * height - offset), style, 'line', parent)
    else:
      self.draw_SVG_line( (-1 * offset, offset), (-1 * height - offset, offset), style, 'line', parent)

    # use 1 inch offset, this is global setting
    start = offset
    end = offset
    for width in str_list:
      iwidth = self.unittouu(width+'in')
      end = end + iwidth
      if orientation == 'horizontal' :
        self.draw_SVG_line( (end, -1 * offset), (end, -1 *  height - offset), style,  'line', parent) 
        self.draw_SVG_line( (start, -2 *  height/3 - offset), (end,-2 * height/3 - offset), style, 
          'line', parent)
        font_style['text-anchor'] = 'middle'
        self.place_text(width+ ' in', start / 2 + end / 2, 
            -2 *  height/3 - offset - offset /2, 
            font_style, parent)
      else: 
        self.draw_SVG_line( (-1 * offset, end), (-1 * height - offset, end), style,  'line', parent) 
        self.draw_SVG_line( (-1 *  height*2 /3 - offset, start), 
            (-1 * height * 2/3 - offset, end), style, 'line', parent)
        self.place_text(width + ' in', -1 *  height*2 /3 - offset - offset/2, 
            start/2 + end / 2 + self.unittouu('0.718in'), 
            font_style, parent)

      start = start + iwidth

  def place_text(self, msg, x, y, style, parent):
    text = inkex.etree.Element(inkex.addNS('text', 'svg'))
    text.text = msg
    text.set('x', str(x))
    text.set('y', str(y))
    text.set('style', simplestyle.formatStyle(style))
    parent.append(text)
    

  def draw_SVG_line(self,(x1, y1), (x2, y2), style, name, parent):
    line_style   = style
    line_attribs = {'style':simplestyle.formatStyle(line_style),
      inkex.addNS('label','inkscape'):name,
      'd':'M '+str(x1)+','+str(y1)+' L '+str(x2)+','+str(y2)}
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )


  # find or create a layer given layer name and parent
  def find_or_create_layer(self, parent, layer_name):
    path='//svg:g[@inkscape:label="%s"]'%layer_name
    el_list = self.document.xpath(path, namespaces = inkex.NSS)
    if el_list:
      layer = el_list[0]
    else:       
      layer = inkex.etree.SubElement(parent, 'g')
      layer.set(inkex.addNS('label', 'inkscape'), layer_name )
      layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
    return layer


if __name__ == '__main__':
  e = SignTool_AuxLines()
  e.affect()

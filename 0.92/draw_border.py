#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
# draw_border.py
Draw the border for the SignTool package

Copyright (C) February 2018, June 2018, February 2020 George Zhang

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
This program changes the page size and creates a border on new layer. 
'''

import inkex
import simplestyle, simpletransform
import sys
import math

def draw_SVG_line(x1, y1, x2, y2, style, name, parent):
  line_style = {'stroke': style['stroke_color'],
           'stroke-width': str(style['stroke_width']), 
           'fill': style['fill'] }
  line_attribs = {'style': simplestyle.formatStyle(line_style), 
            inkex.addNS('label', 'inkscape'): name,
            'd': 'M ' + str(x1) + ',' + str(y1) + ' L' +
               str(x2) + ',' + str(y2) }
  elm = inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), line_attribs )
  return elm
  
def draw_SVG_circle(x, y, radius, style, name, parent):
  circle_style = {'stroke': style['stroke_color'],
           'stroke-width': str(style['stroke_width']), 
           'fill': style['fill'] }
  circle_attribs = {'style': simplestyle.formatStyle(circle_style), 
            inkex.addNS('label', 'inkscape'): name, 
            'cx': str(x), 'cy': str(y), 
            'r': str(radius) }
  elm = inkex.etree.SubElement(parent, inkex.addNS('circle', 'svg'), circle_attribs)
  return elm
  
def draw_mark(x, y, radius, style, name, parent):
  draw_SVG_circle(x, y, radius, style, name + 'circle', parent)
  draw_SVG_line(x - radius, y, x + radius, y, style, name + 'line1', parent)
  draw_SVG_line(x, y - radius, x, y + radius, style, name + 'line1', parent)

# draw four corner marks  
def draw_corner_marks(width, height, ra, style_stars, layer_bk):
  draw_mark(ra, ra, 0.5 * ra, style_stars, 'mark1', layer_bk)
  draw_mark((width + 1) * ra, ra, 0.5 * ra, style_stars, 'mark2', layer_bk)
  draw_mark(ra, (height + 1) * ra, 0.5 * ra, style_stars, 'mark3', layer_bk)
  draw_mark((width + 1) * ra, (height + 1) * ra, 0.5 * ra, style_stars, 'mark4', layer_bk)

def draw_outside_marks(width, height, ra, style_stars, layer_bk):
  draw_mark((width/2 + 1) * ra, -0.5 * ra, 0.5 * ra, style_stars, 'outmark1', layer_bk)
  draw_mark((width/2 + 1) * ra, (height + 2 + 0.5) * ra, 0.5 * ra, style_stars, 'outmark2', layer_bk)
  draw_mark(-0.5 * ra, (height /2 + 1) * ra, 0.5 * ra, style_stars, 'outmark2', layer_bk)
  draw_mark((width + 2 + 0.5) * ra, (height /2 + 1) * ra, 0.5 * ra, style_stars, 'outmark2', layer_bk)

# draw diamond border four corner marks  
def draw_diamond_corner_marks(width, height, ra, style_stars, layer_bk):
  draw_mark(width / 2 * ra, ra, 0.5 * ra, style_stars, 'mark1', layer_bk)
  draw_mark(width /2 * ra, (height - 1) * ra, 0.5 * ra, style_stars, 'mark2', layer_bk)
  draw_mark(ra, height /2 * ra, 0.5 * ra, style_stars, 'mark3', layer_bk)
  draw_mark((width -1) * ra, height / 2 * ra, 0.5 * ra, style_stars, 'mark4', layer_bk)


#draw an SVG rectangle with radius
def draw_SVG_rect_ri(x, y, width, height, radius, style, name, parent):
  line_style = {'stroke': style['stroke_color'],
           'stroke-width': str(style['stroke_width']), 
           'fill': style['fill'] }
  rect_ri_attribs = { 'style' : simplestyle.formatStyle(line_style),
           'width' : str(width), 'height' : str(height),
           'rx' : str(radius), 'ry' : str(radius),
           'x' : str(x), 'y' : str(y),
           inkex.addNS('label', 'inkscape') : name } 
  elm = inkex.etree.SubElement(parent, inkex.addNS('rect', 'svg'), rect_ri_attribs )
  return elm

def draw_SVG_rect(x, y, width, height, style, name, parent):
  line_style = {'stroke': style['stroke_color'],
           'stroke-width': str(style['stroke_width']), 
           'fill': style['fill'] }
  rect_ri_attribs = { 'style' : simplestyle.formatStyle(line_style),
           'width' : str(width), 'height' : str(height),
           'x' : str(x), 'y' : str(y),
           inkex.addNS('label', 'inkscape') : name } 
  elm = inkex.etree.SubElement(parent, inkex.addNS('rect', 'svg'), rect_ri_attribs )
  return elm


class SignTool_Border(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)
    self.style_stroke = {}

    self.OptionParser.add_option("--tab", action="store", type="string", dest="active_tab", default="Rectangle")
    
    self.OptionParser.add_option("--width", action="store", type="int", dest="width", default="0" )
    self.OptionParser.add_option("--height", action="store", type="int", dest="height", default="0" )
    self.OptionParser.add_option("--radius", action="store", type="float", dest="radius", default="0" )
    self.OptionParser.add_option("--offset", action="store", type="float", dest="offset", default="0" )
    self.OptionParser.add_option("--bdwidth", action="store", type="float", dest="bdwidth", default="0" )
    
    self.OptionParser.add_option("--diamond_width", action="store", type="int", dest="diamond_width", default="0" )
    self.OptionParser.add_option("--diamond_radius", action="store", type="float", dest="diamond_radius", default="0" )
    self.OptionParser.add_option("--diamond_offset", action="store", type="float", dest="diamond_offset", default="0" )
    self.OptionParser.add_option("--diamond_bdwidth", action="store", type="float", dest="diamond_bdwidth", default="0" )
    
    self.OptionParser.add_option("--bar_width", action="store", type="int", dest="bar_width", default="0" )
    self.OptionParser.add_option("--bar_height", action="store", type="float", dest="bar_height", default="0" )

    self.OptionParser.add_option("--bDrawMark", action="store", type="inkbool", dest="bDrawMark", default=False )
    self.OptionParser.add_option("--fStrokeWidth", action="store", type="float", dest="fStrokeWidth", default="0" )

  def effect(self):
    so = self.options
    
    self.style_stroke = {
      'stroke_color': '#000000',
      'stroke_width': self.unittouu(str(so.fStrokeWidth) + 'px'),
      'fill': 'none'}
    
    # pass string value is "rect", this is really weired
    # grep to find it was used in gcodetools.py 
    if so.active_tab == '"rect"':
      self.drawRectBorder()
    elif so.active_tab == '"diamond"':
      self.drawDiamondBorder()
    elif so.active_tab == '"bar"':
      self.drawBar()
    else:
      inkex.debug('Please choose other tabs, then apply')

  def drawDiamondBorder(self):
    so = self.options
    w = so.diamond_width
    h = w
    r = so.diamond_radius
    off = so.diamond_offset
    bdw = so.diamond_bdwidth
    
    ra = 25.4
    svg_elem = self.document.getroot()
    
    page_width = w * math.cos( math.radians(45)) * 2 + 2
    page_height = page_width
    
    svg_elem.set('width', str(page_width) + 'in')
    svg_elem.set('height', str(page_height) + 'in')
    svg_elem.set('viewBox', '0 0 ' + str(page_width * ra) + ' ' 
                   + str(page_height * ra) )  

    layer_bd = self.createLayer(svg_elem,'border') 
  
    style_bd = self.style_stroke
  
    trans_str = 'translate(' + str( page_width / 2 * ra) + ',' + str( 1 * ra) + ') '
    trans_str += 'rotate(' + str(45) + ')'
    trans_mat = simpletransform.parseTransform(trans_str)
  
    elm = draw_SVG_rect_ri(0, 0, w * ra, h * ra, 
            r * ra, style_bd, 'border_outside', layer_bd)
    simpletransform.applyTransformToNode(trans_mat, elm)

    
    if off > 0 :
      elm = draw_SVG_rect_ri(off * ra, off * ra, 
              (w-2*off) * ra , (h-2*off) * ra,
              (r-off) * ra , style_bd, 'border_offset', layer_bd)
      simpletransform.applyTransformToNode(trans_mat, elm)
      
    elm = draw_SVG_rect_ri((off+bdw) * ra, (off+bdw) * ra,
            (w - 2*off - 2 * bdw) * ra, 
            (h - 2*off - 2 * bdw) * ra, 
            (r - off - bdw) * ra, style_bd, 'border_inside', layer_bd)
    simpletransform.applyTransformToNode(trans_mat, elm)    
   
    layer_bk = self.createLayer(svg_elem,'corner_marks') 
    
   
    if self.options.bDrawMark: 
      draw_diamond_corner_marks(page_width, page_height, ra, style_bd, layer_bk)

  def drawBar(self):
    so = self.options
    w = so.bar_width
    h = so.bar_height
    
    svg_elem = self.document.getroot()
    layer_bd = self.findLayer(svg_elem, 'border')
    
    # place in the middle of drawing
    ra = 25.4
    style_bd = self.style_stroke
      
    page_w = svg_elem.get('width')
    page_h = svg_elem.get('height')
    elm = draw_SVG_rect( self.unittouu(page_w) / 2 - (w /2 ) * ra, 
                        self.unittouu(page_h) / 2 - (h /2) * ra , 
                        w * ra, h * ra, 
                        style_bd, 'bar', layer_bd)
    
      
  def drawRectBorder(self): 
    so = self.options
    w = (so.width)  # in inches
    h = (so.height)
    r = so.radius
    off = so.offset
    bdw = so.bdwidth
    
    #inkex.debug(str(self.unittouu('1in'))) this returns 25.3999...
    ra = 25.4  # inch to mm 
    svg_elem = self.document.getroot()
    
    style_bd = self.style_stroke
    
    page_width = w + 1 * 2
    page_height = h + 1 * 2
    svg_elem.set('width', str(page_width)+'in' )
    svg_elem.set('height', str(page_height)+'in' )
    svg_elem.set('viewBox', '0 0 ' + str(page_width * ra) + ' ' 
                   + str(page_height * ra) )

    layer_bk = self.createLayer(svg_elem,'corner_marks') 
    
    if self.options.bDrawMark: 
      draw_corner_marks(w, h, ra, style_bd, layer_bk)
      draw_outside_marks(w, h, ra, style_bd, layer_bk)


    layer_bd = self.createLayer(svg_elem,'border') 
    trans_str = 'translate(' + str( 1 * ra) + ',' + str( 1 * ra) + ')'
    trans_mat = simpletransform.parseTransform(trans_str)

    if w == 0 or h == 0 or r == 0:
      return

    elm = draw_SVG_rect_ri(0, 0, w * ra, h * ra, 
            r * ra, style_bd, 'border_outside', layer_bd)
    simpletransform.applyTransformToNode(trans_mat, elm)

    
    if off > 0 :
      elm = draw_SVG_rect_ri(off * ra, off * ra, 
              (w-2*off) * ra , (h-2*off) * ra,
              (r-off) * ra , style_bd, 'border_offset', layer_bd)
      simpletransform.applyTransformToNode(trans_mat, elm)
      
    elm = draw_SVG_rect_ri((off+bdw) * ra, (off+bdw) * ra,
            (w - 2*off - 2 * bdw) * ra, 
            (h - 2*off - 2 * bdw) * ra, 
            (r - off - bdw) * ra, style_bd, 'border_inside', layer_bd)
    simpletransform.applyTransformToNode(trans_mat, elm) 

 
  # Create a layer given layer name and parent
  # 6/13/2018 Change logic to delete layer if existing, then create
  def createLayer(self, parent, layer_name):
    path='//svg:g[@inkscape:label="%s"]'%layer_name
    el_list = self.document.xpath(path, namespaces = inkex.NSS)
    if el_list:
      layer = el_list[0]
      layer_parent = layer.getparent()
      layer_parent.remove(layer)
      
    layer = inkex.etree.SubElement(parent, 'g')
    layer.set(inkex.addNS('label', 'inkscape'), layer_name )
    layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
    return layer

    
  def findLayer(self, parent, layer_name):
    path='//svg:g[@inkscape:label="%s"]'%layer_name
    el_list = self.document.xpath(path, namespaces = inkex.NSS)
    if el_list:
      layer = el_list[0]
    else:
      path_layer = '//svg:g[@inkscape:groupmode="layer"]'
      elem_list = self.document.xpath(path_layer, namespaces = inkex.NSS) 
      if elem_list:
        layer = elem_list[0]
      else: 
        layer = self.createLayer(self.document.getroot(), 'layer_new')
    return layer

if __name__ == '__main__':
  e = SignTool_Border()
  e.affect()

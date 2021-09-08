#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
# draw_arrowhead.py
Draw arrowhead for the SignTool package

Copyright (C) June 2018 George Zhang

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


import inkex
import simplestyle, simpletransform, simplepath
import sys
import math


class SignTool_Arrowhead(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)
    
    self.OptionParser.add_option("--length", action="store", type="float", 
            dest="length", default="0" )
    self.OptionParser.add_option("--angle", action="store", type="float", 
            dest="angle", default="0" )
    self.OptionParser.add_option("-t", "--type", action="store", 
            type="string", dest="arrow_type", default="start" )
    
  def effect(self):
        
    pts = [] #initialise in case nothing is selected and following loop is not executed
    for id, node in self.selected.iteritems():
        if node.tag == inkex.addNS('path','svg'):
            pts = self.get_n_points_from_path( node, 2 ) 
            #find the (x,y) coordinates of the first 2 points of the path
    arrow_type = self.options.arrow_type
    L = self.unittouu('1px') * self.options.length
    A = math.radians(self.options.angle)
           
    if len(pts) == 2:
      
      pt0, pt1  = (pts[0], pts[1])
      eps = 0.01
      
      if inkex.are_near_relative(pt0[0], pt1[0], eps):
        self.draw_SVG_vertical(pt0, pt1, L, A, arrow_type)
      elif inkex.are_near_relative(pt0[1], pt1[1], eps):
        self.draw_SVG_horizontal(pt0, pt1, L, A, arrow_type)
      else: 
        self.draw_SVG_arrowhead(pt0, pt1, L, A, arrow_type)
        
        
  def draw_SVG_arrowhead(self, (x0, y0), (x1, y1), L, A, arrow_type):
    T = L * math.cos(A / 2)
    
    if x1 > x0:
      pt0 = (x0, y0)
      pt1 = (x1, y1)
    else:
      pt0 = (x1, y1)
      pt1 = (x0, y0)
      
    pt4 = self.point_on_line(pt0, pt1, T)
    alpha = math.atan2(pt1[1] - pt0[1], pt1[0] - pt0[0])
    dist = L * math.sin(A / 2)
    vec42 = ( dist * math.cos(alpha + math.pi / 2), 
              dist * math.sin(alpha + math.pi / 2) )
    pt2 = (pt4[0] + vec42[0], pt4[1] + vec42[1])
    vec43 = ( dist * math.cos(alpha - math.pi / 2), 
              dist * math.sin(alpha - math.pi / 2) )
    pt3 = (pt4[0] + vec43[0], pt4[1] + vec43[1])
    pt9 = self.point_on_line(pt0, pt1, T - self.unittouu('2px'))
    
    pt7 = self.point_on_line(pt1, pt0, T)
    vec76 = vec42
    pt6 = (pt7[0] + vec76[0], pt7[1] + vec76[1])
    vec75 = vec43
    pt5 = (pt7[0] + vec75[0], pt7[1] + vec75[1])
    pt8 = self.point_on_line(pt1, pt0, T - self.unittouu('2px'))

    
    style = {
      'stroke': 'none',
      'stroke-width':  '0',
      'fill': '#000000'}
  
    line_style = {
      'stroke': '#000000',
      'stroke-width':  self.unittouu('1px'),
      'fill': 'none'}
    if arrow_type == 'both':
    #   self.draw_SVG_line(pc, pt, style, 'line', self.current_layer)
      self.draw_SVG_head(pt0, pt2, pt3, style, 'head', self.current_layer)
      self.draw_SVG_head(pt1, pt5, pt6, style, 'head', self.current_layer)
      self.draw_SVG_line(pt8, pt9, line_style, 'line', self.current_layer)
    elif arrow_type == 'end':
      self.draw_SVG_head(pt1, pt5, pt6, style, 'head', self.current_layer)
      self.draw_SVG_line(pt8, pt0, line_style, 'line', self.current_layer)
    elif arrow_type == 'start':
      self.draw_SVG_head(pt0, pt2, pt3, style, 'head', self.current_layer)
      self.draw_SVG_line(pt1, pt9, line_style, 'line', self.current_layer)
      
    for id, node in self.selected.iteritems():
      if node.tag == inkex.addNS('path','svg'):
        node_parent = node.getparent()
        node_parent.remove(node)
    
        
  def draw_SVG_horizontal(self, (x0, y0), (x1, y1), L, A, arrow_type):
    T = L * math.cos(A / 2)
    if x1 > x0:
      pt0 = (x0, y0)
      pt1 = (x1, y1)
    else:
      pt0 = (x1, y1)
      pt1 = (x0, y0)
    pt4 = self.point_on_line(pt0, pt1, T)
    pt2 = (pt4[0], pt4[1] - L * math.sin(A / 2))
    pt3 = (pt4[0], pt4[1] + L * math.sin(A /2 ))
    
    pt7 = self.point_on_line(pt1, pt0, T)
    pt5 = (pt7[0], pt7[1] - L * math.sin(A / 2))
    pt6 = (pt7[0], pt7[1] + L * math.sin(A /2 ))
    
    pt8 = (pt7[0] + self.unittouu('2px'), pt7[1])
    pt9 = (pt4[0] - self.unittouu('2px'), pt4[1])
      
    style = {
      'stroke': 'none',
      'stroke-width':  '0',
      'fill': '#000000'}
  
    line_style = {
      'stroke': '#000000',
      'stroke-width':  self.unittouu('1px'),
      'fill': 'none'}
    if arrow_type == 'both':
    #   self.draw_SVG_line(pc, pt, style, 'line', self.current_layer)
      self.draw_SVG_head(pt0, pt2, pt3, style, 'head', self.current_layer)
      self.draw_SVG_head(pt1, pt5, pt6, style, 'head', self.current_layer)
      self.draw_SVG_line(pt8, pt9, line_style, 'line', self.current_layer)
    elif arrow_type == 'end':
      self.draw_SVG_head(pt1, pt5, pt6, style, 'head', self.current_layer)
      self.draw_SVG_line(pt8, pt0, line_style, 'line', self.current_layer)
    elif arrow_type == 'start':
      self.draw_SVG_head(pt0, pt2, pt3, style, 'head', self.current_layer)
      self.draw_SVG_line(pt1, pt9, line_style, 'line', self.current_layer)
      
    for id, node in self.selected.iteritems():
      if node.tag == inkex.addNS('path','svg'):
        node_parent = node.getparent()
        node_parent.remove(node)
        
  def draw_SVG_vertical(self, (x0, y0), (x1, y1), L, A, arrow_type ):      
    
    T = L * math.cos(A / 2) 
    if y1 > y0:
      pt0 = (x0, y0)
      pt1 = (x1, y1)
    else:
      pt0 = (x1, y1)
      pt1 = (x0, y0)
    pt4 = self.point_on_line(pt0, pt1, T)
    pt2 = (pt4[0] - L * math.sin(A / 2), pt4[1])
    pt3 = (pt4[0] + L * math.sin(A / 2), pt4[1])
    
    pt7 = self.point_on_line(pt1, pt0, T)
    pt5 = (pt7[0] - L * math.sin(A / 2), pt7[1])
    pt6 = (pt7[0] + L * math.sin(A / 2), pt7[1])
    
    pt8 = (pt7[0], pt7[1] + self.unittouu('2px'))
    pt9 = (pt4[0], pt4[1] - self.unittouu('2px'))

    style = {
      'stroke': 'none',
      'stroke-width':  '0',
      'fill': '#000000'}
  
    line_style = {
      'stroke': '#000000',
      'stroke-width':  self.unittouu('1px'),
      'fill': 'none'}
    if arrow_type == 'both':
    #   self.draw_SVG_line(pc, pt, style, 'line', self.current_layer)
      self.draw_SVG_head(pt0, pt2, pt3, style, 'head', self.current_layer)
      self.draw_SVG_head(pt1, pt5, pt6, style, 'head', self.current_layer)
      self.draw_SVG_line(pt8, pt9, line_style, 'line', self.current_layer)
    elif arrow_type == 'start':
      self.draw_SVG_head(pt1, pt5, pt6, style, 'head', self.current_layer)
      self.draw_SVG_line(pt8, pt0, line_style, 'line', self.current_layer)
    elif arrow_type == 'end':
      self.draw_SVG_head(pt0, pt2, pt3, style, 'head', self.current_layer)
      self.draw_SVG_line(pt1, pt9, line_style, 'line', self.current_layer)
      
    for id, node in self.selected.iteritems():
      if node.tag == inkex.addNS('path','svg'):
        node_parent = node.getparent()
        node_parent.remove(node)
        
      
  def draw_SVG_head(self, (x0, y0), (x1, y1), (x2, y2), style, name, parent):
        
    line_style   = style
    
    pathd = 'M %s %s ' % (x0, y0)
    pathd += 'L %s %s ' % (x1, y1)
    pathd += 'L %s %s ' % (x2, y2)
    pathd += 'Z'
        
    arrow_attribs = { 'style' : simplestyle.formatStyle(line_style),
             'd' : pathd, 
             inkex.addNS('label', 'inkscape') : name } 
    elem = inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), arrow_attribs )
  
  def draw_SVG_line(self,(x1, y1), (x2, y2), style, name, parent):
    line_style   = style
    line_attribs = {'style':simplestyle.formatStyle(line_style),
      inkex.addNS('label','inkscape'):name,
      'd':'M '+str(x1)+','+str(y1)+' L '+str(x2)+','+str(y2)}
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )


  def point_on_line(self, (x0, y0), (x1, y1), T):
    d = self.distance((x0, y0), (x1, y1))
    ratio = T / d
    x = x1 * ratio + x0 * (1 - ratio)
    y = y1 * ratio + y0 * (1 - ratio)
    return (x, y)
  
  #return the angle opposite side c
  def angle_from_3_sides(self, a, b, c): #return the angle opposite side c
    cosx = (a*a + b*b - c*c)/(2*a*b)  #use the cosine rule
    return math.acos(cosx)
      
  #find the pythagorean distance
  def distance(self, (x0,y0), (x1,y1)):
    return math.sqrt( (x0-x1)*(x0-x1) + (y0-y1)*(y0-y1) )
    
  #returns a list of first n points (x,y) in an SVG path-representing node
  def get_n_points_from_path(self, node, n):

    p = simplepath.parsePath(node.get('d')) #parse the path
    
    xi = [] #temporary storage for x and y (will combine at end)
    yi = []
    
    for cmd,params in p:                    
        defs = simplepath.pathdefs[cmd]
        for i in range(defs[1]):
            if   defs[3][i] == 'x' and len(xi) < n:
                xi.append(params[i])
            elif defs[3][i] == 'y' and len(yi) < n:
                yi.append(params[i])

    if len(xi) == n and len(yi) == n:
        points = [] # returned pairs of points
        for i in range(n):
            points.append( [ xi[i], yi[i] ] )
    else:
        #inkex.errormsg(_('Error: Not enough nodes to gather coordinates.')) #fail silently and exit, rather than invoke an error console
        return [] #return a blank
        
    return points
    

if __name__ == '__main__':
  e = SignTool_Arrowhead()
  e.affect()



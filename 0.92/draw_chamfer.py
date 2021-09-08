#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
# draw_chamfer.py
Draw the chamfer path for the SignTool package

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


class SignTool_Chamfer(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)
    
    self.OptionParser.add_option("--radius", action="store", type="float", 
            dest="radius", default="0" )
            
    
  def effect(self):
        
    pts = [] #initialise in case nothing is selected and following loop is not executed
    for id, node in self.selected.iteritems():
        if node.tag == inkex.addNS('path','svg'):
            pts = self.get_n_points_from_path( node, 3 ) 
            #find the (x,y) coordinates of the first 3 points of the path
    R = self.unittouu('1in') * self.options.radius
            
    if len(pts) == 3:
      pt0, pt1, pt2 = (pts[0], pts[1], pts[2])
      
      s_a = self.distance(pt0, pt1)
      s_b = self.distance(pt1, pt2)
      s_c = self.distance(pt0, pt2)
      
      angle = self.angle_from_3_sides(s_a, s_b, s_c)
      delta = math.pi - angle
      T = R * math.tan(delta / 2)
      pc = self.point_on_line( pt1, pt0, T)
      pt = self.point_on_line( pt1, pt2, T)
  
      style = {
        'stroke': '#000000',
        'stroke-width':  self.unittouu('1px'),
        'fill': 'none'}

   #   self.draw_SVG_line(pc, pt, style, 'line', self.current_layer)
      self.draw_SVG_arc(pt0, pc, pt, pt2, R, style, 'arc', self.current_layer)
      
  def draw_SVG_arc(self, (x0, y0), (x1, y1), (x2, y2), (x3, y3), R , style, name, parent):
        
    line_style   = style
    
    pathd = 'M %s %s ' % (x0, y0)
    pathd += 'L %s %s ' % (x1, y1)
    pathd += 'A %s %s %s %s %s %s %s ' % (R, R, 0, 0, 1, x2, y2)
    pathd += 'L %s %s ' % (x3, y3)
        
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
  e = SignTool_Chamfer()
  e.affect()



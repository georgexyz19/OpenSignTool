#!/usr/bin/env python 

'''
Copyright (C) December 2017, February 2018, June 2018 George Zhang

December 2017 Wrote the first version
The equations are from this webpage
http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm

June 2018 Added code to handle divide by zero error
Two circles have the same radius

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

'''


import sys
from math import *
import inkex
import simplestyle
import simplepath

def draw_SVG_line( (x1, y1), (x2, y2), name, parent):
    line_style   = { 'stroke':'#000000', 
        'stroke-width':str(Draw_Tangent.unittouu(e, '1px')), 'fill':'none' }
    line_attribs = {'style':simplestyle.formatStyle(line_style),
                    inkex.addNS('label','inkscape'):name,
                    'd':'M '+str(x1)+','+str(y1)+' L '+str(x2)+','+str(y2)}
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )

def distance( (x0,y0),(x1,y1)):
    return sqrt( (x0-x1)*(x0-x1) + (y0-y1)*(y0-y1) )

#returns a list of first n points (x,y) in an SVG path-representing node
def get_n_points_from_path( node, n):
    p = simplepath.parsePath(node.get('d')) 
    xi = [] 
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
        return [] #return a blank
        
    return points


class Draw_Tangent(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        
        self.OptionParser.add_option("--tab",
                action="store", type="string", 
                dest="tab", default="sampling",
                help="The selected UI-tab when OK was pressed") 
                
        self.OptionParser.add_option("--point_to_circle",
                        action="store", type="inkbool", 
                        dest="point_to_circle", default=False)
        self.OptionParser.add_option("--line_between_circle",
                        action="store", type="inkbool", 
                        dest="line_between_circle", default=False)

    def effect(self):
        
        so = self.options #shorthand
        
        pts = [] 
        
        if so.point_to_circle:
            for id, node in self.selected.iteritems():
                if node.tag == inkex.addNS('path','svg'):
                    pts = get_n_points_from_path( node, 3 ) 

            if len(pts) == 3: 
                
                group_translation = 'translate(' + str( pts[1][0] ) + ','+ str( pts[1][1] ) + ')'
                group_attribs = {inkex.addNS('label','inkscape'):'TriangleElements',
                      'transform':group_translation }
                layer = inkex.etree.SubElement(self.current_layer, 'g', group_attribs)
                
                xp = pts[0][0] - pts[1][0]
                yp = pts[0][1] - pts[1][1]
                
                r = distance( ( pts[1][0] , pts[1][1] ), ( pts[2][0] , pts[2][1] ))
                
                x1 = (r*r*xp + r*yp * sqrt(xp*xp + yp*yp - r*r) )/ (xp*xp + yp*yp)
                y1 = (r*r*yp - r*xp * sqrt(xp*xp + yp*yp - r*r) )/ (xp*xp + yp*yp)
                
                x2 = (r*r*xp - r*yp * sqrt(xp*xp + yp*yp - r*r) )/ (xp*xp + yp*yp)
                y2 = (r*r*yp + r*xp * sqrt(xp*xp + yp*yp - r*r) )/ (xp*xp + yp*yp)
            
                draw_SVG_line( (xp, yp), (x1, y1), 'Line', layer)
                draw_SVG_line( (xp, yp), (x2, y2), 'Line', layer)
                
        if so.line_between_circle:
            for id, node in self.selected.iteritems():
                if node.tag == inkex.addNS('path', 'svg'):
                    pts = get_n_points_from_path( node, 4 )
                    
            if len(pts) == 4:
                
                a = pts[0][0]
                b = pts[0][1]
                
                r0 = distance( ( pts[1][0], pts[1][1]), (a, b) )
                
                c = pts[2][0]
                d = pts[2][1]
                
                r1 = distance( (pts[3][0], pts[3][1]), (c, d) )
                
                eps = 0.01
                if  inkex.are_near_relative(r0, r1, eps):
                    #special condition
                    if not inkex.are_near_relative(c, a, eps):
                        angle = atan((d - b) / (c - a))
                    else:
                        angle = pi / 2

                    angle_plus = angle + pi / 2
                    point0_x = a + r0 * cos(angle_plus)
                    point0_y = b + r0 * sin(angle_plus)
                    point1_x = c + r1 * cos(angle_plus)
                    point1_y = d + r1 * sin(angle_plus)
                    
                    draw_SVG_line( (point0_x, point0_y), (point1_x, point1_y),  'Line', self.current_layer)
                    
                    angle_plus = angle - pi / 2
                    point0_x = a + r0 * cos(angle_plus)
                    point0_y = b + r0 * sin(angle_plus)
                    point1_x = c + r1 * cos(angle_plus)
                    point1_y = d + r1 * sin(angle_plus)
                    
                    draw_SVG_line( (point0_x, point0_y), (point1_x, point1_y),  'Line', self.current_layer)
                        
                else:
                    xp = ( c * r0 - a * r1 ) / (r0 -r1)
                    yp = ( d * r0 - b * r1 ) / (r0 -r1)
                    
                    denominator1 = (xp -a) * (xp -a) + (yp -b) * (yp -b)
                    
                    sqrt1 = sqrt( (xp - a) * (xp - a) + (yp - b) * (yp - b) - r0 * r0 )
                    
                    xt1 = ( r0 * r0 * (xp -a) + r0 * (yp -b) * sqrt1 ) / denominator1 + a
                    xt2 = ( r0 * r0 * (xp -a) - r0 * (yp -b) * sqrt1 ) / denominator1 + a
                    
                    yt1 = ( r0 * r0 * (yp -b) - r0 * (xp -a) * sqrt1 ) / denominator1 + b
                    yt2 = ( r0 * r0 * (yp -b) + r0 * (xp -a) * sqrt1 ) / denominator1 + b
                    
                    denominator2 = (xp - c)* (xp -c) + (yp -d) * (yp -d )
                    
                    sqrt2 = sqrt( (xp -c) * (xp - c) + (yp -d) * (yp -d) - r1*r1)
                    
                    xt3 = (r1 * r1 * (xp -c) + r1* (yp -d) * sqrt2 ) / denominator2 + c
                    xt4 = (r1 * r1 * (xp -c) - r1* (yp -d) * sqrt2 ) / denominator2 + c
                    
                    yt3 = (r1 * r1 * (yp -d) - r1 * (xp -c) * sqrt2 )/ denominator2 + d
                    yt4 = (r1 * r1 * (yp -d) + r1 * (xp -c) * sqrt2 ) /denominator2 + d
                    
                    draw_SVG_line( (xt1, yt1), (xt3, yt3),  'Line', self.current_layer)
                    draw_SVG_line( (xt2, yt2), (xt4, yt4),  'Line', self.current_layer)
                
if __name__ == '__main__':   
    e = Draw_Tangent()
    e.affect()

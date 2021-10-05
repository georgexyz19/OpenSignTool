#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
draw_arrowhead.py

Copyright June 2018 George Zhang <georgexyz19@gmail.com>
Copyright Sept 2021 George Zhang - updated for Inkscape 1.1

See this link for more infomation
https://inkscapetutorial.org/arrowhead-extension.html

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
'''


import inkex
from inkex import Style, Line, PathElement
from inkex import DirectedLineSegment, Vector2d
from inkex import units
from inkex.paths import Path, Move, Line

import math

class Arrow():
    def __init__(self, L, A, start_type, style_ratio, sty):
        self.L = L
        self.A = A
        self.start_type = start_type
        self.style_ratio = style_ratio
        self.sty = sty
        self.new_sty = Style({'stroke': 'none', 'stroke-width':'0', 
            'fill': sty['stroke']})

    def cal_points(self, lineseg):
        L, A, offset = (self.L, self.A, self.style_ratio)
        line_vec = lineseg.vector
        side_length = L * math.tan(math.radians(A) / 2)
        side_vec1 = Vector2d(-1 * line_vec.y, line_vec.x) / line_vec.length * \
                    side_length
        side_vec2 = Vector2d(line_vec.y, -1 * line_vec.x) / line_vec.length * \
                    side_length
        pt_start = lineseg.start
        pt_on_line = Vector2d(lineseg.point_at_length(L))
        pt_offset = Vector2d(lineseg.point_at_length(L * (1 - offset)))
        pt_side1 = pt_on_line + side_vec1
        pt_side2 = pt_on_line + side_vec2
        return (pt_start, pt_side1, pt_offset, pt_side2)

    def add_arrow(self, lineseg, parent):
        pts = self.cal_points(lineseg)
        elem = self.create_arrow(*pts)
        parent.add(elem)

    def create_arrow(self, point1, point2, point3, point4):
        name = 'arrowhead'
        elem = inkex.PathElement()
        elem.update(**{
            'style': self.new_sty,
            'inkscape:label': name,
            'd': 'M ' + str(point1.x) + ',' + str(point1.y) +
                ' L ' + str(point2.x) + ',' + str(point2.y) +
                ' L ' + str(point3.x) + ',' + str(point3.y) + 
                ' L ' + str(point4.x) + ',' + str(point4.y) + 
                ' z'})
        return elem


class NewPath():
    def __init__(self, pathelem, arrow):
        self.pathelem = pathelem
        self.arrow = arrow
        self.style = pathelem.style.copy()
        self.path = pathelem.path.to_absolute()
        self.start_type = arrow.start_type 

    def line_width(self):
        try:
            line_wid = units.parse_unit(self.style['stroke-width'])[0]
        except:
            line_wid = 0.264583 #self.svg.unittouu('1px') ### no svg
        return line_wid

    def start_end(self):
        path = self.path
        start, end = path[0].args, path[1].args
        if len(end) == 1: # handle H and V
            end = path[1].to_line(path[0]).args
        return (Vector2d(start), Vector2d(end))

    def multi_segments(self):
        start, end = self.start_end()
        line = DirectedLineSegment(start, end)
        start = self.cal_shorten_point(line)
        self.path[0] = Move(start.x, start.y)
        pathelem_new = PathElement.new(self.path)
        pathelem_new.style = self.arrow.sty
        self.pathelem.replace_with(pathelem_new)
        return pathelem_new

    def cal_shorten_point(self, lineseg):
        linewidth = self.line_width()
        A = self.arrow.A
        side_length = linewidth / 2
        offset_length = side_length / math.tan(math.radians(A) / 2)
        offset = offset_length + linewidth
        pt_on_line = Vector2d(lineseg.point_at_length(offset))
        return pt_on_line

    def new_pathelem(self):
        start, end = self.start_end()

        if self.start_type == 'start':
            line = DirectedLineSegment(start, end)
            start = self.cal_shorten_point(line)
            npath = self.new_path(start, end)
            self.pathelem.replace_with(npath)
            return npath
        elif self.start_type == 'end':
            line = DirectedLineSegment(end, start)
            end = self.cal_shorten_point(line)
            npath = self.new_path(start, end)
            self.pathelem.replace_with(npath)
            return npath
        else:
            line = DirectedLineSegment(start, end)
            start_new = self.cal_shorten_point(line)
            line = DirectedLineSegment(end, start)
            end_new = self.cal_shorten_point(line)
            npath = self.new_path(start_new, end_new)
            self.pathelem.replace_with(npath)
            return npath

    def new_arrow(self, parent):
        start, end = self.start_end()
        starttype = self.start_type
        if starttype == 'start' or starttype == 'both':
            line = DirectedLineSegment(start, end)
            self.arrow.add_arrow(line, parent)
        if starttype == 'end' or starttype == 'both':
            line = DirectedLineSegment(end, start)
            self.arrow.add_arrow(line, parent)     

    def new_path(self, start, end):
        # this is similar to draw_SVG_tri, but uses new classes in inkex
        # This code is probably easier to understand
        path = Path()
        path.append([Move(start.x, start.y), Line(end.x, end.y)] )
        pathelem = PathElement.new(path)
        pathelem.style = self.style
        return pathelem


class ArrowHead(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--length', type=float, default=0.0,
                          dest='length', help='length of the arrow head')
        pars.add_argument('--angle', type=float, default=0.0,
                          dest='angle', help='angle of the arrow head')
        pars.add_argument('--type', default='start',
                          dest='start_type', help='start, end, or both')
        pars.add_argument('--style', default='normal',
                          dest='style_type', help='normal or sharp style')

    def effect(self):
        if not self.svg.selected:
            raise inkex.AbortExtension('Please selected a line path element')

        layer = self.svg.get_current_layer()
        sel = self.svg.selection
        sel = sel.filter(PathElement)
        sel = sel.first()  # selected pathelment
        st = sel.style  # style of selected path

        L = self.svg.unittouu(str(self.options.length) + 'px')
        A = self.options.angle
        start_type = self.options.start_type
        style_type = self.options.style_type
        style_ratio = 0.0 if style_type == 'normal' else .25

        arrow = Arrow(L, A, start_type, style_ratio, st)
        newpath = NewPath(sel, arrow)

        # special condition of have more than two segments in path
        if len(newpath.path) > 2:
            newpath.start_type = arrow.start_type = 'start' # override both
            newpath.new_arrow(layer)
            newpath.multi_segments()
            return 

        newpath.new_arrow(layer)
        newpath.new_pathelem()

  
if __name__ == '__main__':
    ArrowHead().run()

#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
# draw_border.py
Draw the border for the SignTool package

Copyright (C) February 2018, June 2018, February 2020 
Copyright October 2021 George Zhang - updated for Inkscape 1.1

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

import math
import inkex
from inkex import Rectangle, Layer, NSS
from inkex import Circle, Line, Vector2d
from inkex import Transform

class DrawBorder(object):
    """"contains drawing methods for both rect, diamond, and bar"""
    def _draw_rect_ri(self, x, y, w, h, r, st):
        elem = Rectangle()

        if r == 0:
            elem.update(**{'x': str(x), 'y': str(y), 
                'width': str(w), 'height': str(h),})
        else:
            elem.update(**{
                'x': str(x), 'y': str(y), 
                'width': str(w), 'height': str(h),
                'rx': str(r), 'ry': str(r) 
                })
        elem.set('style', st)
        return elem

       # easier to write as a class method
    def _draw_mark(self, center, radius, st):
        marks = []
        el = Circle.new(center=center, radius=radius)
        el.style = st
        marks.append(el)

        start = center - Vector2d(radius, 0)
        end = center + Vector2d(radius, 0)
        el_line1 = Line.new(start=start, end=end)
        el_line1.style = st
        marks.append(el_line1)

        start = center - Vector2d(0, radius)
        end = center + Vector2d(0, radius)
        el_line2 = Line.new(start=start, end=end)
        el_line2.style = st
        marks.append(el_line2)

        return marks


# try to design it as unitless
class RectBorder(DrawBorder):
    def __init__(self, w, h, r, offset, bdwidth):
        self.w = w
        self.h = h
        self.r = r
        self.offset = offset
        self.bdwidth = bdwidth

    def draw_borders(self, x, y, st):
        borders = []
        elem_outside = self._draw_rect_ri(x, y, self.w, self.h, self.r, st)
        borders.append(elem_outside)

        if self.offset > 0:
            elem_offset = self._draw_rect_ri(x + self.offset, 
                y + self.offset, 
                self.w - 2 * self.offset, 
                self.h - 2 * self.offset, 
                self.r - self.offset, st)
            borders.append(elem_offset)

        elem_inside = self._draw_rect_ri(x + self.offset + self.bdwidth, 
                y + self.offset + self.bdwidth, 
                self.w - 2 * self.offset - 2 * self.bdwidth, 
                self.h - 2 * self.offset -  2 * self.bdwidth, 
                self.r - self.offset - self.bdwidth, st)
        borders.append(elem_inside)

        return borders

    def draw_corner_marks(self, x, y, radius, st):
        mark1 = self._draw_mark(Vector2d(x, y), radius, st)
        mark2 = self._draw_mark(Vector2d(x + self.w, y), radius, st)
        mark3 = self._draw_mark(Vector2d(x + self.w, y + self.h), radius, st)
        mark4 = self._draw_mark(Vector2d(x, y + self.h), radius, st)

        return mark1 + mark2 + mark3 + mark4


class DiamondBorder(DrawBorder):
    def __init__(self, w, r, offset, bdwidth):
        self.w = w
        self.h = w
        self.r = r
        self.offset = offset
        self.bdwidth = bdwidth  # border width
        
    def draw_borders(self, x, y, st):  # x, y center of canvas
        borders = []

        a = x - self.w / 2
        b = y - self.h / 2  
        elem_outside = self._draw_rect_ri( a, b, 
            self.w, self.h, 
            self.r, st)
        
        trans_str = 'rotate(' + str(45) + ',' + \
                str(x ) + ',' + str(y ) + ') '

        tr =  Transform(trans_str)
        elem_outside.transform = tr
        borders.append(elem_outside)

        if self.offset > 0:
            elem_offset = self._draw_rect_ri(a + self.offset, 
                b + self.offset, 
                self.w - 2 * self.offset, 
                self.h - 2 * self.offset, 
                self.r - self.offset, st)
            elem_offset.transform = tr 
            borders.append(elem_offset)

        elem_inside = self._draw_rect_ri(a + self.offset + self.bdwidth, 
                a + self.offset + self.bdwidth, 
                self.w - 2 * self.offset - 2 * self.bdwidth, 
                self.h - 2 * self.offset -  2 * self.bdwidth, 
                self.r - self.offset - self.bdwidth, st)
        elem_inside.transform = tr 

        borders.append(elem_inside)  # code is similar to rect, how to unit two?

        return borders        

    def draw_corner_marks(self, x, y, side_dist, radius, st): # x, y center of canvas    

        mark1 = self._draw_mark(Vector2d(x, side_dist), radius, st)
        mark2 = self._draw_mark(Vector2d(side_dist, y), radius, st)
        mark3 = self._draw_mark(Vector2d(x * 2 - side_dist, y), radius, st)
        mark4 = self._draw_mark(Vector2d(x, y * 2 - side_dist), radius, st)

        return mark1 + mark2 + mark3 + mark4


class BarBorder(DrawBorder):
    def __init__(self, width, height):
        self.w = width
        self.h = height

    def draw_bar(self, x, y, st):
        bars = []
        elem = self._draw_rect_ri(x, y, self.w, self.h, 0, st)
        bars.append(elem)
        return bars


class SignTool_Border(inkex.EffectExtension):

    def add_arguments(self, pars):
        '''Boilerplate code to handle ui arguments'''
        pars.add_argument("--tab", type=str, dest="active_tab", default="Rectangle")
        pars.add_argument("--width", type=int, dest="width", default="0")
        pars.add_argument("--height", type=int, dest="height", default="0")
        pars.add_argument("--radius", type=float, dest="radius", default="0")
        pars.add_argument("--offset", type=float, dest="offset", default="0")
        pars.add_argument("--bdwidth", type=float, dest="bdwidth", default="0")

        pars.add_argument("--diamond_width", type=int, dest="diamond_width", default="0")
        pars.add_argument("--diamond_radius", type=float, dest="diamond_radius", default="0")
        pars.add_argument("--diamond_offset", type=float, dest="diamond_offset", default="0")
        pars.add_argument("--diamond_bdwidth", type=float, dest="diamond_bdwidth", default="0")

        pars.add_argument("--bar_width", type=int, dest="bar_width", default="0")
        pars.add_argument("--bar_height", type=float, dest="bar_height", default="0")

        pars.add_argument("--changeCanvasSize", type=inkex.Boolean, 
                          dest="changeCanvasSize", default=True)
        pars.add_argument("--bDrawMark", type=inkex.Boolean, dest="bDrawMark", default=False)
        pars.add_argument("--fStrokeWidth", type=float, dest="fStrokeWidth", default="0")


    def effect(self):
        so = self.options

        self.style_stroke = {
            'stroke': '#000000',
            'stroke_width': self.svg.unittouu(str(so.fStrokeWidth) + 'px'),
            'fill': 'none'}

        if so.active_tab == 'rect': # a system extension bug fixed in 1.1
            self.drawRectBorder()
        elif so.active_tab == 'diamond':
            self.drawDiamondBorder()
        elif so.active_tab == 'bar':
            self.drawBar()
        else:
            self.debug('\n\nPlease choose other tabs, \n'
                        'Rect tab draws a rect, \n'
                        'Diamond tab draws a diamond border, \n'
                        'then click apply')

    def _convert_unit(self, value):
        return self.svg.unittouu(str(value) + 'in')

    def _set_page_size(self, page_width, page_height):
        self.svg.set('width', str(page_width) + 'in')
        self.svg.set('height', str(page_height) + 'in')
        ratio = self.svg.unittouu('1in')
        self.svg.set('viewBox', '0 0 ' + str(ratio * page_width) + 
                        ' ' + str(ratio * page_height))

    def drawDiamondBorder(self):
        so = self.options

        (w, r, off, bdw) = map(self._convert_unit, (so.diamond_width, so.diamond_radius, 
                            so.diamond_offset, so.diamond_bdwidth))

        page_width = so.diamond_width * math.cos(math.radians(45)) * 2 + 2 
        page_height = page_width

        if so.changeCanvasSize:

            self._set_page_size(page_width, page_height)

        border = DiamondBorder(w, r, off, bdw)
        elems = border.draw_borders(self._convert_unit(page_width) / 2, 
                                    self._convert_unit(page_height) / 2, self.style_stroke)

        border_layer = self.find_or_create_layer(self.svg, 'diamond_border')
        border_layer.add(*elems)

        if so.bDrawMark:
            elems = border.draw_corner_marks(self._convert_unit(page_width) / 2, 
                self._convert_unit(page_height) / 2, self.svg.unittouu('1in'), 
                self.svg.unittouu('1in'), self.style_stroke)
            border_marks_layer = self.find_or_create_layer(self.svg, 'border_marks')
            border_marks_layer.add(*elems)


    def drawRectBorder(self):
        so = self.options

        (w, h, r, off, bdw) = map(self._convert_unit, 
                    (so.width, so.height, so.radius, so.offset, so.bdwidth))

        if so.changeCanvasSize:
            page_width = so.width + 2 
            page_height = so.height + 2

            self._set_page_size(page_width, page_height)            

        border = RectBorder(w, h, r, off, bdw)
        elems = border.draw_borders(self.svg.unittouu('1in'), self.svg.unittouu('1in'), 
            self.style_stroke)

        border_layer = self.find_or_create_layer(self.svg, 'border')
        border_layer.add(*elems)

        if so.bDrawMark:
            elems = border.draw_corner_marks(self.svg.unittouu('1in'), self.svg.unittouu('1in'), 
                self.svg.unittouu('1in'), self.style_stroke)
            border_marks_layer = self.find_or_create_layer(self.svg, 'border_marks')
            border_marks_layer.add(*elems)
            
   
    def drawBar(self):
        so = self.options
        (width, height) = map(self._convert_unit, (so.bar_width, so.bar_height) )

        bar = BarBorder(width, height)

        style_bd = self.style_stroke

        page_w = self.svg.unittouu(self.svg.get('width'))
        page_h = self.svg.unittouu(self.svg.get('height'))

        elems = bar.draw_bar((page_w - width) / 2, 
                            (page_h - height) / 2, self.style_stroke)

        border_layer = self.find_or_create_layer(self.svg, 'border')
        border_layer.add(*elems)


    def find_or_create_layer(self, svg, name):
        # find an existing layer or create a new layer
        # need import inkex at the beginning of the module
        layer_name = 'Layer %s' % name
        path = '//svg:g[@inkscape:label="%s"]' % layer_name
        elements = svg.xpath(path, namespaces=NSS)
        if elements:
            layer = elements[0]
        else:
            layer = Layer.new(layer_name)
            self.svg.add(layer)
        return layer


if __name__ == '__main__':
    e = SignTool_Border()
    e.run()

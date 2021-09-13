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

import simpletransform
import simplestyle
import math
import sys
import inkex

from inkex import Rectangle, Layer, NSS
from inkex import Circle, Line, Vector2d

def draw_SVG_line(x1, y1, x2, y2, style, name, parent):
    line_style = {'stroke': style['stroke_color'],
                  'stroke-width': str(style['stroke_width']),
                  'fill': style['fill']}
    line_attribs = {'style': simplestyle.formatStyle(line_style),
                    inkex.addNS('label', 'inkscape'): name,
                    'd': 'M ' + str(x1) + ',' + str(y1) + ' L' +
                    str(x2) + ',' + str(y2)}
    elm = inkex.etree.SubElement(
        parent, inkex.addNS('path', 'svg'), line_attribs)
    return elm


def draw_SVG_circle(x, y, radius, style, name, parent):
    circle_style = {'stroke': style['stroke_color'],
                    'stroke-width': str(style['stroke_width']),
                    'fill': style['fill']}
    circle_attribs = {'style': simplestyle.formatStyle(circle_style),
                      inkex.addNS('label', 'inkscape'): name,
                      'cx': str(x), 'cy': str(y),
                      'r': str(radius)}
    elm = inkex.etree.SubElement(
        parent, inkex.addNS('circle', 'svg'), circle_attribs)
    return elm


# def draw_mark(x, y, radius, style, name, parent):
#     draw_SVG_circle(x, y, radius, style, name + 'circle', parent)
#     draw_SVG_line(x - radius, y, x + radius, y, style, name + 'line1', parent)
#     draw_SVG_line(x, y - radius, x, y + radius, style, name + 'line1', parent)

# # draw four corner marks


# def draw_corner_marks(width, height, ra, style_stars, layer_bk):
#     draw_mark(ra, ra, 0.5 * ra, style_stars, 'mark1', layer_bk)
#     draw_mark((width + 1) * ra, ra, 0.5 * ra, style_stars, 'mark2', layer_bk)
#     draw_mark(ra, (height + 1) * ra, 0.5 * ra, style_stars, 'mark3', layer_bk)
#     draw_mark((width + 1) * ra, (height + 1) * ra,
#               0.5 * ra, style_stars, 'mark4', layer_bk)


def draw_outside_marks(width, height, ra, style_stars, layer_bk):
    draw_mark((width/2 + 1) * ra, -0.5 * ra, 0.5 *
              ra, style_stars, 'outmark1', layer_bk)
    draw_mark((width/2 + 1) * ra, (height + 2 + 0.5) * ra,
              0.5 * ra, style_stars, 'outmark2', layer_bk)
    draw_mark(-0.5 * ra, (height / 2 + 1) * ra, 0.5 *
              ra, style_stars, 'outmark2', layer_bk)
    draw_mark((width + 2 + 0.5) * ra, (height / 2 + 1) * ra,
              0.5 * ra, style_stars, 'outmark2', layer_bk)

# draw diamond border four corner marks


def draw_diamond_corner_marks(width, height, ra, style_stars, layer_bk):
    draw_mark(width / 2 * ra, ra, 0.5 * ra, style_stars, 'mark1', layer_bk)
    draw_mark(width / 2 * ra, (height - 1) * ra,
              0.5 * ra, style_stars, 'mark2', layer_bk)
    draw_mark(ra, height / 2 * ra, 0.5 * ra, style_stars, 'mark3', layer_bk)
    draw_mark((width - 1) * ra, height / 2 * ra,
              0.5 * ra, style_stars, 'mark4', layer_bk)


# draw an SVG rectangle with radius
def draw_SVG_rect_ri(x, y, width, height, radius, style, name, parent):
    line_style = {'stroke': style['stroke_color'],
                  'stroke-width': str(style['stroke_width']),
                  'fill': style['fill']}
    rect_ri_attribs = {'style': simplestyle.formatStyle(line_style),
                       'width': str(width), 'height': str(height),
                       'rx': str(radius), 'ry': str(radius),
                       'x': str(x), 'y': str(y),
                       inkex.addNS('label', 'inkscape'): name}
    elm = inkex.etree.SubElement(
        parent, inkex.addNS('rect', 'svg'), rect_ri_attribs)
    return elm


def draw_SVG_rect(x, y, width, height, style, name, parent):
    line_style = {'stroke': style['stroke_color'],
                  'stroke-width': str(style['stroke_width']),
                  'fill': style['fill']}
    rect_ri_attribs = {'style': simplestyle.formatStyle(line_style),
                       'width': str(width), 'height': str(height),
                       'x': str(x), 'y': str(y),
                       inkex.addNS('label', 'inkscape'): name}
    elm = inkex.etree.SubElement(
        parent, inkex.addNS('rect', 'svg'), rect_ri_attribs)
    return elm











# try to design it as unitless
class RectBorder():
    def __init__(self, w, h, r, offset, bdwidth):
        self.w = w
        self.h = h
        self.r = r
        self.offset = offset
        self.bdwidth = bdwidth

    def _draw_rect_ri(self, x, y, w, h, r, st):
        elem = Rectangle()
        elem.update(**{
            'x': str(x), 
            'y': str(y), 
            'width': str(w), 
            'height': str(h),
            'rx': str(r), 
            'ry': str(r) 
        })
        elem.set('style', st)
        return elem

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

    # much easier to write as a class method
    def draw_mark(self, center, radius, st):
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

    def draw_corner_marks(self, x, y, radius, st):
        mark1 = self.draw_mark(Vector2d(x, y), radius, st)
        mark2 = self.draw_mark(Vector2d(x + self.w, y), radius, st)
        mark3 = self.draw_mark(Vector2d(x + self.w, y + self.h), radius, st)
        mark4 = self.draw_mark(Vector2d(x, y + self.h), radius, st)

        return mark1 + mark2 + mark3 + mark4




class SignTool_Border(inkex.EffectExtension):

    def add_arguments(self, pars):
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

        if so.active_tab == 'rect': # an extension bug fixed in 1.1
            self.drawRectBorder()
        elif so.active_tab == 'diamond':
            self.drawDiamondBorder()
        elif so.active_tab == 'bar':
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

        page_width = w * math.cos(math.radians(45)) * 2 + 2
        page_height = page_width

        svg_elem.set('width', str(page_width) + 'in')
        svg_elem.set('height', str(page_height) + 'in')
        svg_elem.set('viewBox', '0 0 ' + str(page_width * ra) + ' '
                     + str(page_height * ra))

        layer_bd = self.createLayer(svg_elem, 'border')

        style_bd = self.style_stroke

        trans_str = 'translate(' + str(page_width / 2 *
                                       ra) + ',' + str(1 * ra) + ') '
        trans_str += 'rotate(' + str(45) + ')'
        trans_mat = simpletransform.parseTransform(trans_str)

        elm = draw_SVG_rect_ri(0, 0, w * ra, h * ra,
                               r * ra, style_bd, 'border_outside', layer_bd)
        simpletransform.applyTransformToNode(trans_mat, elm)

        if off > 0:
            elm = draw_SVG_rect_ri(off * ra, off * ra,
                                   (w-2*off) * ra, (h-2*off) * ra,
                                   (r-off) * ra, style_bd, 'border_offset', layer_bd)
            simpletransform.applyTransformToNode(trans_mat, elm)

        elm = draw_SVG_rect_ri((off+bdw) * ra, (off+bdw) * ra,
                               (w - 2*off - 2 * bdw) * ra,
                               (h - 2*off - 2 * bdw) * ra,
                               (r - off - bdw) * ra, style_bd, 'border_inside', layer_bd)
        simpletransform.applyTransformToNode(trans_mat, elm)

        layer_bk = self.createLayer(svg_elem, 'corner_marks')

        if self.options.bDrawMark:
            draw_diamond_corner_marks(
                page_width, page_height, ra, style_bd, layer_bk)

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
        elm = draw_SVG_rect(self.unittouu(page_w) / 2 - (w / 2) * ra,
                            self.unittouu(page_h) / 2 - (h / 2) * ra,
                            w * ra, h * ra,
                            style_bd, 'bar', layer_bd)




    def drawRectBorder(self):
        so = self.options

        w = self.svg.unittouu(str(so.width) + 'in')  # in inches
        h = self.svg.unittouu(str(so.height) + 'in')
        r = self.svg.unittouu(str(so.radius) + 'in')
        off = self.svg.unittouu(str(so.offset) + 'in')
        bdw = self.svg.unittouu(str(so.bdwidth) + 'in')

        if so.changeCanvasSize:
            page_width = so.width + 2 
            page_height = so.height + 2
            self.svg.set('width', str(page_width) + 'in')
            self.svg.set('height', str(page_height) + 'in')
            ratio = self.svg.unittouu('1in')
            self.svg.set('viewBox', '0 0 ' + str(ratio * page_width) + 
                            ' ' + str(ratio * page_height))


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

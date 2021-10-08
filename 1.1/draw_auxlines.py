"""
# draw_auxlines.py
Draw the auxilary lines for the SignTool package

Copyright (C) February 2018, June 2018 George Zhang
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
This program create auxilary lines on a new layer. 
'''


import re
import inkex
from inkex import NSS, Layer
from inkex import Vector2d, Line, TextElement
from opensigntool_util import find_or_create_layer


class SignTool_AuxLines(inkex.EffectExtension):

    def add_arguments(self, pars):
        pars.add_argument("--dimensions", type=str,
                          dest='dimensions', default='0')
        pars.add_argument("--type", type=str,
                          dest='line_direction', default='horizontal')
        pars.add_argument("--fStrokeWidth", type=float,
                          dest='stroke_width', default='0')

    def effect(self):
        so = self.options
        # need to add code for irregular string input

        str_input = so.dimensions
        lstr = self.verify_str(str_input)

        alignment_layer = find_or_create_layer(self.svg, 'align_lines')
        elems = self.draw_alignment_lines(
            lstr, so.line_direction, so.stroke_width)
        alignment_layer.add(*elems)

    def verify_str(self, str_input):
        str_r = str_input.replace(';', ',')
        str_r = str_r.replace(':', ',')

        # only digits, spaces, ',' and '.' not sub'ed
        str_remove = re.sub(r'[^\d\s,.]', '', str_r)
        str_l = str_remove.split(',')
        strlist = [s.strip() for s in str_l]
        return strlist

    def draw_alignment_lines(self, str_list, line_direction, stroke_width):

        st = {
            'stroke': '#000000',
            'stroke-width': self.svg.unittouu(str(stroke_width) + 'px'),
            'fill': 'none'}

        font_style = {
            'font-size': '0.5in',
            'alignment-baseline': 'middle',
            'text-anchor': 'end'}

        height = self.svg.unittouu('3in')
        offset = self.svg.unittouu('1in')

        elems = []
        if line_direction == 'horizontal':
            elem = self._draw_line(
                Vector2d(offset, -1 * offset), Vector2d(offset, -1 * height - offset), st)
        else:
            elem = self._draw_line(
                Vector2d(-1 * offset, offset), Vector2d(-1 * height - offset, offset), st)
        elems.append(elem)

        # use 1 inch offset, this is global setting
        start = offset
        end = offset

        for width in str_list:
            iwidth = self.svg.unittouu(width+'in')
            end = end + iwidth
            if line_direction == 'horizontal':
                el1 = self._draw_line(
                    Vector2d(end, -1 * offset), Vector2d(end, -1 * height - offset), st)
                el2 = self._draw_line(Vector2d(start, -2 * height/3 - offset),
                                      Vector2d(end, -2 * height/3 - offset), st)

                font_style_h = font_style.copy()
                font_style_h.update({'text-anchor': 'middle'})
                tel = self._place_text(width + ' in', start / 2 + end / 2,
                                       -2 * height/3 - offset - offset / 2,
                                       font_style_h)
                elems.extend([el1, el2, tel])
            else:
                el1 = self._draw_line(
                    Vector2d(-1 * offset, end), Vector2d(-1 * height - offset, end), st)
                el2 = self._draw_line(Vector2d(-1 * height*2 / 3 - offset, start),
                                      Vector2d(-1 * height * 2/3 - offset, end), st)
                tel = self._place_text(width + ' in', -1 * height*2 / 3 - offset - offset/2,
                                       start/2 + end / 2 +
                                       self.svg.unittouu('0.718in'),
                                       font_style)
                elems.extend([el1, el2, tel])
            start = start + iwidth

        return elems

    def _place_text(self, msg, x, y, st):
        tel = TextElement()
        tel.text = msg
        tel.set('x', str(x))
        tel.set('y', str(y))
        tel.set('style', st)
        return tel

    def _draw_line(self, v1, v2, st):
        el = Line.new(start=(v1.x, v1.y), end=(v2.x, v2.y))
        el.style = st
        return el


if __name__ == '__main__':
    e = SignTool_AuxLines()
    e.run()

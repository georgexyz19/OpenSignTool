'''
draw_signarrow.py
The program to draw arrows shown on 2004 Standard Sign Book P6-2

Copyright June 2018 George Zhang <georgexyz19@gmail.com>
Copyright Sept 2021 George Zhang - updated for Inkscape 1.1

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


import math

from inkex import EffectExtension, TextElement, Style, Path
from inkex import PathElement, Transform, Layer, NSS

from util import find_or_create_layer


tb = [['2', '2.313', '4.313', '0.313', '0.375'],
      ['2.25', '2.625', '4.5', '0.375', '0.438'],
      ['2.5', '2.875', '5.063', '0.375', '0.5'],
      ['2.625', '3', '5.25', '0.375', '0.5'],
      ['2.75', '3', '5.563', '0.438', '0.563'],
      ['3', '3.5', '6.125', '0.438', '0.563'],
      ['3.125', '3.625', '6.375', '0.5', '0.625'],
      ['3.25', '3.75', '6.625', '0.5', '0.625'],
      ['3.313', '3.813', '6.688', '0.5', '0.688'],
      ['3.5', '4', '7.125', '0.563', '0.688'],
      ['3.75', '4.313', '7.625', '0.563', '0.75'],
      ['4', '4.625', '8.125', '0.625', '0.813'],
      ['4.063', '4.75', '8.25', '0.625', '0.813'],
      ['4.25', '4.875', '8.625', '0.625', '0.813'],
      ['4.375', '5', '8.875', '0.688', '0.875'],
      ['4.5', '5.188', '9.125', '0.688', '0.875'],
      ['4.75', '5.438', '9.625', '0.75', '1'],
      ['4.875', '5.625', '9.875', '0.75', '1'],
      ['5', '5.75', '10.125', '0.75', '1'],
      ['5.25', '6', '10.625', '0.813', '1.063'],
      ['5.5', '6.375', '11.125', '0.875', '1.125'],
      ['5.75', '6.625', '11.688', '0.875', '1.125'],
      ['6', '6.875', '12.188', '0.938', '1.188'],
      ['6.5', '7.5', '13.188', '1', '1.625'],
      ['7', '8', '14.188', '1.063', '1.375'],
      ['7.5', '8.625', '15.188', '1.125', '1.5'],
      ['8', '9.188', '16.25', '1.25', '1.625'],
      ]


class SignTool_Arrow(EffectExtension):

    def effect(self):

        layer = find_or_create_layer(self.svg, 'arrows')
        style = {
            'stroke': '#000000',
            'stroke-width': self.svg.unittouu('1px'),
            'fill': 'none'}

        font_style = {
            'font-size': '0.5in',
            'alignment-baseline': 'middle',
            'text-anchor': 'center'}

        ratio = self.svg.unittouu('1in')

        dy = 0
        for r in tb:
            r0, r1, r2, r3, r4 = (float(r[0]), float(
                r[1]), float(r[2]), float(r[3]), float(r[4]))
            dy += ratio * r0 / 2 + 2 * ratio * r1
            self.draw_SVG_arrow(0, dy, r0, r1, r2, r3,
                                r4, style, layer)
            self.place_text('A=' + str(r0), 0, dy, font_style, layer)

    def place_text(self, msg, x, y, st, parent):
        text = TextElement()
        text.text = msg
        text.set('x', str(x))
        text.set('y', str(y))
        text.set('style', Style(st))
        parent.append(text)


    def draw_SVG_arrow(self, x, y, A, B, C, D, E, st, parent):

        ratio = self.svg.unittouu('1in')
        A, B, C, D, E = (A*ratio, B*ratio, C*ratio, D*ratio, E*ratio)

        a = math.atan2(B, C)
        b = math.atan(math.sqrt(B * B + C * C - E * E) / E) - a
        c = math.atan2(B, D + E)
        d = math.radians(270 - math.degrees(c))

        k = (B + E * math.sin(d)) / (A + E * math.cos(d) - (A + D))
        b0 = -1 * k * (A + D)  # note to revise the equation
        x0 = (A / 2 - b0) / k  # b should be b0
        y0 = A / 2

        line_style = st
        pathd = 'M %s %s ' % (0, 0)
        pathd += 'L %s %s ' % (0, A / 2)
        pathd += 'L %s %s ' % (x0, y0)
        pathd += 'L %s %s ' % (A + E * math.cos(d), B + E * math.sin(d))
        pathd += 'A %s %s %s %s %s %s %s ' % (E, E, 0,
                          0, 0, A + E * math.cos(b), B + E * math.sin(b))

        pathd += 'L %s %s ' % (A + C, 0)

        pathd += 'L %s %s ' % (A + E * math.cos(b), -1 * (B + E * math.sin(b)))
        pathd += 'A %s %s %s %s %s %s %s ' % (
            E, E, 0, 0, 0, A + E * math.cos(d), -1 * (B + E * math.sin(d)))
        pathd += 'L %s %s ' % (x0, -1 * y0)
        pathd += 'L %s %s ' % (0, -1 * A / 2)

        pathd += 'Z'

        path = Path(pathd)
        pel = PathElement.new(path)

        pel.set('style', Style(line_style))
        pel.set('transform', Transform(f'translate({x}, {y})'))
        parent.add(pel)


if __name__ == '__main__':
    e = SignTool_Arrow()
    e.run()

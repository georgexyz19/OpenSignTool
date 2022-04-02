"""
# place_message.py
Place a line of message on the drawing

Copyright (C) February 2018, June 2018, February 2020 George Zhang
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


import inkex
import copy
from place_message_tb import *
import re
import gzip

from inkex import Rectangle
from inkex import Group, addNS
from inkex import Transform, Style

from opensigntool_util import find_or_create_layer
from inkex.elements._base import load_svg

# import logging
# logging.basicConfig(filename='/home/george/Desktop/new-logging.txt', 
#     filemode='w', format='%(levelname)s: %(message)s', level=logging.DEBUG)



# import simpletransform
# import simplestyle


def table(s):
    if s.strip().upper() == 'B':
        return table_B
    elif s.strip().upper() == 'C':
        return table_C
    elif s.strip().upper() == 'D':
        return table_D
    elif s.strip().upper() == 'E':
        return table_E
    elif s.strip().upper() == 'F':
        return table_F
    elif s.strip().upper() == 'EM':
        return table_EM


def downtb(s):
    if s.strip().upper() == 'B':
        return downtb_B
    elif s.strip().upper() == 'C':
        return downtb_C
    elif s.strip().upper() == 'D':
        return downtb_D
    elif s.strip().upper() == 'E':
        return downtb_E
    elif s.strip().upper() == 'F':
        return downtb_F
    elif s.strip().upper() == 'EM':
        return downtb_EM


class LoadLetter(inkex.InputExtension):

    def __init__(self, str_etree=None):
        super().__init__()
        self.document = self.load(str_etree)

    def load(self, stream):
        """Load the stream as an svg xml etree"""
        document = load_svg(stream)
        self.svg = document.getroot()
        return document

    def effect(self):
        """Effect isn't needed for a lot of Input extensions"""
        return NotImplemented('effect method should not be called')


class SignToolMessage(inkex.EffectExtension):
    # def __init__(self):
        # inkex.Effect.__init__(self)

        # self.OptionParser.add_option("--message", action="store",
        #                              type="string", dest="message", default="")
        # self.OptionParser.add_option("--fontsize", action="store",
        #                              type="string", dest="fontsize",
        #                              default="", help="Font Size of B,C,D,E,EM,F")
        # self.OptionParser.add_option("--fontheight", action="store",
        #                              type="float", dest="fontheight", default="0")
        # self.OptionParser.add_option("--dist_to_top", action="store",
        #                              type="float", dest="dist_to_top", default="0")
        # self.OptionParser.add_option("--bDrawBox", action="store",
        #                              type="inkbool", dest="bDrawBox", default=False)

    def __init__(self):
        super().__init__()

        # load sign_letters 

        # very basic protection agaist people messing with letter
        with gzip.open('sign_letters', 'rb') as f:
            str_etree = f.read()

        letter = LoadLetter(str_etree)
        # letter.add_arguments()
        # letter.load(str_etree)

        self.letter_svg = letter.svg

        # svg = letter.svg     
        # for e in svg.getiterator():
        #     # out id info
        #     attr = e.attrib
        #     idattr = attr.get('id', 'none')
        #     # logging.debug(f'e.id is { idattr }') ## now I can load a letter
        #     # logging.debug(f'e.id is { idattr }') ## now I can load a letter

        # elem = letter.svg.getElementById('E66')
        # logging.debug(f'{elem}')

        # logging.debug(f'{elem.bounding_box()}')

        # # groot, gidmap = inkex.etree.XMLID(str_etree)
        # # self.groot = groot
        # # self.gidmap = gidmap

    def add_arguments(self, pars):
      
        pars.add_argument('--message', type=str, dest='message', default='0')
        pars.add_argument('--fontsize', type=str, dest='fontsize', default='0')
        pars.add_argument('--fontheight', type=float, dest='fontheight', default='0')
        pars.add_argument('--dist_to_top', type=float, dest='dist_to_top', default='0')
        pars.add_argument('--bdraw_box', type=inkex.Boolean, dest='bdraw_box', default=False)


    def effect(self):

        so = self.options
        # logging.debug(f'so is {so}')
        # self.unittouu = self.svg.unittouu

        fontheight = self.svg.unittouu(str(so.fontheight)+'in')
        message = so.message
        fontsize = so.fontsize  # et 'E'
        dist_to_top = self.svg.unittouu(str(so.dist_to_top + 1)+'in')
        self.fontsize = fontsize  # this needs to be dealt with

        layer = find_or_create_layer(self.svg, 'messages')
        group = self.create_group(layer, message)  # group at center of page
        layer.add(group)

        msg_width = self.message_width(message, fontsize, fontheight)
        doc_width = self.svg.width # unittouu(self.getDocumentWidth())

        # logging.debug(f'msg widht is {msg_width}')
        # logging.debug(f'doc width is {doc_width}')


        self.draw_message(message, fontsize, fontheight, doc_width / 2 -
                          msg_width / 2, dist_to_top, group)

    def create_group(self, parent, group_name):
        group = Group()
        group.set(addNS('label', 'inkscape'), group_name)
        return group

    # return an element of a character
    def get_char(self, letter):
        if letter == 'cent':
            id = self.fontsize + 'cent'
            elem = self.letter_svg.getElementById(id)               # self.gidmap[id]
            return elem
        else:
            code = ord(letter)
            id = self.fontsize + str(code)
            elem = self.letter_svg.getElementById(id)         #self.gidmap[id]
            return elem

    def get_box(self, elem, transform=None):
        #elem = self.get_char(letter)
        bbox = elem.bounding_box(transform=transform)
        return (bbox.left, bbox.right, bbox.top, bbox.bottom )

    def remove_id(self, d, key):
        if key in d:
            del d[key]
        return d

    # is upper case or is a number, those align vertical center
    # or is one of the eleven characters &!#()@?$-=+
    def is_align_center(self, letter):
        if letter.isupper() or (letter in "0123456789") or (letter in "&!#()@?$-=+:"):
            return True
        else:
            return False

    def parse_message(self, message):
        if not message:
            return
        message = message.strip()
        message = re.sub(' +', ' ', message)  # combine multiple space into 1

        message_list = []
        char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890&!"#$*.,:()-@=+?'

        i = 0
        while i < len(message):
            if message[i] in char_set:
                message_list.append(('letter', message[i]))
            elif message[i] == ' ':
                message_list.append(('space', ' '))
            elif message[i] == '/':
                message_list.pop()
                message_list.append(('fraction', message[i-1: i+2]))
                i = i + 1
            elif message[i] == '|':
                j = i+1
                while j < len(message):
                    if message[j] == '|':
                        message_list.append(('distance', message[i+1:j]))
                        i = j
                        break
                    j = j + 1
            elif message[i] == '\\':
                j = i+1
                while j < len(message):
                    if message[j] == '\\':
                        message_list.append(('cent', message[i+1:j]))
                        i = j
                        break
                    j = j + 1

            i = i + 1
        return message_list

    def draw_message(self, message, fontsize, fontheight, xleft_in, ytop_in, parent):
        msg_list = self.parse_message(message)

        xleft = xleft_in
        ytop = ytop_in
        bfirst = True
        i = 0
        while i < len(msg_list):

            le = msg_list[i]
            if le[0] == 'letter':
                (le_left, le_width, le_right) = self.letter_size(
                    le[1], fontsize, fontheight)

                if bfirst:
                    le_left = 0
                    bfirst = False

                xleft = xleft + le_left
                self.draw_letter(
                    le[1], fontsize, fontheight, xleft, ytop, parent)
                xleft = xleft + le_width + le_right

            elif le[0] == 'space':
                if msg_list[i-1][0] == 'letter' and msg_list[i+1][0] == 'letter':
                    xleft = xleft + self.space_width(fontsize, fontheight,
                                                     msg_list[i-1][1], msg_list[i+1][1])
                else:               # / left right are zero, x has strange results
                    xleft = xleft + \
                        self.space_width(fontsize, fontheight, '/', '/')

            elif le[0] == 'fraction':
                self.draw_fraction(
                    le[1], fontsize, fontheight, xleft, ytop, parent)
                xleft = xleft + \
                    self.fraction_width(le[1], fontsize, fontheight)

            elif le[0] == 'distance':
                if msg_list[i-1][0] == 'letter' and msg_list[i+1][0] == 'letter':
                    xleft = xleft + \
                        self.distance_width(
                            le[1], fontsize, fontheight, msg_list[i-1][1], msg_list[i+1][1])
                else:
                    xleft = xleft + \
                        self.distance_width(
                            le[1], fontsize, fontheight, '/', '/')

            elif le[0] == 'cent':
                (le_left, le_width, le_right) = self.letter_size(
                    'cent', fontsize, fontheight)

                if bfirst:
                    le_left = 0
                    bfirst = False

                xleft = xleft + le_left
                self.draw_letter('cent', fontsize, fontheight,
                                 xleft, ytop, parent)
                xleft = xleft + le_width + le_right

            i = i + 1

    def message_width(self, message, fontsize, fontheight):
        msg_list = self.parse_message(message)

        xleft = 0  # xleft_in
        #ytop = ytop_in
        bfirst = True
        i = 0
        (le_left, le_width, le_right) = (0, 0, 0)
        while i < len(msg_list):

            le = msg_list[i]
            if le[0] == 'letter':
                (le_left, le_width, le_right) = self.letter_size(
                    le[1], fontsize, fontheight)

                if bfirst:
                    le_left = 0
                    bfirst = False

                xleft = xleft + le_left + le_width + le_right
                #self.draw_letter(le[1], fontsize, fontheight, xleft, ytop, parent)
                #xleft = xleft + le_width + le_right

            elif le[0] == 'space':
                if msg_list[i-1][0] == 'letter' and msg_list[i+1][0] == 'letter':
                    xleft = xleft + self.space_width(fontsize, fontheight,
                                                     msg_list[i-1][1], msg_list[i+1][1])
                else:               # / left right are zero, x has strange results
                    xleft = xleft + \
                        self.space_width(fontsize, fontheight, '/', '/')

            elif le[0] == 'fraction':
                #self.draw_fraction(le[1] ,fontsize, fontheight, xleft, ytop, parent)
                xleft = xleft + \
                    self.fraction_width(le[1], fontsize, fontheight)

            elif le[0] == 'distance':
                if msg_list[i-1][0] == 'letter' and msg_list[i+1][0] == 'letter':
                    xleft = xleft + self.distance_width(le[1], fontsize, fontheight,
                                                        msg_list[i-1][1], msg_list[i+1][1])
                else:
                    xleft = xleft + \
                        self.distance_width(
                            le[1], fontsize, fontheight, '/', '/')

            elif le[0] == 'cent':
                (le_left, le_width, le_right) = self.letter_size(
                    'cent', fontsize, fontheight)

                if bfirst:
                    le_left = 0
                    bfirst = False

                xleft = xleft + le_left + le_width + le_right
                #self.draw_letter('cent', fontsize, fontheight, xleft, ytop, parent)
                #xleft = xleft + le_width + le_right

            i = i + 1

        width = xleft - le_right
        return width

    def fraction_width(self, message, fontsize, fontheight):

        space_ratio = {'B': 0.65, 'C': 0.75, 'D': 0.85,
                       'E': 1.0, 'EM': 1.0, 'F': 1.15}

        whole_width = fontheight * 1.5 * 7 / 6 * space_ratio[fontsize] / 0.85

        if message[0] != '1':
            whole_width = fontheight * 1.5 * 8 / 6

        return whole_width

    # draw fractions, message in the format of 1/2 2/3
    # width is 7/6 of height
    def draw_fraction(self, message, fontsize, fontheight, xleft, ytop, parent):
        if len(message) != 3 and message[1] != '/':
            return

        whole_width = self.fraction_width(message, fontsize, fontheight)

        # draw numerator
        ytop_n = ytop - fontheight / 4.0
        self.draw_letter(message[0], fontsize,
                         fontheight, xleft, ytop_n, parent)

        # draw slash
        space_width = whole_width - self.letter_size(message[0], fontsize, fontheight)[1] - \
            self.letter_size(message[2], fontsize, fontheight)[1]
        xleft_slash = xleft + self.letter_size(message[0], fontsize, fontheight)[1] + \
            space_width * 9 / 16 - \
            self.letter_size(message[1], fontsize, fontheight)[1] / 2

        if message[2] == '4':
            xleft_slash = xleft_slash + space_width * 2 / 16

        ytop_slash = ytop_n + fontheight / 2.0
        self.draw_letter(message[1], fontsize, fontheight,
                         xleft_slash, ytop_slash, parent)

        # draw denominator
        xleft_d = xleft + whole_width - \
            self.letter_size(message[2], fontsize, fontheight)[1]
        ytop_d = ytop + fontheight / 4.0
        self.draw_letter(message[2], fontsize,
                         fontheight, xleft_d, ytop_d, parent)


    def distance_width(self, distance, fontsize, fontheight, prev_letter, next_letter):
        d_width = self.unittouu(distance + 'in')
        prev_letter_r = self.letter_size(prev_letter, fontsize, fontheight)[2]
        next_letter_l = self.letter_size(next_letter, fontsize, fontheight)[0]
        d_width = d_width - prev_letter_r - next_letter_l
        return d_width

    # do not support 2 spaces together
    def space_width(self, fontsize, fontheight, prev_letter, next_letter):
        space_ratio = {'B': 0.65, 'C': 0.75, 'D': 0.85,
                       'E': 1.0, 'EM': 1.0, 'F': 1.15}
        space_width = fontheight * 3.0 / 4.0 * space_ratio[fontsize]
        prev_letter_r = self.letter_size(prev_letter, fontsize, fontheight)[2]
        next_letter_l = self.letter_size(next_letter, fontsize, fontheight)[0]
        space_w = space_width - prev_letter_r - next_letter_l
        return space_w

    # letter size in the table (assume 4 inch letter) font size ABCD
    def letter_size(self, letter, fontsize, fontheight):
        ratio = fontheight * 1/4  # table values are in 4 inch letter height
        left = table(fontsize)[letter][0] * ratio  # fontsize BCDEEMF
        w_letter = table(fontsize)[letter][1] * ratio
        right = table(fontsize)[letter][2] * ratio
        return (left, w_letter, right)

    # ytop is top of the letter to top sign edge
    def draw_letter(self, letter, fontsize, fontheight, xleft, ytop, parent):

        elem = copy.deepcopy(self.get_char(letter))

        new_id = self.svg.get_unique_id(prefix='id')   # self.uniqueId(elem.attrib['id'])

        # new_id = self.uniqueId(elem.attrib['id'])
        elem.attrib['id'] = new_id

        bbox = self.get_box(elem)  # returns xmin, xmax, ymin, and ymax

        # logging.debug(f'bbox is {bbox}')

        l_width = bbox[1] - bbox[0]
        l_height = bbox[3] - bbox[2]

        left = self.letter_size(letter, fontsize, fontheight)[0]
        w_letter = self.letter_size(letter, fontsize, fontheight)[1]
        right = self.letter_size(letter, fontsize, fontheight)[2]

        # xleft, ytop, w_letter, fontheight is the box size
        # logging.debug(f'bdraw_box is {self.options.bdraw_box}')

        if self.options.bdraw_box:

            st = {
            'stroke': '#000000',
            'stroke-width': self.svg.unittouu('3px'),
            'fill': 'none'}

            e1 = self._draw_rect(xleft, ytop, w_letter,
                               fontheight, st, letter)
            parent.add(e1)  ## added
 
        l_ratio = w_letter / l_width

        # logging.debug(f'l_ratio is {l_ratio}')  ###

        # scale elem to fontheight inch size
        t1 = 'scale(' + str(l_ratio) + ')'

        trans1 = Transform(t1)

        # m1 = simpletransform.parseTransform(t1)
        # simpletransform.applyTransformToNode(m1, elem)

        if letter in 'gjpqy",*abcdeosuQ':   # one of the eight characters has down
            down = downtb(fontsize)[letter]
        else:
            down = 0
        down = down * fontheight / 2  # down units is in 2 inch letters

        bbox = self.get_box(elem, trans1)  ## apply to elem 

        # logging.debug(f'bbox is {bbox}')


        if not self.is_align_center(letter):  # lowcase align bottom
            t2 = 'translate(' + \
                str(xleft + w_letter / 2 - (bbox[0] + bbox[1])/2) + ',' + \
                str(ytop + fontheight - bbox[3] + down) + ')'
        else:
            t2 = 'translate(' + \
                str(xleft + w_letter / 2 - (bbox[0] + bbox[1])/2) + ',' + \
                str(ytop + fontheight/2 - (bbox[2] + bbox[3])/2 + down) + ')'

        trans2 = Transform(t2)
        elem.transform = trans2 * trans1    # this is quite tricky  
        # m2 = simpletransform.parseTransform(t2)
        # simpletransform.applyTransformToNode(m2, elem)

        parent.append(elem)

    def _draw_rect(self, x, y, width, height, st, name):
        el = Rectangle.new(x, y, width, height)
        el.style = st
        el.set(addNS('label', 'inkscape'), name)
        return el


if __name__ == '__main__':
    e = SignToolMessage()
    e.run()



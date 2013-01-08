# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004 by Jaroslav Benkovsky, <edheldil@users.sf.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sys

try:
    import PIL
except:
    pass

import image


class ImageSequence (image.Image):

    def __init__ (self):
        image.Image.__init__ (self)


    def get_frame_lol (self):
        """Return list of lists of frames"""
        return [[]]

    def frame_to_image (self, obj):
        raise UnimplementedError()


    def to_image (self, obj=None):
        if obj:
            return self.frame_to_image(obj)

        lol = self.get_frame_lol()
        frame_list = sum (lol, [])
        ncols = 16

        nrows = (len (frame_list) + ncols - 1) / ncols
        bbox = self.get_hmin_bbox(frame_list)
        #print 'bbox', bbox
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        
        pad = 2
        font_start = 1
        
        self.width = w = ncols * (cw + pad)
        self.height = h = nrows * (ch + pad)
        #print 'cw', cw, 'ch', ch, 'w', w, 'h', h

        im = PIL.Image.new ('RGB', (w, h), 0xffffff)
        #imf = self.get_image (frame_list[5])
        #im.paste (imf, (0, 0))
        self.image = im

        for i in range (1, ncols):
            x = i * (cw + pad)
            for j in range (h):
                if j % 2:
                    im.putpixel ((x, j), 0x0000ff)

        for i in range (1, nrows):
            y = i * (ch + pad)
            for j in range (w):
                if j % 2:
                    im.putpixel ((j, y), 0xff0000)


        for n, obj in enumerate(frame_list):
            imf = self.get_image (obj)
            n += font_start
            nc = n % ncols
            nr = n / ncols
            dx = nc * (cw + pad) + pad/2 + (cw-imf.size[0])/2
            dy = nr * (ch + pad) + pad/2 - bbox[1]- imf.y

            im.paste (self.get_image (obj), (dx, dy))

        return im

        data = [ '\xff\xff\xff\xff' ] * w * h

        for i in range (1, ncols):
            x = i * (cw + pad)
            for j in range (h):
                ndx = j * w + x
                if j % 2:
                    data[ndx] = '\xff\x00\x00\xff'

        for i in range (1, nrows):
            y = i * (ch + pad)
            for j in range (w):
                ndx = y * w + j
                if j % 2:
                    data[ndx] = '\xff\x00\x00\xff'

        for n, obj in enumerate(frame_list):
            n += font_start
            nc = n % ncols
            nr = n / ncols
            dx = nc * (cw + pad) + pad/2 + (cw-obj['width'])/2
            dy = nr * (ch + pad) + pad/2 - bbox[1]- obj['y']
            for i in range (obj['height']):
                for j in range (obj['width']):
                    p = self.get_pixel (j, i, obj)
                    nx = dx + j
                    ny = dy + i
                    ndx = ny * w + nx
                    if p[3] >= 128:
                        data[ndx] = '%c%c%c\xff' %(p[0], p[1], p[2])

        self.pixels = ''.join(data)


    # FIXME: select only a cycle or specific frames
    def get_max_bbox (self, frames):
        """Returns bounding box enclosing all frames, including their anchors"""
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        
        for obj in frames:
            x1 = min (x1, - obj['x'])
            y1 = min (y1, - obj['y'])
            x2 = max (x2, obj['width'] - obj['x'])
            y2 = max (y2, obj['height'] - obj['y'])

        return (x1, y1, x2, y2)


    def get_min_bbox (self, frames):
        """Returns bounding box enclosing all frames, ignoring their anchors"""
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        
        for obj in frames:
            x2 = max (x2, obj['width'])
            y2 = max (y2, obj['height'])

        return (x1, y1, x2, y2)


    def get_hmin_bbox (self, frames):
        """Returns bounding box enclosing all frames, ignoring x-component
        of their anchors. This is suitable for displaying fonts."""
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        
        for obj in frames:
            img = self.get_image (obj)
            y1 = min (y1, - img.y)
            x2 = max (x2, img.size[0])
            y2 = max (y2, img.size[1] - img.y)

        return (x1, y1, x2, y2)

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
from __future__ import print_function
import sys

try:
    import PIL.Image
except:
    pass

class Image (object):

    def __init__ (self):
        #super (Image, self).__init__(self)
        object.__init__ (self)
        self.image = None


    def to_image (self, obj=None):
        if obj:
            w = obj['width']
            h = obj['height']
            pixels = obj['pixels']
        else:
            try:
                w = self.width
                h = self.height
            except AttributeError:
                w = self.header['width']
                h = self.header['height']

            try:
                pixels = self.pixels
            except AttributeError:
                pixels = self.header['pixels']

        img = PIL.Image.fromstring ('RGBA', (w, h), pixels, "raw", 'RGBA', 0, 1)

        if obj:
            obj['image'] = img
        else:
            self.image = img

        return img
        

    def get_image (self, obj=None):
        img = None
        if obj:
            if not 'image' in obj:
                self.to_image(obj)
            img = obj['image']

        else:
            if not self.image:
                self.to_image()
            img = self.image

        return img


#    def get_pixel (self, x, y, obj=None):
#        if obj:
#            w = obj['width']
#            h = obj['height']
#            pixels = obj['pixels']
#        else:
#            w = self.width
#            h = self.height
#            pixels = self.pixels
#        
#        ndx = 4 * (y * w + x)
#        return [ ord(p) for p in pixels[ndx:ndx+4] ]
#
#        
    def print_bitmap (self, obj=None):
        img = self.get_image(obj)
        gray = ' #*+:.'
        grsz = len (gray) - 1

        w = img.size[0]
        h = img.size[1]
        pixels = img.tostring()
        
        for ndx in range (h*w):
            r = ord(pixels[4*ndx])
            g = ord(pixels[4*ndx+1])
            b = ord(pixels[4*ndx+2])
            a = ord(pixels[4*ndx+3])
                
            if a < 128:
                gr = 0
            else:
                gr = 1 + (r + g + b) / (3 * (255 / grsz))
                if gr >= grsz:
                    gr = grsz - 1
            sys.stdout.write (gray[gr])
            if (ndx+1) % w == 0:
                sys.stdout.write ("\n")

#
#    def read_frame_ppm (self,  fh):
#        line = fh.readline ()
#        if line != 'P6\n':
#            print "Not PNM P6 header"
#            return None
#            
#        line = fh.readline ()
#        while line.startswith ('#'):
#            line = fh.readline ()
#        
#        try:
#            width,  height = map (int, line.split(" "))
#        except e:
#            print "Not PNM"
#            return None
#            
#        buf = fh.read ()
#        print len(buf)
#        ndx = 0
#        for i in range (height):
#            for j in range (width):
#                print buf[ndx],  buf[ndx+1],  buf[ndx+2]
#                r,  g,  b = map (int, (buf[ndx],  buf[ndx+1],  buf[ndx+2]))
#                print r,  g,  b
#                
#                ndx += 3
#    
#    
#    def write_frame_ppm (self, fh,  obj):
#        fh.write ("P6\n")
#        fh.write ("# ie_shell BAM frame %d %d\n" %(obj['xcenter'], obj['ycenter']));
#        #fh.write ("# ie_shell BAM2 frame %d %d\n" %(obj['xcenter'], obj['ycenter']));
#        
#        fh.write ("%d %d\n" %(obj['width'], obj['height']));
#        fh.write ("255\n");
#
#        ndx = 0
#        for i in range (obj['height']):
#            for j in range (obj['width']):
#                pix = obj['frame_data'][ndx]
#                #if pix == transparent_color:
#                #   .....
#                
#                col= self.palette_entry_list[pix]
#                fh.write ('%c%c%c' %(col['r'], col['g'], col['b']))
#                ndx = ndx + 1


    
    def view (self, obj=None):
        img = self.get_image(obj)
            
        if img:
            img.show ()
        else:
            print("Image could not be created", file=sys.stderr)

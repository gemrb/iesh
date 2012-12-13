#!/usr/bin/env python
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2012 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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

"""Combine several image files to a single BAM image, as specified by a project file.

Example project file:

# frame <name> <compressed color> <x> <y> <filename>
frame f0 0 0 0 images/cursor1.bmp
frame f1 0 5 5 images/cursor2.bmp

# cycle <name> <frame>  [<frame> ...]
cycle c0 f0 f1

"""

import sys
import PIL.Image as pi

import re

from infinity.formats import bam
from infinity import stream


class BAMComposer (object):
	frame_re = re.compile (r'^frame\s+([A-Za-z_][A-Za-z0-9_.-]*)\s+(\d+)\s+([+-]?\d+)\s+([+-]?\d+)\s+(.*)')
	cycle_re = re.compile (r'^cycle\s+([A-Za-z_][A-Za-z0-9_.-]*)((\s+[A-Za-z_][A-Za-z0-9_.-]*)+)')

	def __init__ (self):
		self.frame_lines = []
		self.cycle_lines = []

		self.names = {}
		self.colors = {}
		self.palette = [ {'r': 0, 'g': 255, 'b': 0, 'a': 0} ]
		self.color_ndx = 1

	
	def get_color (self, r, g, b):
		"""Allocate RGB color in a palette and return its color index"""

		try:
			c = self.colors[(r,g,b)]
		except KeyError:
			self.colors[(r, g, b)] = c = [self.color_ndx, 0]
			self.palette.append ({ 'r': r, 'g': g, 'b': b, 'a': 0 })
			self.color_ndx += 1

			if self.color_ndx > 256:
				raise RuntimeError ("Too many colors")

		c[1] += 1
		return c[0]


	def read_project (self, filename):
		"""Read project file"""
		fh = open (filename)

		while True:
			line = fh.readline ()

			if line == '':
				break
			
			line = line.strip()
			if line == '' or line[0] == '#':
				continue

			mo = self.frame_re.match (line)
			if mo:
				self.names[mo.group(1)] = len (self.frame_lines)
				self.frame_lines.append ((mo.group(1), int(mo.group(2)), int(mo.group(3)), int(mo.group(4)), mo.group(5)))

			mo = self.cycle_re.match (line)
			if mo:
				# FIXME: name is not used yet
				#self.names[mo.group(1)] = len (self.cycle_lines)
				fnames = re.split (r'\s+', mo.group(2).strip())
				self.cycle_lines.append ((mo.group(1), fnames))

		fh.close ()


	def create_bam (self):
		"""Create a new BAM object and add to it frames and cycles"""

		b = bam.BAM_Format()

		for f in self.frame_lines:
			frame = self.create_frame (f[4], f[1], f[2], f[3])
			b.frame_list.append (frame)
		
		for c in self.cycle_lines:
			cycle = self.create_cycle(c[1])
			b.cycle_list.append (cycle)

		b.palette_entry_list = self.palette

		b.header = h = {}
		h['signature'] = 'BAM '
		h['version'] = 'V1  '
		h['frame_cnt'] = len (b.frame_list)
		h['cycle_cnt'] = len (b.cycle_list)
		h['comp_color_ndx'] = 0
		h['frame_off'] = 0
		h['palette_off'] = 0
		h['frame_lut_off'] = 0

		return b


	def create_frame (self, filename, transparent, x, y):
		"""Read an image and make a BAM frame from it.
		Note that if the original image is not indexed, PIL
		does a very poor job converting it. Moreover,
		searching for the transparent color is not implemented
		yet, so it's disabled."""
		
		im = pi.open (filename)
		if im.mode != 'P':
			raise RuntimeError ("Only indexed images are supported as source")
			im = im.convert("P")
		pal = im.getpalette()

		data = []
		for i in range (im.size[1]):
			for j in range (im.size[0]):
				pix = im.getpixel ((j, i))
				if pix == transparent:
					pix = 0
				else:
					r, g, b = pal[3*pix], pal[3*pix+1], pal[3*pix+2]
					pix = self.get_color (r, g, b)
				data.append (pix)

		if x < 0:
			x += 65536
		if y < 0:
			y += 65536

		f = {}
		f['width'] = im.size[0]
		f['height'] = im.size[1]
		f['x'] = x
		f['y'] = y
		f['uncompressed'] = 0
		f['frame_data_off'] = 0
		f['frame_data'] = data
		
		return f

	
	def create_cycle (self, fnames):
		c = {}
		c['frame_cnt'] = len (fnames)
		c['frame_list'] = [ self.names[n] for n in fnames ]
		c['framelut_ndx'] = 0

		return c		


if __name__ == '__main__':
	composer = BAMComposer ()
	composer.read_project(sys.argv[1])
	b = composer.create_bam()

	f = stream.FileStream ().open (sys.argv[2], 'wb')
	b.write (f)
	f.close ()

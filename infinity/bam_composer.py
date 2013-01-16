#!/usr/bin/env python
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

"""Combine several image files to a single BAM image, as specified by a project file.

Example project file:

# palette same|first|auto|<filename>
palette same

# frame <name> <compressed color> <x> <y> <filename>
frame f0 0 0 0 images/cursor1.bmp
frame f1 0 5 5 images/cursor2.bmp

# cycle <name> <frame>  [<frame> ...]
cycle c0 f0 f1

"""

import os.path
import re
import sys

import PIL.Image as pi

from infinity.formats import bam
from infinity import stream


class BAMComposer (object):
	frame_re = re.compile (r'^frame\s+([A-Za-z_][A-Za-z0-9_.-]*)\s+(\d+)\s+([+-]?\d+)\s+([+-]?\d+)\s+(.*)')
	cycle_re = re.compile (r'^cycle\s+([A-Za-z_][A-Za-z0-9_.-]*)((\s+[A-Za-z_][A-Za-z0-9_.-]*)+)')
	palette_re = re.compile (r'^palette\s+(.*)')

	def __init__ (self):
		self.frames = []
		self.cycle_lines = []
		self.palette_file = 'auto'

		self.names = {}
		self.palette = None
		self.transparent = 0

	
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
				self.names[mo.group(1)] = len (self.frames)
				self.frames.append ({
					'name': mo.group(1),
					'transparent': mo.group(2),
					'x': int(mo.group(3)),
					'y': int (mo.group(4)),
					'filename': mo.group(5),
					})
				continue

			mo = self.cycle_re.match (line)
			if mo:
				# FIXME: name is not used yet
				#self.names[mo.group(1)] = len (self.cycle_lines)
				fnames = re.split (r'\s+', mo.group(2).strip())
				self.cycle_lines.append ((mo.group(1), fnames))
				continue
						
			mo = self.palette_re.match (line)
			if mo:
				self.palette_file = mo.group(1)
				continue

		fh.close ()


	def create_bam (self):
		"""Create a new BAM object and add to it frames and cycles"""

		b = bam.BAM_Format()


		self.read_frames()
		self.make_palette()

		for f in self.frames:
			self.convert_frame (f)

		for f in self.frames:
			frame = self.create_frame (f)
			b.frame_list.append (frame)
		
		for c in self.cycle_lines:
			cycle = self.create_cycle(c[1])
			b.cycle_list.append (cycle)

		b.palette_entry_list = self.create_palette()

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


	def make_palette(self):
		if self.palette_file == 'auto':
			self.palette, self.transparent = self.create_common_palette ()
		elif self.palette_file == 'same':
			self.palette, self.transparent = self.get_frame_palette(self.frames[0])
		elif self.palette_file == 'first':
			self.palette, self.transparent = self.get_frame_palette(self.frames[0])
		else:
			self.palette, self.transparent = self.load_palette (self.palette_file)

		# set transparent the same rgb as another color entry

		
	def find_transparent(self, im):
		p = im.getpalette()
		
		for i in range(256):
			if p[3*i] == 0 and p[3*i+1] == 255 and p[3*i+2] == 0:
				return i

		return None



	def load_palette (self, filename):
		im = pi.open (filename)
		if im:
			if im.mode != 'P':
				raise ValueError ("Palette image is not indexed color mode: " + filename)
			return im, self.find_transparent(im)
			
		f = open (filename)
		buf = f.read(768)
		f.close()

		if len(buf) != (3 * 256): # FIXME: 255 or 256?
			# FIXME:allow smaller palettes
			print("Palette size should be  255", file=sys.stderr)
		
		im = pi.new ('P', (1, 1))
		im.putpalette (struct.unpack ('768B', buf))

		return im, self.find_transparent(im)


	def create_common_palette (self):
		w = h = 0
		for f in self.frames:
			w = max (w, f['image'].size[0])
			h += f['image'].size[1]
		
		im = pi.new ('RGB', (w, h), color=(0, 255, 0))

		h = 0			
		for f in self.frames:
			im2 = f['image']
			im.paste (im2, (0, h))
			h += im2.size[1]
		
		#im.show()

		im2 = im.quantize (colors=256)
		transparent = self.find_transparent (im2)

		if transparent is None:
			im2 = im.quantize (colors=255)
			transparent = 255
			
		return im2.crop((0, 0, 1, 1)), transparent


	def get_frame_palette (self, frame):
		im = frame['image']
		transparent = self.find_transparent(im)
		# FIXME: take frame's transparent settings into account
		return im, transparent


	def read_frames (self):
		for frame in self.frames:
			frame['image'] = pi.open (frame['filename'])


	def convert_frame (self, frame):
		im = frame['image']
		
		data = []

		if im.mode == 'P' and (self.palette_file == 'same' or (self.palette_file == 'first' and frame == self.frames[0])):
			for i in range (im.size[1]):
				for j in range (im.size[0]):
					pix = im.getpixel ((j, i))
					data.append(pix)

		elif im.mode == 'P':
			im2 = im.convert('RGB').quantize(palette=self.palette)
			
			for i in range (im.size[1]):
				for j in range (im.size[0]):
					pix = im.getpixel ((j, i))
					pix2 = im2.getpixel ((j, i))
					if pix == 0: # FIXME
						pix = 0
					else:
						pix= pix2
					data.append (pix)

			
		elif im.mode == 'RGBA':
			im2 = im.convert('RGB').quantize(palette=self.palette)
			
			for i in range (im.size[1]):
				for j in range (im.size[0]):
					pix = im.getpixel ((j, i))
					pix2 = im2.getpixel ((j, i))
					if pix[3] <= 127:
						pix = 0
					else:
						pix = pix2
					data.append (pix)

		elif im.mode == 'RGB':
			im2 = im.quantize(palette=self.palette)

			for i in range (im.size[1]):
				for j in range (im.size[0]):
					pix = im.getpixel ((j, i))
					pix2 = im2.getpixel ((j, i))
					if pix == (0, 0, 0): # FIXME
						pix = 0
					else:
						pix = pix2
					data.append (pix)

		else:
			raise ValueError ("Unsupported mode '%s' for image: %s" %(im.mode, frame['filename']))

		
		frame['data'] = data



	def create_frame (self, frame):
		"""Read an image and make a BAM frame from it."""

		x = frame['x']
		y = frame['y']

		if x < 0:
			x += 65536
		if y < 0:
			y += 65536

		f = {}
		f['width'] = frame['image'].size[0]
		f['height'] = frame['image'].size[1]
		f['x'] = x
		f['y'] = y
		f['uncompressed'] = 0
		f['frame_data_off'] = 0
		f['frame_data'] = frame['data']
		
		return f

	
	def create_cycle (self, fnames):
		c = {}
		c['frame_cnt'] = len (fnames)
		c['frame_list'] = [ self.names[n] for n in fnames ]
		c['framelut_ndx'] = 0

		#print c
		return c


	def create_palette (self):
		pal = []
		p = self.palette.getpalette()
		
		for i in range (256):
			pal.append ({ 'r': p[3*i], 'g': p[3*i+1], 'b': p[3*i+2], 'a': 0 })
			
		return pal



def help ():
	print("Usage: %s <project file> <output file>" %os.path.basename (sys.argv[0]), file=sys.stderr)

if __name__ == '__main__':
	if len (sys.argv) != 3:
		help()
		sys.exit (1)

	composer = BAMComposer ()
	composer.read_project(sys.argv[1])
	b = composer.create_bam()

	f = stream.FileStream ().open (sys.argv[2], 'wb')
	b.write (f)
	f.close ()

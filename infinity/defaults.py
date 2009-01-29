# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2008 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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


# FIXME: add descriptions to the options

options = {
    'core.chitin_file': ['CHITIN.KEY', ""], 
    'core.dialog_file': ['dialog.tlk', ""],  
    'pager': ['more', "Program to use for paging command output"],  
 
    'stream.debug_coverage': [False, "On stream close print info on offsets not read or read more than once"], 
    'format.debug_read': [False, "Print each read op to stdout"], 
    'format.debug_write': [False, "Print each write op to stdout"], 

    'format.bam.force_rle': [True,  "Assume that frame data is always RLE encoded"], 
    'format.bam.decode_frame_data': [True, "Decode BAM frame data"], 
    'format.bam.print_frame_bitmap': [True, "Print BAM frame data"], 
    'format.bam.print_palette': [True, "Print BAM frame palette" ], 

    'format.biff.read_data': [False,  "When reading BIFF file read its data too"], 

    'format.key.tick_size': [ 100, "# of RESREFs read to print a dot" ], 
    'format.key.tack_size': [ 5000, "# of RESREFs read to print a number" ], 
    'format.key.max_read_resrefs': [None,  "Max # of RESREFs to read from KEY file"], 

    'format.mos.print_tiles': [True,  "Print MOS tiles"], 
    'format.mos.print_palettes': [False,  "Print MOS palettes"], 

    'format.tis.print_tiles': [False,  "Print TIS tiles"], 
    'format.tis.print_palettes': [False,  "Print TIS palettes"], 
    
    'format.tlk.tick_size': [ 100, "# of STRREFs read to print a dot" ], 
    'format.tlk.tack_size': [ 5000, "# of STRREFs read to print a number" ], 
    'format.tlk.decode_strrefs': [True,  "Read TLK strrefs, not only header"], 

}

# End of file defaults.py

# -*-python-*-
# ie_shell.py - Simple shell for Infinity Engine-based game files
# Copyright (C) 2004-2009 by Jaroslav Benkovsky, <edheldil@users.sf.net>
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

schedule_mask = { 2^0: '00:30-01:29', 2^1: '01:30-02:29', 2^2: '02:30-03:29', 2^3: '03:30-04:29', 2^4: '04:30-05:29', 2^5: '05:30-06:29 (dawn)', 2^6: '06:30-07:29 (day)', 2^7: '07:30-08:29', 2^8: '08:30-09:29', 2^9: '09:30-10:29', 2^10: '10:30-11:29', 2^11: '11:30-12:29', 2^12: '12:30-13:29', 2^13: '13:30-14:29', 2^14: '14:30-15:29', 2^15: '15:30-16:29', 2^16: '16:30-17:29', 2^17: '17:30-18:29', 2^18: '18:30-19:29', 2^19: '19:30-20:29', 2^20: '20:30-21:29 (dusk)', 2^21: '21:30-22:29 (night)', 2^22: '22:30-23:29', 2^23: '23:30-00:29' }

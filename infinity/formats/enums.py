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

item_types = {
  0x0000: 'Books/misc',
  0x0001: 'Amulets and necklaces',
  0x0002: 'Armor',
  0x0003: 'Belts and girdles',
  0x0004: 'Boots',
  0x0005: 'Arrows',
  0x0006: 'Bracers and gauntlets',
  0x0007: 'Helms, hats, and other head-wear',
  0x0008: 'Keys (not in Icewind Dale?)',
  0x0009: 'Potions',
  0x000a: 'Rings',
  0x000b: 'Scrolls',
  0x000c: 'Shields (not in IWD)',
  0x000d: 'Food',
  0x000e: 'Bullets (for a sling)',
  0x000f: 'Bows',
  0x0010: 'Daggers',
  0x0011: 'Maces (in BG, this includes clubs)',
  0x0012: 'Slings',
  0x0013: 'Small swords',
  0x0014: 'Large swords',
  0x0015: 'Hammers',
  0x0016: 'Morning stars',
  0x0017: 'Flails',
  0x0018: 'Darts',
  0x0019: 'Axes',
  0x001a: 'Quarterstaff',
  0x001b: 'Crossbow',
  0x001c: 'Hand-to-hand weapons (fist, fist irons, punch daggers, etc)',
  0x001d: 'Spears',
  0x001e: 'Halberds (2-handed polearms)',
  0x001f: 'Crossbow bolts',
  0x0020: 'Cloaks and robes',
  0x0021: 'Gold pieces',
  0x0022: 'Gems',
  0x0023: 'Wands',
  0x0024: 'Container/eye/broken armor',
  0x0025: 'Books/Broken shield/bracelet',
  0x0026: 'Familiars/Broken sword/earring',
  0x0027: 'Tattoos (PST)',
  0x0028: 'Lenses (PST)',
  0x0029: 'Buckler/teeth',
  0x002a: 'Candle',
  0x002b: 'Unknown',
  0x002c: 'Clubs (IWD)',
  0x002d: 'Unknown',
  0x002e: 'Unknown',
  0x002f: 'Large Shield (IWD)',
  0x0030: 'Unknown',
  0x0031: 'Medium Shield (IWD)',
  0x0032: 'Notes',
  0x0033: 'Unknown',
  0x0034: 'Unknown',
  0x0035: 'Small Shield (IWD)',
  0x0036: 'Unknown',
  0x0037: 'Telescope (IWD)',
  0x0038: 'Drink (IWD)',
  0x0039: 'Great Sword (IWD)',
  0x003a: 'Container',
  0x003b: 'Fur/pelt',
  0x003c: 'Leather Armor',
  0x003d: 'Studded Leather Armor',
  0x003e: 'Chain Mail',
  0x003f: 'Splint Mail',
  0x0040: 'Half Plate',
  0x0041: 'Full Plate',
  0x0042: 'Hide Armor',
  0x0043: 'Robe',
  0x0044: 'Unknown',
  0x0045: 'Bastard Sword',
  0x0046: 'Scarf',
  0x0047: 'Food (IWD2)',
  0x0048: 'Hat',
  0x0049: 'Gauntlet'
  }
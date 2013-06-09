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


from infinity import core
from infinity.format import Format, register_format
from infinity.formats import enums

class ARE_V91_Format (Format):
    header_desc = (
            { 'key': 'signature',
              'type': 'STR4',
              'off': 0x0000,
              'label': 'Signature' },
            
            { 'key': 'version',
              'type': 'STR4',
              'off':0x0004,
              'label': 'Version'},
            
            { 'key': 'wed',
              'type': 'RESREF',
              'off': 0x0008,
              'label': 'Corresponding WED file' },

            { 'key': 'unsaved_time',
              'type': 'DWORD',
              'off': 0x0010,
              'label': 'Seconds since last save' },


            { 'key': 'area_flag',
              'type': 'DWORD',
              'off': 0x0014,
              'mask': {
                  0x01: 'Save disabled',
                  0x02: 'Rest disabled',
                  0x04: 'Unknown bit2',
                  0x08: 'Lock battle music'
                  },
              'label': 'Area flag (AREAFLAG.IDS)'},

            { 'key': 'north_area',
              'type': 'RESREF',
              'off': 0x0018,
              'label': 'Area to the North'},

            { 'key': 'unknown_20',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Unknown 20'},

            { 'key': 'east_area',
              'type': 'RESREF',
              'off': 0x0024,
              'label': 'Area to the East'},

            { 'key': 'unknown_2C',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Unknown 2C'},

            { 'key': 'south_area',
              'type': 'RESREF',
              'off': 0x0030,
              'label': 'Area to the South'},

            { 'key': 'unknown_38',
              'type': 'DWORD',
              'off': 0x0038,
              'label': 'Unknown 38'},

            { 'key': 'west_area',
              'type': 'RESREF',
              'off': 0x003C,
              'label': 'Area to the West'},

            { 'key': 'unknown_44',
              'type': 'DWORD',
              'off': 0x0044,
              'label': 'Unknown 44'},


            { 'key': 'flags',
              'type': 'WORD',
              'off': 0x0048,
              'mask': {
                  0x01: 'outdoor',
                  0x02: 'day/night',
                  0x04: 'weather',
                  0x08: 'city',
                  0x10: 'forest',
                  0x20: 'dungeon',
                  0x40: 'extended night',
                  0x80: 'can rest inddors',
                  },
              'label': 'Flag (AREATYPE.IDS)'},


            { 'key': 'rain_chance',
              'type': 'WORD',
              'off': 0x004A,
              'label': 'Rain chance'},

            { 'key': 'snow_chance',
              'type': 'WORD',
              'off': 0x004C,
              'label': 'Snow chance'},

            { 'key': 'fog_chance',
              'type': 'WORD',
              'off': 0x004E,
              'label': 'Fog chance (unimpl)'},

            { 'key': 'lightning_chance',
              'type': 'WORD',
              'off': 0x0050,
              'label': 'Lightning chance'},

            { 'key': 'unknown_52',
              'type': 'WORD',
              'off': 0x0052,
              'label': 'Unknown 52'},

            { 'key': 'unknown_54',
              'type': 'BYTES',
              'off': 0x0054,
              'size': 16,
              'label': 'Unknown 54'},

            { 'key': 'actor_off',
              'type': 'DWORD',
              'off': 0x0064,
              'label': 'Actors offset'},

            { 'key': 'actor_cnt',
              'type': 'WORD',
              'off': 0x0068,
              'label': '# of actors'},

            { 'key': 'region_cnt',
              'type': 'WORD',
              'off': 0x006A,
              'label': '# of regions'},

            { 'key': 'region_off',
              'type': 'DWORD',
              'off': 0x006C,
              'label': 'Regions offset'},

            { 'key': 'spawnpoint_off',
              'type': 'DWORD',
              'off': 0x0070,
              'label': 'Spawnpoint offset'},

            { 'key': 'spawnpoint_cnt',
              'type': 'DWORD',
              'off': 0x0074,
              'label': '# of spawnpoints'},

            { 'key': 'entrance_off',
              'type': 'DWORD',
              'off': 0x0078,
              'label': 'Entrances offset'},

            { 'key': 'entrance_cnt',
              'type': 'DWORD',
              'off': 0x007C,
              'label': '# of entrances'},

            { 'key': 'container_off',
              'type': 'DWORD',
              'off': 0x0080,
              'label': 'Containers offset'},

            { 'key': 'container_cnt',
              'type': 'WORD',
              'off': 0x0084,
              'label': '# of containers'},

            { 'key': 'item_cnt',
              'type': 'WORD',
              'off': 0x0086,
              'label': '# of items'},

            { 'key': 'item_off',
              'type': 'DWORD',
              'off': 0x0088,
              'label': 'Item offset'},

            { 'key': 'vertex_off',
              'type': 'DWORD',
              'off': 0x008C,
              'label': 'Vertices offset'},

            { 'key': 'vertex_cnt',
              'type': 'WORD',
              'off': 0x0090,
              'label': '# of vertices'},

            { 'key': 'ambient_cnt',
              'type': 'WORD',
              'off': 0x0092,
              'label': '# of ambient sounds'},

            { 'key': 'ambient_off',
              'type': 'DWORD',
              'off': 0x0094,
              'label': 'Ambients offset'},

            { 'key': 'variable_off',
              'type': 'DWORD',
              'off': 0x0098,
              'label': 'Variables offset'},

            { 'key': 'variable_cnt',
              'type': 'DWORD',
              'off': 0x009C,
              'label': '# of variables'},

            { 'key': 'unknown_A0',
              'type': 'DWORD',
              'off': 0x00A0,
              'label': 'Unknown A0'},

            { 'key': 'area_script',
              'type': 'RESREF',
              'off': 0x00A4,
              'label': 'Area Script Resref'},

            { 'key': 'explored_bitmask_size',
              'type': 'DWORD',
              'off': 0x00AC,
              'label': 'Explored bitmask size'},

            { 'key': 'explored_bitmask_off',
              'type': 'DWORD',
              'off': 0x00B0,
              'label': 'Explored bitmask offset'},

            { 'key': 'door_cnt',
              'type': 'DWORD',
              'off': 0x00B4,
              'label': '# of doors'},

            { 'key': 'door_off',
              'type': 'DWORD',
              'off': 0x00B8,
              'label': 'Doors offset'},

            { 'key': 'animation_cnt',
              'type': 'DWORD',
              'off': 0x00BC,
              'label': '# of animations'},

            { 'key': 'animation_off',
              'type': 'DWORD',
              'off': 0x00C0,
              'label': 'Animations offset'},

            { 'key': 'tiled_object_cnt',
              'type': 'DWORD',
              'off': 0x00C4,
              'label': '# of tiled of objects'},

            { 'key': 'tiled_object_off',
              'type': 'DWORD',
              'off': 0x00C8,
              'label': 'Tiled objects offset'},

            { 'key': 'song_off',
              'type': 'DWORD',
              'off': 0x00CC,
              'label': 'Song entries offset'},

            { 'key': 'rest_interrupt_off',
              'type': 'DWORD',
              'off': 0x00D0,
              'label': 'Interruption of rest party option offset'},

            { 'key': 'unknown_D4',
              'type': 'BYTES',
              'off': 0x00D4,
              'size': 88,
              'label': 'Unknown D4' },

            )
    

    actor_desc = (
            { 'key': 'actor_name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Actor name (for editors)' },
        
            { 'key': 'position',
                'type': 'POINT',
                'off': 0x0020,
                'label': 'Current actor position' },
        
            { 'key': 'destination',
                'type': 'POINT',
                'off': 0x0024,
                'label': 'Current actor destination' },
        
            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0028,
                'mask': { 0x01: 'CRE not attached', 0x02: 'Unknown 0x02', 0x04: 'Unknown 0x04', 0x08: 'Override script name' },
                'label': 'Flags' },
        
            { 'key': 'spawned_flag',
                'type': 'WORD',
                'off': 0x002C,
                'label': 'Spawned flag' },

            { 'key': 'letter',
                'type': 'BYTE',
                'off': 0x002E,
                'label': 'Resref fragment (1 letter)' },

            { 'key': 'difficulty_margin',
                'type': 'BYTE',
                'off': 0x002F,
                'label': 'Difficulty margin' },
        
            { 'key': 'animation',
                'type': 'DWORD',
                'off': 0x0030,
                'label': 'Animation' },
        
            { 'key': 'orientation',
                'type': 'DWORD',
                'off': 0x0034,
                'enum': { 0: 'S', 1: 'SSW', 2: 'SW', 3: 'WSW', 4: 'W', 5: 'WNW', 6: 'NW', 7: 'NNW', 8: 'N', 9: 'NNE', 10: 'NE', 11: 'ENE', 12: 'E', 13: 'ESE', 14: 'SE', 15: 'SSE' },
                'label': 'Orientation' },
        
            { 'key': 'unknown_38',
                'type': 'DWORD',
                'off': 0x0038,
                'label': 'Unknown 38' },
        
            { 'key': 'unknown_3C',
                'type': 'DWORD',
                'off': 0x003C,
                'label': 'Unknown 3C' },
        
            { 'key': 'appearance_time',
                'type': 'DWORD',
                'off': 0x0040,
                'mask': enums.schedule_mask,
                'label': 'Actor appearance time' },
        
            { 'key': 'times_spoken_to',
                'type': 'DWORD',
                'off': 0x0044,
                'label': 'Number of times spoken to (in SAV)' },
        
            { 'key': 'dialog',
                'type': 'RESREF',
                'off': 0x0048,
                'label': 'Dialog (overrides CRE dialog)' },
        
            { 'key': 'script_override',
                'type': 'RESREF',
                'off': 0x0050,
                'label': 'Script (override)' },
        
            { 'key': 'script_general',
                'type': 'RESREF',
                'off': 0x0058,
                'label': 'Script (general)' },
        
            { 'key': 'script_class',
                'type': 'RESREF',
                'off': 0x0060,
                'label': 'Script (class)' },
        
            { 'key': 'script_race',
                'type': 'RESREF',
                'off': 0x0068,
                'label': 'Script (race)' },
        
            { 'key': 'script_default',
                'type': 'RESREF',
                'off': 0x0070,
                'label': 'Script (default)' },
        
            { 'key': 'script_specific',
                'type': 'RESREF',
                'off': 0x0078,
                'label': 'Script (specific)' },
        
            { 'key': 'cre_file',
                'type': 'RESREF',
                'off': 0x0080,
                'label': 'CRE file' },
        
            { 'key': 'cre_off',
                'type': 'DWORD',
                'off': 0x0088,
                'label': 'Embedded CRE offset' },
        
            { 'key': 'cre_size',
                'type': 'DWORD',
                'off': 0x008C,
                'label': 'Embedded CRE size' },
        
            { 'key': 'unknown_90',
                'type': 'BYTES',
                'off': 0x0090,
                'size': 128,
                'label': 'Unknown 90' },
            )

    # These used to be called info points in IESDP, but include info points, triggers and exits
    region_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Region name (for editors)' },

            { 'key': 'type',
                'type': 'WORD',
                'off': 0x0020,
                'enum': { 0: 'Proximity', 1: 'Info', 2: 'Travel' },
                'label': 'Region type' },

            { 'key': 'bounding_box',
                'type': 'RECT',
                'off': 0x0022,
                'label': 'Minimal bounding box' },

            { 'key': 'vertex_cnt',
                'type': 'WORD',
                'off': 0x002A,
                'label': 'Count of border vertices' },

            { 'key': 'vertex_ndx',
                'type': 'DWORD',
                'off': 0x002C,
                'label': 'First vertex index' },

            { 'key': 'unknown_30',
                'type': 'DWORD',
                'off': 0x0030,
                'label': 'Unknown 30' },

            { 'key': 'cursor_ndx',
                'type': 'DWORD',
                'off': 0x0034,
                'enum': { 22: 'info point', 28: 'inside exit', 30: 'outside exit' },
                'pst:enum': { 20: 'info', 34: 'exit' },
                'label': 'Frame index to cursors.bam' },

            { 'key': 'destination_area',
                'type': 'RESREF',
                'off': 0x0038,
                'label': 'Resref of destination area for exits' },

            { 'key': 'destination_entrance',
                'type': 'STR32',
                'off': 0x0040,
                'label': 'Entrance in destination area for exits' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0060,
                'mask': { 0x01: 'Invisible trap', 0x02: 'Reset trap (proximity)', 0x04: 'Party required (travel)', 0x08: 'Detectable', 0x10: 'Unknown bit4', 0x20: 'Unknown bit5', 0x40: 'NPC can trigger', 0x80: 'Unknown bit7', 0x100: 'Deactivated (proximity)', 0x200: 'NPC can\'t pass (travel)', 0x400: 'Alternative point', 0x800: 'Used by door?', 0x1000: 'Unknown bit12', 0x2000: 'Unknown bit13', 0x4000: 'Unknown bit14', 0x8000: 'Unknown bit15' },
                'label': 'Flags' },

            { 'key': 'info_text',
                'type': 'STRREF',
                'off': 0x0064,
                'label': 'Info point text' },

            { 'key': 'trap_detection_difficulty',
                'type': 'WORD',
                'off': 0x0068,
                'label': 'Trap detection difficulty (%)' },

            { 'key': 'trap_removal_difficulty',
                'type': 'WORD',
                'off': 0x006A,
                'label': 'Trap removal difficulty (%)' },

            { 'key': 'trapped',
                'type': 'WORD',
                'off': 0x006C,
                'label': 'Region is trapped' },

            { 'key': 'trap_detected',
                'type': 'WORD',
                'off': 0x006E,
                'label': 'Trap has been detected' },

            { 'key': 'trap_launch_location',
                'type': 'POINT',
                'off': 0x0070,
                'label': 'Trap launch location' },

            { 'key': 'key_item',
                'type': 'RESREF',
                'off': 0x0074,
                'label': 'Key item' },

            { 'key': 'script',
                'type': 'RESREF',
                'off': 0x007C,
                'label': 'Region script' },

            { 'key': 'alternative_use_point',
                'type': 'POINT',
                'off': 0x0084,
                'label': 'Alternative use point' },

            { 'key': 'unknown_88',
                'type': 'DWORD',
                'off': 0x0088,
                'label': 'Unknown 88' },

            { 'key': 'unknown_8C',
                'type': 'BYTES',
                'off': 0x008C,
                'size': 44,
                'label': 'Unknown 8C' },

            )

    spawnpoint_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Spawnpoint name' },

            { 'key': 'location',
                'type': 'POINT',
                'off': 0x0020,
                'label': 'Spawnpoint location' },

            { 'key': 'cre_resref',
                'type': 'RESREF',
                'off': 0x0024,
                'count': 10,
                'label': 'CRE Resref' },

            { 'key': 'cre_resref_cnt',
                'type': 'WORD',
                'off': 0x0074,
                'label': 'CRE Resref count' },

            { 'key': 'base_spawn_cnt',
                'type': 'WORD',
                'off': 0x0076,
                'label': 'Base creature number to spawn' },

            { 'key': 'spawn_interval',
                'type': 'WORD',
                'off': 0x0078,
                'label': 'Time interval [s] between spawns' },

            { 'key': 'spawn_method',
                'type': 'WORD',
                'off': 0x007A,
                'enum': { 1: 'Rest', 2: 'Revealed' },
                'label': 'Spawn method' },

            { 'key': 'unknown_7C',
                'type': 'DWORD',
                'off': 0x007C,
                'label': 'Unknown 7C' },

            { 'key': 'unknown_80',
                'type': 'WORD',
                'off': 0x0080,
                'label': 'Unknown 80' },

            { 'key': 'unknown_82',
                'type': 'WORD',
                'off': 0x0082,
                'label': 'Unknown 82' },

            { 'key': 'max_spawn_cnt',
                'type': 'WORD',
                'off': 0x0084,
                'label': 'Max spawned number' },

            { 'key': 'active_flag',
                'type': 'WORD',
                'off': 0x0086,
                'label': 'Active flag' },

            { 'key': 'appearance_time',
                'type': 'DWORD',
                'off': 0x0088,
                'mask': enums.schedule_mask,
                'label': 'Spawnpoint appearance time' },
        
            { 'key': 'day_chance',
                'type': 'WORD',
                'off': 0x008C,
                'label': 'Day chance?' },

            { 'key': 'night_chance',
                'type': 'WORD',
                'off': 0x008E,
                'label': 'Night chance?' },

            { 'key': 'unknown_90',
                'type': 'BYTES',
                'off': 0x0090,
                'size': 56,
                'label': 'Unknown 90' },
            )

    entrance_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Entrance name' },

            { 'key': 'location',
                'type': 'POINT',
                'off': 0x0020,
                'label': 'Entrance location point' },

            { 'key': 'direction',
                'type': 'WORD',
                'off': 0x0024,
                'label': 'Entrance direction' },

            { 'key': 'unknown_26',
                'type': 'BYTES',
                'off': 0x0026,
                'size': 66,
                'label': 'Unknown 26' },
            )

    container_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Container name (for editors)' },

            { 'key': 'location',
                'type': 'POINT',
                'off': 0x0020,
                'label': 'Container location' },

            { 'key': 'type',
                'type': 'WORD',
                'off': 0x0024,
                'enum': { 0x00: 'N/A', 0x01: 'Bag', 0x02: 'Chest', 0x03: 'Drawer', 0x04: 'Pile', 0x05: 'Table', 0x06: 'Shelf', 0x07: 'Altar', 0x08: 'Nonvisible', 0x09: 'Spellbook', 0x0A: 'Body', 0x0B: 'Barrel', 0x0C: 'Crate' },
                'label': 'Container type' },

            { 'key': 'lock_difficulty',
                'type': 'WORD',
                'off': 0x0026,
                'label': 'Lock difficulty' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0028,
                'mask': { 0x01: 'Locked', 0x02: 'Unknown bit1', 0x04: 'Unknown bit2', 0x08: 'Reset trap', 0x10: 'Unknown bit4', 0x20: 'Disabled' },
                'label': 'Flags' },

            { 'key': 'trap_detection_difficulty',
                'type': 'WORD',
                'off': 0x002C,
                'label': 'Trap detection difficulty' },

            { 'key': 'trap_removal_difficulty',
                'type': 'WORD',
                'off': 0x002E,
                'label': 'Trap removal difficulty' },

            { 'key': 'trapped',
                'type': 'WORD',
                'off': 0x0030,
                'label': 'Container is trapped' },

            { 'key': 'trap_detected',
                'type': 'WORD',
                'off': 0x0032,
                'label': 'Trap has been detected' },

            { 'key': 'trap_launch_target',
                'type': 'POINT',
                'off': 0x0034,
                'label': 'Trap launch target' },

            { 'key': 'bounding_box',
                'type': 'RECT',
                'off': 0x0038,
                'label': 'Minimal bounding box' },

            { 'key': 'item_ndx',
                'type': 'DWORD',
                'off': 0x0040,
                'label': 'First item index' },

            { 'key': 'item_cnt',
                'type': 'DWORD',
                'off': 0x0044,
                'label': 'Item count' },

            { 'key': 'trap_script',
                'type': 'RESREF',
                'off': 0x0048,
                'label': 'Resref of trap script' },

            { 'key': 'vertex_ndx',
                'type': 'DWORD',
                'off': 0x0050,
                'label': 'First vertex index' },

            { 'key': 'vertex_cnt',
                'type': 'DWORD',
                'off': 0x0054,
                'label': 'Count of border vertices' },

            { 'key': 'unknown_58',
                'type': 'STR32',
                'off': 0x0058,
                'label': 'Unknown 58 (some trap trigger?)' },

            { 'key': 'key_resref',
                'type': 'RESREF',
                'off': 0x0078,
                'label': 'Resref of key item' },

            { 'key': 'unknown_80',
                'type': 'DWORD',
                'off': 0x0080,
                'label': 'Unknown 80' },

            { 'key': 'lockpick_strref',
                'type': 'STRREF',
                'off': 0x0084,
                'label': 'Strref when lockpicking' },

            { 'key': 'unknown_88',
                'type': 'BYTES',
                'off': 0x0088,
                'size': 56,
                'label': 'Unknown 88' },
            )


    item_desc = (
            { 'key': 'item_resref',
                'type': 'RESREF',
                'off': 0x0000,
                'label': 'ITM resource Resref' },
            
            { 'key': 'expiration_time',
                'type': 'WORD',
                'off': 0x0008,
                'label': 'Item expiration time (replace with drained item)' },

            { 'key': 'usage1',
                'type': 'WORD',
                'off': 0x000A,
                'label': 'Usage 1 (usually # of items or charges)' },
                
            { 'key': 'usage2',
                'type': 'WORD',
                'off': 0x000C,
                'label': 'Usage 2 (usually # of sec. charges)' },
                
            { 'key': 'usage3',
                'type': 'WORD',
                'off': 0x000E,
                'label': 'Usage 3 (usually # of terc. charges)' },
                
            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0010,
                'mask': { 0x1: 'Identified', 0x2: 'Unstealable', 0x4: 'Stolen', 0x8: 'Undroppable' },
                'label': 'Flags' },
                
            )


    vertex_desc = (
            { 'key': 'vertex',
                'type': 'POINT',
                'off': 0x0000,
                'label': 'Vertex' },
            )

    ambient_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Ambient name' },

            { 'key': 'origin_point',
                'type': 'POINT',
                'off': 0x0020,
                'label': 'Origin point' },

            { 'key': 'radius',
                'type': 'WORD',
                'off': 0x0024,
                'label': 'Sound radius' },

            { 'key': 'height',
                'type': 'BYTES', # FIXME: should not be WORD?
                'off': 0x0026,
                'size': 2,
                'label': 'Sound height' },

            { 'key': 'unknown_28',
                'type': 'BYTES',
                'off': 0x0028,
                'size': 6,
                'label': 'Unknown 28' },

            { 'key': 'volume',
                'type': 'WORD',
                'off': 0x002E,
                'label': 'Sound volume (%)' },

            { 'key': 'sound_resref',
                'type': 'RESREF',
                'off': 0x0030,
                'count': 10,
                'label': 'Sound Resref' },

            { 'key': 'sound_resref_cnt',
                'type': 'WORD',
                'off': 0x0080,
                'label': 'Count of sound Resrefs' },

            { 'key': 'unknown_82',
                'type': 'WORD',
                'off': 0x0082,
                'label': 'Unknown 82' },

            { 'key': 'base_time_interval',
                'type': 'DWORD',
                'off': 0x0084,
                'label': 'Base time interval [s] between sounds' },

            { 'key': 'base_time_deviation',
                'type': 'DWORD',
                'off': 0x0088,
                'label': 'Base time deviation' },

            { 'key': 'appearance_time',
                'type': 'DWORD',
                'off': 0x008C,
                'mask': enums.schedule_mask,
                'label': 'Ambient appearance time' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0090,
                'mask': { 0x01: 'Ambient enabled', 0x02: 'Disable environmental fx', 0x04: 'Global', 0x08: 'Random ambient selection', 0x10: 'Unknown bit4', 0x20: 'Unknown bit5', 0x40: 'Unknown bit6', 0x80: 'Unknown bit7' },
                'label': 'Flags' },

            { 'key': 'unknown_94',
                'type': 'BYTES',
                'off': 0x0094,
                'size': 64,
                'label': 'Unknown 94' },
            )


    variable_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Variable name' },
            
            { 'key': 'unknown_20',
                'type': 'BYTES',
                'off': 0x0020,
                'size': 8,
                'label': 'Unknown 20' },
            
            { 'key': 'value',
                'type': 'DWORD',
                'off': 0x0028,
                'label': 'Variable value' },
            
            { 'key': 'unknown_2C',
                'type': 'BYTES',
                'off': 0x002C,
                'size': 40,
                'label': 'Unknown 2C' },

            )

    door_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Long name' },

            { 'key': 'door_id',
                'type': 'STR8',
                'off': 0x0020,
                'label': 'Door ID (WED link)' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0028,
                'mask': { 0x0001: 'Door open', 0x0002: 'Locked', 0x0004: 'Reset trap', 0x0008: 'Trap detectable', 0x0010: 'Broken', 0x0020: 'Can\'t close', 0x0040: 'Linked', 0x0080: 'Door hidden', 0x0100: 'Door found', 0x0200: 'Don\'t block LOS', 0x0400: 'Remove key', 0x0800: 'Slide' },
                'label': 'Flags' },

            { 'key': 'open_vertex_ndx',
                'type': 'DWORD',
                'off': 0x002C,
                'label': 'First vertex index of open door outline' },

            { 'key': 'open_vertex_cnt',
                'type': 'WORD',
                'off': 0x0030,
                'label': 'Count of vertices in open door outline' },

            { 'key': 'closed_vertex_cnt',
                'type': 'WORD',
                'off': 0x0032,
                'label': 'Count of vertices in closed door outline' },

            { 'key': 'closed_vertex_ndx',
                'type': 'DWORD',
                'off': 0x0034,
                'label': 'First vertex index of closed door outline' },

            { 'key': 'open_bounding_box',
                'type': 'RECT',
                'off': 0x0038,
                'label': 'Open door bounding box' },

            { 'key': 'closed_bounding_box',
                'type': 'RECT',
                'off': 0x0040,
                'label': 'Closed door bounding box' },

            { 'key': 'impeded_closed_vertex_ndx',
                'type': 'DWORD',
                'off': 0x0048,
                'label': 'First vertex index of closed door impeded cell block' },

            { 'key': 'impeded_closed_vertex_cnt',
                'type': 'WORD',
                'off': 0x004C,
                'label': 'Count of vertices in closed door impeded cell block' },

            { 'key': 'impeded_open_vertex_cnt',
                'type': 'WORD',
                'off': 0x004E,
                'label': 'Count of vertices in open door impeded cell block' },

            { 'key': 'impeded_open_vertex_ndx',
                'type': 'DWORD',
                'off': 0x0050,
                'label': 'First vertex index of open door impeded cell block' },

            { 'key': 'unknown_54',
                'type': 'WORD',
                'off': 0x0054,
                'label': 'Unknown 54' },

            { 'key': 'unknown_56',
                'type': 'WORD',
                'off': 0x0056,
                'label': 'Unknown 56' },

            { 'key': 'open_door_sound',
                'type': 'RESREF',
                'off': 0x0058,
                'label': 'Open door sound' },

            { 'key': 'close_door_sound',
                'type': 'RESREF',
                'off': 0x0060,
                'label': 'Close door sound' },

            { 'key': 'cursor_ndx',
                'type': 'DWORD',
                'off': 0x0068,
                'label': 'Frame index to cursors.bam' },

            { 'key': 'trap_detection_difficulty',
                'type': 'WORD',
                'off': 0x006C,
                'label': 'Trap detection difficulty' },

            { 'key': 'trap_removal_difficulty',
                'type': 'WORD',
                'off': 0x006E,
                'label': 'Trap removal difficulty' },

            { 'key': 'trapped',
                'type': 'WORD',
                'off': 0x0070,
                'label': 'Door is trapped' },

            { 'key': 'trap_detected',
                'type': 'WORD',
                'off': 0x0072,
                'label': 'Trap has been detected' },

            { 'key': 'trap_launch_target',
                'type': 'POINT',
                'off': 0x0074,
                'label': 'Trap launch target' },

            { 'key': 'key_resref',
                'type': 'RESREF',
                'off': 0x0078,
                'label': 'Key item Resref' },

            { 'key': 'door_script',
                'type': 'RESREF',
                'off': 0x0080,
                'label': 'Door script Resref' },

            { 'key': 'detection_difficulty',
                'type': 'DWORD',
                'off': 0x0088,
                'label': 'Detection difficulty (secret doors)' },

            { 'key': 'lock_difficulty',
                'type': 'DWORD',
                'off': 0x008C,
                'label': 'Lock difficulty [%]' },

            { 'key': 'approach_location',
                'type': 'POINT',
                'off': 0x0090,
                'count': 2,
                'label': 'Location to approach the door' },

            { 'key': 'lockpick_strref',
                'type': 'STRREF',
                'off': 0x0098,
                'label': 'Lockpick strref' },

            { 'key': 'region_link',
                'type': 'STR32',
                'off': 0x009C,
                'label': 'Region link' },

            { 'key': 'dialog_name',
                'type': 'STRREF',
                'off': 0x00BC,
                'label': 'Name used in dialogs' },

            { 'key': 'dialog_resref',
                'type': 'RESREF',
                'off': 0x00C0,
                'label': 'Door\'s dialog Resref' },
            )
    
    animation_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Animation name' },

            { 'key': 'centre',
                'type': 'POINT',
                'off': 0x0020,
                'label': 'Centre point' },

            { 'key': 'appearance_time',
                'type': 'DWORD',
                'off': 0x0024,
                'mask': enums.schedule_mask,
                'label': 'Appearance time' },

            { 'key': 'bam_resref',
                'type': 'RESREF',
                'off': 0x0028,
                'label': 'Animation BAM resref' },

            { 'key': 'bam_sequence',
                'type': 'WORD',
                'off': 0x0030,
                'label': 'BAM sequence number' },

            { 'key': 'bam_frame',
                'type': 'WORD',
                'off': 0x0032,
                'label': 'Number of frame within BAM sequence' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0034,
                'mask': { 0x0001: 'Anim enabled', 0x0002: 'Black is transparent', 0x0004: 'Non-self illumination', 0x0008: 'Partial animation', 0x0010: 'Synchronized draw', 0x0020: 'Unknown bit5', 0x0040: 'Wall doesn\'t hide anim', 0x0080: 'Invisible in dark', 0x0100: 'Not cover', 0x0200: 'Play all frames', 0x0400: 'Use palette bitmap', 0x0800: 'Mirrored', 0x1000: 'Show in combat', 0x2000: 'Unknown bit13', 0x4000: 'Unknown bit14', 0x8000: 'Unknown bit15'  },
                'label': 'Flags' },

            { 'key': 'height',
                'type': 'WORD',
                'off': 0x0038,
                'label': 'Height' },

            { 'key': 'transparency',
                'type': 'WORD',
                'off': 0x003A,
                'label': 'Transparency (255 is invisible)' },

            { 'key': 'starting_frame',
                'type': 'WORD',
                'off': 0x003C,
                'label': 'Starting frame (0 is random)' },

            { 'key': 'looping_chance',
                'type': 'BYTE',
                'off': 0x003E,
                'label': 'Looping chance (0 is 100)' },

            { 'key': 'skip_cycles',
                'type': 'BYTE',
                'off': 0x003F,
                'label': 'Skip cycles' },

            { 'key': 'palette',
                'type': 'RESREF',
                'off': 0x0040,
                'label': 'Palette' },

            { 'key': 'unknown_48',
                'type': 'DWORD',
                'off': 0x0048,
                'label': 'Unknown 48' },
            )


#    automap_note_desc = (
#            { 'key': 'x',
#                'type': 'WORD',
#                'off': 0x0000,
#                'label': 'X coordinate' },
#                
#            { 'key': 'y',
#                'type': 'WORD',
#                'off': 0x0002,
#                'label': 'Y coordinate' },
#                         
#            { 'key': 'text',
#                'type': 'STRREF',
#                'off': 0x0004,
#                'label': 'Note text' },
#                
#            { 'key': 'strref_location',
#                'type': 'WORD',
#                'off': 0x0008,
#                'enum': {0 : 'External (TOH/TOT)', 1: 'Internal (TLK)' },
#                'label': 'STRREF location' },
#                
#            { 'key': 'color',
#                'type': 'WORD',
#                'off': 0x000A,
#                'enum': {0 : 'Gray', 1: 'Violet', 2: 'Green', 3: 'Orange', 4: 'Red', 5: 'Blue', 6: 'Dark blue', 7: 'Light gray' },
#                'label': 'Note pin color / type' },
#                
#            { 'key': 'note_count_plus_10',
#                'type': 'DWORD',
#                'off': 0x000C,
#                'label': 'Note count + 10' },
#                
#            { 'key': 'unknown_10',
#                'type': 'BYTES',
#                'off': 0x0010,
#                'size': 36,
#                'label': 'Unknown 10' },
#                
#            )


    tiled_object_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Tiled object name' },

            { 'key': 'unknown_20',
                'type': 'RESREF',
                'off': 0x0020,
                'label': 'Unknown 20' },

            { 'key': 'unknown_28',
                'type': 'DWORD',
                'off': 0x0028,
                'label': 'Unknown 28' },

            { 'key': 'open_search_squares_start',
                'type': 'DWORD',
                'off': 0x002C,
                'label': 'Open search squares start' },

            { 'key': 'open_search_squares_cnt',
                'type': 'DWORD',
                'off': 0x0030,
                'label': 'Open search squares count' },

            { 'key': 'closed_search_squares_start',
                'type': 'DWORD',
                'off': 0x0034,
                'label': 'Closed search squares start' },

            { 'key': 'closed_search_squares_cnt',
                'type': 'DWORD',
                'off': 0x0038,
                'label': 'Closed search squares count' },

            { 'key': 'unknown_3C',
                'type': 'BYTES',
                'off': 0x003C,
                'size': 48,
                'label': 'Unknown 3C' },

            )


    song_desc = (
            { 'key': 'day_song_ref_no',
                'type': 'DWORD',
                'off': 0x0000,
                'label': 'Day song reference number' },

            { 'key': 'night_song_ref_no',
                'type': 'DWORD',
                'off': 0x0004,
                'label': 'Night song reference number' },

            { 'key': 'win_song_ref_no',
                'type': 'DWORD',
                'off': 0x0008,
                'label': 'Win song reference number' },

            { 'key': 'battle_song_ref_no',
                'type': 'DWORD',
                'off': 0x000C,
                'label': 'Battle song reference number' },

            { 'key': 'lose_song_ref_no',
                'type': 'DWORD',
                'off': 0x0010,
                'label': 'Lose song reference number' },

            { 'key': 'unknown_14',
                'type': 'DWORD',
                'off': 0x0014,
                'count': 5,
                'label': 'Unknown 14' },

            { 'key': 'main_day_ambient_1',
                'type': 'RESREF',
                'off': 0x0028,
                'label': 'Main day ambient 1 (WAV)' },

            { 'key': 'main_day_ambient_2',
                'type': 'RESREF',
                'off': 0x0030,
                'label': 'Main day ambient 2 (WAV)' },

            { 'key': 'main_day_ambient_volume',
                'type': 'DWORD',
                'off': 0x0038,
                'label': 'Main day ambient volume [%]' },

            { 'key': 'main_night_ambient_1',
                'type': 'RESREF',
                'off': 0x003C,
                'label': 'Main night ambient 1 (WAV)' },

            { 'key': 'main_night_ambient_2',
                'type': 'RESREF',
                'off': 0x0044,
                'label': 'Main night ambient 2 (WAV)' },

            { 'key': 'main_night_ambient_volume',
                'type': 'DWORD',
                'off': 0x004C,
                'label': 'Main night ambient volume [%]' },

            { 'key': 'reverb',
                'type': 'DWORD',
                'off': 0x0050,
                'enum': 'reverb',
                'label': 'Reverb (if REVERB.IDS exists)' },

            { 'key': 'unknown_54',
                'type': 'BYTES',
                'off': 0x0054,
                'size': 60,
                'label': 'Unknown 54' },
            )

    
    rest_interrupt_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Name' },

            { 'key': 'strref',
                'type': 'STRREF',
                'off': 0x0020,
                'count': 10,
                'label': 'Interrupt explanation Strref' },

            { 'key': 'cre_resref',
                'type': 'RESREF',
                'off': 0x0048,
                'count': 10,
                'label': 'CRE resref to spawn' },

            { 'key': 'cre_cnt',
                'type': 'WORD',
                'off': 0x0098,
                'label': 'Count of CRE entries' },

            { 'key': 'unknown_9A',
                'type': 'WORD',
                'off': 0x009A,
                'label': 'Unknown 9A (freq? diff?)' },

            { 'key': 'unknown_9C',
                'type': 'DWORD',
                'off': 0x009C,
                'label': 'Unknown 9C' },

            { 'key': 'unknown_A0',
                'type': 'WORD',
                'off': 0x00A0,
                'label': 'Unknown A0' },

            { 'key': 'unknown_A2',
                'type': 'WORD',
                'off': 0x00A2,
                'label': 'Unknown A2' },

            { 'key': 'spawned_cnt_max',
                'type': 'WORD',
                'off': 0x00A4,
                'label': 'Max number of spawned creatures' },

            { 'key': 'unknown_A6',
                'type': 'WORD',
                'off': 0x00A6,
                'label': 'Unknown A6' },

            { 'key': 'day_chance',
                'type': 'WORD',
                'off': 0x00A8,
                'label': 'Day chance?' },

            { 'key': 'night_chance',
                'type': 'WORD',
                'off': 0x00AA,
                'label': 'Night chance?' },

            { 'key': 'unknown_AC',
                'type': 'BYTES',
                'off': 0x00AC,
                'size': 56,
                'label': 'Unknown AC' },
            )



    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'AREA'
        
        self.actor_list = []
        self.region_list = []
        self.spawnpoint_list = []
        self.entrance_list = []
        self.container_list = []
        self.item_list = []
        self.vertex_list = []
        self.ambient_list = []
        self.variable_list = []
        self.explored_bitmask = None
        self.door_list = []
        self.animation_list = []
        ##self.automap_note_list = []
        self.tiled_object_list = []
        self.song = None
        self.rest_interrupt = None


    def read (self, stream):
        self.read_header (stream)
        
        self.read_list (stream, 'actor')
        self.read_list (stream, 'region')
        self.read_list (stream, 'spawnpoint')
        self.read_list (stream, 'entrance')
        self.read_list (stream, 'container')
        self.read_list (stream, 'item')
        self.read_list (stream, 'vertex')
        self.read_list (stream, 'ambient')
        self.read_list (stream, 'variable')
        self.explored_bitmask = stream.read_blob (self.header['explored_bitmask_off'], self.header['explored_bitmask_size'])
        self.read_list (stream, 'door')
        self.read_list (stream, 'animation') 
        ##self.read_list (stream, 'automap_note')
            
        self.read_list (stream, 'tiled_object')

        obj = {}
        self.read_struc (stream, self.header['song_off'], self.song_desc, obj)
        self.song = obj

        obj = {}
        self.read_struc (stream, self.header['rest_interrupt_off'], self.rest_interrupt_desc, obj)
        self.rest_interrupt = obj


    def write (self, stream):
        off = self.get_struc_size (self.header_desc)

        off = self.write_list (stream, off, 'actor')
        off = self.write_list (stream, off, 'region')
        off = self.write_list (stream, off, 'spawnpoint')
        off = self.write_list (stream, off, 'entrance')
        off = self.write_list (stream, off, 'container')
        off = self.write_list (stream, off, 'item')
        off = self.write_list (stream, off, 'vertex')
        off = self.write_list (stream, off, 'ambient')
        off = self.write_list (stream, off, 'variable')

        stream.write_blob (self.explored_bitmask, off)
        off  += len (self.explored_bitmask)

        off = self.write_list (stream, off, 'door')
        off = self.write_list (stream, off, 'animation')
        ##off = self.write_list (stream, off, 'automap_note')
        off = self.write_list (stream, off, 'tiled_object')

        self.header['song_off'] = off
        self.write_struc (stream, off, self.song_desc, self.song)
        off += self.get_struc_size (self.song_desc)

        self.header['rest_interrupt_off'] = off
        self.write_struc (stream, off, self.rest_interrupt_desc, self.rest_interrupt)
        off += self.get_struc_size (self.rest_interrupt_desc)

        self.write_header (stream)

    def printme (self):
        self.print_header ()
            
        self.print_list ('actor')
        self.print_list ('region')
        self.print_list ('spawnpoint')
        self.print_list ('entrance')
        self.print_list ('container')
        self.print_list ('item')
        self.print_list ('vertex')
        self.print_list ('ambient')
        self.print_list ('variable')
        # "Explored" bitmask. We need map width and height to print the mask, though and they're not in the ARE structure
        self.print_list ('door')
        self.print_list ('animation') 
        ##self.print_list ('automap_note')
        self.print_list ('tiled_object')
        self.print_struc (self.song, self.song_desc)
        self.print_struc (self.rest_interrupt, self.rest_interrupt_desc)


register_format ('AREA', 'V9.1', ARE_V91_Format)

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

class ARE_Format (Format):
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
                  0x01: 'can save',
                  0x02: 'tutorial',
                  0x04: 'dead magic',
                  0x08: 'dream'
                  },
              'label': 'Area flag (AREAFLAG.IDS)'},

            { 'key': 'north_area',
              'type': 'RESREF',
              'off': 0x0018,
              'label': 'Area to the North'},

            { 'key': 'unknown_20',
              'type': 'DWORD',
              'off': 0x0020,
              'label': 'Unknown north 20'},

            { 'key': 'east_area',
              'type': 'RESREF',
              'off': 0x0024,
              'label': 'Area to the East'},

            { 'key': 'unknown_2C',
              'type': 'DWORD',
              'off': 0x002C,
              'label': 'Unknown east 20'},

            { 'key': 'south_area',
              'type': 'RESREF',
              'off': 0x0030,
              'label': 'Area to the South'},

            { 'key': 'unknown_38',
              'type': 'DWORD',
              'off': 0x0038,
              'label': 'Unknown south 38'},

            { 'key': 'west_area',
              'type': 'RESREF',
              'off': 0x003C,
              'label': 'Area to the West'},

            { 'key': 'unknown_44',
              'type': 'DWORD',
              'off': 0x0044,
              'label': 'Unknown west 44'},


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


            { 'key': 'actor_off',
              'type': 'DWORD',
              'off': 0x0054,
              'label': 'Actors offset'},

            { 'key': 'actor_cnt',
              'type': 'WORD',
              'off': 0x0058,
              'label': '# of actors'},

            { 'key': 'infopoint_cnt',
              'type': 'WORD',
              'off': 0x005A,
              'label': '# of infopoints, triggerpoints and exits'},

            { 'key': 'infopoint_off',
              'type': 'DWORD',
              'off': 0x005C,
              'label': 'Offset of infopoints, triggerpoints and exits'},

            { 'key': 'spawnpoint_off',
              'type': 'DWORD',
              'off': 0x0060,
              'label': 'Spawnpoint offset'},

            { 'key': 'spawnpoint_cnt',
              'type': 'DWORD',
              'off': 0x0064,
              'label': '# of spawnpoints'},

            { 'key': 'entrance_off',
              'type': 'DWORD',
              'off': 0x0068,
              'label': 'Entrances offset'},

            { 'key': 'entrance_cnt',
              'type': 'DWORD',
              'off': 0x006C,
              'label': '# of entrances'},

            { 'key': 'container_off',
              'type': 'DWORD',
              'off': 0x0070,
              'label': 'Containers offset'},

            { 'key': 'container_cnt',
              'type': 'WORD',
              'off': 0x0074,
              'label': '# of containers'},

            { 'key': 'item_cnt',
              'type': 'WORD',
              'off': 0x0076,
              'label': '# of items'},

            { 'key': 'item_off',
              'type': 'DWORD',
              'off': 0x0078,
              'label': 'Item offset'},

            { 'key': 'vertex_off',
              'type': 'DWORD',
              'off': 0x007C,
              'label': 'Vertices offset'},

            { 'key': 'vertex_cnt',
              'type': 'WORD',
              'off': 0x0080,
              'label': '# of vertices'},

            { 'key': 'ambient_cnt',
              'type': 'WORD',
              'off': 0x0082,
              'label': '# of ambient sounds'},

            { 'key': 'ambient_off',
              'type': 'DWORD',
              'off': 0x0084,
              'label': 'Ambients offset'},

            { 'key': 'variable_off',
              'type': 'DWORD',
              'off': 0x0088,
              'label': 'Variables offset'},

            { 'key': 'variable_cnt',
              'type': 'DWORD',
              'off': 0x008C,
              'label': '# of variables'},

            { 'key': 'unknown_90',
              'type': 'DWORD',
              'off': 0x0090,
              'label': 'Unknown 90'},

            { 'key': 'area_script',
              'type': 'RESREF',
              'off': 0x0094,
              'label': 'Area Script Resref'},

            { 'key': 'explored_bitmask_size',
              'type': 'DWORD',
              'off': 0x009C,
              'label': 'Explored bitmask size'},

            { 'key': 'explored_bitmask_off',
              'type': 'DWORD',
              'off': 0x00A0,
              'label': 'Explored bitmask offset'},

            { 'key': 'door_cnt',
              'type': 'DWORD',
              'off': 0x00A4,
              'label': '# of doors'},

            { 'key': 'door_off',
              'type': 'DWORD',
              'off': 0x00A8,
              'label': 'Doors offset'},

            { 'key': 'animation_cnt',
              'type': 'DWORD',
              'off': 0x00AC,
              'label': '# of animations'},

            { 'key': 'animation_off',
              'type': 'DWORD',
              'off': 0x00B0,
              'label': 'Animations offset'},

            { 'key': 'tiled_object_cnt',
              'type': 'DWORD',
              'off': 0x00B4,
              'label': '# of tiled of objects'},

            { 'key': 'tiled_object_off',
              'type': 'DWORD',
              'off': 0x00B8,
              'label': 'Tiled objects offset'},

            { 'key': 'song_off',
              'type': 'DWORD',
              'off': 0x00BC,
              'label': 'Song entries offset'},

            { 'key': 'rest_interrupt_off',
              'type': 'DWORD',
              'off': 0x00C0,
              'label': 'Interruption of rest party option offset'},

            { 'key': 'automap_note_off',
              'type': 'DWORD',
              'off': 0x00C4,
              'label': 'Automap notes offset (non PST)'}, # PST has 0xFFFFFFFF here

            )
    
    header2_desc = (
            { 'key': 'automap_note_cnt',
              'type': 'DWORD',
              'off': 0x00C8,
              'label': '# of automap notes (non PST)'}, # PST has automap_note_off here

            { 'key': 'projectile_trap_off',
              'type': 'DWORD',
              'off': 0x00CC,
              'label': 'Projectile traps offset (non PST)'}, # PST has automap_note_cnt here

            { 'key': 'projectile_trap_cnt',
              'type': 'DWORD',
              'off': 0x00D0,
              'label': '# of projectile traps'},

            { 'key': 'unknown_D4',
              'type': 'BYTES',
              'off': 0x00D4,
              'size': 4 * 18,
              'label': 'Unknown D4'},
            )

    header2_pst_desc = (
            { 'key': 'automap_note_pst_off',
              'type': 'DWORD',
              'off': 0x00C8,
              'label': 'Automap notes offset (PST)'}, # non-PST have automap_note_cnt here

            { 'key': 'automap_note_pst_cnt',
              'type': 'DWORD',
              'off': 0x00CC,
              'label': '# of automap notes (PST)'}, # non-PST have projectile_trap_off here

            { 'key': 'projectile_trap_cnt',
              'type': 'DWORD',
              'off': 0x00D0,
              'label': '# of projectile traps'},

            { 'key': 'unknown_D4',
              'type': 'BYTES',
              'off': 0x00D4,
              'size': 4 * 18,
              'label': 'Unknown D4'},
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
                'mask': { 0x01: 'CRE not attached', 0x02: 'Unknown 0x02', 0x04: 'Unknown 0x04', 0x08: 'Actor name as death var' },
                'label': 'Flags' },
        
            { 'key': 'spawned_flag',
                'type': 'DWORD',
                'off': 0x002C,
                'label': 'Spawned flag (in memory)' },
        
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
                'mask': { 2^0: '00:30-01:29', 2^1: '01:30-02:29', 2^2: '02:30-03:29', 2^3: '03:30-04:29', 2^4: '04:30-05:29', 2^5: '05:30-06:29', 2^6: '06:30-07:29', 2^7: '07:30-08:29', 2^8: '08:30-09:29', 2^9: '09:30-10:29', 2^10: '10:30-11:29', 2^11: '11:30-12:29', 2^12: '12:30-13:29', 2^13: '13:30-14:29', 2^14: '14:30-15:29', 2^15: '15:30-16:29', 2^16: '16:30-17:29', 2^17: '17:30-18:29', 2^18: '18:30-19:29', 2^19: '19:30-20:29', 2^20: '20:30-21:29 (dusk)', 2^21: '21:30-22:29 (night)', 2^22: '22:30-23:29', 2^23: '23:30-00:29' },
                'label': 'Actor appearance time' },
        
            { 'key': 'times_spoken_to',
                'type': 'DWORD',
                'off': 0x0044,
                'label': 'Number of times spoken to (in SAV)' },
        
            { 'key': 'dialog',
                'type': 'RESREF',
                'off': 0x0048,
                'label': 'Dialog (overrides CRE dialog)' },
        
            { 'key': 'script',
                'type': 'RESREF',
                'off': 0x0050,
                'label': 'Script (override)' },
        
            { 'key': 'script',
                'type': 'RESREF',
                'off': 0x0058,
                'label': 'Script (class)' },
        
            { 'key': 'script',
                'type': 'RESREF',
                'off': 0x0060,
                'label': 'Script (race)' },
        
            { 'key': 'script',
                'type': 'RESREF',
                'off': 0x0068,
                'label': 'Script (general)' },
        
            { 'key': 'script',
                'type': 'RESREF',
                'off': 0x0070,
                'label': 'Script (default)' },
        
            { 'key': 'script',
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
                'label': 'CRE structure offset' },
        
            { 'key': 'cre_size',
                'type': 'DWORD',
                'off': 0x008C,
                'label': 'CRE structure size' },
        
            { 'key': 'unknown_90',
                'type': 'BYTES',
                'off': 0x0090,
                'size': 128,
                'label': 'Unknown 90' },
    )

    # These are called info points in IESDP, but include info points, triggers and exits
    infopoint_desc = (
            { 'key': 'name',
                'type': 'STR32',
                'off': 0x0000,
                'label': 'Hotspot/Infopoint name (for editors)' },

            { 'key': 'type',
                'type': 'WORD',
                'off': 0x0020,
                'enum': { 0: 'Proximity', 1: 'Info', 2: 'Travel' },
                'label': 'Hotspot/Infopoint type' },

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

            { 'key': 'trapped_flag',
                'type': 'WORD',
                'off': 0x006C,
                'label': 'Trapped flag' },

            { 'key': 'trap_detected',
                'type': 'WORD',
                'off': 0x006E,
                'label': 'Trap detected flag' },

            { 'key': 'trap_launch_location',
                'type': 'POINT',
                'off': 0x0070,
                'label': 'Trap launch location' },

            { 'key': 'key_type',
                'type': 'BYTES',
                'off': 0x0074,
                'size': 8,
                'label': 'Key type (usage unknown)' },

            { 'key': 'script',
                'type': 'RESREF',
                'off': 0x007C,
                'label': 'Script (if trigger point)' },

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

            { 'key': 'unknown_B4',
                'type': 'POINT',
                'off': 0x00B4,
                'label': 'Unknown B4' },

            { 'key': 'unknown_B8',
                'type': 'DWORD',
                'off': 0x00B8,
                'label': 'Unknown B8' },

            { 'key': 'dialog_pst',
                'type': 'RESREF',
                'off': 0x00BC,
                'label': 'Dialog Resref (PST only?)' },
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

            { 'key': 'cre_resref_0',
                'type': 'RESREF',
                'off': 0x0024,
                'label': 'CRE Resref 0' },

            { 'key': 'cre_resref_1',
                'type': 'RESREF',
                'off': 0x002C,
                'label': 'CRE Resref 1' },

            { 'key': 'cre_resref_2',
                'type': 'RESREF',
                'off': 0x0034,
                'label': 'CRE Resref 2' },

            { 'key': 'cre_resref_3',
                'type': 'RESREF',
                'off': 0x003C,
                'label': 'CRE Resref 3' },

            { 'key': 'cre_resref_4',
                'type': 'RESREF',
                'off': 0x0044,
                'label': 'CRE Resref 4' },

            { 'key': 'cre_resref_5',
                'type': 'RESREF',
                'off': 0x004C,
                'label': 'CRE Resref 5' },

            { 'key': 'cre_resref_6',
                'type': 'RESREF',
                'off': 0x0054,
                'label': 'CRE Resref 6' },

            { 'key': 'cre_resref_7',
                'type': 'RESREF',
                'off': 0x005C,
                'label': 'CRE Resref 7' },

            { 'key': 'cre_resref_8',
                'type': 'RESREF',
                'off': 0x0064,
                'label': 'CRE Resref 8' },

            { 'key': 'cre_resref_9',
                'type': 'RESREF',
                'off': 0x006C,
                'label': 'CRE Resref 9' },

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
                'type': 'WORD',
                'off': 0x007C,
                'enum': { 0: 'Disable spawnpoint' },
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
                'mask': { 2^0: '00:30-01:29', 2^1: '01:30-02:29', 2^2: '02:30-03:29', 2^3: '03:30-04:29', 2^4: '04:30-05:29', 2^5: '05:30-06:29', 2^6: '06:30-07:29', 2^7: '07:30-08:29', 2^8: '08:30-09:29', 2^9: '09:30-10:29', 2^10: '10:30-11:29', 2^11: '11:30-12:29', 2^12: '12:30-13:29', 2^13: '13:30-14:29', 2^14: '14:30-15:29', 2^15: '15:30-16:29', 2^16: '16:30-17:29', 2^17: '17:30-18:29', 2^18: '18:30-19:29', 2^19: '19:30-20:29', 2^20: '20:30-21:29 (dusk)', 2^21: '21:30-22:29 (night)', 2^22: '22:30-23:29', 2^23: '23:30-00:29' },
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
                'size': 66,    # FIXME: IESDP has 62 here....
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

            { 'key': 'is_trapped',
                'type': 'WORD',
                'off': 0x0030,
                'label': 'Container is trapped' },

            { 'key': 'is_detected',
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
                'type': 'WORD',
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

            { 'key': 'unlockable_tlk_ref',
                'type': 'DWORD',
                'off': 0x0084,
                'label': 'TLK ref when lockpicking unlockable container' },

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
                'type': 'BYTES',
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
                'label': 'Sound volume' },

            { 'key': 'sound_resref_0',
                'type': 'RESREF',
                'off': 0x0030,
                'label': 'Sound Resref 0' },

            { 'key': 'sound_resref_1',
                'type': 'RESREF',
                'off': 0x0038,
                'label': 'Sound Resref 1' },

            { 'key': 'sound_resref_2',
                'type': 'RESREF',
                'off': 0x0040,
                'label': 'Sound Resref 2' },

            { 'key': 'sound_resref_3',
                'type': 'RESREF',
                'off': 0x0048,
                'label': 'Sound Resref 3' },

            { 'key': 'sound_resref_4',
                'type': 'RESREF',
                'off': 0x0050,
                'label': 'Sound Resref 4' },

            { 'key': 'sound_resref_5',
                'type': 'RESREF',
                'off': 0x0058,
                'label': 'Sound Resref 5' },

            { 'key': 'sound_resref_6',
                'type': 'RESREF',
                'off': 0x0060,
                'label': 'Sound Resref 6' },

            { 'key': 'sound_resref_7',
                'type': 'RESREF',
                'off': 0x0068,
                'label': 'Sound Resref 7' },

            { 'key': 'sound_resref_8',
                'type': 'RESREF',
                'off': 0x0070,
                'label': 'Sound Resref 8' },

            { 'key': 'sound_resref_9',
                'type': 'RESREF',
                'off': 0x0078,
                'label': 'Sound Resref 9' },

            { 'key': 'sound_resref_cnt',
                'type': 'WORD',
                'off': 0x0080,
                'label': 'Count of sound Resrefs' },

            { 'key': 'sound_resref_cnt2',
                'type': 'WORD',
                'off': 0x0082,
                'label': 'Count of sound Resrefs or 0' },

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
                'mask': { 2^0: '00:30-01:29', 2^1: '01:30-02:29', 2^2: '02:30-03:29', 2^3: '03:30-04:29', 2^4: '04:30-05:29', 2^5: '05:30-06:29', 2^6: '06:30-07:29', 2^7: '07:30-08:29', 2^8: '08:30-09:29', 2^9: '09:30-10:29', 2^10: '10:30-11:29', 2^11: '11:30-12:29', 2^12: '12:30-13:29', 2^13: '13:30-14:29', 2^14: '14:30-15:29', 2^15: '15:30-16:29', 2^16: '16:30-17:29', 2^17: '17:30-18:29', 2^18: '18:30-19:29', 2^19: '19:30-20:29', 2^20: '20:30-21:29 (dusk)', 2^21: '21:30-22:29 (night)', 2^22: '22:30-23:29', 2^23: '23:30-00:29' },
                'label': 'Ambient appearance time' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0090,
                'mask': { 0x01: 'Ambient enabled', 0x02: 'Reverb', 0x04: 'Global', 0x08: 'Random ambient selection', 0x10: 'Unknown bit4', 0x20: 'Unknown bit5', 0x40: 'Unknown bit6', 0x80: 'Unknown bit7' },
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

            { 'key': 'short_name',
                'type': 'STR8',
                'off': 0x0020,
                'label': 'Short name' },

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

            { 'key': 'impeded_open_vertex_ndx',
                'type': 'DWORD',
                'off': 0x0048,
                'label': 'First vertex index of open door impeded cell block' },

            { 'key': 'impeded_open_vertex_cnt',
                'type': 'WORD',
                'off': 0x004C,
                'label': 'Count of vertices in open door impeded cell block' },

            { 'key': 'impeded_closed_vertex_cnt',
                'type': 'WORD',
                'off': 0x004E,
                'label': 'Count of vertices in closed door impeded cell block' },

            { 'key': 'impeded_closed_vertex_ndx',
                'type': 'DWORD',
                'off': 0x0050,
                'label': 'First vertex index of closed door impeded cell block' },

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

            { 'key': 'trapped_flag',
                'type': 'WORD',
                'off': 0x0070,
                'label': 'Trapped flag' },

            { 'key': 'trap_detected_flag',
                'type': 'WORD',
                'off': 0x0072,
                'label': 'Trap detected flag' },

            { 'key': 'trap_launch_target',
                'type': 'POINT',
                'off': 0x0074,
                'label': 'Trap launch target' },

            { 'key': 'key_resref',
                'type': 'RESREF',
                'off': 0x0078,
                'label': 'Key item Resref' },

            { 'key': 'key_script',
                'type': 'RESREF',
                'off': 0x0080,
                'label': 'Key item script Resref' },

            { 'key': 'detection_difficulty',
                'type': 'DWORD',
                'off': 0x0088,
                'label': 'Detection difficulty (secret doors)' },

            { 'key': 'lock_difficulty',
                'type': 'DWORD',
                'off': 0x008C,
                'label': 'Lock difficulty [%]' },

            { 'key': 'approach_location_0',
                'type': 'POINT',
                'off': 0x0090,
                'label': 'First location to approach the door' },

            { 'key': 'approach_location_1',
                'type': 'POINT',
                'off': 0x0094,
                'label': 'Second location to approach the door' },

            { 'key': 'unpickable_strref',
                'type': 'STRREF',
                'off': 0x0098,
                'label': 'Picklock attempt on unpickable door strref' },

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
                'mask': { 2^0: '00:30-01:29', 2^1: '01:30-02:29', 2^2: '02:30-03:29', 2^3: '03:30-04:29', 2^4: '04:30-05:29', 2^5: '05:30-06:29', 2^6: '06:30-07:29', 2^7: '07:30-08:29', 2^8: '08:30-09:29', 2^9: '09:30-10:29', 2^10: '10:30-11:29', 2^11: '11:30-12:29', 2^12: '12:30-13:29', 2^13: '13:30-14:29', 2^14: '14:30-15:29', 2^15: '15:30-16:29', 2^16: '16:30-17:29', 2^17: '17:30-18:29', 2^18: '18:30-19:29', 2^19: '19:30-20:29', 2^20: '20:30-21:29 (dusk)', 2^21: '21:30-22:29 (night)', 2^22: '22:30-23:29', 2^23: '23:30-00:29' },
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


    automap_note_pst_desc = (
            { 'key': 'x',
                'type': 'DWORD',
                'off': 0x0000,
                'label': 'X coordinate' },
                
            { 'key': 'y',
                'type': 'DWORD',
                'off': 0x0004,
                'label': 'Y coordinate' },
                
            { 'key': 'text',
                'type': 'BYTES',
                'off': 0x0008,
                'size': 500,
                'label': 'Note text' },
                
            { 'key': 'color',
                'type': 'DWORD',
                'off': 0x01FC,
                'enum': {0 : 'Blue (user)', 1: 'Red (game)' },
                'label': 'Note pin color / type' },
                
            { 'key': 'unknown_200',
                'type': 'BYTES',
                'off': 0x0200,
                'size': 5 * 4,
                'label': 'Unknown 200' },
                
            )

    automap_note_desc = (
            { 'key': 'x',
                'type': 'WORD',
                'off': 0x0000,
                'label': 'X coordinate' },
                
            { 'key': 'y',
                'type': 'WORD',
                'off': 0x0002,
                'label': 'Y coordinate' },
                         
            { 'key': 'text',
                'type': 'STRREF',
                'off': 0x0004,
                'label': 'Note text' },
                
            { 'key': 'strref_location',
                'type': 'WORD',
                'off': 0x0008,
                'enum': {0 : 'External (TOH/TOT)', 1: 'Internal (TLK)' },
                'label': 'STRREF location' },
                
            { 'key': 'color',
                'type': 'WORD',
                'off': 0x000A,
                'enum': {0 : 'Gray', 1: 'Violet', 2: 'Green', 3: 'Orange', 4: 'Red', 5: 'Blue', 6: 'Dark blue', 7: 'Light gray' },
                'label': 'Note pin color / type' },
                
            { 'key': 'note_count_plus_10',
                'type': 'DWORD',
                'off': 0x000C,
                'label': 'Note count + 10' },
                
            { 'key': 'unknown_10',
                'type': 'BYTES',
                'off': 0x0010,
                'size': 36,
                'label': 'Unknown 10' },
                
            )


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

            { 'key': 'primary_search_squares_start',
                'type': 'DWORD',
                'off': 0x002C,
                'label': 'Primary search squares start' },

            { 'key': 'primary_search_squares_cnt',
                'type': 'DWORD',
                'off': 0x0030,
                'label': 'Primary search squares count' },

            { 'key': 'secondary_search_squares_start',
                'type': 'DWORD',
                'off': 0x0034,
                'label': 'Secondary search squares start' },

            { 'key': 'secondary_search_squares_cnt',
                'type': 'DWORD',
                'off': 0x0038,
                'label': 'Secondary search squares count' },

            { 'key': 'unknown_3C',
                'type': 'BYTES',
                'off': 0x003C,
                'size': 48,
                'label': 'Unknown 3C' },

            )


    projectile_trap_desc = (
            { 'key': 'projectile_resref',
                'type': 'RESREF',
                'off': 0x0000,
                'label': 'Projectile resref' },

            { 'key': 'effect_block_off',
                'type': 'DWORD',
                'off': 0x0008,
                'label': 'Effect block offset' },

            { 'key': 'effect_block_size',
                'type': 'DWORD',
                'off': 0x000C,
                'label': 'Effect block size' },

            { 'key': 'unknown_10',
                'type': 'DWORD',
                'off': 0x0010,
                'label': 'Unknown 10' },

            { 'key': 'position',
                'type': 'POINT',
                'off': 0x0014,
                'label': 'Position' },

            { 'key': 'unknown_18',
                'type': 'WORD',
                'off': 0x0018,
                'label': 'Unknown 18' },
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
                'label': 'Unknown 14' },

            { 'key': 'unknown_18',
                'type': 'DWORD',
                'off': 0x0018,
                'label': 'Unknown 18' },

            { 'key': 'unknown_1C',
                'type': 'DWORD',
                'off': 0x001C,
                'label': 'Unknown 1C' },

            { 'key': 'unknown_20',
                'type': 'DWORD',
                'off': 0x0020,
                'label': 'Unknown 20' },

            { 'key': 'unknown_24',
                'type': 'DWORD',
                'off': 0x0024,
                'label': 'Unknown 24' },

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

            { 'key': 'pst_songflag_ids',
                'type': 'DWORD',
                'off': 0x0050,
                'enum': 'songflag',
                'label': 'PST SongFlag.IDS link' },

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

            { 'key': 'strref_0',
                'type': 'STRREF',
                'off': 0x0020,
                'label': 'Strref 0' },

            { 'key': 'strref_1',
                'type': 'STRREF',
                'off': 0x0024,
                'label': 'Strref 1' },

            { 'key': 'strref_2',
                'type': 'STRREF',
                'off': 0x0028,
                'label': 'Strref 2' },

            { 'key': 'strref_3',
                'type': 'STRREF',
                'off': 0x002C,
                'label': 'Strref 3' },

            { 'key': 'strref_4',
                'type': 'STRREF',
                'off': 0x0030,
                'label': 'Strref 4' },

            { 'key': 'strref_5',
                'type': 'STRREF',
                'off': 0x0034,
                'label': 'Strref 5' },

            { 'key': 'strref_6',
                'type': 'STRREF',
                'off': 0x0038,
                'label': 'Strref 6' },

            { 'key': 'strref_7',
                'type': 'STRREF',
                'off': 0x003C,
                'label': 'Strref 7' },

            { 'key': 'strref_8',
                'type': 'STRREF',
                'off': 0x0040,
                'label': 'Strref 8' },

            { 'key': 'strref_9',
                'type': 'STRREF',
                'off': 0x0044,
                'label': 'Strref 9' },

            { 'key': 'cre_resref_0',
                'type': 'RESREF',
                'off': 0x0048,
                'label': 'CRE resref 0' },

            { 'key': 'cre_resref_1',
                'type': 'RESREF',
                'off': 0x0050,
                'label': 'CRE resref 1' },

            { 'key': 'cre_resref_2',
                'type': 'RESREF',
                'off': 0x0058,
                'label': 'CRE resref 2' },

            { 'key': 'cre_resref_3',
                'type': 'RESREF',
                'off': 0x0060,
                'label': 'CRE resref 3' },

            { 'key': 'cre_resref_4',
                'type': 'RESREF',
                'off': 0x0068,
                'label': 'CRE resref 4' },

            { 'key': 'cre_resref_5',
                'type': 'RESREF',
                'off': 0x0070,
                'label': 'CRE resref 5' },

            { 'key': 'cre_resref_6',
                'type': 'RESREF',
                'off': 0x0078,
                'label': 'CRE resref 6' },

            { 'key': 'cre_resref_7',
                'type': 'RESREF',
                'off': 0x0080,
                'label': 'CRE resref 7' },

            { 'key': 'cre_resref_8',
                'type': 'RESREF',
                'off': 0x0088,
                'label': 'CRE resref 8' },

            { 'key': 'cre_resref_9',
                'type': 'RESREF',
                'off': 0x0090,
                'label': 'CRE resref 9' },

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
        
        # pst and bg/bg2/iwd formats differ in automap_note
        self.is_pst = False;
        
        self.actor_list = []
        self.infopoint_list = []
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
        self.automap_note_list = []
        self.automap_note_pst_list = []
        self.tiled_object_list = []
        self.projectile_trap_list = []
        self.song = None
        self.rest_interrupt = None


    def read (self, stream):
        self.read_header (stream)
        self.is_pst = self.header['automap_note_off'] == 0xffffffff
        
        if self.is_pst:
            self.read_header (stream, self.header2_pst_desc)
        else:
            self.read_header (stream, self.header2_desc)
        
        self.read_list (stream, 'actor')
        self.read_list (stream, 'infopoint')
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
        if self.is_pst:
            self.read_list (stream, 'automap_note_pst')
        else:
            self.read_list (stream, 'automap_note')
            
        self.read_list (stream, 'tiled_object')
        
        if not self.is_pst:
            self.read_list (stream, 'projectile_trap')

        obj = {}
        self.read_struc (stream, self.header['song_off'], self.song_desc, obj)
        self.song = obj

        obj = {}
        self.read_struc (stream, self.header['rest_interrupt_off'], self.rest_interrupt_desc, obj)
        self.rest_interrupt = obj


    def write (self, stream):
        off = self.get_struc_size (self.header_desc)

        off = self.write_list (stream, off, 'actor')
        off = self.write_list (stream, off, 'infopoint')
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
        if self.is_pst:
            off = self.write_list (stream, off, 'automap_note_pst')
        else:
            off = self.write_list (stream, off, 'automap_note')
        off = self.write_list (stream, off, 'tiled_object')
        if not self.is_pst:
            off = self.write_list (stream, off, 'projectile_trap')

        self.header['song_off'] = off
        self.write_struc (stream, off, self.song_desc, self.song)
        off += self.get_struc_size (self.song_desc)

        self.header['rest_interrupt_off'] = off
        self.write_struc (stream, off, self.rest_interrupt_desc, self.rest_interrupt)
        off += self.get_struc_size (self.rest_interrupt_desc)

        self.write_header (stream)
        if self.is_pst:
            self.write_header (stream, self.header2_pst_desc)
        else:
            self.write_header (stream, self.header2_desc)

    def printme (self):
        self.print_header ()
        if self.is_pst:
            self.print_header (self.header2_pst_desc)
        else:
            self.print_header (self.header2_desc)
            
        self.print_list ('actor')
        self.print_list ('infopoint')
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
        if self.is_pst:
            self.print_list ('automap_note_pst')
        else:
            self.print_list ('automap_note')
        self.print_list ('tiled_object')
        if not self.is_pst:
            self.print_list ('projectile_trap')
        self.print_struc (self.song, self.song_desc)
        self.print_struc (self.rest_interrupt, self.rest_interrupt_desc)


register_format ('AREA', 'V1.0', ARE_Format)

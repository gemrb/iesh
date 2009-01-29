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


from infinity.format import Format, register_format


class STOR_Format (Format):

    header_desc = (
            { 'key': 'signature',
                'type': 'STR4',
                'off': 0x0000,
                'label': 'Signature' },
            
            { 'key': 'version',
                'type': 'STR4',
                'off':0x0004,
                'label': 'Version'},

            { 'key': 'type',
                'type': 'DWORD',
                'off': 0x0008,
                'enum': { 0: 'Store', 1: 'Tavern', 2: 'Inn', 3: 'Temple' },
                'label': 'Type' },

            { 'key': 'name',
                'type': 'STRREF',
                'off': 0x000C,
                'label': 'Name strref' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0010,
                'mask':  { 0x0001: 'Sells items', 0x0002: 'Buys items', 0x0004: 'Identify', 0x0008: 'Steal', 0x0010: 'Donate', 0x0020: 'Cures', 0x00040: 'Drinks', 0x0080: 'Unknown bit7', 0x0100: 'Unknown bit8', 0x0200: 'Unknown bit9', 0x0400: 'Unknown/Recharge?', 0x0800: 'Unknown bit11', 0x1000: 'Buy fenced goods' },
                'label': 'Flags' },

            { 'key': 'sell_price_markup',
                'type': 'DWORD',
                'off': 0x0014,
                'label': 'Sell price markup (% of base price when store sells)' },

            { 'key': 'buy_price_markup',
                'type': 'DWORD',
                'off': 0x0018,
                'label': 'Buy price markup (% of base price when store buys)' },


            { 'key': 'depreciation_rate',
                'type': 'DWORD',
                'off': 0x001C,
                'label': 'Depreciation rate' },

            { 'key': 'steal_failure_chance',
                'type': 'WORD',  #FIXME: IESDP has DWORD here
                'off': 0x0020,
                'label': 'Steal failure chance' },

            { 'key': 'capacity',
                'type': 'WORD',  #FIXME: IESDP has DWORD here
                'off': 0x0022,
                'label': 'Capacity' },

            { 'key': 'unknown_24',
                'type': 'BYTES',
                'off': 0x0024,
                'size': 8,
                'label': 'Unknown 24' },

            { 'key': 'bought_item_off',
                'type': 'DWORD',
                'off': 0x002C,
                'label': 'Offset of items bought here' },

            { 'key': 'bought_item_cnt',
                'type': 'DWORD',
                'off': 0x0030,
                'label': 'Count of items bought here' },
  
              { 'key': 'sold_item_off',
                'type': 'DWORD',
                'off': 0x0034,
                'label': 'Offset of items for sale' },
  
            { 'key': 'sold_item_cnt',
                'type': 'DWORD',
                'off': 0x0038,
                'label': 'Count of items for sale' },
  
            { 'key': 'lore',
                'type': 'DWORD',
                'off': 0x003C,
                'label': 'Lore' },
  
            { 'key': 'id_price',
                'type': 'DWORD',
                'off': 0x0040,
                'label': 'ID price' },
  
            { 'key': 'rumours_tavern',
                'type': 'RESREF',
                'off': 0x0044,
                'label': 'Rumours (tavern)' },
  
            { 'key': 'drink_off',
                'type': 'DWORD',
                'off': 0x004C,
                'label': 'Offset to drinks' },
  
            { 'key': 'drink_cnt',
                'type': 'DWORD',
                'off': 0x0050,
                'label': 'Count of drinks' },
  
            { 'key': 'rumours_temple',
                'type': 'RESREF',
                'off': 0x0054,
                'label': 'Rumours (temple)' },
  
            { 'key': 'room_flags',
                'type': 'DWORD',
                'off': 0x005C,
                'mask': { 0x01: 'Peasant', 0x02: 'Merchant', 0x04: 'Noble', 0x08: 'Royal' },
                'label': 'Room type flags' },
  
            { 'key': 'price_peasant_room',
                'type': 'DWORD',
                'off': 0x0060,
                'label': 'Price of a peasant room' },
  
            { 'key': 'price_merchant_room',
                'type': 'DWORD',
                'off': 0x0064,
                'label': 'Price of a merchant room' },
  
            { 'key': 'price_noble_room',
                'type': 'DWORD',
                'off': 0x0068,
                'label': 'Price of a noble room' },
  
            { 'key': 'price_royal_room',
                'type': 'DWORD',
                'off': 0x006C,
                'label': 'Price of a royal room' },
  
            { 'key': 'cure_off',
                'type': 'DWORD',
                'off': 0x0070,
                'label': 'Offset to cures' },
  
            { 'key': 'cure_cnt',
                'type': 'DWORD',
                'off': 0x0074,
                'label': 'Count of cures' },
  
            { 'key': 'unknown_78',
                'type': 'BYTES',
                'off': 0x0078,
                'size': 36,
                'label': 'Unknown 78' },
            )

    bought_item_desc = (
            { 'key': 'type',
                'type': 'DWORD',
                'off': 0x0000,
                'enum': 'itemtypes',
                'label': 'Type' },
    )


    sold_item_desc = (
            { 'key': 'itm_resref',
                'type': 'RESREF',
                'off': 0x0000,
                'label': 'ITM resref' },

            { 'key': 'unknown_08',
                'type': 'WORD',
                'off': 0x0008,
                'label': 'Unknown 08' },

            { 'key': 'usage_1',
                'type': 'WORD',
                'off': 0x000A,
                'label': 'Usage 1/Stock amount' },

            { 'key': 'usage_2',
                'type': 'WORD',
                'off': 0x000C,
                'label': 'Usage 2' },

            { 'key': 'usage_3',
                'type': 'WORD',
                'off': 0x000E,
                'label': 'Usage 3' },

            { 'key': 'flags',
                'type': 'DWORD',
                'off': 0x0010,
                'mask': { 0x01: 'Identified', 0x02: 'Unstealable', 0x04: 'Stolen', 0x08: 'Undroppable' },
                'label': 'Flags' },

            { 'key': 'amount_in_stock',
                'type': 'DWORD',
                'off': 0x0014,
                'label': 'Amount in stock' },

            { 'key': 'infinite_supply_flag',
                'type': 'DWORD',
                'off': 0x0018,
                'label': 'Infinite supply flag (1=infinite stock)' },

            { 'key': 'trigger_strref',
                'type': 'STRREF',
                'off': 0x001C,
                'label': 'Trigger strref' },

            { 'key': 'unknown_20',
                'type': 'BYTES',
                'off': 0x0020,
                'size': 56,
                'label': 'Unknown 20' },
    )


    drink_desc = (
            { 'key': 'rumour_resref',
                'type': 'RESREF',
                'off': 0x0000,
                'label': 'Rumour resref' },

            { 'key': 'name',
                'type': 'STRREF',
                'off': 0x0008,
                'label': 'Drink name' },

            { 'key': 'price',
                'type': 'DWORD',
                'off': 0x000C,
                'label': 'Drink price' },

            { 'key': 'strength',
                'type': 'DWORD',
                'off': 0x0010,
                'label': 'Alcoholic strength' },
    )


    cure_desc = (
            { 'key': 'spl_resref',
                'type': 'RESREF',
                'off': 0x0000,
                'label': 'SPL resref' },

            { 'key': 'price',
                'type': 'DWORD',
                'off': 0x0008,
                'label': 'Price of this cure' },
    )


    def __init__ (self):
        Format.__init__ (self)
        self.expect_signature = 'STOR'

        self.bought_item_list = []
        self.sold_item_list = []
        self.drink_list = []
        self.cure_list = []


    def read (self, stream):
        self.read_header (stream)
        
        self.read_list (stream, 'bought_item')
        self.read_list (stream, 'sold_item')
        self.read_list (stream, 'drink')
        self.read_list (stream, 'cure')

    def write (self, stream):
        off = self.get_struc_size (self.header_desc)
        off = self.write_list (stream, off, 'sold_item')
        off = self.write_list (stream, off, 'drink')
        off = self.write_list (stream, off, 'cure')
        off = self.write_list (stream, off, 'bought_item')

        self.write_header (stream)


    def printme (self):
        self.print_header ()

        self.print_list ('bought_item')
        self.print_list ('sold_item')
        self.print_list ('drink')
        self.print_list ('cure')


        
register_format ('STOR', 'V1.1', STOR_Format)

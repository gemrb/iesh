# finding the maximum value of a stat
# remember to load game data first!
# look at restype_list in core.py to get format type values
cretype = 0x3f1
max = -100
name = ""
for r, o in ObjectIterator(type=cretype, names="none"):
     t = load_object (r['resref_name'], cretype).header['morale_recovery_time']
     if t > max:
         max = t
         name = r['resref_name']
print max, " first found in ", name

aretype = 0x3f2
# only show entries where ambient1 and ambient2 differ
unique = True

oi = ObjectIterator(type=aretype, names="none", error="msg")
for r, area in oi:
	if not area or not hasattr(area, "song"):
		print r['resref_name'],
		continue
	d1 = area.song['main_day_ambient_1']
	d2 = area.song['main_day_ambient_2']
	n1 = area.song['main_night_ambient_1']
	n2 = area.song['main_night_ambient_2']
	dv = str(area.song['main_day_ambient_volume'])
	nv = str(area.song['main_night_ambient_volume'])
	res = r['resref_name'] + " | Normal ambient count: " + str(len(area.ambient_list))
	show = False
	if d1 or d2:
		if d1 != d2 or not unique:
			res += " | day: " + d1 + ":" + d2
			show = True
	if n1 or n2:
		if n1 != n2 or not unique:
			res += " | night: " + n1 + ":" + n2
			show = True
	if nv != "100" or dv != "100":
		if nv != dv or not unique:
			res += " | vol: " + dv + ":" + nv
			show = True
	if show:
		print res

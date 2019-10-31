# search for dialogs with high flag bits set
# in vanilla versions, only edwinj of bg2 matches

dlgtype = 0x3f3

for r, dlg in ObjectIterator(type=dlgtype, names="none"):
	#print r['resref_name']
	for tr in dlg.transition_list:
		#print tr
		flg = tr['flags']
		if flg <= 0x100:
			continue
		print "dlg: " + str(r['resref_name']) + " / " + str(flg&0x1ff)
		dlg.print_transition(tr)

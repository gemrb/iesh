# verifying that pst indeed uses area name instead
# of wed name for resdata ini lookup (ar3006a)
#import string
aretype = 0x3f2
initype = 0x802

for r, o in ObjectIterator(type=aretype, names="none"):
	t = load_object (r['resref_name'], aretype).header['wed'].lower()
	name = (r['resref_name']).lower()
	try:
		wi = load_object (t, initype)
		wi = t + ".ids"
	except:
		wi = "none"
	try:
		ai = load_object (name, initype)
		ai = name + ".ids"
	except:
		ai = "none"
	if ai != wi:
		print name, "\thas wed:", t, "wed ini:", wi, "area ini:", ai


from pymindwave import headset
from pymindwave.pyeeg import bin_power
from datetime import timedelta, datetime
import sys, time, urllib2, json
import numpy as np
import os
def average(table):
	transposed = zip(*table)
	avg = lambda items: float(sum(items)) / len(items)
	averages = map(avg, transposed)
	return averages


if __name__ == "__main__":
	f=open("brainmove",'w')
	f.write("@relation neurosky \n")
	f.write("\n")
	f.write("@attribute delta real \n@attribute theta real \n@attribute loAlpha real \n@attribute hiAlpha real \n@attribute loBeta real \n@attribute hiBeta real \n@attribute loGamma real \n@attribute midGamma real \n@attribute movimiento {arriba,abajo} \n")
	f.write("\n \n@data \n")
	hs = headset.Headset('/dev/tty.MindWaveMobile-DevA')
	time.sleep(1)
	if hs.get_state() != 'connected':
		hs.disconnect()

	while hs.get_state() != 'connected':
		time.sleep(1)
		print 'current state: {0}'.format(hs.get_state())
		if (hs.get_state() == 'standby'):
			print 'trying to connect...'
			hs.connect()
	wave_list=list()
	for j in range(0,2):
		if j == 0:
			print "apreta enter y comienza a reaizar movimiento hacia arriba"
		else:
			print "apreta enter y comienza a realizar movimiento hacia abajo"
		raw_input()
		start=datetime.now()
		while (datetime.now()-start)<=timedelta(seconds=10):
			#print "Leyendo..."
			time.sleep(1);
			vector=hs.get('waves_vector')
			if hs.parser.poor_signal > 0:
				print "Poor Signal"
			else:
				print 'vector: {0}'.format(vector)
				f.write(str('{0}'.format(vector)).replace("[","").replace("]",""))
				if j == 0:
					f.write(',arriba')
				else:
					f.write(',abajo')
				f.write('\n')
				wave_list.append(vector)
	promedios=average(wave_list)
	print promedios
	print 'disconnecting...'
	hs.disconnect()
	f.close()
	hs.destroy()
	os.system('mv brainmove brain.arff')
	sys.exit(0)
import csv
import sys




class USBPacketTxn():
	def __init__(self,idx,op,dev,ep,timestmp,duration,data):
		self.op = op
		self.dev = dev
		self.idx = idx
		self.ep = ep
		self.microseconds = 0
		self.data = data
		self.children = []
		self.timestamp = 0
		self.timeFromTotalPhaseTimestamp(timestmp)
		self.duration = duration
	
	def addChild(self,pkttxn):
		self.children.append(pkttxn)

	def addChild(self,child):
		self.children.append(child)
	
	def dictData(self):
		return {'idx':self.idx,'op':self.op,'dev':self.dev,'ep':self.ep,'timstamp':self.microseconds,'data':self.data, 'duration':self.duration}

	def timeFromTotalPhaseTimestamp(self,ts):
		t = ts.split(':')
		n = t[1].split('.')
#		print(ts)
		self.microseconds =  ((int(t[0]) * 1000000) * 60) + (int(n[0]) * 1000000) + (int(n[1]) * 1000) + int(n[2])


#csv_record_index = 0

def getNextPacket(f,cr,offsetlist):

	packet_level0 = []
	for (si,ei) in offsetlist:
		for row in cr[si:ei+1]:
			if row['Record'][:6] in ['OUT tx','IN txn']:
				packet_level0.append(USBPacketTxn(int(row['Index']),"_".join(row['Record'].split()[:2]),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['Control Transfer']:
				packet_level0.append(USBPacketTxn(int(row['Index']),row['Record'].replace(' ','_'),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['Get Device Descriptor']:
				packet_level0.append(USBPacketTxn(int(row['Index']),row['Record'].replace(' ','_'),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['Set Address']:
				packet_level0.append(USBPacketTxn(int(row['Index']),row['Record'].replace(' ','_'),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['Get String Descriptor']:
				packet_level0.append(USBPacketTxn(int(row['Index']),row['Record'].replace(' ','_'),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['Get Device Qualifier Descriptor']:
				packet_level0.append(USBPacketTxn(int(row['Index']),row['Record'].replace(' ','_'),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['Get Configuration Descriptor']:
				packet_level0.append(USBPacketTxn(int(row['Index']),row['Record'].replace(' ','_'),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['Set Configuration']:
				packet_level0.append(USBPacketTxn(int(row['Index']),row['Record'].replace(' ','_'),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['   DATA0 packet','   DATA1 packet']:
				f.read(int(row['Len'].split()[0]))
			elif row['Record'][:9] in ['   IN txn','   OUT tx']:
				packet_level0.append(USBPacketTxn(int(row['Index']),"_".join(row['Record'].split()[:2]),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['   OUT packet','   IN packet']:
				f.read(int(row['Len'].split()[0]))
			elif row['Record'] in ['   ACK packet']:
				f.read(int(row['Len'].split()[0]))
			elif row['Record'] in ['   SETUP txn']:
				packet_level0.append(USBPacketTxn(int(row['Index']),"_".join(row['Record'].split()[:2]),int(row['Dev']),int(row['Ep']),row['m:s.ms.us'],row['Dur'],f.read(int(row['Len'].split()[0]))))
			elif row['Record'] in ['      DATA0 packet','      DATA1 packet']:
				f.read(int(row['Len'].split()[0]))
			elif row['Record'] in ['      OUT packet','      IN packet']:
				f.read(int(row['Len'].split()[0]))
			elif row['Record'] in ['      SETUP packet']:
				f.read(int(row['Len'].split()[0]))
			elif row['Record'] in ['      ACK packet']:
				f.read(int(row['Len'].split()[0]))
			elif 'IN-NAK]' in row['Record'].split():
				pass #trash
			elif row['Record'] == 'Capture started (Aggregate)':
				pass #trash
			else:
				print (row)
				print("\n\n")


	return packet_level0

def getTransmissionOffsetTuples(cr):
	record_offset = []
	
	prevrid = 0
	lasttxn = 0
	for rid in range(len(cr)):
		row = cr[rid]
		if 'Record' in row and 'Len' in row and row['Len'] != '':

			if row['Record'][:6] in ['OUT tx','IN txn']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid
		
			elif row['Record'] in ['Control Transfer']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid

			elif row['Record'] in ['Get Device Descriptor']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid

			elif row['Record'] in ['Set Address']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid

			elif row['Record'] in ['Get String Descriptor']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid

			elif row['Record'] in ['Get Device Qualifier Descriptor']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid

			elif row['Record'] in ['Get Configuration Descriptor']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid

			elif row['Record'] in ['Set Configuration']:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
					lasttxn = rid

			elif row['Record'] in ['   OUT packet','   IN packet','      OUT packet','      IN packet']:
				prevrid = rid

			elif row['Record'].strip() in ['DATA0 packet','DATA1 packet']:
				prevrid = rid

			elif row['Record'] in ['   ACK packet','      ACK packet']:
				prevrid = rid

			elif row['Record'][:9] in ['   IN txn','   OUT tx']:
				prevrid = rid

			elif row['Record'] in ['   SETUP txn']:
				prevrid = rid

			elif row['Record'] in ['      SETUP packet']:
				prevrid = rid

			else:
				if lasttxn != rid:
					record_offset.append((lasttxn,prevrid))
				
				lasttxn = rid

	return record_offset





filebasename = sys.argv[1]

f = open("%s.bin" % filebasename,"rb")
csv_file = open("%s.csv" % filebasename, mode='r')
#csv_file.readline()
csv_reader = csv.DictReader(csv_file)
cr = [x for x in csv_reader]
#print(cr)

offsets = getTransmissionOffsetTuples(cr)

print (offsets)

for p in getNextPacket( f,cr,offsets):
	print(p.dictData())
##print (i)

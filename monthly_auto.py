import os
import json
import xlwt
import glob
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory


font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.colour_index = 2
font0.bold = True
font0.align='center'
b_font= xlwt.Font()
b_font.name = 'Times New Roman'
b_font.bold = True
style0 = xlwt.XFStyle()
style1 = xlwt.XFStyle()
style0.font = font0
style1.font= b_font
#use of python-tk to choose directory for data analytics processing.
print "please choose your desired directory"
path = str(askdirectory())+'/'
print "path:",path
dirs = os.listdir(path)

for foldername in dirs:
	#print str(foldername)
	b=0
	print len(dirs)
	wb = xlwt.Workbook()
	ws = wb.add_sheet('Concentrator data')

	
	#ws.write(0, 1,beat_time, style0)
	ws.write(0, 0, 'Ecop',style1)
	ws.write(0, 1, 'Voltage',style1)
	ws.write(0, 2, 'Date Time',style1)
	ws.write(0, 3, 'Beat Time:',style1)
	path1 = path+str(foldername)
	#print path1
	folpath=os.listdir(path1)
	json_access=glob.glob(os.path.join(path1, '*.json'))
	
	for filename in json_access:
		#print filename
		print "length is  :",len(json_access)

		f = open(filename).read()
		
		#data = json.loads(f)
		try:		
		    data = json.loads(f)
		    print data['grid_name']

		    beat_time = data['snapshot_list'][0].values()[0]
		    print beat_time
		    node_list = data['snapshot_list'][0].values()[1]
		    #print node_list

		    a=len(node_list)
		    print "Length of node_list :",a

		#ws.write(1+b, 3,"Beat Time :",style0)
		#ws.write(1+b, 4,beat_time,style0)
		
		    i=range(0,a)
		    for x in i:
			#print "Voltage is :"+str(node_list[x]['voltage'])+" of meter :"+str(node_list[x]['address']
			ws.write(x+2+b, 0,str(node_list[x]['address']))
			ws.write(x+2+b, 1,str(node_list[x]['r_phase_voltage']))
			ws.write(x+2+b, 2,str(node_list[x]['date_time']))
			ws.write(x+2+b, 3,beat_time,style0)
		    b=(b+a)+2
		except ValueError:
		    pass
	try:
   	    os.stat(str(path)+"datacheck")
	except:
	    os.mkdir(str(path)+"datacheck")
	wb.save(str(path)+"datacheck/"+str(foldername)+".xls")
	#wb.save("/home/asus/conc_data_out/ls"+str(foldername)+".xls")

		#i=range(0,len(node_list))
		#for x in i:
		#	print "Voltage is :"+str(node_list[x]['voltage'])+" of meter :"+str(node_list[x]['address'])
		#print data
		#8cd7e85435f0ad04a0540037436ae9593608cf7f456bf8ff1d44f659572ec8dc *pycharm-professional-5.0.4.tar.gz This is the check Sum for the pyCharm
		#print js

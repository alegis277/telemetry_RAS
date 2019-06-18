import matplotlib.pyplot as plt
import numpy as np
import serial
import threading
import time
from matplotlib.widgets import Button


DIRECCION_SERIAL = "/dev/tty.holi-SPPDev"
BAUD_RATE = 230400
SALTO_DE_LINEA = '\n'
FIN_LINEA_CONSTANTES = '!'
VENTANA = 1500
ESCALA_ERROR = 100

global errorData, proportionalData, integralData, receiveData, receiveData, totalData
errorData = []
proportionalData = []
integralData = []
derivativeData = []
totalData = []
receiveData = True

global dataKp, dataTd, dataTi, dataVset

dataKp = 0
dataTd = 0
dataTi = 0
dataVset = 0

btSerial = serial.Serial(DIRECCION_SERIAL, baudrate=BAUD_RATE)
print("Connected to Line Follower")

def kill_node(evt):
	global receiveData
	receiveData = False

class Index(object):

	def MoreKp(self, event):
		btSerial.write("1".encode())

	def LessKp(self, event):
		btSerial.write("2".encode())

	def MoreTd(self, event):
		btSerial.write("3".encode())

	def LessTd(self, event):
		btSerial.write("4".encode())

	def MoreTi(self, event):
		btSerial.write("5".encode())

	def LessTi(self, event):
		btSerial.write("6".encode())

	def MoreVset(self, event):
		btSerial.write("7".encode())

	def LessVset(self, event):
		btSerial.write("8".encode())



def ServerBT():
	global errorData, proportionalData, integralData, receiveData, receiveData, totalData
	global dataKp, dataTd, dataTi, dataVset
	line = ""

	while(receiveData):

		try:

			received = btSerial.read().decode()
			line += received

			if received == SALTO_DE_LINEA:

				dataRcv = line.split(',')

				errorData.pop(0) if len(errorData)>VENTANA else None
				proportionalData.pop(0) if len(proportionalData)>VENTANA else None
				integralData.pop(0) if len(integralData)>VENTANA else None
				derivativeData.pop(0) if len(derivativeData)>VENTANA else None
				totalData.pop(0) if len(totalData)>VENTANA else None
					

				errorData.append(float(dataRcv[0])*ESCALA_ERROR)
				proportionalData.append(float(dataRcv[1]))
				integralData.append(float(dataRcv[2]))
				derivativeData.append(float(dataRcv[3]))
				totalData.append(proportionalData[-1]+integralData[-1]+derivativeData[-1])
				
				line = ""

			elif received == FIN_LINEA_CONSTANTES:

				dataRcv = line.strip(FIN_LINEA_CONSTANTES).split('#')

				dataKp = dataRcv[0]
				dataTd = dataRcv[1]
				dataTi = dataRcv[2]
				dataVset = dataRcv[3]

				#print('KP', dataRcv[0], '\t', 'TD', dataRcv[1], '\t', 'TI', dataRcv[2], '\t', 'Vset', dataRcv[3])


		except:
			line=""


threading.Thread(target=ServerBT).start()

plt.rcParams["figure.figsize"] = (14,7)
f, axes = plt.subplots(2,2)

axes[0,0].grid(b=True, which='major', color='#AAAAAA', linestyle='-')
axes[0,1].grid(b=True, which='major', color='#AAAAAA', linestyle='-')
axes[1,0].grid(b=True, which='major', color='#AAAAAA', linestyle='-')
axes[1,1].grid(b=True, which='major', color='#AAAAAA', linestyle='-')

axes[0,0].set_xlim(0,VENTANA)
axes[0,1].set_xlim(0,VENTANA)
axes[1,0].set_xlim(0,VENTANA)
axes[1,1].set_xlim(0,VENTANA)

#axes[0,0].set_ylim(-10,10)
#axes[0,1].set_ylim(-10,10)
#axes[1,0].set_ylim(-10,10)
#axes[1,1].set_ylim(-10,10)

distancia1Leyendas = 1.14
distancia2Leyendas = 1.27

f.canvas.mpl_connect('close_event', kill_node)

plt.ion()
plt.show()

addData = False

callback = Index()

ax1 = plt.axes([0.78, 0.01, 0.05, 0.04])
ax2 = plt.axes([0.85, 0.01, 0.05, 0.04])
ax3 = plt.axes([0.78-0.05*4, 0.01, 0.05, 0.04])
ax4 = plt.axes([0.85-0.05*4, 0.01, 0.05, 0.04])
ax5 = plt.axes([0.78-0.05*8, 0.01, 0.05, 0.04])
ax6 = plt.axes([0.85-0.05*8, 0.01, 0.05, 0.04])
ax7 = plt.axes([0.78-0.05*12, 0.01, 0.05, 0.04])
ax8 = plt.axes([0.85-0.05*12, 0.01, 0.05, 0.04])

bnext = Button(ax1, '- $V_{set}$')
bnext.on_clicked(callback.LessVset)
bprev = Button(ax2, '+ $V_{set}$')
bprev.on_clicked(callback.MoreVset)
bnext_1 = Button(ax3, '- $T_i$')
bnext_1.on_clicked(callback.LessTi)
bprev_1 = Button(ax4, '+ $T_i$')
bprev_1.on_clicked(callback.MoreTi)
bnext_2 = Button(ax5, '- $T_d$')
bnext_2.on_clicked(callback.LessTd)
bprev_2 = Button(ax6, '+ $T_d$')
bprev_2.on_clicked(callback.MoreTd)
bnext_3 = Button(ax7, '- $K_p$')
bnext_3.on_clicked(callback.LessKp)
bprev_3 = Button(ax8, '+ $K_p$')
bprev_3.on_clicked(callback.MoreKp)





while receiveData:

	if addData:
		dataPlotError.remove()
		#dataPlotP.remove()
		#dataPlotI.remove()
		#dataPlotD.remove()
		dataPlotError_1.remove()
		dataPlotError_2.remove()
		dataPlotError_3.remove()
		dataPlotP_sec.remove()
		dataPlotI_sec.remove()
		dataPlotD_sec.remove()
		dataPlotTotal.remove()
		kp_text.remove()
		td_text.remove()
		ti_text.remove()
		vset_text.remove()
		del dataPlotError
		#del dataPlotP
		#del dataPlotI
		#del dataPlotD
		del dataPlotError_1
		del dataPlotError_2
		del dataPlotError_3
		del dataPlotP_sec
		del dataPlotI_sec
		del dataPlotD_sec
		del dataPlotTotal
		del kp_text
		del td_text
		del ti_text
		del vset_text

	dataPlotError, = axes[0,0].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')
	#dataPlotP, = axes[0,0].plot(list(range(len(proportionalData))), proportionalData, c='darkmagenta', label='P')
	#dataPlotI, = axes[0,0].plot(list(range(len(integralData))), integralData, c='midnightblue', label='I')
	#dataPlotD, = axes[0,0].plot(list(range(len(derivativeData))), derivativeData, c='green', label='D')
	dataPlotTotal, = axes[0,0].plot(list(range(len(totalData))), totalData, c='black', label='Total')

	dataPlotError_1, = axes[0,1].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')
	dataPlotError_2, = axes[1,0].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')
	dataPlotError_3, = axes[1,1].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')

	dataPlotP_sec, = axes[0,1].plot(list(range(len(proportionalData))), proportionalData, c='darkmagenta', label='P')
	dataPlotI_sec, = axes[1,0].plot(list(range(len(integralData))), integralData, c='midnightblue', label='I')
	dataPlotD_sec, = axes[1,1].plot(list(range(len(derivativeData))), derivativeData, c='green', label='D')



	kp_text = plt.text(-2.5, 0.39, "%.2f"%(float(dataKp)), transform=plt.gca().transAxes)
	td_text = plt.text(1.5, 0.39, "%.2f"%(float(dataTd)), transform=plt.gca().transAxes)
	ti_text = plt.text(5.5, 0.39, "%.2f"%(float(dataTi)), transform=plt.gca().transAxes)
	vset_text = plt.text(9.5, 0.39, "%.2f"%(float(dataVset)), transform=plt.gca().transAxes)


	axes[0,0].legend(loc="upper center", bbox_to_anchor=[distancia1Leyendas, distancia2Leyendas], ncol=5)


	plt.draw()
	plt.pause(0.001)
	addData = True

	time.sleep(100E-3)






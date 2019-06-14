import matplotlib.pyplot as plt
import numpy as np
import serial
import threading
import time


DIRECCION_SERIAL = "/dev/tty.holi-SPPDev"
BAUD_RATE = 230400
SALTO_DE_LINEA = '\n'
VENTANA = 1500
ESCALA_ERROR = 100

global errorData, proportionalData, integralData, receiveData, receiveData, totalData
errorData = []
proportionalData = []
integralData = []
derivativeData = []
totalData = []
receiveData = True

btSerial = serial.Serial(DIRECCION_SERIAL, baudrate=BAUD_RATE)
print("Connected to Line Follower")

def kill_node(evt):
	global receiveData
	receiveData = False


def ServerBT():
	global errorData, proportionalData, integralData, receiveData, receiveData, totalData
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


while receiveData:

	if addData:
		dataPlotError.remove()
		dataPlotP.remove()
		dataPlotI.remove()
		dataPlotD.remove()
		dataPlotError_1.remove()
		dataPlotError_2.remove()
		dataPlotError_3.remove()
		dataPlotP_sec.remove()
		dataPlotI_sec.remove()
		dataPlotD_sec.remove()
		dataPlotTotal.remove()
		del dataPlotError
		del dataPlotP
		del dataPlotI
		del dataPlotD
		del dataPlotError_1
		del dataPlotError_2
		del dataPlotError_3
		del dataPlotP_sec
		del dataPlotI_sec
		del dataPlotD_sec
		del dataPlotTotal

	dataPlotError, = axes[0,0].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')
	dataPlotP, = axes[0,0].plot(list(range(len(proportionalData))), proportionalData, c='darkmagenta', label='P')
	dataPlotI, = axes[0,0].plot(list(range(len(integralData))), integralData, c='midnightblue', label='I')
	dataPlotD, = axes[0,0].plot(list(range(len(derivativeData))), derivativeData, c='green', label='D')
	dataPlotTotal, = axes[0,0].plot(list(range(len(totalData))), totalData, c='black', label='Total')

	dataPlotError_1, = axes[0,1].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')
	dataPlotError_2, = axes[1,0].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')
	dataPlotError_3, = axes[1,1].plot(list(range(len(errorData))), errorData, c='firebrick', label='Error')

	dataPlotP_sec, = axes[0,1].plot(list(range(len(proportionalData))), proportionalData, c='darkmagenta', label='P')
	dataPlotI_sec, = axes[1,0].plot(list(range(len(integralData))), integralData, c='midnightblue', label='I')
	dataPlotD_sec, = axes[1,1].plot(list(range(len(derivativeData))), derivativeData, c='green', label='D')

	axes[0,0].legend(loc="upper center", bbox_to_anchor=[distancia1Leyendas, distancia2Leyendas], ncol=5)


	plt.draw()
	plt.pause(0.001)
	addData = True

	time.sleep(100E-3)






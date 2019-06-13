import matplotlib.pyplot as plt
import numpy as np
import serial
import threading
import time

DIRECCION_SERIAL = "/dev/tty.holi-SPPDev"
BAUD_RATE = 230400
SALTO_DE_LINEA = '\n'
VENTANA = 1500

global errorData, proportionalData, integralData, receiveData, receiveData
errorData = []
proportionalData = []
integralData = []
derivativeData = []
receiveData = True

btSerial = serial.Serial(DIRECCION_SERIAL, baudrate=BAUD_RATE)
print("Connected to Line Follower")

def kill_node(evt):
	global receiveData
	receiveData = False


def ServerBT():
	global errorData, proportionalData, integralData, receiveData, receiveData
	line = ""

	while(receiveData):

		try:

			received = btSerial.read().decode()
			line += received

			if received == SALTO_DE_LINEA:

				if len(errorData)>VENTANA:
					errorData.pop(0)

				errorData.append(float(line))
				
				line = ""
		except:
			line=""


threading.Thread(target=ServerBT).start()

f, ax1 = plt.subplots()

ax1.grid(b=True, which='major', color='#AAAAAA', linestyle='-')

plt.xlim(0,VENTANA)
#plt.ylim(-25,25)

f.canvas.mpl_connect('close_event', kill_node)

plt.ion()
plt.show()

addData = False

while receiveData:

	if addData:
		dataPlot.remove()
		del dataPlot

	dataPlot, = plt.plot(list(range(len(errorData))), errorData, c='firebrick')

	plt.draw()
	plt.pause(0.001)
	addData = True

	time.sleep(10E-3)






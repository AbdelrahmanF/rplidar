#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import re
import os
from fsplit.filesplit import FileSplit
import time
import struct

in_file_idx = 0
PORT_NAME = 'COM4'
DMAX = 4000
IMIN = 0
IMAX = 50


def update_line(num, iterator, line):
    #print("update_line***********")
    scan = next(iterator, "over and out")
    #print(scan)
    #print(len(scan))
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    #print(offsets)
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,


def split_input():
	#https://stackoverflow.com/questions/16289859/splitting-large-text-file-into-smaller-text-files-by-line-numbers-using-python
	#Matt Anderson
	lines_per_file = 360
	smallfile = None
	file_idx = 0
	with open('C:/Users/afahmy/Downloads/rplidar-master/examples/read.txt') as bigfile:
		for lineno, line in enumerate(bigfile):
			if lineno % lines_per_file == 0:
				if smallfile:
					smallfile.close()
					file_idx += 1
				small_filename = './temp/scan_{}.txt'.format(file_idx)
				smallfile = open(small_filename, "w")
			smallfile.write(line)
		if smallfile:
			smallfile.close()


def load_scans():
    #print("my_gen***********")
    i = 1
    global in_file_idx
    #print(in_file_idx) 
    file_list = os.listdir('C:/Users/afahmy/Downloads/rplidar-master/examples/temp/')
    #print(file_list)
    temp_tuple = ()
    ftuple = []
    temp_line = [[0] * 360 for i in range(360)]
    temp_idx = 0
    while in_file_idx < len(file_list):
        #print("in_file_idx")
        print(in_file_idx)
        with open('C:/Users/afahmy/Downloads/rplidar-master/examples/temp/'+file_list[in_file_idx]) as file:
            iterator = [tuple(line.split()) for line in file.readlines()]   
 
        iter_idx = 0 
        tuple_idx = 0
        #print(iterator)
        while iter_idx < len(iterator):
            temp_tuple = tuple([int(iterator[iter_idx][1]), float(iterator[iter_idx][2]), float(iterator[iter_idx][3])])
            iterator[iter_idx] = temp_tuple

            iter_idx += 1
        #print(iterator) 
        in_file_idx += 1
        yield iterator
            


def run():
	#lidar = RPLidar(PORT_NAME)
	split_input()
	fig = plt.figure()
	ax = plt.subplot(111, projection='polar')
	line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX], cmap=plt.cm.Greys_r, lw=0)
	ax.set_rmax(DMAX)
	ax.grid(True)

	iterator = load_scans()
	#print(iterator)
	ani = animation.FuncAnimation(fig, update_line,fargs=(iterator, line), interval=50)
	plt.show()
	#lidar.stop()
	#lidar.disconnect()

if __name__ == '__main__':
	run()

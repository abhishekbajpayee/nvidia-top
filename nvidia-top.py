import subprocess as sp
import xml.etree.ElementTree as ET
import time
import os
import sys
import curses as crs

def display_info(root, scr):

    gpunum = 0

    for gpu in root.findall('gpu'):
        
        # Name
        name = gpu.find('product_name').text
        
        # Memory Use
        mem = gpu.find('memory_usage')
        memu = mem.find('used').text
        nmemu = memu.split()
        memt = mem.find('total').text
        nmemt = memt.split()
        memuse = memu + '/' + memt
        usage = float(nmemu[0])*100/float(nmemt[0])
        
        # Power Use
        pow = gpu.find('power_readings')
        upow = pow.find('power_draw').text
        tpow = pow.find('power_limit').text
        powuse = upow + '/' + tpow
        
        # Temp
        temp = gpu.find('temperature')
        temp = temp.find('gpu_temp').text
        
        line = '%3d' % gpunum + '%25s' % name + '%20s' % memuse + '%15.2f' % usage + '%15s' % powuse + '%10s' % temp
        scr.addstr(gpunum+8, 0, line)

        gpunum = gpunum+1

# ---Main Section---

width = 88

data = sp.check_output(['nvidia-smi', '-q', '-x'])
root = ET.fromstring(data)

timestamp = root.find('timestamp').text
driver = root.find('driver_version').text
n = int(root.find('attached_gpus').text)

scr = crs.initscr()
scr.keypad(1)

scr.addstr(0, 0, 'nvidia-top' + '%*s' % (width-10, 'ESC to quit'))
scr.addstr(1, 0, 'Timestamp:\t' + timestamp)
scr.addstr(2, 0, 'Driver Version:\t' + driver)
scr.addstr(3, 0, 'Number of GPUs:\t' + repr(n))

# Drawing header
scr.addstr(5, 0, '-' * width)
scr.addstr(6, 0, '%3s' % '#' + '%25s' % 'Name' + '%20s' % 'Mem. Use' + '%15s' % '% Mem. Use' + '%15s' % 'Pow. Use' + '%10s' % 'Temp.')
scr.addstr(7, 0, '-' * width)

# 10 tenths = 1 sec <- this is the polling frequency
crs.halfdelay(10)

while (1):
    
    data = sp.check_output(['nvidia-smi', '-q', '-x'])
    root = ET.fromstring(data)

    timestamp = root.find('timestamp').text
    scr.addstr(1, 0, 'Timestamp:\t' + timestamp)

    display_info(root, scr)

    scr.refresh()
    
    key = scr.getch()
    if (key == 27):
        break

crs.endwin()

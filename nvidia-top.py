import subprocess as sp
import xml.etree.ElementTree as ET
import time
import os
import sys
import curses as crs

def header(csr):
    
    csr.addstr(4, 0, '----------------------------------------------------------------------------------------')
    csr.addstr(5, 0, '%3s' % '#' + '%25s' % 'Name' + '%20s' % 'Mem. Use' + '%15s' % '% Mem. Use' + '%15s' % 'Pow. Use' + '%10s' % 'Temp.')
    csr.addstr(6, 0, '----------------------------------------------------------------------------------------')

def display_info(root, scr):

    gpunum = 0

    for gpu in root.findall('gpu'):
        
        # Name
        name = gpu.findall('product_name')
        name =  name[0].text
        
        # Memory Use
        mem = gpu.findall('memory_usage')
        memu = mem[0][1].text
        nmemu = memu.split()
        memt = mem[0][0].text
        nmemt = memt.split()
        memuse = memu + '/' + memt
        usage = float(nmemu[0])*100/float(nmemt[0])
        
        # Power Use
        pow = gpu.findall('power_readings')
        pow = pow[0]
        upow = pow[2].text
        tpow = pow[3].text
        powuse = upow + '/' + tpow
        
        # Temp
        temp = gpu.findall('temperature')
        temp = temp[0]
        temp = temp[0].text
        
        line = '%3d' % gpunum + '%25s' % name + '%20s' % memuse + '%15.2f' % usage + '%15s' % powuse + '%10s' % temp
        scr.addstr(gpunum+8, 0, line)

        gpunum = gpunum+1

# ---Main Section---

width = 88

data = sp.check_output(['nvidia-smi', '-q', '-x'])
root = ET.fromstring(data)

timestamp = root[0].text
driver = root[1].text
n = int(root[2].text)

scr = crs.initscr()
scr.keypad(1)

scr.addstr(0, 0, 'nvidia-top' + '%*s' % (width-10, 'ESC to quit'))
scr.addstr(1, 0, 'Timestamp:\t' + timestamp)
scr.addstr(2, 0, 'Driver Version:\t' + driver)
scr.addstr(3, 0, 'Number of GPUs:\t' + repr(n))

# Drawing header
scr.addstr(4, 0, '-' * width)
scr.addstr(5, 0, '%3s' % '#' + '%25s' % 'Name' + '%20s' % 'Mem. Use' + '%15s' % '% Mem. Use' + '%15s' % 'Pow. Use' + '%10s' % 'Temp.')
scr.addstr(6, 0, '-' * width)

# 10 tenths = 1 sec <- this is the polling frequency
crs.halfdelay(10)

while (1):
    
    data = sp.check_output(['nvidia-smi', '-q', '-x'])
    root = ET.fromstring(data)

    timestamp = root[0].text
    scr.addstr(1, 0, 'Timestamp:\t' + timestamp)

    display_info(root, scr)

    scr.refresh()
    
    key = scr.getch()
    if (key == 27):
        break

crs.endwin()

import os
os.system("cat /proc/cpuinfo | grep -m 3 'model name\|cpu cores\|vendor_id' > japerez_systemDetails.txt")
os.system('cat /proc/version >> japerez_systemDetails.txt')

os.system('cat /proc/uptime >> uptime.txt')
# code to read time and write to file - Uptime since last boot
with open('uptime.txt') as f:
    timeUp = f.read().split()
# converting input seconds to dd:hh:mm:ss: format
secsleft = float(timeUp[0])
days = int(secsleft // (3600 * 24))
secsleft -= days*3600 * 24
hours = int(secsleft // 3600)
secsleft -= hours * 3600
mins = int(secsleft // 60)
secsleft -= mins*60
wFormat = str(days).zfill(2) + ':' + str(hours).zfill(2) + ':' + str(mins).zfill(2) + ':' + str(int(secsleft)).zfill(2) + '\n'
uptime = 'Time since last boot:\t' + wFormat
# writing to systemdetails file
sysdetails = open('japerez_systemDetails.txt', 'a')
sysdetails.write(uptime)
sysdetails.close()

#Reading boot logs and converting to format
os.system("/proc/self/root/usr/bin/last > bootlog.txt")
with open('bootlog.txt') as f:
	log = f.readlines()
bootline = log[3].split()
boottime = bootline[7]
lastboot = 'Last boot time:\t\t\t' + '00:' + boottime + ':00'
#Writing to systemdeatils file
sysdetails = open('japerez_systemDetails.txt', 'a')
sysdetails.write(lastboot)
sysdetails.close()

os.system('cat /proc/diskstats > disk.txt')
# Reading and summing successful disk reads to find total disk requests
# Successful reads is in column 4 or in list[3]
with open('disk.txt') as f:
    diskinfo = f.readlines()
lines = list()
for i in diskinfo:
	lines.append(i.split())
sum = 0
for i in range(len(lines)):
    sum += int(lines[i][3])
total = '\nDisk Requests made:\t\t' + str(sum) + '\nNumber of Processes:\t'
sysdetails = open('japerez_systemDetails.txt', 'a')
sysdetails.write(total)
sysdetails.close()

#Getting # of processes created since last boot
os.system('ls /proc | grep ''[0-9]'' | wc -l >> japerez_systemDetails.txt')

#File clean up
os.system('rm -r uptime.txt')
os.system('rm -r disk.txt')
os.system('rm -r bootlog.txt')

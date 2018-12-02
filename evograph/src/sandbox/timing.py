'''
Created on Dec 2, 2018

@author: Brandon
'''


import datetime
import time
from multiprocessing import Pool
import os
import sys
#===============================================================================
# 
# start = datetime.datetime.now()
# time.sleep(5)
# finish = datetime.datetime.now()
# print (finish - start).seconds
#===============================================================================

#pool = multiprocessing.Pool()
#print pool._processes

#print os.cpu_count

#print multiprocessing.cpu_count()

#pool = Pool(processes=451)
#pool.close()



def test(num):
    print num
    


print '-----------------'
iterRange = list(range(0, 3))
start = datetime.datetime.now() 
#p = Pool(100)
#p.map(test, iterRange)
time.sleep(2)
finish = datetime.datetime.now()
print finish - start
dif = (finish - start).total_seconds()
print dif

print '-----------------'
        
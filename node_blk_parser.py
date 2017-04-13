# Author: Pratik Mishra, Iowa State University

import os
import sys
import operator
import csv

from sys import argv
from operator import itemgetter, attrgetter, methodcaller

size_of_disk = 250  # 250 GB disk

total_no_banks = (size_of_disk*1024/128)        # Total Bank Counts 128MB banks

def output_to_file(output_banks=[],*args):
        #print "Banks:%s\n" % output_banks
        notzero = 0 # Banks which donot have 0 access
        # all banks not used
        for k in output_banks:
                if k[1] !=0:
                        notzero +=1
        number_used_banks =  notzero
        print "Number of Used Banks:%d\n" % number_used_banks

        with open((sys.argv[1]+'_bank_list.csv'),'w+') as bank_file:
                bank_file.write("Bank,MB Accessed")
                bank_file.write("\n")
                writer = csv.writer(bank_file, delimiter=',')
                writer.writerows(output_banks)

        bank_file.close()
def read_blkfile():

        #counters
        counter_total = 0
        counter_write = 0
        counter_read = 0

        # Number of Blocks Read/Written
        number_blocks_written = 0
        number_blocks_read = 0

        # data tranfer variables
        total_read_MB = 0.0
        total_write_MB = 0.0
        read_MB = 0.0
        write_MB = 0.0
        lba = 0         # Logical block Address
        xfrlen = 0	# transfer length corresponding to the specifc event

        store = []
       # Bank Variables
        size_of_disk = 250  # 250 GB disk

        total_no_banks = (size_of_disk*1024/128)        # Total Bank Counts 128MB banks
        Bank = [0]*total_no_banks	# Bank number
        data_banks = [0]*total_no_banks

        sorted_banks = []	# According to access count
        top_20_percent = []
        no_of_banks_intop20 = 0
        # Zip for dictionary
        wrap = {}
        data_intop20 = 0.0
        total_data_inall = 0.0
        counter_greater_128MB = 0
        counter_less_128MB = 0
        with open(sys.argv[1],'r') as teragen_file:
                for line in teragen_file:
                        l = line.strip()        # remove whitespaces from beginning and end
                        store_line = l.split()  # split a line according to whitespaces between


                        try:
                            	if (store_line[0].find(',') == 1) and (int(store_line[4])==0) and (store_line[5]== 'C'):                          
                                        counter_total = counter_total + 1
                                        lba = int(store_line[7])
                                        xfrlen = int(store_line[9])
                                        if (xfrlen >= 256):
                                                counter_greater_128MB += 1
                                        else:
                                             	counter_less_128MB += 1
                                        if store_line[6] == ('W' or 'WS'):
                                                counter_write += 1
                                                number_blocks_written += xfrlen
                                                write_MB = float(xfrlen)*512.0/(1024.0*1024.0)
                                                total_write_MB += write_MB
                                                Bank [(lba+xfrlen)*512/(128*1024*1024)] += 1	  # 128 MB = Bank Size as Hadoop
                                                data_banks[(lba+xfrlen)*512/(128*1024*1024)] += write_MB           

                                        if store_line[6] == 'R':
                                                counter_read += 1
                                                number_blocks_read += xfrlen
                                                read_MB =float(xfrlen)*512.0/(1024.0*1024.0)
                                                total_read_MB += read_MB
                                                Bank [(lba+xfrlen)*512/(128*1024*1024)] += 1
                                                data_banks[(lba+xfrlen)*512/(128*1024*1024)] += read_MB


                        except IndexError:
                                continue

        #Bank Counters

        total_no_banks = len(Bank)
        wrap = zip(Bank,data_banks)
        sorted_banks = sorted(wrap,key=itemgetter(0),reverse=True) # In descending order
        no_of_banksintop20 = 20*total_no_banks/100

        output_to_file(sorted_banks)


        percent_write = (float(counter_write/float(counter_total))*100)
        percent_read =  (float(counter_read/float(counter_total))*100)
        print "Total:%d\n" % counter_total
        print "Write:%d\n" % counter_write
        print "Read:%d\n" % counter_read
        print "Percentage Read:%f\n" % percent_read
        print "Percentage Write:%f\n" % percent_write
        print "Data Write:%f\n" % total_write_MB
        print "Data Read:%f\n" % total_read_MB
        print "Requests greater than 128 MB:%d\n" % counter_greater_128MB
        print "Requests less than 128 MB:%d\n" % counter_less_128MB
        print "number of blocks written:%d\n" % (number_blocks_written)
        #print " Banks:%s\n"% Bank


        print "Total Number of Banks:%d\n"% total_no_banks

        #print "Sorted Banks:%s\n" %sorted_banks



        teragen_file.close()






def main():

	size_of_disk = 250  # 250 GB disk

        total_no_banks = (size_of_disk*1024/128)        # Total Bank Counts 128MB banks

        read_blkfile()

main()



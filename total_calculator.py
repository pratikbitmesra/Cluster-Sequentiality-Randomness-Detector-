# This is the first line of defence to tackle large traces
# Pratik Mishra, Iowa State University
# The traces we are dealing are more than atleast 15GB of traces. 
# Hence, this program reads through the traces and generates a csv
# with the required information we want.
# Compile using: python extract_info.py trace_file_from_system
# The output would be a trace_file_from_system_useful_info.csv
# We need this so that we reduce the data we need to deal for
# analysis to only useful data and we dont need to run through
# the trace files again and again.
# The output csv would be 
#
import os
import sys
import operator
import csv

from sys import argv
from operator import itemgetter, attrgetter, methodcaller


size_of_disk = 250  # 250 GB disk
total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts 128MB banks
     
def output_to_file(output_bins=[],*args):

        
def read_blkfile():


        
        size_of_disk = 250  # 250 GB disk
        total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts 128MB banks
        
        lba = 0
        xfrlen = 0
        timestamp = 0.0
        operation = 0
        bin_number = 0
        
        lba_list = []
        xfrlen_list = []
        timestamp_list = []
        operation_list = []
        bin_list = []
        
        wrap = {}
        
        with open(sys.argv[1],'r') as teragen_file:
                for line in teragen_file:
                        l = line.strip()        # remove whitespaces from beginning and end
                        store_line = l.split()  # split a line according to whitespaces between


                        try:
                                if (store_line[0].find(',') == 1) and (int(store_line[4]
                                ==0)) and (store_line[5]=='C'):
                                        lba = int(store_line[7])
                                        xfrlen = int(store_line[9])
                                        timestamp = float(store_line[3])
                                        operation = store_line[6]
                                        bin_number = int((lba+xfrlen)*512/(128*1024*1024))
                                        
                                        
                                        
                                        lba_list.append(lba)                
                                        xfrlen_list.append(xfrlen)
                                        timestamp_list.apped(timestamp)
                                        operation_list.append(operation)
                                        bin_list.append(bin_number)
                                        
                        
                        except IndexError:
                                continue
        
        
        wrap = zip(bin_list,lba_list,xfrlen_list,operation_list,timestamp_list)
        
        output_to_file(wrap)
        
        teragen_file.close() 


def main():

	size_of_disk = 250  # 250 GB disk

        total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts 128MB banks

        read_blkfile()

main()


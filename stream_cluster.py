# Program 2: stream_cluster.py : Differentiates streams from disturbances
# Author: Pratik Mishra, Iowa State University.
# Compile : python stream_locator.py trace_file_from_system_extracted_info.csv
# The input file is the output from extract_info.py
# Output:trace_file_from_system_extracted_info.csv_bin_info.csv
# Format



import os
import sys
import operator
import csv
import itertools

from itertools import groupby
from sys import argv
from operator import itemgetter, attrgetter, methodcaller


size_of_disk = 250  # 250 GB disk
total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts. each bin os 128MB



def read_extracted_csv():

        
        size_of_disk = 250  # 250 GB disk
        total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts 128MB banks
        
        
        lba_list = []
        xfrlen_list = []
        timestamp_list = []
        operation_list = []
        bin_list = []
        
        clustered_bins = []
        
        flag = 0             # REMOVE the headings of the csv "bin_number,lba,xfrlen,operation,timestamp"
        
        with open(sys.argv[1],'r') as extracted_csv:
                for line in extracted_csv:
                        l = line.strip()        # remove whitespaces from beginning and end
                        store_line = l.split(',')  # split a line according to ',' as CSV is comma separated 
                        
                        
                        try:
                                if (flag == 1):
                                        bin_list.append(int(store_line[0]))
                                        lba_list.append(int(store_line[1]))
                                        xfrlen_list.append(int(store_line[2]))
                                        operation_list.append(store_line[3])
                                        timestamp_list.append(float(store_line[4]))
                                        
                                        
                        
                                flag = 1
                        except IndexError:
                                continue

        
        
        extracted_csv.close()
        
        clustered_bins=[list(v) for k,v in itertools.groupby(bin_list)]
        bin_number = []
        bin_count = []
        end_time = []
        xfrlen_bin_sum = []
        #xfrlen_sum = 0
        counter = 0
        flag_counter = 0
        for y in clustered_bins:
                bin_number.append(y[len(y)-1])
                bin_count.append(len(y))
                counter = counter + len(y)
                
                end_time.append(timestamp_list[counter-1])                
                xfrlen_bin_sum.append(sum(xfrlen_list[flag_counter:counter])/(2*1024.0))
                flag_counter = flag_counter + len(y)                
                        
        single_bin = []
        single_bin = zip(bin_number,bin_count,xfrlen_bin_sum,end_time)
        with open((sys.argv[1]+'_bin_info.csv'),'w+') as bin_info_file:
                bin_info_file.write("bin_number,bin_count,xfrlen_bin_sum,end_time")
                bin_info_file.write("\n")
                writer = csv.writer(bin_info_file, delimiter=',')
                writer.writerows(single_bin)

        bin_info_file.close()
        
def main():

	size_of_disk = 250  # 250 GB disk

        total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts 128MB banks

        read_extracted_csv()

main()

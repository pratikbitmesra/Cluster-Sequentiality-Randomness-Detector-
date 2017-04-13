#3. bins_vs_xfrlen.py: FInd the index of bins where they occur, add the xfrlen to find total xfrlen
# Author: Pratik Mishra, Iowa State University
# Compile: python bin_vs_xfrlen.py trace_file_from_system_extracted_info.csv_bin_info.csv
# Output from bin_cluster is input to this progrm
# Output is a file named trace_file_from_system_extracted_info.csv_bin_info.csv_bin_vs_xfrlensum.csv

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
        
       
        bin_number = []
        bin_count = []
        xfrlen_bin_sum = []
        end_time = []
        operation_bin = []
        #bin_list = []
        
        clustered_bins = []
        
        flag = 0             # REMOVE the headings of the csv "bin_number,lba,xfrlen,operation,timestamp"
        
        with open(sys.argv[1],'r') as extracted_csv:
                for line in extracted_csv:
                        l = line.strip()        # remove whitespaces from beginning and end
                        store_line = l.split(',')  # split a line according to ',' as CSV is comma separated 
                        
                        
                        try:
                                if (flag == 1):
                                #if (flag == 1 and (store_line[3] == "W" or store_line[3]=="WS")): # for writes
                                        bin_number.append(int(store_line[0]))
                                        bin_count.append(int(store_line[1]))
                                        xfrlen_bin_sum.append(float(store_line[2]))
                                        operation_bin.append(store_line[3])
                                        end_time.append(store_line[4])
                                        #timestamp_list.append(float(store_line[4]))
                                        
                                        
                        
                                flag = 1
                        except IndexError:
                                continue

        
        
        extracted_csv.close()
        
        #clustered_bins=[list(v) for k,v in itertools.groupby(bin_list)]
        bin_full_number = []
        bin_full_count = []
        end_full_time = []
        xfrlen_full_sum = []
        already_read = []
        #xfrlen_sum = 0
        counter = 0
        count_sum = 0
        xfrlen_sum = 0
        flag_counter = 0
        for y in bin_number:
                if ((y in already_read) == False):
                        indx = [i for i,x in enumerate(bin_number) if x == y]
                        bin_full_number.append(y)
                        for x in indx:
                                count_sum = count_sum+bin_count[x]
                                xfrlen_sum = xfrlen_sum+xfrlen_bin_sum[x]
                        xfrlen_full_sum.append(xfrlen_sum)
                        bin_full_count.append(count_sum)
                        end_full_time.append(end_time[indx[len(indx)-1]])                        
                        already_read.append(bin_number[indx[len(indx)-1]])
                        
                        indx = []
                        count_sum = 0           
                        xfrlen_sum = 0
        single_bin = []
        #single_bin = zip(bin_full_number,bin_full_count,xfrlen_full_sum,end_full_time)
        single_bin = sorted(zip(bin_full_number,bin_full_count,xfrlen_full_sum,end_time),key=itemgetter(3),reverse=False)
        with open((sys.argv[1]+'_bin_vs_xfrlensum_write.csv'),'w+') as bin_info_file:
                bin_info_file.write("bin_number,bin_full_count,xfrlen_full_sum,end_full_time")
                bin_info_file.write("\n")
                writer = csv.writer(bin_info_file, delimiter=',')
                writer.writerows(single_bin)

        bin_info_file.close()
        
def main():

	size_of_disk = 250  # 250 GB disk

        total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts 128MB banks

        read_extracted_csv()

main()

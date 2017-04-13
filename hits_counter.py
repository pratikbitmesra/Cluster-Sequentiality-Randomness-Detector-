# Program 3: python hits_counter.py terasort200_new_extracted_info.csv terasort200_new_2_extracted_info.csvra.csv
# Author: Pratik Mishra, Iowa State University



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
                        
        ### For calculating streams and randomness
        out = []
        out_xfrlen = []
        d = []
        c = []
        ra = [] 
        ra_xfrlen = []
        tolerance = [1,-1,2,-2,0]      
        count = 0
        first = bin_number[0]
        last = 0
        flag = 0
        for x in bin_number:
                if (x-first) in tolerance:
                        d.append(first)
                elif ((count>1) and ((first-bin_number[count-2]) in tolerance)):
                        d.append(first)
                        out.append(d) # streams
                        #flag = flag + len(d)
                        #for y in d:
                                #out_xfrlen.append(sum(xfrlen_bin_sum[flag-len(d):flag]))
                        d = []
                else:
                        
                        #c.append(bin_number[count-1])
                        ra.append(bin_number[count-1]) #random
                        #flag = flag + 1
                        #d = []
                        #c = []
                
                count = count + 1
        
                first = x
        rand_bin = []
        flag = 0
        with open(sys.argv[2],'r') as bin_info_random: 
                for line in bin_info_random:
                        l1 = line.strip()        # remove whitespaces from beginning and end
                        store_line1 = l1.split(',')  # split a line according to ',' as CSV is comma separated 
                        
                        
                        try:
                                if (flag == 1):
                                        rand_bin.append(int(store_line1[0]))
                                        
                                        
                                        
                        
                                flag = 1
                        except IndexError:
                                continue
        bin_info_random.close()
        hits = 0
        #print ra
        for element in rand_bin:
                if element in ra:
                        hits = hits + 1
        #hits = [list(set(ra).intersection(rand_bin))]
        print "HITS:%d" %hits
        print "Randomness %d" % len(ra)
        
        ## fOR Event Based in same bin
        time_hits = 0
        for x in rand_bin[0:2500]:
                if x in rand_bin[2500:(len(rand_bin)-2)]:
                         time_hits = time_hits + 1
        print "TIME-HITS:%d" %time_hits  
def main():

	size_of_disk = 250  # 250 GB disk

        total_no_bins = (size_of_disk*1024/128)        # Total Bin Counts 128MB banks

        read_extracted_csv()

main()

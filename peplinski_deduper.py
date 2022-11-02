#!/usr/bin/env python

#This is the python script for deduplicating SAM files from PCR amplification
#Use regex to separate CIGAR strings by letter

import argparse
import re
import bioinfo

def get_args():
    #defines variables
    parser = argparse.ArgumentParser(description="This script is for the deduplication of PCR reads, leaving only a single copy of each read. -f, -o, and -u are required variables.")
    parser.add_argument("-f", help="inputs the absolute path to a sorted SAM file (*.sam) for deduplication.", required=True)
    parser.add_argument("-o", help="creates a SAM file (*.sam) into which the single copies of each read will be written. If absolute path is not \
    given, will create the file in the present working directory.", required=True)
    parser.add_argument("-u", help="the absolute path to a text file (*.txt) containing a list of UMIs separated by line breaks.", required=True)
    return parser.parse_args()
args=get_args()

#initialize a set to store chr, adj pos, strand, and UMI
samset = set()
umiset = set()

#unknown umi counter
unknownumi = 0

#opens files for reading & writing and assigns them abbreviations
fh = open(args.f, "r")
fw = open(args.o, "w")
fu = open(args.u, "r")

#adds the umis from the input file to a set
for x in fu:
    x = x.strip('\n')
    umiset.add(x)

#the main deduper functions
while True:
    line = fh.readline()
    if line == "": #when the readline reaches an empty line it stops
        break
    if line.startswith("@"): #writing out the header lines to the output
        fw.write(line)
    else:
        splitline = line.split('\t') #splits the file into columns separated by tabs
        umi = splitline[0].split(":")[7] #finding the umi in the remaining lines
        if umi not in umiset: #looks through the umi set and confirms whether the umi matches 
            unknownumi += 1
            continue
        chrom = splitline[2] #to add chromosome number
        flag = int(splitline[1]) #interprets the bitwise flag
        if((flag & 16) == 16): #reverse strand
            strand = ("-")
            total = bioinfo.reverse_adj_position(splitline[5], int(splitline[3])) #finds the bioinfo reverse function
        else:
            strand = ("+") #forward strand
            total = bioinfo.forward_adj_position(splitline[5], int(splitline[3])) #finds the bioinfo forward function
        info = (chrom, total, strand, umi) #adds the necessary information to a tuple
        if info not in samset: #if the tuple is in the set, don't add it again
            samset.add(info) #otherwise, add the tuple to the set
            fw.write(line) #and write the line out to the output file

print(unknownumi)

fh.close()
fw.close()
fu.close()
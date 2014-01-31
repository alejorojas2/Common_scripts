#!/usr/bin/env python


import sys
import re

#Reading files

fasta_file = open(sys.argv[1],"r")
line = fasta_file.readline()

seqs = {}

#for line in fasta_file:
while line !="":
    if line.startswith('>'):
        name = line[1:].rstrip('\n')
        seq = fasta_file.readline().rstrip('\n')
        seqs[name] = seq
    line = fasta_file.readline()

print "fasta file contains %i sequences" % (len(seqs.keys()))

fasta_file.close()

#Selecting specific sequences for TTTTTT nucleotides
req_seq  = {}

for i in seqs:
    name = i
    seq = seqs[i]
    pattern = re.search("T{6,8}",seq)
    if pattern:
        ind = pattern.span()
	up_seq = seq[ind[0]-6:ind[0]]
	gc_count = re.findall("[GC]",up_seq)
	
	up_seq25 = seq[ind[0]-25:ind[0]]
	gc_count25 = re.findall("[GC]",up_seq25)
	
	if len(gc_count) > 3 and len(gc_count25) > 0:
	    gc_perc = float(len(gc_count25))/len(up_seq25)
	    
	    if gc_perc > 0.5:
		final_seq = seq[ind[0]-25:ind[1]]
		req_seq[name]=final_seq
		print name
		print final_seq
		print gc_perc
	else:
	    continue
	
    else:
        continue
   
print "%i sequences that match '%s' value" % (len(req_seq.keys()),"T 6-8")

#Writing output fasta file
output = open("intergenic_Ea_Q.fasta","w")

for i in req_seq:
    name = i
    seq = req_seq[i]
    output.write(">%s\n%s\n" % (name,seq))

output.close()

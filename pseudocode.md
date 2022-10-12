#### PSEUDOCODE ####

This is the pseudocode for the deduper project to remove PCR duplicates from a SAM file (Reference Based PCR Duplicate Removal tool)

### THE PROBLEM ###

During library preparation for sequencing of DNA and/or RNA, a necessary step is to use polymerase-chain reaction amplication to increase the amount of DNA or RNA content that will be fed into a sequencer. While this step is necessary, it also creates a number of PCR duplicates that go through the sequencing, quality filtering/trimming, during the subsequent alignment step, they're turned into SAM files. The overall problem is that these duplicates are just that, duplicates and thus need to be removed before counting. 

PCR duplicates can be identified because they have the same chromosome, starting base position, and strand. They have to have all three to be duplicates.

## DEVELOP THE ALGORITHM ##

1. Clean up the SAM file by removing the chromosome/scaffolding before the SAM headers.
2. Sort the SAM file by base position using samtools.
3. Write an adjusted position function that will take the starting positon (SAM column 4) and adjust it. If it's a forward strand, account for soft clipping. If it's a reverse strand, account for soft clipping, indels (I's and D's), and skipped regions (N's).
4. Read the file line by line using readline() and split the files by column
5. Create a set in which you will put the chromosome (col 3), adjusted position (col 4), strand (col 2), and UMI (col 1) as the key. 
6. If the key is unique, write its corresponding line to the file. 

# HIGH LEVEL FUNCTIONS #

def adj_position():
    '''This function inputs the starting position and adjusts it for soft clipping on the forward strand and soft clipping, indels, and skipped regions for the reverse'''  

def deduper():
    '''This function reads the file line by line using readline() and splits the files by column. It will interpret the bitwise flag to determine the strandedness. It adds to a set in which it will put the chromosome (col 3), adjusted position (col 4), strand (col 2), and UMI (col 1) as the key. 
    with open('file', 'w') as x:
        x.write(line)
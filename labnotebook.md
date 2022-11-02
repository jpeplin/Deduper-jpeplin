# LAB NOTEBOOK - DEDUPER
### JACK PEPLINSKI - 11/2/22

## PART 1 - PSEUDOCODE

This is the pseudocode for the deduper project to remove PCR duplicates from a SAM file (Reference Based PCR Duplicate Removal tool)

### THE PROBLEM

During library preparation for sequencing of DNA and/or RNA, a necessary step is to use polymerase-chain reaction amplication to increase the amount of DNA or RNA content that will be fed into a sequencer. While this step is necessary, it also creates a number of PCR duplicates that go through the sequencing, quality filtering/trimming, during the subsequent alignment step, they're turned into SAM files. The overall problem is that these duplicates are just that, duplicates and thus need to be removed before counting. 

PCR duplicates can be identified because they have the same chromosome, starting base position, and strand. They have to have all three to be duplicates.

### DEVELOP THE ALGORITHM

1. Clean up the SAM file by removing the chromosome/scaffolding before the SAM headers.
2. Sort the SAM file by base position using samtools.
3. Write an adjusted position function that will take the starting positon (SAM column 4) and adjust it. If it's a forward strand, account for soft clipping. If it's a reverse strand, account for soft clipping, indels (I's and D's), and skipped regions (N's).
4. Read the file line by line using readline() and split the files by column
5. Create a set in which you will put the chromosome (col 3), adjusted position (col 4), strand (col 2), and UMI (col 1) as the key. 
6. If the key is unique, write its corresponding line to the file. 

### HIGH LEVEL FUNCTIONS

def adj_position():
    '''This function inputs the starting position and adjusts it for soft clipping on the forward strand and soft clipping, indels, and skipped regions for the reverse'''  

def deduper():
    '''This function reads the file line by line using readline() and splits the files by column. It will interpret the bitwise flag to determine the strandedness. It adds to a set in which it will put the chromosome (col 3), adjusted position (col 4), strand (col 2), and UMI (col 1) as the key. 
    with open('file', 'w') as x:
        x.write(line)

## PART 2 - PEER REVIEWS

##### Logan Wallace:

Excellent work!! Step 1 is a good idea and I like having the rev_comp function to interpret the bitwise flag. Seems like you have a good understanding of the assignment.

For 2C in your pseudocode, consider trying a different method for storing the values that you want to keep (not a dictionary) because you’ll want an immutable storage method for the read’s information. I’m also not sure you’ll need to keep the CIGAR string in whatever storage device you use because once you adjust the starting position you won’t need it anymore. Same thing with the bitwise flag, you’re only using that to determine strandedness so you can just interpret that before you store it.

Consider a separate function for deduplicating (separate from the ones you have) in which you’ll write out the new SAM. It might be useful to put in bioinfo.

Nice job!

- Jack

 

##### Kaitlyn Li:

Nice work!! I like that you included a sorting function at the top of your code. The regex stuff is great for interpreting CIGAR strings. In “Single-end reads,” making a new SAM file will probably be the best way.

Some things to ask yourself: what kind of storage method will you use to extract the UMI, location, position, seq match, etc. for each of your reads (immutable or mutable?)? Are those the things you’ll include to deduplicate? Will your soft clipping adjustment method work for both the forward and reverse strands? Will you need to account for other kinds of CIGAR string shenanigans?

Great job!

- Jack

 

##### Sophia Soriano:

Nice job! You’ve put a lot of thought and effort into your pseudocode which will pay off in the coding part of things! It’s good that you’ve decided to write the file as you read it so that you’re not storing the extracted lines in your memory (it will speed things up computationally by a ton).

I would consider saving your UMI, RNAME, strand, and position in a different (immutable) storage device because you’ll run into problems with a dictionary. You probably don’t need to include the cigar string in that once you’ve adjusted for position.

Excellent work!

- Jack

## PART 3 - DEDUPER.PY

#### CIGAR/BIOINFO

For writing deduper, I knew that I needed to write at least one function for adjusting the position of the reads using CIGAR strings and regex. I started with the reverse strand because it was the most difficult. At first, I started with a simple regex that used [0-9] before each letter (N, M, D, or S) and added that to the position. But that did not account for duplicate letters in a CIGAR string so I instituted a for loop to count each occurence and add it back at the end. For soft clipping on the reverse, you have to include only soft clipping at the end of the string so I used $ at the end of the regex. 

The forward strand was much easier, but I had to use ^ at the beginning of the regex for soft clipping. Originally I had the ^ at the end which didn't work. I added both of these functions to bioinfo. 

#### THE SCRIPT

##### THE SET-UP

The first thing is to input argparse and write useful help messages detailing what the script was for: namely, deduplicating using an input sorted SAM, creating an output SAM, and using a .txt list of UMIs. 

I needed to create two sets: one for storing a tuple of chr, adj pos, strand, and UMI and one for the list of UMI's I would grab from the UMI.txt file. To do the latter, I needed a simple for loop that would strip the file of the line breaks and add the UMIs to a set. 

I also set a counter for unknown UMIs and I opened all the files from the argparse functions. 

##### THE MAIN FUNCTION

The meat of the deduper script is within a "while True:" statement. 

I open with a readline(). Leslie helped me by incorporating a line == "": break which will stop the while True when it reaches a line with nothing in it. If the line startswith @ it is a header and should write the header to the output file. Else, I split the line into columns, grab the last 8 characters of the first column to get the umi and check if the umi is in the umi set. If not, add to the unknown counter and continue. If yes, interpret the bitwise flag. If the flag is 16, the strand is reverse so it should incorporate the bioinfo reverse adjusted position function and assign the "-" to the tuple. If not, it's forward so it will use the forward adjusted position function and assign the "+". 

The function will then add the relevant info to the tuple and check if the tuple is already in the initial set as it reads line. If not, it should write the tuple to the set and write the line in the output file. Finally, the files should be closed. 

My biggest challenge with this project was that I accidentally was interpreting the wrong column number for the bitwise flag :)))). Big oops. A big shoutout to Justine for helping me find that bug. 

Overall, I actually enjoyed this project as frustrating as that bug was... In retrospect, everything makes a lot of sense. It just took a long time to wrap my head around. 
all:
	morloc make kraken.loc

.PHONY: clean
clean:
	rm -f pool* nexus*

.PHONY: test
test:
	# test the vtp default programs
	morloc make main.loc
	# run kraken, store table as TAB-delimited file
	./nexus.py defaultKraken '"output.txt"' '"reads/mini_SL335871.R1.fastq.gz"' '"reads/mini_SL335871.R2.fastq.gz"'
	# make MPA
	./nexus.py defaultMPA '"output.txt"' > mpa.txt

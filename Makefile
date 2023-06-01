all:
	morloc make kraken.loc

.PHONY: clean
clean:
	rm -f pool* nexus*

.PHONY: test
test:
	./nexus.py krakenPaired '{"threads":4,"checkNames":false,"db":"test/minikraken_20171101_4GB_dustmasked","minHits":2,"preload":true,"quick":true}' '"test/reads_1.fq.gz"' '"test/reads_2.fq.gz"'

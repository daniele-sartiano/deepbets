all: classify

DATABASE = data/database.sqlite

dataset.tsv: $(DATABASE)
	python extractor.py > $@ 2> log.out


train.tsv: dataset.tsv
	cut -f2 < $< > $@


labels.tsv: dataset.tsv
	cut -f3 < $< > $@


classify: train.tsv labels.tsv
	python classifier.py

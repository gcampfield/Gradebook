clean:
	find . -name "*.pyc" | xargs rm

commit:
	git add .
	git commit

db:
	python db_create.py

run:
	python run.py

run-noreload:
	python run.py -noreload

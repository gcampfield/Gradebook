default:
	python run.py

db:
	python db_create.py

run:
	python run.py

run-noreload:
	python run.py -noreload

test:
	echo "No tests yet"

clean:
	find . -name "*.pyc" | xargs rm

commit:
	git add .
	git commit

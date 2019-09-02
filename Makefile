install:
	pip install -r requirements.txt

dev:
	cd app && ln -sf config_dev.py config.py

test:
	cd app && ln -sf config_test.py config.py

prod:
	cd app && ln -sf config_prod.py config.py

clean:
	pyclean .
install:
	pip install -r requirements.txt

dev:
	cd app && ln -sf config_dev.py config.py

test:
	cd app && ln -sf config_test.py config.py

prod:
	cd app && ln -sf config_prod.py config.py

init_db:
	cd script && ./init_db.sh

drop_db:
	cd script && ./drop_db.sh

init_data:
	cd script && ./init_data.sh

clean:
	pyclean .
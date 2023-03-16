PIPENV_VERSION_COMMAND := pipenv --version

.PHONY=beers-api
beers-api: # Run beers-api
	if [ ! command -v ${PIPENV_VERSION_COMMAND} 2> /dev/null ]; then @echo "pipenv installed" else @echo "pipenv not found"; @exit 1; fi;
	if [ ! -f "${PWD}/apps/beers_api/.env" ]; then cp ${PWD}/apps/beers_api/.env.example .env; fi;
	cd ${PWD}/apps/beers_api && pipenv install && pipenv run uvicorn main:app --reload
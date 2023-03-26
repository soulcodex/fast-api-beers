PIPENV_VERSION_COMMAND := pipenv --version
KEY := "python-coruña-2023"

.PHONY=beers-api
beers-api: # Run beers-api
	if [ ! command -v ${PIPENV_VERSION_COMMAND} 2> /dev/null ]; then @echo "pipenv installed" else @echo "pipenv not found"; @exit 1; fi;
	if [ ! -f "${PWD}/apps/beers_api/.env" ]; then cp ${PWD}/apps/beers_api/.env.example ${PWD}/apps/beers_api/.env; fi;
	cd ${PWD}/apps/beers_api && pipenv install && pipenv run uvicorn main:app --reload

.PHONY=beers-listing
beers-listing: # Beers listing
	@curl http://localhost:8000/v1/beers | json_pp

.PHONY=beers-listing-secured
beers-listing-secured: # Beers listing using an API KEY
	@curl http://localhost:8000/v1/beers?_token=$$KEY | json_pp

.PHONY=beer-by-name
beer-by-name: # One beer type by name
	BEER=$(shell bash -c 'read -p "Insert a type of beer: " beer; echo $$beer') && \
	curl --request GET "http://localhost:8000/v1/beers/$${BEER}" | json_pp

.PHONY=documentation
documentation: # Show documentation UI
	@google-chrome http://localhost:8000/docs
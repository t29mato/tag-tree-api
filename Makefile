API_DOCS_FILE_PATH := ./starrydata/api/docs/openapi.yaml

api-docs:
	python manage.py generateschema --file $(API_DOCS_FILE_PATH)
	sed -i -e 's/- api/- starrydata/g' $(API_DOCS_FILE_PATH)
	cat ./starrydata/api/docs/jsonapi.yaml >> $(API_DOCS_FILE_PATH)
	sed -i -e '/components\/parameters\/sort/d' $(API_DOCS_FILE_PATH)

# FIXME: If it installes yq on docker container, move this command to api-docs
# https://stackoverflow.com/questions/68159658/i-cant-install-yq-on-docker-image-python3
api-docs-fix:
	yq -i eval 'del(.paths.[].put)'  ./starrydata/api/docs/openapi.yaml
	yq -i eval 'del(.components.schemas.relationshipLinks.properties.self.description)'  ./starrydata/api/docs/openapi.yaml
	# CONFIRM: nullのものをnumberにしておいて良いか
	yq -i eval '.components.schemas.nulltype.type = "number"'  ./starrydata/api/docs/openapi.yaml


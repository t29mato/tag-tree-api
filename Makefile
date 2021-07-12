API_DOCS_FILE_PATH := ./starrydata/api/docs/openapi.yaml

api-docs:
	python manage.py generateschema --file $(API_DOCS_FILE_PATH)

# FIXME: If it installes yq on docker container, move this command to api-docs
# https://stackoverflow.com/questions/68159658/i-cant-install-yq-on-docker-image-python3
api-docs-fix:
	# Add JSON:API Schemas
	cat ./starrydata/api/docs/jsonapi.yaml >> $(API_DOCS_FILE_PATH)

	# Remove sort parameters, it's duplicated.
	sed -i '' -e '/components\/parameters\/sort/d' $(API_DOCS_FILE_PATH)

	# Add type to POST schema
	yq -i eval '.paths./api/databases.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/papers.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/figures.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/samples.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/fabrication_processes.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/synthesis_method_tags.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/synthesis_method_tag_tree_nodes.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/polymer_tags.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths./api/polymer_nodes.post.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml

	# Add type to PATCH schema
	yq -i eval '.paths."/api/fabrication_processes/{id}".patch.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths."/api/synthesis_method_tags/{id}".patch.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths."/api/synthesis_method_tag_tree_nodes/{id}".patch.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	# yq -i eval '.paths."/api/polymer_tags/{id}".patch.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml
	yq -i eval '.paths."/api/polymer_nodes/{id}".patch.requestBody.content["application/vnd.api+json"].schema.type="object"' ./starrydata/api/docs/openapi.yaml

	# Remove PUT methods
	yq -i eval 'del(.paths.[].put)'  ./starrydata/api/docs/openapi.yaml

	# Replace type of nulltype, avoids the API-client generating error.
	yq -i eval '.components.schemas.nulltype.type = "number"'  ./starrydata/api/docs/openapi.yaml

	# Replace tag name
	sed -i '' -e 's/- api/- starrydata/g' $(API_DOCS_FILE_PATH)

api-client:
	# Generate API client
	docker run --rm -v "${PWD}/starrydata/api/docs/:/workspace" openapitools/openapi-generator-cli:v5.1.1 generate \
		-i /workspace/openapi.yaml \
		-g typescript-axios \
		-o /workspace/dist

	# Move to API client directory
	rm -rf ../api-client/dist
	mv starrydata/api/docs/dist ../api-client/dist

	# Replace Set object, avoids typescript error
	sed -i '' -e 's/Set;/Set<any>;/' ../api-client/dist/api.ts

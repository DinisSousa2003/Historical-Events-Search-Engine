#!/bin/bash

# This script expects a container started with the following command.
 #docker run -p 8983:8983 --name pri_44 -v ${PWD}:/data -d solr:9.3 solr-precreate conflicts

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/conflicts/schema

curl -X POST -H 'Content-type:application/json' --data-binary "@./outputs/data.json" http://localhost:8983/solr/conflicts/update?commit=true

# Populate collection using mapped path inside container.
docker exec -it pri_44 bin/post -c conflicts ./outputs/data.json

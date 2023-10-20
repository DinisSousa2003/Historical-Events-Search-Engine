#!/bin/bash

# This script expects a container started with the following command.
# docker run -p 8983:8983 --name pri_44 -v ${PWD}:/data -d solr:9.3 solr-precreate historicalEvents

# Schema definition via API
curl -X POST -H 'Content-type:application/json' \
    --data-binary "@./schema.json" \
    http://localhost:8983/solr/historicalEvents/schema

# Populate collection using mapped path inside container.
docker exec -it pri_44 bin/post -c historicalEvents ./outputs/data.json

#!/bin/bash

# This script expects a container started with the following command.
# docker run -p 8983:8983 --name pri_44 -v ${PWD}:/data -d solr:9.3 solr-precreate conflicts
#


#remove its schema and documents
docker exec -it pri_44 bin/solr delete -c conflicts

#create core conflicts
docker exec -it pri_44 bin/solr create -c conflicts

docker exec -it pri_44 cp /data/related_terms.txt /var/solr/data/conflicts/related_terms.txt



# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary "@./schema.json" http://localhost:8983/solr/conflicts/schema

#,!!! data.json is a copy of the file from /outputs, the relative path was not working
curl -X POST -H 'Content-type:application/json' --data-binary "@./data.json" http://localhost:8983/solr/conflicts/update?commit=true

# Populate collection using mapped path inside container.
#docker exec -it pri_44 bin/post -c conflicts ./outputs/data.json

#xdg-open http://localhost:8983/

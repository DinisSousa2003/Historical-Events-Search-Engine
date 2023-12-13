#!/bin/bash
# This script expects a container started with the following command.
# docker run -p 8983:8983 --name pri_44 -v ${PWD}:/data -d solr:9.3 solr-precreate conflicts
# sleep 10

#remove its schema and documents
docker exec -it pri_44 bin/solr delete -c conflicts
#create core conflicts
docker exec -it pri_44 bin/solr create -c conflicts

sleep 2
docker exec -it pri_44 cp /data/related_terms.txt /var/solr/data/conflicts/related_terms.txt
docker exec -it pri_44 cp /data/solrconfig.xml /var/solr/data/conflicts/conf/solrconfig.xml

#reload container beacuse solrconfig.xml was changed
docker restart pri_44
sleep 4

#docker exec -it pri_44 bin/solr start -e techproducts -Dsolr.ltr.enabled=true

# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary "@./schema.json" http://localhost:8983/solr/conflicts/schema
#,!!! data.json is a copy of the file from /outputs, the relative path was not working
curl -X POST -H 'Content-type:application/json' --data-binary "@./data.json" http://localhost:8983/solr/conflicts/update?commit=true

curl -XDELETE 'http://localhost:8983/solr/conflicts/schema/feature-store/_DEFAULT_'
curl -XPUT 'http://localhost:8983/solr/conflicts/schema/feature-store' --data-binary "@./myFeatures.json" -H 'Content-type:application/json'
curl -XPUT 'http://localhost:8983/solr/conflicts/schema/model-store' --data-binary "@./myModel.json" -H 'Content-type:application/json'


# Populate collection using mapped path inside container.
#docker exec -it pri_44 bin/post -c conflicts ./outputs/data.json
#xdg-open http://localhost:8983/
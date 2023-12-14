#!/bin/bash

# This script expects a container started with the following command.
#docker run -p 8983:8983 --name pri_44_semantic -v ${PWD}:/data -d solr:9.3 solr-precreate conflicts
#sleep 5


#remove its schema and documents
docker exec -it pri_44_semantic bin/solr delete -c conflicts

#create core conflicts
docker exec -it pri_44_semantic bin/solr create -c conflicts

docker exec -it pri_44_semantic cp /data/related_terms.txt /var/solr/data/conflicts/related_terms.txt
docker exec -it pri_44_semantic cp /data/solrconfig.xml /var/solr/data/conflicts/conf/solrconfig.xml

#reload container beacuse solrconfig.xml was changed
docker restart pri_44_semantic
sleep 4


# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary "@./schema_semantic.json" http://localhost:8983/solr/conflicts/schema
#,!!! data.json is a copy of the file from /outputs, the relative path was not working
curl -X POST -H 'Content-type:application/json' --data-binary "@./data_semantic.json" http://localhost:8983/solr/conflicts/update?commit=true

curl -XDELETE 'http://localhost:8983/solr/conflicts/schema/feature-store/FeaturesStoreV1'
curl -XPUT 'http://localhost:8983/solr/conflicts/schema/feature-store' --data-binary "@./myFeatures.json" -H 'Content-type:application/json'

curl -XDELETE 'http://localhost:8983/solr/conflicts/schema/model-store/myModel'
curl -XPUT 'http://localhost:8983/solr/conflicts/schema/model-store' --data-binary "@./myModel.json" -H 'Content-type:application/json'


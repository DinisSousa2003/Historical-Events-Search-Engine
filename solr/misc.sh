curl -XDELETE 'http://localhost:8983/solr/conflicts/schema/feature-store/FeaturesStoreV1'
curl -XPUT 'http://localhost:8983/solr/conflicts/schema/feature-store' --data-binary "@./myFeatures.json" -H 'Content-type:application/json'

curl -XDELETE 'http://localhost:8983/solr/conflicts/schema/model-store/myModel'
curl -XPUT 'http://localhost:8983/solr/conflicts/schema/model-store' --data-binary "@./myModel.json" -H 'Content-type:application/json'

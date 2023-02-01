curl localhost:8080 \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "context": {
          "eventId": "1147091835525187",
          "timestamp": "2020-04-23T07:38:57.772Z",
          "eventType": "google.storage.object.finalize",
          "resource": {
             "service": "storage.googleapis.com",
             "name": "canvas-pathway-374021/buckets/stack-cf-data-pipeline-hist/2023-02-01/key_stats.csv.parquet.gzip",
             "type": "storage#object"
          }
        },
        "data": {
          "bucket": "stack-cf-data-pipeline-hist",
          "contentType": "application/octet-stream",
          "kind": "storage#object",
          "md5Hash": "...",
          "metageneration": "1",
          "name": "2023-02-01/key_stats.csv.parquet.gzip",
          "size": "352",
          "storageClass": "REGIONAL",
          "timeCreated": "2020-04-23T07:38:57.230Z",
          "timeStorageClassUpdated": "2020-04-23T07:38:57.230Z",
          "updated": "2020-04-23T07:38:57.230Z"
        }
      }'
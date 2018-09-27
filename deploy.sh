
# Deploy Cloud Function to parse CDN logs
# https://cloud.google.com/functions/docs/calling/
cd cf_parse_cdn_logs 
export cloud_function_name="parse_cdn_logs"
export cloud_storage_bucket_name="cdn_logs_z2018"
gcloud functions deploy $cloud_function_name \
    --runtime python37 \
    --trigger-resource $cloud_storage_bucket_name \
    --trigger-event google.storage.object.finalize
cd ..



# Deploy Cloud Function to load CDN logs (json) into BigQuery
# https://cloud.google.com/functions/docs/calling/
cd cf_load_to_bq
export cloud_function_name="load_cdn_logs_to_bq"
export cloud_storage_bucket_name="cdn_logs_z2018"
gcloud functions deploy $cloud_function_name \
    --runtime python37 \
    --trigger-resource $cloud_storage_bucket_name \
    --trigger-event google.storage.object.finalize
cd ..



# Delete function from Google Cloud Functions
#gcloud functions delete &cloud_func_name





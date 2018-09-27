# Create function (as main.py)
def load_cdn_logs_to_bq(data, context):
    """
        Background Cloud Function to be triggered by Cloud Storage.
        
        Args:
            data (dict): The Cloud Functions event payload.
            context (google.cloud.functions.Context): Metadata of triggering event.
        Returns:
            None; the output is written to Stackdriver Logging
    """
    import re
    import json
    from google.cloud import storage
    from google.cloud import bigquery
    
    # Arguments
    bq_dataset_name = 'zdataset'
    bq_table_name   = 'cdn_logs'
    
    # Used for Testing
    #data = {'bucket':'cdn_logs_z2018','name':'cdn_logs.json'}
    #bq_dataset_name = 'zdataset' 
    #bq_table_name   = 'cdn_logs'
    
    if re.search('\.json$', data['name']):
        
        client      = bigquery.Client()
        dataset_ref = client.dataset(bq_dataset_name)
        job_config  = bigquery.LoadJobConfig()
        job_config.autodetect = True
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        uri = 'gs://{}/{}'.format(data['bucket'], data['name'])
        load_job = client.load_table_from_uri(
            uri,
            dataset_ref.table(bq_table_name),
            job_config=job_config) 
        
        assert load_job.job_type == 'load'
        
        load_job.result() # Waits for table load to complete.
        
        if load_job.state == 'DONE':
            bq_num_rows = client.get_table(dataset_ref.table(bq_table_name)).num_rows
            print('Successfully inserted {} rows into BigQuery table: {}'.format(bq_num_rows, bq_table_name) )

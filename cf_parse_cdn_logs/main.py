# Create function (as main.py)
def parse_cdn_log(data, context):
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
     
    # Used for Testing
    #data = {'bucket':'cdn_logs_z2018','name':'cdn_logs.txt'}
    
    if re.search('\.txt$', data['name']):
        
        client  = storage.Client()
        bucket  = client.get_bucket(data['bucket'])
        blob    = bucket.get_blob(data['name'])
        blobstr = blob.download_as_string()
        lines   = blobstr.decode('utf-8').split('\n')
        
        json_records = []
        
        for line in lines:
            
            elements = re.match('\
t_now=([0-9]+) \
t_elapsed=([0-9\.]+) \
t_ttfb=([0-9\.]+) \
t_start=([0-9\.]+) \
t_end=([0-9\.]+) \
req_ip=([0-9\.]+) \
req_method=([A-Z]+) \
req_host=(.*?) \
req_url=(.*?) \
resp_status=(.*?) \
resp_size=(.*?) \
resp_age=(.*?) \
resp_xcache=(.*?) \
resp_setcookie=(.*?) \
req_ua=(.*?) \
req_ref=(.*?) \
resp_xcache=(.*?) \
fastly_pop=(.*?) \
fastly_shield=(.*?) \
fastly_region=(.*?) \
fastly_state=(.*?) \
fastly_hits=(.*?) \
fastly_restarts=(.*?) \
geo_continent=(.*?) \
geo_country=(.*?) \
geo_region=(.+)\
',line)
            
            json_payload = {
                "t_now":elements.group(1),
                "t_elapsed":elements.group(2),
                "t_ttfb":elements.group(3),
                "t_start":elements.group(4),
                "t_end":elements.group(5),
                "req_ip":elements.group(6),
                "req_method":elements.group(7),
                "req_host":elements.group(8),
                "req_url":elements.group(9),
                "resp_status":elements.group(10),
                "resp_size":elements.group(11),
                "resp_age":elements.group(12),
                "resp_xcache":elements.group(13),
                "resp_setcookie":elements.group(14),
                "req_ua":elements.group(15),
                "req_ref":elements.group(16),
                "resp_xcache":elements.group(17),
                "fastly_pop":elements.group(18),
                "fastly_shield":elements.group(19),
                "fastly_region":elements.group(20),
                "fastly_state":elements.group(21),
                "fastly_hits":elements.group(22),
                "fastly_restarts":elements.group(23),
                "geo_continent":elements.group(24),
                "geo_country":elements.group(25),
                "geo_region":elements.group(26)
            }
            
            json_records.append( json.dumps(json_payload) )
        
        json_records = '\n'.join( json_records ).replace('\\""','"').replace('"\\"','"').replace('\\"','"')
        
        # Load delimited json records to Google Cloud Storage
        client = storage.Client()
        bucket = client.get_bucket(data['bucket'])
        blob   = bucket.blob(data['name'].replace('.txt','.json'))
        blob.upload_from_string(data=json_records, content_type='text/plain')
        print('Created gs://{}/{}'.format(data['bucket'], data['name'].replace('.txt','.json') ))

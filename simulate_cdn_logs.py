
#####################################################################################
#
#   Simulate CDN Logs
#
#   USAGE: file.py --bucket_name BUCKET_NAME --iteration_count ITERATION_COUNT
#          file.py --bucket_name=cdn_logs_z2018 --iteration_count=100
#
#####################################################################################



import re
import json
import datetime,time
import random
import argparse
from google.cloud.storage import Blob
from google.cloud import storage



def simulate_cdn_logs(iteration_count):
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
        ]
    
    list_of_states = ['CA']*20 + ['TX']*20 + ['FL']*15 + ['NY']*15 + ['IL']*10 + ['PA']*5 + ['OH']*5 + ['GA'] + ['NC'] + ['SC']*5
    
    cdn_logs = []
    
    for i in range(iteration_count):
        
        simulated_date = (2018, 9, random.randint(1,30), random.randint(0,23), random.randint(0,57), random.randint(0,59), 1,1,1 ) #(2018, 9, 17, 17, 3, 38, 1, 48, 0)
        unix_datetime  = int(time.mktime( simulated_date )) #datetime.datetime.now().timetuple()))
        elaspsed_time  = int(random.triangular(0,100, 50))
        
        xcache_state = random.choice(['MISS']*8 + ['HIT']*2)
        
        cdn_log =  ''
        cdn_log += 't_now={} '.format( unix_datetime )
        cdn_log += 't_elapsed={} '.format( elaspsed_time )
        cdn_log += 't_ttfb={} '.format( round((int(random.triangular(0,100,20)) / 1000), 4) )
        cdn_log += 't_start={} '.format( unix_datetime - elaspsed_time )
        cdn_log += 't_end={} '.format( unix_datetime )
        cdn_log += 'req_ip={} '.format( '104.237.{}.{}'.format(random.randint(1,254), random.randint(1,254)) )
        cdn_log += 'req_method={} '.format( 'GET' )
        cdn_log += 'req_host={} '.format( 'www.cnn.com' )
        cdn_log += 'req_url={} '.format( '/2018/09/{}/{}/'.format( random.randint(10,30), random.choice(['us','world','politics','opinions','health','entertainment','tech','style','travel','sports']) ) )
        cdn_log += 'resp_status={} '.format( random.choice( [200]*80 + [404]*20 ) )
        cdn_log += 'resp_size={} '.format( int(random.triangular(200, 175000, 2000)) )
        cdn_log += 'resp_age={} '.format( 0 )
        cdn_log += 'resp_xcache={} '.format( xcache_state )
        cdn_log += 'resp_setcookie={} '.format( 1 )
        cdn_log += 'req_ua={} '.format( random.choice(user_agents) )
        cdn_log += 'req_ref={} '.format( 'https://www.cnn.com' )
        cdn_log += 'resp_xcache={} '.format( xcache_state )
        cdn_log += 'fastly_pop={} '.format( 'IAD' )
        cdn_log += 'fastly_shield={} '.format( 1 )
        cdn_log += 'fastly_region={} '.format( 'US-East' )
        cdn_log += 'fastly_state={} '.format( '{}-CLUSTER'.format(xcache_state) )
        cdn_log += 'fastly_hits={} '.format( 0 if xcache_state=='MISS' else 1 )
        cdn_log += 'fastly_restarts={} '.format( 0 )
        cdn_log += 'geo_continent={} '.format( 'NA' )
        cdn_log += 'geo_country={} '.format( 'US' )
        cdn_log += 'geo_region={}'.format( random.choice( list_of_states ) )
        
        cdn_logs.append(cdn_log)
    
    cdn_log_count = len(cdn_logs)
    cdn_logs      = '\n'.join( cdn_logs )
    print('[ INFO ] Simulated {} records'.format(cdn_log_count) )
    return cdn_logs, cdn_log_count



# Write cdn_logs string blob storage in Google Cloud Storage
def write_str_to_gcs(bucket_name, blob_str):
    '''
        Write blob string to Google Cloud Storage
    '''
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    #encryption_key = 'c7f32af42e45e85b9848a6a14dd2a8f6'
    bucket_filename = 'cdn_log_{}.txt'.format( datetime.datetime.now().strftime('%Y%m%d_%H%M%S') )
    blob = Blob(bucket_filename, bucket) # encryption_key=encryption_key)
    blob.upload_from_string( blob_str )
    print('[ INFO ] Wrote cdn logs to gs://{}/{}'.format(bucket_name, bucket_filename) )



if __name__ == "__main__":
    
    # Arguments - Only used for testing
    #args =  {
    #            "bucket_name": "cdn_logs_z2018",
    #            "iteration_count": 100
    #        }
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket_name",     required=True, type=str, help="Google Cloud Storage bucket name")
    ap.add_argument("--iteration_count", required=True, type=int, help="Number of CDN logs to simulate")
    args = vars(ap.parse_args())
    
    # Simulate CDN Logs
    cdn_logs, cdn_log_count = simulate_cdn_logs( args['iteration_count'] )
    
    # # Write cdn_logs string blob storage in Google Cloud Storage
    write_str_to_gcs(args['bucket_name'], cdn_logs)
    
    print('[ INFO ] Simulation Complete')



#ZEND

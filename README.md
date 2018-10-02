<h3>CDN Log Analysis on Google Cloud Platform</h3>
This repo provides sample code, demonstrating how to process CDN logs on <a href="https://cloud.google.com/">Google Cloud Platform. </a>
<br>
<br><b>Here's the general process:</b>
<br>&nbsp;&nbsp;&nbsp;&nbsp;1) Raw CDN logs are written to a Google Cloud Storage bucket.
<br>&nbsp;&nbsp;&nbsp;&nbsp;2) When a CDN log is written/created, a Google Cloud Function is trigger, which parses the logs.
<br>&nbsp;&nbsp;&nbsp;&nbsp;3) The parses logs are written back to Cloud Storage as a delimited json file.
<br>&nbsp;&nbsp;&nbsp;&nbsp;4) A second Cloud Function is triggered once the json is created, which loads the logs into BigQuery.
<br>&nbsp;&nbsp;&nbsp;&nbsp;5) BigQuery is used for data exploration and analysis (Data Studio is used for visualization).
<br>&nbsp;&nbsp;&nbsp;&nbsp;6) ML models (sklearn) are deployed to CloudML to detect anonalies and identify trends.
<br>
<br><img src="screenshots/Screenshot 2018-10-02 at 12.48.55 PM.png" class="inline"/>
<br>
<br><b>Data Studio Dashboard (quick mock up):</b>
<br><img src="screenshots/Screenshot 2018-10-02 at 1.42.48 PM.png" class="inline"/>
<br>
<br><b>Setup and Execution</b> (... in progress ...)
<br>
<br>Prerequisites:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;Sign-up for <a href="https://cloud.google.com/">Google Cloud Platform Account</a>
<br>
<br>Setup:
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;Clone this repo
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;Create a Google Cloud Storage called "cdn_logs_z2018"
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;Create a Cloud Function to parse_cdn_logs (<a href="https://github.com/zaratsian/gcp_analyze_cdn_logs/tree/master/cf_parse_cdn_logs">code here</a>)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;Create a Cloud Function to load_to_bq (<a href="https://github.com/zaratsian/gcp_analyze_cdn_logs/tree/master/cf_load_to_bq">code here</a>)
<br>&nbsp;&nbsp;&nbsp;&nbsp;&bull;&nbsp;&nbsp;Simulate logs using this <a href="https://github.com/zaratsian/gcp_analyze_cdn_logs/blob/master/simulate_cdn_logs.py">code</a> (which will simulate data and write it to Cloud Storage)

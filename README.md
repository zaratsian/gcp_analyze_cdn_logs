<h3>Analyze CDN Logs on Google Cloud Platform</h3>
This repo provides sample code, demonstrating how to process CDN logs on <a href="https://cloud.google.com/">Google Cloud Platform. </a>
<br>
<br>Here's the process:
<br>&nbsp;&nbsp;&nbsp;&nbsp;1) Raw CDN logs are written to a bucket in Google Cloud Storage.
<br>&nbsp;&nbsp;&nbsp;&nbsp;2) When a new CDN log is created, a Cloud Function is trigger, which parses the logs.
<br>&nbsp;&nbsp;&nbsp;&nbsp;3) The parses logs are written back to Cloud Storage as a delimited json file.
<br>&nbsp;&nbsp;&nbsp;&nbsp;4) A second Cloud Function is triggered once the json is created, and this logs the parsed data into BigQuery, where additional data analysis and exploration can occur.
<br>&nbsp;&nbsp;&nbsp;&nbsp;5) Machine learning models, contained within Cloud ML, are able to analyze the data within BigQuery in order to detect anomalies and predict spikes in activity and topic.
<br>
<br><b>References:</b>
<br>

<h3>Analyze CDN Logs on Google Cloud Platform</h3>
This repo provides sample code, demonstrating how to process CDN logs on <a href="https://cloud.google.com/">Google Cloud Platform. </a>
<br>
<br>Here's the process:
<br>&nbsp;&nbsp;&nbsp;&nbsp;1) Raw CDN logs are written to a Google Cloud Storage bucket.
<br>&nbsp;&nbsp;&nbsp;&nbsp;2) When a CDN log is written/created, a Google Cloud Function is trigger, which parses the logs.
<br>&nbsp;&nbsp;&nbsp;&nbsp;3) The parses logs are written back to Cloud Storage as a delimited json file.
<br>&nbsp;&nbsp;&nbsp;&nbsp;4) A second Cloud Function is triggered once the json is created, which loads the logs into BigQuery.
<br>&nbsp;&nbsp;&nbsp;&nbsp;5) BigQuery is used for data exploration and analysis (Data Studio is used for visualization).
<br>&nbsp;&nbsp;&nbsp;&nbsp;6) ML models (sklearn) are deployed to CloudML to detect anonalies and identify trends.
<br>
<br><b>Reference Architecture:</b>
<br><img src="screenshots/Screenshot 2018-10-02 at 12.48.55 PM.png" class="inline"/>
<br>
<br><b>Data Studio Dashboard (quick mock up):
<br><img src="screenshots/Screenshot 2018-10-02 at 1.42.48 PM.png" class="inline"/>
<br>


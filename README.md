pylebeat
========

Experimental lambda function to send Cloudwatch Logs to an OnPrem ELK stack.

# Add custom fields
Edit the `fields` section in pylebeat.yml to add more custom fields to your log message

# Output
Currently supported outputs are:
- redis

# ToDo
Enable Logstash Output
Enable Elasticsearch Output


# Testing
Use Pylambda for local development and deployment to S3/Lambda
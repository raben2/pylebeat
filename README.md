pylebeat
========
Experimental lambda function to send Cloudwatch Logs to an OnPrem ELK stack.

## Add custom fields
Edit the `fields` section in pylebeat.yml to add more custom fields to your log messageg

## Output
Currently supported outputs are:
- redis

## ToDo
- enable Logstash Output
- enable Elasticsearch Output


## Testing
Use Pylambda for local development and deployment to S3/Lambda
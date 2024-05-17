import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    start_time = int(event['start_time'])
    end_time = int(event['end_time'])

    client = boto3.client('cloudtrail')

    # convert from UNIX timestamps to datetime
    start_time = datetime.utcfromtimestamp(start_time)
    end_time = datetime.utcfromtimestamp(end_time)

    unique_users = set()

    # Get CloudTrail events
    paginator = client.get_paginator('lookup_events')
    for page in paginator.paginate(StartTime=start_time, EndTime=end_time):
        for event in page['Events']:
            ct_event = json.loads(event['CloudTrailEvent'])
            try: 
                unique_users.add(ct_event['userIdentity']['userName'])
            except KeyError:
                try:
                    arn = ct_event['userIdentity']['arn']
                    # since session part starts after "assumed-role/<role-name>/", 
                    # we create a list of segments divided by '/' and get the last element
                    user = arn.split('/')[-1] if '/' in arn else arn
                    unique_users.add(user)
                except KeyError:
                    pass
                
    return sorted(list(unique_users))

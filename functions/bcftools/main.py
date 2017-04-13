"""
Lambda example with external dependency
"""

import logging
from subprocess import Popen, PIPE
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def return_msg(out, err, status = 200):
    return {
                'statusCode': status,
                'body': json.dumps({"out": out, "err": err}),
                'headers': {
                    'Content-Type': 'application/json',
                }
            }


def handle(event, context):
    logger.info("%s ------ %s", event, context)
    if 'body' not in event:
        return return_msg(None, "Error: must specify VCF and region", 400)
    body = event['body']
    if 'region' and 'vcf' not in body:
        return return_msg(None, "Error: must specify VCF and region", 400)

    data = json.loads(body)

    #need regex to check if region is valid
    region = data['region']
    start = region.split(":")[1].split("-")[0]
    end = region.split(':')[1].split("-")[1]
    if !(start-end < 999999 and start-end > 0):
        return return_msg(None, "Invalid start and end region values", 400)




    
    logger.info("%s", event['body'])
    out, err = Popen(["./bcftools"], stdout = PIPE, stderr = PIPE).communicate()
    logger.info(out + " out")
    logger.info(err + " err")

    return return_msg(out, err, 200)

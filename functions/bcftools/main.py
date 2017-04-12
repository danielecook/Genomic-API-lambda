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
    if 'vcf' not in body:
        return return_msg(None, "Error: must specify VCF and region", 400)

    
    logger.info("%s", event['body'])
    out, err = Popen(["./bcftools"], stdout = PIPE, stderr = PIPE).communicate()
    logger.info(out + " out")
    logger.info(err + " err")

    return return_msg(out, err, 200)

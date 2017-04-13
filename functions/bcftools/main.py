"""
Lambda example with external dependency
"""

import logging
from subprocess import Popen, PIPE
import json
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def msg(out, err, event, status = 200):
    return {
                'statusCode': status,
                'body': {"out": out, "err": err, "event": event},
                'headers': {
                    'Content-Type': 'application/json',
                }
            }

def handle(event, context):
    if 'region' not in event or 'vcf' not in event:
        return msg(None, "Error: must specify VCF and region", event, 400)

    m = re.match("^([0-9A-Za-z]+):([0-9]+)-([0-9]+)$", event['region'])
    
    if not m:
        return msg(None, "Invalid region", 400)

    chrom = m.group(1)
    start = int(m.group(2))
    end = int(m.group(3))
    #if !(start-end < 1e6 and start .group(3))- end > 0):
    #    return msg(None, "Invalid start and end region values", 400)

    
    logger.info("%s", event['body'])
    out, err = Popen(["./bcftools"], stdout = PIPE, stderr = PIPE).communicate()
    logger.info(out + " out")
    logger.info(err + " err")

    return msg(out, err, 200)

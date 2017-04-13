"""
Lambda example with external dependency
"""

import logging
from subprocess import Popen, PIPE
import re
import json
import os
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_region(region):
    m = re.match("^([0-9A-Za-z]+):([0-9]+)-([0-9]+)$", region)
    if not m:
        return msg(None, "Invalid region", 400)

    chrom = m.group(1)
    start = int(m.group(2))
    end = int(m.group(3))
    return chrom, start, end

def msg(out, err, event, status=200):
    if out == "":
        out = None
    if err == "":
        err = None
    if type(err) == str and err.startswith("[E::hts_open]"):
        err = err.strip()
    return {
        'statusCode': status,
        'body': {"out": out, "err": err, "event": event},
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def handle(event, context):
    try:
        os.chdir("/tmp")
        if 'body' in event:
            event = json.loads(event['body'])
        logger.info(event)
        if 'region' not in event or 'vcf' not in event:
            return msg(None, "Must specify vcf and region", event, 400)

        chrom, start, end = get_region(event['region'])
        event['vcf'] = event['vcf'].replace("https://", "http://")

        if start >= end:
            return msg(None, "Invalid start and end region values", event, 400)
        if end - start > 1e6:
            return msg(None, "Maximum region size is 100 kb", event, 400)

        comm = ["/var/task/bcftools", "view", event["vcf"], event['region']]
        logger.info(' '.join(comm))
        out, err = Popen(comm, stdout=PIPE, stderr=PIPE).communicate()
        logger.info(out + " out")
        logger.info(err + " err")
        return msg(out, err, 200)
    except Exception as e:
        return msg(None, e, event, 400)

import json
import logging

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

def ping(event, context):
    """
    Sanity check endpoint that echoes back 'PONG' to the sender.
    """
    response = {
        "statusCode": 200,
        "body": "PONG!"
    }

    return response


import json
import logging
import boto3
import logging
import time

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

dynamodb = boto3.resource("dynamodb")

def ping(event, context):
    """
    Sanity check endpoint that echoes back 'PONG' to the sender.
    """
    response = {
        "statusCode": 200,
        "body": "PONG!"
    }

    return response

def insertTest(event, context):
    """
    test insert into db
    """
    logger.info("Ping requested")

    #TESTING: make sure the DB works
    table = dynamodb.Table("serverless-chat__Messages")
    timestamp = int(time.time())

    table.put_item(Item={"Room":"general", "Index": 0,
        "Timestamp": timestamp, "Username": "ping-user",
        "Content": "PING!"})
    logger.debug("Item added to the database.")

    response = {
        "statusCode": 200,
        "body": "PONG!"
    }

    return response

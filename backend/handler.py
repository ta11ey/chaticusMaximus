import json
import logging
import boto3
import logging
import time

logger = logging.getLogger("handler_logger")
logger.setLevel(logging.DEBUG)

CNXS_TABLE = "serverless-chat__Connections"
MSG_TABLE = "serverless-chat__Messages"
dynamodb = boto3.resource("dynamodb")

def _get_body(event):
    try:
        return json.loads(event.get("body", ""))
    except:
        logger.debug("event body could not be JSON decoded.")
        return {}

def _get_response(status_code, body):
    if not isinstance(body, str):
        body = json.dumps(body)
    return {"statusCode": status_code, "body": body}

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
    table = dynamodb.Table(MSG_TABLE)
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

def connection_manager(event, context):
    """
    Handles connecting and disconnecting for the Websocket.
    """
    connectionID = event["requestContext"].get("connectionId", 123)

    if event["requestContext"]["eventType"] == "CONNECT":
        logger.info("Connect requested")
        table = dynamodb.Table(CNXS_TABLE)
        table.put_item(Item={"ConnectionID": connectionID})
        return _get_response(200, "Connect Successful")
    elif event["requestContext"]["eventType"] == "DISCONNECT":
        logger.info("Disconnect requested")
        table = dynamodb.Table(CNXS_TABLE)
        table.delete_item(Key={"ConnectionID": connectionID})
        return _get_response(200, "Disonnect Successful.")
    else:
        logger.info("Connection manager received unrecognized eventType.")
        return _get_response(500, "Unrecognized eventType.")

def send_message(event, context):
    """
    When a message is sent on the socket, forward it to all connections.
    """
    logger.info("Message sent on WebSocket.")

    # Ensure all required fields were provided
    body = _get_body(event)
    for attribute in ["username", "content"]:
        if attribute not in body:
            logger.debug("Failed: '{}' not in message dict."\
                    .format(attribute))
            return _get_response(400, "'{}' not in message dict"\
                    .format(attribute))

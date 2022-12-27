import os
import json
from jarvis import Jarvis

def parse_message(content):
    data = content['body']
    print(f"*** INFO: {data}")
    try:
        parts = data.split('&')
        body = [part for part in parts if 'Body' in part]
        data = body[0].split("=")
        response = data[1]
        print(response)
    except Exception as e:
        response = ""
    return response

def main(event, context):
    print("*** INFO: main")
    jarvis = Jarvis()
    print(event)
    event = parse_message(event)
    if "fd" in event:
        # case 2: This get triggered by Twilio to handle a response
        print("*** INFO: Generating & Sending daily notification")
        # Jarvis sends daily stats
        # Kratos sends exercise recommendation and food recommendation
        if 'yes' in event:
            jarvis.process_feedbacks(feedback=True)
        elif 'no' in event:
            jarvis.process_feedbacks(feedback=False)
        else:
            print("No Update")
    else:
        # case 1: This gets triggered for daily notification
        print("*** INFO: Handling response")
        jarvis.run_routines()
    return True


def lambda_handler(event, context):
    status = main(event, context)
    if not status:
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
    return {
        'statusCode': 200,
        'body': json.dumps('Request handled.')
    }


if __name__ == "__main__":
    main(event={"key": "value"}, context={"key": "value"})

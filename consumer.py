from azure.servicebus import ServiceBusClient, ServiceBusMessage, AutoLockRenewer
from datetime import datetime, timedelta, timezone
import time
import json
import subprocess
import os
import logging
import uuid
import traceback
from core.settings import Settings
from core.ml_utils import evaluation
from core.ml_utils.detection import predict
from core.helpers.azure_blob_helper import download_blob_2, download_model, upload_blob
from core.utils.clean import clean_input_evaluate, reformat_output_evaluate

settings = Settings()
tz = timezone(timedelta(hours=7))
CONNECTION_STR  = settings.ASB_CONNECTION_STRING
QUEUE_NAME_INPUT  = settings.QUEUE_NAME_INPUT
QUEUE_NAME_OUTPUT = settings.QUEUE_NAME_OUTPUT
QUEUE_NAME_INSERT = settings.QUEUE_NAME_INSERT
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
now = datetime.now()
current_time = now.strftime("%m-%d-%Y-%H-%M-%S")

class_name = settings.CLASS_NAME
class_path = os.path.join("./core/ml_utils/ml_classes", class_name)
if not os.path.isfile(class_path):
    if not os.path.isdir("core/ml_utils/ml_classes"):
        os.makedirs("core/ml_utils/ml_classes")
    download_model(class_name, class_path)
names = open(class_path).read().strip().split("\n")

"""
Input:
{
  "tenant_id": "7e32ad73-8339-4f36-bf5a-6098f7fa4446",
  "shots_id": 8706,
  "image_id": 10706,
  "image_code": "10706",
  "image_name": "64ef03035be86_CAP2179379959028132294.jpg",
  "tracking_code": "453",
  "image_date": "2023-08-30T15:50:42",
  "image_url": "https://rtqc.blob.core.windows.net/trackingphotos/7e32ad73-8339-4f36-bf5a-6098f7fa4446/2023/08/30/64ef03035be86_CAP2179379959028132294.jpg",
  "request_id": "43",
  "program_code": "Test_06",
  "plan_code": "KHDG0708",
  "level_code": null,
  "criteria_code": null,
  "sku_group": null,
  "outlet_code": "CT00380425",
  "ship_to_code": "CT00380425",
  "route_code": null,
  "posm_code": "0022194",
  "posm_type": "VC",
  "number_of_floor": 5,
  "is_combo": 1,
  "error": null,
  "time_sent": "2023-08-30T08:51:16.7422411+00:00"
}
"""

def evaluate(message: dict):
    try:
        result = message.copy()
        tz = timezone(timedelta(hours=7))
        start_process = datetime.now()
        start_process = start_process.astimezone(tz)
        start_process_str = start_process.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        result.update( {"image_detail_results": {}} )
        result["image_detail_results"]['create_date'] = start_process.strftime('%Y-%m-%d')
        result["image_detail_results"]["image_url"] = os.path.basename(result["image_url"])

        # download image; setup upload path
        start_time_download = time.time()
        download_path_temp = 'temp/' + str(uuid.uuid4())+ "_" + os.path.basename(result['image_url'])
        upload_path_temp = 'temp/' + str(uuid.uuid4())+ "_" + os.path.basename(result['image_url'])
        status = download_blob_2(result['image_url'], download_path_temp)
        if status == 404:
            raise Exception("Image not found")
        end_time_download = time.time()
        time_download = end_time_download - start_time_download

        # detect image
        start_time_detection = time.time()
        detection_result = predict(download_path_temp, names)
        end_time_detection = time.time()
        time_detection = end_time_detection - start_time_detection

        # evaluate image
        start_time_evaluation = time.time()
        evaluation_input = clean_input_evaluate(detection_result, classes=names, download_path_temp=download_path_temp, 
                                                upload_path_temp=upload_path_temp, 
                                                number_of_floor=result["number_of_floor"], is_combo=result["is_combo"])
        evaluation_result = evaluation.safe_evaluate(evaluation_input)
        result["image_detail_results"]  = reformat_output_evaluate(result["image_detail_results"], evaluation_result, detection_result)
        end_time_evaluation = time.time()
        time_evaluation = end_time_evaluation - start_time_evaluation

        # upload image
        start_time_upload = time.time()
        url = upload_blob(evaluation_result["result_image_path"])
        end_time_upload = time.time()
        time_upload = end_time_upload - start_time_upload
        result["image_detail_results"]["image_result_path"] = url

        # reformat data of process
        tz = timezone(timedelta(hours=7))
        end_process = datetime.now()
        end_process = end_process.astimezone(tz)
        end_process = end_process.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        total_time = time_download + time_detection + time_evaluation + time_upload
        result["image_detail_results"]['time_download'] = f'{time_download:.4f}'
        result["image_detail_results"]['time_detection'] = f'{time_detection:.4f}'
        result["image_detail_results"]['time_evaluation'] = f'{time_evaluation:.4f}'
        result["image_detail_results"]['time_upload'] = f'{time_upload:.4f}'
        result["image_detail_results"]['total_time'] = f'{total_time:.4f}'
        result['image_result'] = int(result["image_detail_results"]['evaluation_result'])
        result['start_process'] =  start_process_str
        result['end_process'] = end_process
        result['detection_result'] = detection_result
        remove_image_temp = "rm -rf " + download_path_temp
        subprocess.call(remove_image_temp, shell=True)
    except Exception as e:
        traceback.print_exc()
        result['error'] = str(e)
    return result

def create_request(msg):
    try:
        result = evaluate(msg)
    except Exception as e:
        message = f"Error {str(e)}"
        try:
            result = {"tenant_id": msg['tenant_id'], 
                    "shots_id": msg['shots_id'], 
                    "image_id": msg['image_id']}
        except Exception as e:
            result = {}
        return 404, message, result
    
    return 200, "success", result


def send_messages_app(msg):
    servicebus_client_output = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    with servicebus_client_output:
        sender = servicebus_client_output.get_queue_sender(queue_name=QUEUE_NAME_OUTPUT)
        with sender:
            message = ServiceBusMessage(msg)
            sender.send_messages(message)
            return message

def send_messages_db(msg):
    servicebus_client_output = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
    with servicebus_client_output:
        sender = servicebus_client_output.get_queue_sender(queue_name=QUEUE_NAME_INSERT)
        with sender:
            message = ServiceBusMessage(msg)
            sender.send_messages(message)
            return message

renewer = AutoLockRenewer()
with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME_INPUT)
    with receiver:
        for msg in receiver:
            try:
                renewer.register(receiver, msg, max_lock_renewal_duration=100)
                str_msg = str(msg)
                msg2dict = json.loads(str_msg)
                get_time = datetime.now()
                get_time = get_time.astimezone(tz)
                start_time_process = get_time
                get_time = get_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                msg2dict['time_get'] = get_time
                            
                status, message, result = create_request(msg2dict)
                response = {"status": status, "message": message, "result": result}
                with open("result.json", "w") as f:
                    json.dump(response, f,ensure_ascii=False)
                response_str = json.dumps(response,ensure_ascii=False)
                # complete the message
                send_messages_app(response_str)
                receiver.complete_message(msg)
                if status == 200:
                    # insert to db
                    push_time = datetime.now()
                    push_time = push_time.astimezone(tz)
                    end_time_process = push_time
                    push_time = push_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    response['time_push'] = push_time   
                    total_time_process = (end_time_process - start_time_process).total_seconds()
                    response['total_time_process'] = total_time_process
                    response_str = json.dumps(response,ensure_ascii=False)
                    send_messages_db(response_str)
                    logging.warning(f"Message: {response_str} has been sent to output queue")
            except Exception as e:
                receiver.complete_message(msg)
                logging.warning(f"Message: {msg} has been deleted with error: {e}")
                time.sleep(60)
                continue
renewer.close()
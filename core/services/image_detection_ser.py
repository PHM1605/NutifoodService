import os
import subprocess
import time
from datetime import datetime, timedelta, timezone
from requests import sessions
import uuid
from core.ml_utils.utils import predict, predict_rotate
from core.ml_utils.evaluation_spvb import SPVBApp
from core.schemas.template.image_result_schema_request import ImageRequest
from core.helpers.azure_blob_helper import download_blob, download_blob_2
from core.repositories.image_detection_repo import ImageDetectionRepo
import traceback
import sys


class ImageDetectionService():

    def __init__(self, accessDb: sessions, ) -> None:
        # init connect to database
        self._access_db = accessDb
        _engine = self._access_db.get_engine()
        self._image_detection_repo = ImageDetectionRepo(_engine)
        
    
    def run(self, image_path: str):

        detail = predict_rotate(image_path)
        return detail

    def evaluate(self,imageRq: ImageRequest):
        
        # varialbles of image request
        self.tenant_id = imageRq.tenant_id
        self.tracking_code = imageRq.tracking_code
        self.image_id = imageRq.image_id
        self.image_code = imageRq.image_code
        self.image_name = imageRq.image_name
        self.image_date = imageRq.image_date
        self.image_url = imageRq.image_url
        self.image_path_temp = 'temp/' + str(uuid.uuid4())+ "_" + os.path.basename(self.image_url)
        self.request_id = imageRq.request_id
        self.program_code = imageRq.program_code
        self.plan_code = imageRq.plan_code
        self.level_code = imageRq.level_code
        self.criteria_code = imageRq.criteria_code
        self.sku_group = imageRq.sku_group
        self.outlet_code = imageRq.outlet_code
        self.route_code = imageRq.route_code
        self.error = imageRq.error
        self.time_sent = imageRq.time_sent
        self.time_get = imageRq.time_get
        self.shots_id = imageRq.shots_id
        self.ship_to_code = imageRq.ship_to_code
        self.posm_code  = imageRq.posm_code
        self.posm_type = imageRq.posm_type
        self.number_of_floor = imageRq.number_of_floor
        self.iscombo = imageRq.iscombo
    
        
        #download image from azure blob
        result_info = {'tenant_id': self.tenant_id,
                'tracking_code': self.tracking_code,
                'image_id': self.image_id,
                'image_code': self.image_code,
                'image_name': self.image_name,
                'image_date': self.image_date,
                'image_url':self.image_url,
                'request_id': self.request_id,
                'program_code': self.program_code,
                'plan_code': self.plan_code,
                'level_code': self.level_code,
                'criteria_code': self.criteria_code,
                'sku_group': self.sku_group,
                'outlet_code': self.outlet_code,
                'route_code': self.route_code,
                'error': self.error,
                'time_sent': self.time_sent,
                'time_get': self.time_get,
                'shots_id': self.shots_id,
                'ship_to_code': self.ship_to_code,
                'posm_code': self.posm_code,
                'posm_type': self.posm_type,
                'iscombo': self.iscombo,
                'number_of_floor': self.number_of_floor,}
        
        try:
            tz = timezone(timedelta(hours=7))
            start_process = datetime.now()
            start_process = start_process.astimezone(tz)
            start_process = start_process.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            start_time = time.time()
            status = download_blob_2(self.image_url, self.image_path_temp)
            if status == 404:
                raise Exception("Image not found")
        
            end_time = time.time()
            time_download = end_time - start_time
            
            start_time_detection = time.time()
            detail = self.run(self.image_path_temp)
            detection_result = detail.copy()
            end_time_detection = time.time()
            time_detection = end_time_detection - start_time_detection

            
            start_time = time.time()
            spvb_func = SPVBApp()
            detail['iscombo'] = self.iscombo
            detail = spvb_func.analyze_one_image(detail, self.image_path_temp, self.number_of_floor, self.image_url)
            end_time = time.time()
            # print("=============================")
            # print("detail: ", detail)
            # print("=============================")
            
            
            tz = timezone(timedelta(hours=7))
            end_process = datetime.now()
            end_process = end_process.astimezone(tz)
            end_process = end_process.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
            
            detail['time_download'] = time_download
            detail['time_detection'] = time_detection
            detail['total_time'] = detail['time_download'] + detail['time_detection'] + detail['time_evaluation'] + detail['time_upload']
            
            
            detail['time_download'] = f'{detail["time_download"]:.4f}'
            detail['time_detection'] = f'{detail["time_detection"]:.4f}'
            detail['time_evaluation'] = f'{detail["time_evaluation"]:.4f}'
            detail['time_upload'] = f'{detail["time_upload"]:.4f}'
            detail['total_time'] = f'{detail["total_time"]:.4f}'
            result_info['image_detail_results'] = detail
            result_info['image_result'] = int(detail['evaluation_result'])
            result_info['start_process'] =  start_process
            result_info['end_process'] = end_process
            result_info['detection_result'] = detection_result
         
            
            remove_image_temp = "rm -rf " + self.image_path_temp
            print("rmove image temp: ", remove_image_temp)
            subprocess.call(remove_image_temp, shell=True)
        except Exception as e:
            print("====================wrong herer================")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            line_num = exc_tb.tb_lineno
            error_msg = exc_obj
            result_info['error'] = f"Error on line {line_num}: {error_msg}"

        print("result_info: ", result_info)
        return result_info
        
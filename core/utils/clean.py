import copy 

def clean_input_evaluate(detection_result, classes, download_path_temp, upload_path_temp, 
                         number_of_floor, is_combo):
    ret = {}
    ret["consider_full_posm"] = 1
    ret["consider_last_floor"] = 0
    ret["message"] = ""
    ret["posm_type"] = ""
    ret["number_of_floor"] = number_of_floor
    ret["is_combo"] = is_combo
    ret["is_full_posm"] = -1
    ret["is_one_floor"] = -1
    ret["classes"] = classes
    ret["details"] = {"result": {}, "detections": []}
    for brand in detection_result["details"]:
        for item in detection_result["details"][brand]:
            ret["details"]["detections"].append([item[0], item[1], item[2], item[3], item[4], classes.index(brand)])
    ret["reasons"] = {"OTHER": ""}
    ret["image_path"] = download_path_temp
    ret["result_image_path"] = upload_path_temp
    ret["evaluation_result"] = 1
    return ret

def reformat_output_evaluate(image_detail_results, evaluation_result, detection_result):
    image_detail_results["reasons"] = evaluation_result["reasons"]["OTHER"]
    image_detail_results["details"] = evaluation_result["details"]["result"]
    image_detail_results["details"] = {}
    image_detail_results["count_numeric"] = detection_result["count_numberic"]
    image_detail_results["evaluation_result"] = bool(evaluation_result["evaluation_result"])
    image_detail_results["is_full_tu"] = bool(evaluation_result["is_full_posm"])
    image_detail_results["is_combo"] = bool(evaluation_result["is_combo"])
    return image_detail_results
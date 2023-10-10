import os, cv2, copy
from .utils import extract_to_image
import traceback
from .analysis import (
    analyze_groups,
    get_boxes,
    group_boxes
)

def safe_evaluate(request):
    try:
        response = evaluate(request)
    except Exception as e:
        traceback.print_exc()
        print(f"Error for {request['image_path']}: {e}")
        response["time_upload"] = 0
        response["result_image_url"] = ""
    return response

def evaluate(request):
    img_name = request['image_path']
    img0 = cv2.imread(img_name)
    img = copy.deepcopy(img0)
    
    boxes = get_boxes(request)
    groups = group_boxes(boxes)

    # Release json result
    response = analyze_groups(groups, request)
        
    # Extract to image and json
    img = extract_to_image(img, response)
    response.pop("message")
    if response["evaluation_result"] == 1:
        response["result_image_path"] = response["result_image_path"].split('.')[0] + "_output_ok.jpg"
    else:
        response["result_image_path"] = response["result_image_path"].split('.')[0] + "_output_notok.jpg"
    cv2.imwrite(response["result_image_path"], img)
    print(f"Done for {response['result_image_path']}")
    return response

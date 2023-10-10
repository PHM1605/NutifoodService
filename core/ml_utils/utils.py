import copy, cv2, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def draw_result(img, boxes, labels=None):
    """
    Args:
        boxes (list): each is [x1, y1, x2, y2]
    """
    img0 = copy.deepcopy(img)
    classes = get_classes('classes.txt')
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i, box in enumerate(boxes):
        # random generate color
        color = np.random.randint(0,255,size=3)
        color = [int(c) for c in color]
        thickness = int(img.shape[0]/250)
        img0 = cv2.rectangle(img0, (box[0], box[1]), (box[2], box[3]), color, thickness)
        if labels is not None:
            img0 = cv2.putText(img0, classes[labels[i]], (box[0], box[1]+20), font, 0.6, color, 2)
    return img0

def get_classes(class_file):
    with open(class_file, 'r') as f:
        lines = f.readlines()
    return [line[:-1] for line in lines]

def iou_onebox(box1, box2):
    """
    Args:
        box1, box2 (BoundingBox)
    Returns:
        iou_val (float)
        
    """
    x1 = max(box1.x1, box2.x1)
    y1 = max(box1.y1, box2.y1)
    x2 = min(box1.x2, box2.x2)
    y2 = min(box1.y2, box2.y2)
    inter1 = (x2-x1) if x2>x1 else 0
    inter2 = (y2-y1) if y2>y1 else 0
    intersection = inter1 * inter2
    return intersection / (box1.area + box2.area - intersection + 1e-6)
    
def nms_multiclass(boxes, iou_threshold):
    """
    Non-max suppression among different classes
    Args:
        boxes (list): each is BoundingBox
    Returns: 
        boxes_after_nms (list): each is BoundingBox
    """
    boxes = sorted(boxes, key=lambda box: box.prob, reverse=True)
    boxes_after_nms = []
    while boxes:
        chosen_box = boxes.pop()
        boxes = [box for box in boxes 
                 if iou_onebox(chosen_box, box) < iou_threshold
                 ]
        boxes_after_nms.append(chosen_box)
    return boxes_after_nms

def put_text(img, text, loc):
    # set font size; for image-height of 640 fontsize of 16 is ok
    h = img.shape[0]
    font_size = int(16/640*h)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(os.path.join("data/fonts", "SVN-Arial 2.ttf"), font_size)
    bbox = draw.textbbox(loc, text, font=font)
    draw.rectangle(bbox, fill=(0,255,255))
    draw.text(loc, text, font=font, fill=(0,0,255))
    return np.array(img_pil)

def extract_to_image(img, response):
    detections = response["details"]["detections"]
    img = draw_result(img, detections, color=(192,192,192), put_percent=True)
    return img

if __name__ == '__main__':
    # Check get_classes()
    print(get_classes('classes.txt'))
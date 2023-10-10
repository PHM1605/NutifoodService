import numpy as np
from .config import threshold_table
from .models import BoundingBox

def analyze_groups(grps, request):
    """
    Args:
        grps (list): [[box, box, box, box], [...]]
    """
    response = request
    grps = [grp for grp in grps if len(grp) == 4]
    ana_result = {'locs': [], 'labels': []}
    for grp in grps:
        ana_result['locs'].append([grp[0].x1, grp[0].y1, grp[-1].x2, grp[-1].y2])
        ana_result['labels'].append(grp[0].label)
    
    # Calculate level
    def count_labels(labels, selected_label):
        return len([lab for lab in labels if lab==selected_label])
    
    def check_all_greater(xs, ys):
        assert len(xs) == (ys), "ERROR: not equal length"
        for i, x in enumerate(xs):
            if x < ys[i]:
                return False
        return True

    # count products belong to each class
    list_labels = [count_labels(ana_result['labels'], cl) for _, cl in enumerate(request["classes"])]
    response["analysis_result"] = -1
    for ilevel, level in enumerate(reversed(threshold_table)):
        if check_all_greater(list_labels, level):
            response["analysis_result"] = ilevel
    return response

def group_boxes(boxes):
    # Sort from upper to lower
    boxes = sort_upper_to_lower(boxes)
    
    # Group boxes according to height 
    # sorted_boxes: [[box,box,box,box], [box,box], [box,box,box]]
    sorted_boxes = []
    list_y = np.array([b.cen_y for b in boxes])
    diff_y = list_y[1:] - list_y[:-1]
    threshold_h = boxes[0].h/5
    threshold_w = boxes[0].w/2
    indices = np.argwhere(diff_y > threshold_h)[:,0] + 1
    indices = np.append(0, indices)
    indices = np.append(indices, len(list_y))
    sorted_boxes = [boxes[indices[i]:indices[i+1]] for i in range(len(indices)-1)]
    
    # Sort boxes from left to right
    # sorted_boxes: [[box,box,box,box], [box,box], [box,box,box]]
    for i, boxes in enumerate(sorted_boxes):
        boxes = sort_left_to_right(boxes)
        sorted_boxes[i] = boxes
    
    # Remove column(s) which are too far
    for i_row, boxes in enumerate(sorted_boxes):
        boundaries = []
        for i in range(len(boxes)-1):
            if boxes[i+1].x1 - boxes[i].x2 > threshold_w:
                boundaries.append(i+1)
        def count_boxes(boxes):
            return len([box for box in boxes])
        if len(boundaries) > 0:
            boundaries = np.append(0, boundaries)
            boundaries = np.append(boundaries, len(boxes))
            num_boxes = [count_boxes(boxes[boundaries[i]:boundaries[i+1]])
                         for i in range(len(boundaries)-1)]
            chosen_idx = np.argmax(num_boxes)
            sorted_boxes[i_row] = boxes[boundaries[chosen_idx] : boundaries[chosen_idx+1]]
    
    # Remove row(s) which are too far 
    boundaries = [] 
    for i in range(len(sorted_boxes)-1):
        if sorted_boxes[i+1][0].y1 - sorted_boxes[i][0].y2 > threshold_h:
            boundaries.append(i+1)
    if len(boundaries) > 0:
        boundaries = np.append(0, boundaries)
        boundaries = np.append(boundaries, len(sorted_boxes))
        num_boxes = [count_boxes(sorted_boxes[boundaries[i]:boundaries[i+1]])
                     for i in range(len(boundaries)-1)]
        chosen_idx = np.argmax(num_boxes)
        sorted_boxes = sorted_boxes[boundaries[chosen_idx] : boundaries[chosen_idx+1]]
        
    # Group in set of 4
    groups = []
    group = []
    for boxes in sorted_boxes:
        for box in boxes:
            if len(group) == 0:
                group.append(box)
                continue
            if (
                    box.label != group[-1].label # different label
                    or len(group) >=4):
                groups.append(group)
                group = [box]
            else:
                group.append(box)
        groups.append(group)
        group = []
        
    return groups 

def sort_upper_to_lower(boxes):
    boxes.sort(key = lambda box: box.cen_y)
    return boxes

def sort_left_to_right(boxes):
    boxes.sort(key = lambda box: box.cen_x) 
    return boxes

def get_boxes(result_dict):
    boxes = []
    for box in result_dict["details"]["detections"]:
        boxes.append( BoundingBox(box[0], box[1], box[2], box[3], box[4], box[-1]) )
    return boxes

def check_thresholds(classes):
    


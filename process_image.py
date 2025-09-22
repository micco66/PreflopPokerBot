import cv2

def process_frame(frame, rois):
    """
    Minimal example: for each ROI, replace that region with a Canny edge map.
    """
    out = frame.copy()
    for (x, y, w, h) in rois:
        roi = frame[y:y+h, x:x+w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        out[y:y+h, x:x+w] = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return out

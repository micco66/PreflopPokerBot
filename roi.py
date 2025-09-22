import cv2

def get_rois(frame):
    #using pixels on my PC not robust for other systems.
    card_roi_x, card_roi_y, card_roi_width, card_roi_height = 300, 320, 150, 150 
    frame2 = frame.copy()
    cv2.rectangle(frame2, (card_roi_x, card_roi_y), (card_roi_x+card_roi_width, card_roi_y+card_roi_height), (0, 255, 0), 2)
    #seperate live video feed of just ROI
    card_roi_video_in = frame[card_roi_y:card_roi_y+card_roi_height, card_roi_x:card_roi_x+card_roi_width].copy()

    return frame2, card_roi_video_in
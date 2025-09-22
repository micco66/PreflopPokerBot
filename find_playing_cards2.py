import cv2
import numpy as np

def get_playing_cards(video_in):
    """
    To find Playing Cards from a live video feed of the ROI. 
    convert the ROI to greyscale and then threshold it.
    We find the contours in the thresholded image, 
    then sort contours based on area in descending order. 
    select the two largest contours, these are the playing cards. 
    """
    video_in_copy_for_drawing = video_in.copy()
    video_in_copy_for_drawing_in_range_contours = video_in.copy()

    #convert ROI to greyscale.
    gray_video_in = cv2.cvtColor(video_in, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('DEBUG gray VideoIn : ', gray_video_in) 

    #Threshold image. 
    _, threshold_video_in = cv2.threshold(gray_video_in, 220, 255, cv2.THRESH_BINARY) 
    #cv2.imshow('DEBUG threshold VideoIn : ', threshold_video_in) 

    #find contours in thresholded image.
    video_in_contours, _ = cv2.findContours(threshold_video_in, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #draw contours on copy of frame. 
    cv2.drawContours(video_in_copy_for_drawing, video_in_contours, -1, (0, 255, 0), 2) 
    cv2.imshow('DEBUG contours ALL contours found : ', video_in_copy_for_drawing) 

    print(" Number of contours found: ", len(video_in_contours))

    contours_filtered_by_area = filter_contours_by_area(video_in_contours, 1400, 2000)





    def filter_contours_by_area(contours, min_area, max_area):
        """
        Filter contours based on a specified area range.
        """
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if playing_card_min_area <= area <= playing_card_max_area:
            filtered_contours.append(contour)
    return filtered_contours

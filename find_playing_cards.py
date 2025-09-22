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

    #sort contours by area in descending order.
    sorted_contours = sorted(video_in_contours, key=cv2.contourArea, reverse=True)

    #debug contours. 
    #for i, cnt in enumerate(sorted_contours):
    #    area = cv2.contourArea(cnt)
    #    print(f"Contour {i} area: {area}")

    #select the two largest contours.
    playing_card_1_contour = sorted_contours[0]
    playing_card_2_contour = sorted_contours[1]

    #verify the two largest contours are within the expected area range.
    playing_card_area_in_spec_bool = playing_card_area(playing_card_1_contour, playing_card_2_contour)
    print("playing card area in spec: ", playing_card_area_in_spec_bool)

    if playing_card_area_in_spec_bool:
        #draw the two largest contours on copy of frame.
        #draw contours on copy of frame. 
        cv2.drawContours(video_in_copy_for_drawing_in_range_contours, playing_card_1_contour, -1, (0, 255, 0), 2) 
        cv2.drawContours(video_in_copy_for_drawing_in_range_contours, playing_card_2_contour, -1, (0, 255, 0), 2)
        cv2.imshow('DEBUG Contours found in Range : ', video_in_copy_for_drawing_in_range_contours) 
        #verify the contours are rectangular in shape.

    #just a place holder for now.....
        return threshold_video_in

def playing_card_area(contour1, contour2):

    """
    Check if the area of the two contours is within the expected range for playing cards.
    Playing card dimensions: 2.5 inches by 3.5 inches (63.5 mm by 88.9 mm)
    Area in square inches: 2.5 * 3.5 = 8.75 square inches
    Area in square mm: 63.5 * 88.9 = 5647.15 square mm
    """

    #find area of contours. returns area in pixels^2. 
    playing_card_1_contour_area = cv2.contourArea(contour1)
    playing_card_2_contour_area = cv2.contourArea(contour2)
    print("playing card 1 contour area: ", playing_card_1_contour_area)
    print("playing card 2 contour area: ", playing_card_2_contour_area)

    # Define acceptable area range (in pixels) for playing cards.
    # These values may need to be adjusted based on camera resolution and distance.
    playing_card_min_area = 1400  # Minimum area in pixels
    playing_card_max_area = 2000 # Maximum area in pixels
    card_min_area_bool = False
    card_max_area_bool = False

    #check if both contour areas are within the acceptable range of a playing card. 

    #playing card area less then max area. 
    if (playing_card_1_contour_area < playing_card_max_area) and (playing_card_2_contour_area < playing_card_max_area):
        card_min_area_bool = True 
    
    #playing card area greater then min area. 
    if (playing_card_1_contour_area > playing_card_min_area ) and (playing_card_2_contour_area > playing_card_min_area):
        card_max_area_bool = True 

    playing_card_area_in_spec = card_min_area_bool and card_max_area_bool

    return playing_card_area_in_spec

def filter_contours_by_area(contours, min_area, max_area):
    """
    Filter contours based on a specified area range.
    """
    playing_card_min_area = 1400  # Minimum area in pixels
    playing_card_max_area = 2000 # Maximum area in pixels
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if playing_card_min_area <= area <= playing_card_max_area:
            filtered_contours.append(contour)
    return filtered_contours



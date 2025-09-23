import cv2
import numpy as np  

def isolate_playing_card(video_in, card_contour):
    """
    GOAL: Isolate the playing card. Using image segmentation.
    Save the isolated playing card as a still image 
    Display still image of isolated playing cards.
    """
    #card contour contains your two contours. 
    cnt1, cnt2 = card_contour

    # get bounding rectangles for each contour
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    x2, y2, w2, h2 = cv2.boundingRect(cnt2)

    #determine which is left/right 
    if x1 < x2:
        left_playing_card = cnt1
        right_playing_card = cnt2
    else:
        left_playing_card = cnt2
        right_playing_card = cnt1

    #get positions of bounding rectangles for left and right playing cards.
    left_playing_card_countour_x1, left_playing_card_countour_y1, left_playing_card_countour_w1, left_playing_card_countour_h1 = cv2.boundingRect(left_playing_card)
    right_playing_card_countour_x1, right_playing_card_countour_y1, right_playing_card_countour_w1, right_playing_card_countour_h1 = cv2.boundingRect(right_playing_card)

    #crop the playing cards from the video_in image.
    left_playing_card_ROI = video_in[left_playing_card_countour_y1:left_playing_card_countour_y1 + left_playing_card_countour_h1, left_playing_card_countour_x1:left_playing_card_countour_x1 + left_playing_card_countour_w1].copy()
    right_playing_card_ROI = video_in[right_playing_card_countour_y1:right_playing_card_countour_y1 + right_playing_card_countour_h1, right_playing_card_countour_x1:right_playing_card_countour_x1 + right_playing_card_countour_w1].copy()
    
    cv2.imshow("DEBUG left playing card ROI", left_playing_card_ROI)
    cv2.imshow("DEBUG right playing card ROI", right_playing_card_ROI)

    #save the isolated playing cards as still images.
    cv2.imwrite("left_playing_card_ROI.png", left_playing_card_ROI)
    cv2.imwrite("right_playing_card_ROI.png", right_playing_card_ROI)

    return left_playing_card_ROI, right_playing_card_ROI
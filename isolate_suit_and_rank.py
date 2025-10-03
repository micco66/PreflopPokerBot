import cv2

def isolate_suit_and_rank(left_playing_card, right_playing_card):
    """
    GOAL: Isolate the suit and rank from a playing card image. Which is stored in the top left corner of the card. 
    Return the cropped image.
    """

    suit_rank_isolation_distance_width = 25
    suit_rank_isolation_distance_height = 35
    top_left_corner_y = 0
    top_left_corner_x = 0

    #draw ROI on top left corner of playing card. To isolate suit and rank.
    left_playing_card_suit_rank = left_playing_card[top_left_corner_y:top_left_corner_y + suit_rank_isolation_distance_height,top_left_corner_x:top_left_corner_x + suit_rank_isolation_distance_width].copy()
    #display the isolated suit and rank image.
    cv2.imshow("DEBUG left suit and rank isolated", left_playing_card_suit_rank)

    return left_playing_card_suit_rank, right_playing_card

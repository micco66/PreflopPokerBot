import cv2
from camera import open_camera
from roi import get_rois
from find_playing_cards import get_playing_cards
from isolate_playing_card import isolate_playing_card
from isolate_suit_and_rank import isolate_suit_and_rank

def main():

    #open camera. 
    live_video_in = open_camera(1)

    #process live video hit 'q' to quit process. 
    while True:
        
        ok, live_video_in_frame = live_video_in.read()

        if not ok:
            print("Cannot read from camera")
            break
        
        #original live video feed. 
        #cv2.imshow("Original live video feed.(q to quit)", live_video_in_frame)
        #cv2.moveWindow("Original live video feed.(q to quit)", 0,0)

        live_video_with_drawn_rois = get_rois(live_video_in_frame)
        live_video_full_frame = live_video_with_drawn_rois[0]
        live_vdeo_ROI_frame = live_video_with_drawn_rois[1]

        #Display ROI on full video feed and just the ROI video feed.
        cv2.imshow("ROI's drawn on video in", live_video_full_frame)
        cv2.moveWindow("ROI's drawn on video in", 0,0)

        #find playing cards in ROI video feed.
        card_countour = get_playing_cards(live_vdeo_ROI_frame)

        #crop playing cards to isolate suit and rank. 
        if len(card_countour) == 2:
            print("Playing cards detected, isolating playing card.")
            isolate_playing_card_ROI = isolate_playing_card(live_vdeo_ROI_frame, card_countour)
            left_playing_card = isolate_playing_card_ROI[0]
            right_playing_card = isolate_playing_card_ROI[1]
            left_suit_rank, right_suit_rank = isolate_suit_and_rank(left_playing_card, right_playing_card)
            #cv2.imshow("suit and rank isolated image", isolate_suit_and_rank)

        else:
            print("Playing cards not properly detected, skipping Card /suit and rank isolation.")

        #cv2.imshow("display threshold video", card_countour)
        
        #find playing cards in ROI video feed.
        #processed = process_frame(annotated, rois)
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    live_video_in.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
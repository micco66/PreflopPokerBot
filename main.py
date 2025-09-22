import cv2
from camera import open_camera
from roi import get_rois
from find_playing_cards import get_playing_cards
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
        cv2.imshow("Original live video feed.(q to quit)", live_video_in_frame)
        live_video_with_drawn_rois = get_rois(live_video_in_frame)
        live_video_full_frame = live_video_with_drawn_rois[0]
        live_vdeo_ROI_frame = live_video_with_drawn_rois[1]

        #Display ROI on full video feed and just the ROI video feed.
        cv2.imshow("ROI's drawn on full video.", live_video_full_frame)
        cv2.imshow("just ROI video feed. ", live_vdeo_ROI_frame)

        #find playing cards in ROI video feed.
        card_countour = get_playing_cards(live_vdeo_ROI_frame)

        #crop playing cards to isolate suit and rank. 
        suit_and_rank_image = isolate_suit_and_rank(live_vdeo_ROI_frame, card_countour)


        #cv2.imshow("display threshold video", card_countour)
        
        #find playing cards in ROI video feed.
        #processed = process_frame(annotated, rois)
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    live_video_in.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
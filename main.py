import cv2
from camera import open_camera
from roi import get_rois
from find_playing_cards import get_playing_cards

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

        #Drawn ROIS on live video feed
        cv2.imshow("ROI's drawn on full video.", live_video_with_drawn_rois[0])

        #just ROI video feed
        cv2.imshow("just ROI video feed. ", live_video_with_drawn_rois[1])

        #Get playing cards in ROI video feed. 
        card_countour = get_playing_cards(live_video_with_drawn_rois[1])
        #cv2.imshow("display threshold video", card_countour)
        
        #find playing cards in ROI video feed.
        #processed = process_frame(annotated, rois)
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    live_video_in.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
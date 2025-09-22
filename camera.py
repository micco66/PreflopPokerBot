import cv2, time

def open_camera(index=1):
    """
    Opens a camera device with a given index.
    Tries multiple backends for compatibility across systems.
    Returns: an open cv2.VideoCapture object if successful.
    """
    # Try a couple backends so USB cams on Windows behave
    # - CAP_DSHOW: DirectShow (common on Windows)
    # - CAP_MSMF:  Media Foundation (newer Windows API)
    # - 0:         Default backend
    for api in (cv2.CAP_DSHOW, cv2.CAP_MSMF, 0):

         # Attempt to open the camera with the current backend
        cap = cv2.VideoCapture(index, api)

         # If it didn’t open, release and try the next backend
        if not cap.isOpened():
            if cap: cap.release()
            continue
        # If it did open, "warm up" the camera by grabbing a few frames.
        # Some USB cameras return bad/black frames on the very first reads.
        frame = None
        for _ in range(5):
            ok,_ = cap.read()
            if ok:
                # Success! Return the open VideoCapture object
                return cap
            time.sleep(0.02)
        cap.release()
    raise IOError(f"Cannot open camera {index}")

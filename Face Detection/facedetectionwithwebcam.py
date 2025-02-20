import cv2
import sys

def initialize_face_detector():
    """Initialize the face detection cascade classifier."""
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Error: Could not load face cascade classifier")
        sys.exit(1)
    return face_cascade

def setup_video_capture():
    """Initialize video capture from default camera."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture device")
        sys.exit(1)
    return cap

def detect_and_display_faces():
    """Main function to perform real-time face detection."""
    # Initialize face detector and video capture
    face_cascade = initialize_face_detector()
    cap = setup_video_capture()
    
    try:
        while True:
            # Read frame from video capture
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Convert to grayscale for face detection
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the frame
            faces = face_cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            # Draw rectangles around detected faces and show face ROIs
            for (x, y, w, h) in faces:
                # Draw blue rectangle around face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                
                # Extract and display face region of interest (ROI)
                face_roi = frame[y:y + h, x:x + w]
                cv2.imshow('Detected Face', face_roi)
            
            # Display the main frame
            cv2.imshow('Face Detection', frame)
            
            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        # Clean up resources
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_display_faces()
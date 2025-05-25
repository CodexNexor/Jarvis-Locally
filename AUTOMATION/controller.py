import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
active_window = None
smoothing_factor = 0.5  # Smoothing factor for better motion handling
stop_tracking = False  # Flag to stop tracking

def move_window(dx, dy):
    """Moves the active window by the given relative change."""
    try:
        pyautogui.dragRel(dx, dy, duration=0.1)  # Smooth dragging
    except Exception as e:
        print(f"[ERROR] Failed to move window: {e}")

def stop_control():
    """Stops hand tracking by setting the stop flag."""
    global stop_tracking
    stop_tracking = True
    print("[INFO] Stopping hand tracking...")

def track_hand():
    global prev_x, prev_y, stop_tracking
    while not stop_tracking:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_finger = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                h, w, _ = frame.shape
                index_x, index_y = int(index_finger.x * w), int(index_finger.y * h)
                thumb_x, thumb_y = int(thumb_finger.x * w), int(thumb_finger.y * h)

                distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5
                if distance < 60:  # Close fingers to trigger drag
                    if prev_x == 0 and prev_y == 0:
                        prev_x, prev_y = index_x, index_y
                    dx = int((index_x - prev_x) * smoothing_factor)
                    dy = int((index_y - prev_y) * smoothing_factor)
                    move_window(dx, dy)
                    prev_x, prev_y = index_x, index_y
                
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or stop_tracking:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    track_hand()

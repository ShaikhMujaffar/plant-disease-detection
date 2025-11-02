import cv2
import numpy as np
import os

# ============================================================
# CONFIGURATION
# ============================================================
USE_LAPTOP_CAM = False      # Set True for webcam mode
USE_SINGLE_IMAGE = True     # Set True for single image mode
UPLOAD_IMAGE_PATH = UPLOAD_IMAGE_PATH = r"C:\Users\Muzaffar\Desktop\mujju\infected_leaf.jpg"
  # Change this to your test image path
OUTPUT_FOLDER = "out"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ============================================================
# FUNCTION TO DETECT DISEASED AREAS
# ============================================================
def detect_disease(image):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define healthy (green) color range
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Invert to get non-green (possibly infected) areas
    mask_infected = cv2.bitwise_not(mask_green)

    # Calculate infection percentage
    total_pixels = image.shape[0] * image.shape[1]
    infected_pixels = np.count_nonzero(mask_infected)
    infection_fraction = infected_pixels / total_pixels
    infection_percent = round(infection_fraction * 100, 2)

    # Classify infection severity
    if infection_percent < 10:
        status = "Healthy"
        color = (0, 255, 0)
    elif infection_percent < 30:
        status = "Mild Infection"
        color = (0, 255, 255)
    else:
        status = "Severe Infection"
        color = (0, 0, 255)

    # Draw results on image
    result = image.copy()
    cv2.putText(result, f"Infection: {infection_percent}%", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(result, f"Status: {status}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Combine original and mask for visualization
    mask_bgr = cv2.cvtColor(mask_infected, cv2.COLOR_GRAY2BGR)
    combined = np.hstack((image, mask_bgr, result))

    return combined, infection_percent, status

# ============================================================
# MAIN PROGRAM
# ============================================================
def main():
    print("=== PLANT DISEASE DETECTION SYSTEM ===")

    if USE_LAPTOP_CAM:
        print("Running webcam mode... Press 'q' to quit.")
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            output, infection_percent, status = detect_disease(frame)
            cv2.imshow("Disease Detection", output)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    elif USE_SINGLE_IMAGE:
        print(f"Analyzing image: {UPLOAD_IMAGE_PATH}")
        img = cv2.imread(UPLOAD_IMAGE_PATH)
        if img is None:
            print("❌ Error: Could not load image. Check path.")
            return

        output, infection_percent, status = detect_disease(img)
        output_path = os.path.join(OUTPUT_FOLDER, "result.png")
        cv2.imwrite(output_path, output)
        print(f"✅ Done! Saved result to {output_path}")
        print(f"Detected infection: {infection_percent}% - {status}")

        cv2.imshow("Result", output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        print("⚠️ Please enable either USE_LAPTOP_CAM or USE_SINGLE_IMAGE")

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    main()

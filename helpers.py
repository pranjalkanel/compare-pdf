import cv2
import numpy as np
from PIL import Image

def highlight_differences(image1, image2, output_path, threshold=30):
    # Open the two images
    img1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)

    # Compute the absolute difference between the two images
    diff_image = cv2.absdiff(img1, img2)

    # Apply a threshold to create a binary image
    _, thresh_diff = cv2.threshold(diff_image, threshold, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract bounding rectangles from the contours
    rectangles = [cv2.boundingRect(contour) for contour in contours]

    # Merge nearby rectangles
    merged_rectangles = merge_nearby_rectangles(rectangles, max_distance=50)

    # Draw rectangles around each contour
    img_with_rectangles = img2.copy()
    
    for rect in merged_rectangles:
        x, y, w, h = rect
        overlay = img_with_rectangles.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (160, 160, 255), thickness=cv2.FILLED) #cv2.rectangle accepts color code in bgr format and not rgb
        img_with_rectangles = cv2.addWeighted(overlay, 0.5, img_with_rectangles, 1 - 0.5, 0) #0.5 is the opacity



    # ** CODE FOR BIG RECTANGLES**
    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.rectangle(img_with_rectangles, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Convert the result back to PIL Image for saving
    result_image = Image.fromarray(cv2.cvtColor(img_with_rectangles, cv2.COLOR_BGR2RGB))

    # Save the result
    result_image.save(output_path)

def merge_nearby_rectangles(rectangles, max_distance):
    merged_rectangles = []

    for rect in rectangles:
        x, y, w, h = rect
        merged = False

        for merged_rect in merged_rectangles:
            mx, my, mw, mh = merged_rect

            # Check if the rectangles are close horizontally or vertically
            if (
                abs(x + w/2 - mx - mw/2) < max_distance and
                abs(y + h/2 - my - mh/2) < max_distance
            ):
                # Merge the rectangles
                mx = min(x, mx)
                my = min(y, my)
                mw = max(x + w, mx + mw) - mx
                mh = max(y + h, my + mh) - my
                merged_rect[0], merged_rect[1], merged_rect[2], merged_rect[3] = mx, my, mw, mh   #merges y-axis as well 
                # merged_rect[0], merged_rect[2], merged_rect[3] = mx, mw, mh
                merged = True
                break

        if not merged:
            merged_rectangles.append([x, y, w, h])

    return [tuple(rect) for rect in merged_rectangles]
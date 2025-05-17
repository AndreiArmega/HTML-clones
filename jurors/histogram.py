from PIL import Image
import numpy as np
import cv2

def calculate_histogram_similarity(img_path1: str, img_path2: str) -> float:
    img1 = Image.open(img_path1)
    img2 = Image.open(img_path2)

    img1_gray = img1.convert("L")
    img2_gray = img2.convert("L")

    img1_array = np.array(img1_gray)
    img2_array = np.array(img2_gray)

    hist1 = cv2.calcHist([img1_array], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2_array], [0], None, [256], [0, 256])

    
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()

    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return correlation

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python histogram.py <image1> <image2>")
        sys.exit(1)

    score = calculate_histogram_similarity(sys.argv[1], sys.argv[2])
    print(f"{score:.4f}")


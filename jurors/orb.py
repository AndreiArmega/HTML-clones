import sys
import cv2

def calculate_orb_similarity(img_path1: str, img_path2: str) -> float:
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise ValueError(f"Could not load one or both images: {img_path1}, {img_path2}")

    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return 0.0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    matches = sorted(matches, key=lambda x: x.distance)

    num_matches = len(matches)
    min_keypoints = min(len(kp1), len(kp2))
    similarity_score = num_matches / min_keypoints if min_keypoints > 0 else 0.0

    return similarity_score


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python orb.py <image1.png> <image2.png>")
        sys.exit(1)

    try:
        score = calculate_orb_similarity(sys.argv[1], sys.argv[2])
        print(f"{score:.4f}")
    except ValueError as e:
        sys.exit(1)

import cv2
from skimage.metrics import structural_similarity as ssim

def calculate_ssim(img_path1: str, img_path2: str) -> float:
    img1 = cv2.imread(img_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise ValueError("Error loading one or both images.")

    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]), interpolation=cv2.INTER_AREA)

    similarity_index, _ = ssim(img1, img2, full=True, data_range=255)
    return similarity_index

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compare_ssim.py <image1> <image2>")
        sys.exit(1)

    score = calculate_ssim(sys.argv[1], sys.argv[2])
    print(f"{score:.4f}")



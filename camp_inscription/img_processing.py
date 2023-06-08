import os
import cv2
import numpy as np


def img_color_processing(img: np.ndarray) -> np.ndarray:
    """Function that transforms the image to black and white and inverts the colors of the image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    return gray


def process_images_in_dir(input_path: str, output_path: str) -> None:
    """Function that processes all images in the directory"""
    imgs = os.listdir(input_path)
    for img in imgs:
        img_path = os.path.join(input_path, img)
        out_path = os.path.join(output_path, img)
        img = cv2.imread(img_path)
        img = img_color_processing(img)
        cv2.imwrite(out_path, img)


def main() -> None:
    """Main function"""
    input_path = os.path.join(os.getcwd(), "camp_inscription/imgs/logos/y2023")
    output_path = os.path.join(os.getcwd(), "camp_inscription/imgs/inv_logos/y2023")
    process_images_in_dir(input_path, output_path)


if __name__ == "__main__":
    main()

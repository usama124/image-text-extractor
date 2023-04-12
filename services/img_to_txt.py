import cv2
import pytesseract
from langdetect import detect_langs


try:
    from PIL import Image
except ImportError:
    import Image


def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # display(thresh)

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        cv2.rectangle(newImage, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    # print(largestContour)
    print(len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("Data/boxes.jpg", newImage)
    # display("boxes.jpg")
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    # print(minAreaRect)
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle


def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage


def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    print(angle)
    return rotateImage(cvImage, 1.0 * (270 - angle))


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def img_to_txt(img_path: str):
    import os, shutil
    if not os.path.exists("/app/.apt/usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata"):
        print("rus.traineddata file not exists, copying...")
        rus_traindata_file_path = "/app/traineddata/rus.traineddata"
        shutil.copy(rus_traindata_file_path, "/app/.apt/usr/share/tesseract-ocr/4.00/tessdata/")

    if os.path.exists("/app/.apt/usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata"):
        print("rus.traineddata file exists")
    else:
        print("rus.traineddata file not exists")

    img = cv2.imread(img_path)
    fixed = deskew(img)
    # cv2.imwrite("rotated_fixed.jpg", fixed)
    gray_image = grayscale(fixed)

    print(pytesseract.get_languages(config=''))

    img_rgb = cv2.cvtColor(gray_image, cv2.COLOR_BGR2RGB)
    custom_config = r'-l eng+rus --psm 6'
    extractedInformation = pytesseract.image_to_string(img_rgb, config=custom_config)
    detect_langs(extractedInformation)

    return extractedInformation

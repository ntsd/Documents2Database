import difflib
import os

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2

import codecs

#  find Tesseract-OCR path
if os.path.isdir('C:/Program Files (x86)/Tesseract-OCR'):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
elif os.path.isdir('C:/Program Files/Tesseract-OCR'):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
else:
    print("You need to install Tesseract-OCR")

def preprocess(im):
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1)
    # im = im.convert('1')
    # im.save('temp.jpg')
    return im


def image_to_string(image, lang='eng'):
    return pytesseract.image_to_string(image, lang)

def createGrayScaleImage(path, outPath, preprocess="thresh"):
    # load the example image and convert it to grayscale
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    cv2.imwrite(outPath, gray)

if __name__ == '__main__':
    im = Image.open(url)
    im_out = preprocess(im)
    text = pytesseract.image_to_string(im_out, lang='eng+tha')
    print(text)

    # use to check diff
##    try:
##        file = codecs.open('tmp/temp.text', 'r', "utf-8")
##        old_text = file.read()
##        check_diff(old_text, text)
##        file = codecs.open('tmp/temp.text', 'w', "utf-8")
##        file.write(text)
##    except:
##        file = codecs.open('tmp/temp.text', 'w', "utf-8")
##        file.write(text)
    print("\n-------- END -----------")

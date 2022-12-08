import os
import re
import cv2 
import numpy as np
import pytesseract
from pytesseract import Output
from matplotlib import pyplot as plt
from pdf2image import convert_from_path
from PIL import Image
from numpy import *
import datetime
import pandas as pd
from shutil import copy
import shutil
import aspose.words as aw

def pdf_recognizer(pdf_name, row, directory, file_format):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'      # may be changed

    df = pd.DataFrame(columns=['File Name', 'Document Type', 'Found', 'Not Found', 'Date'])
    failures = 0
    row = row
    # Images source
    imgs_dir_short = 'path'
    IMGS_DIR = imgs_dir_short + 'Images\\'        # may be changed
    custom_config = r'--oem 1 --psm 6'
    # Convert pdf to images
    # IMG_DIR = 'path\\Files\\'      # may be changed
    IMG_FAIL_DIR = imgs_dir_short + 'Failures\\'      # may be changed
    IMG_PROPER_DIR = imgs_dir_short + 'Propers\\'      # may be changed
    poppler_path = r"C:\poppler-21.11.0\Library\bin"     # may be changed
    
    if file_format == 0:
        pages = convert_from_path(directory + '/' + pdf_name, poppler_path=poppler_path)
        num = 0
        for page in pages:
            page.save(r"path\Images\{}{}.jpg".format(pdf_name, num))       # may be changed
            num += 1
    else:
        copy(directory + '/' + pdf_name, IMGS_DIR)
        num = 1

    date_pattern = '^([1-9]|0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/([0-2][0-9]|((19|20)\d\d))$'  # EU format, slashes /, catches year 2021 and 21 - 7/12/2021 | 07/12/2021 / 7/07/2021 | 7/7/2021 etc
    date_pattern2 = '^([1-9]|0[1-9]|1[012])/([1-9]|0[1-9]|[12][0-9]|3[01])/([0-2][0-9]|((19|20)\d\d))$' # US format, slashes /, catches year 2021 and 21 
    date_pattern3 = '^([1-9]|0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$'                # EU format, dash -, catches year 2021
    date_pattern4 = '^([1-9]|0[1-9]|1[012])-([1-9]|0[1-9]|[12][0-9]|3[01])-(19|20)\d\d$'                # US format, dash -, catches year 2021
    date_short_eu = '^([1-9]|0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])'
    date_short_us = '^([1-9]|0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])'
    date_month = '^([1-9]|0[1-9]|[12][0-9]|3[01]),([0-2][0-9]|((19|20)\d\d))$'
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    only_year = '^(19|20)\d\d$'
    pdf_index = 0       # for dataframe purpose

    def lines_remover(file_name):
        # remove lines from file to make it more readable for script
        # To convert the Image From GIF to JPG
        if file_format == 3:
            img = Image.open(IMGS_DIR + file_name).convert('RGB')
            new_name = IMGS_DIR + file_name.replace('.GIF', '') + '.jpg'
            img.save(new_name)
            image = cv2.imread(new_name)
            file_name = file_name.replace('.GIF', '') + '.jpg'
        else:
            image = cv2.imread(IMGS_DIR+file_name)
        try:
            result = image.copy()
        except:
            result = image
        # if image is not read properl
        try:
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        except:
            gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(result, [c], -1, (255,255,255), 5)

        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(result, [c], -1, (255,255,255), 5)
        cv2.imwrite(r"path\Images\{}".format(file_name), result)

        return result

    def resizing(image):
        # resize image with given variables to make it more readable
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)      # reshape image, make it bigger and easier to read
        d = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DICT)
        return d

    def shrinking(image):
        # resize image with given variables to make it more readable
        image = cv2.resize(image, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_CUBIC)      # reshape image, make it smalle and easier to read for 
        d = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DICT)
        return d 

    def words_loop(image, d):
        # loop through every found word and look for date and signature
        text = 'Signature'      # text to be found inside file
        text_everify1 = 'E-Verify'
        text_everify2 = 'paycom'
        text_everify3 = 'CORTECH'
        text_everify4 = 'EVerify'
        text_everify5 = 'Verify'
        text_everify6 = 'Verification'

        text_ups = 'ups'
        text_ups_onboarding1 = 'upspre-hire'
        text_ups_onboarding2 = 'upsprehire'
        text_ups_onboarding3 = 'upson-boarding'
        text_ups_onboarding4 = 'upspre-hire'

        text_exhibit1 = 'exhibit'
        text_exhibit2 = 'exhibit12'
        text_exhibit3 = 'code'
        text_exhibit4 = 'codeofconduct'
        text_exhibit5 = 'acknowledgment'
        text_exhibit6 = 'acknowledgmentofstatus'
        text_exhibit7 = 'computer'
        text_exhibit8 = 'computeruseguidelines'
        text_exhibit9 = 'safe'
        text_exhibit10 = 'safeworkmethods'
        # delete empty values

        n_boxes = len(d['text'])
        conf = 0
        index = 0
        too_little = 0

        for i in range(n_boxes):
            # condition to only pick boxes with a confidence > 30%
            if float(d['conf'][i]) > 30:
                conf += 1   
                if re.match(text_everify1, d['text'][i]) or re.match(text_everify2, d['text'][i]) or re.match(text_everify3, d['text'][i]) or re.match(text_everify4, d['text'][i]):
                    index = 1
                    break
                elif re.match(text_everify5, d['text'][i]):
                    new_text = d['text'][i-1] + d['text'][i]
                    if new_text == text_everify4 or new_text == text_everify1:
                        index = 1
                        break
                    else:
                        index = 0
                elif re.match(text_everify6, d['text'][i]):
                    new_text = d['text'][i-1] + d['text'][i] + d['text'][i+1]
                    if new_text == 'CaseVerificationNumber:':
                        index = 1
                        break
                    else:
                        index = 0

                elif re.match(text_ups, d['text'][i].lower()):
                    ups_text = d['text'][i].lower() + d['text'][i+1].lower()
                    ups_text2 = ups_text + d['text'][i+2].lower()
                    if ups_text == text_ups_onboarding1 or ups_text == text_ups_onboarding2 or ups_text == text_ups_onboarding4 or ups_text2 == text_ups_onboarding3 or d['text'][i-2].lower() == 'ltd.':
                        index = 2
                        break
                    else:
                        pass        
                elif re.match(text_exhibit1, d['text'][i].lower()):
                    exhibit_text = d['text'][i] + d['text'][i+1]
                    if re.search(text_exhibit2, exhibit_text.lower()):
                        index = 3
                        break
                elif re.match(text_exhibit3, d['text'][i].lower()):
                    exhibit_text = d['text'][i] + d['text'][i+1] + d['text'][i+2]
                    if re.search(text_exhibit4, exhibit_text.lower()):
                        index = 3
                        break
                elif re.match(text_exhibit5, d['text'][i].lower()):
                    exhibit_text = d['text'][i] + d['text'][i+1] + d['text'][i+2]
                    if re.search(text_exhibit6, exhibit_text.lower()):
                        index = 3
                        break
                elif re.match(text_exhibit7, d['text'][i].lower()):
                    exhibit_text = d['text'][i] + d['text'][i+1] + d['text'][i+2]
                    if re.search(text_exhibit8, exhibit_text.lower()):
                        index = 3
                        break
                elif re.match(text_exhibit9, d['text'][i].lower()):
                    exhibit_text = d['text'][i] + d['text'][i+1] + d['text'][i+2]
                    if re.search(text_exhibit10, exhibit_text.lower()):
                        index = 3
                        break
                else:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)    # green
                    index = 0
            elif float(d['conf'][i]) > 10 and float(d['conf'][i]) <= 30: 
                if re.match(text_everify1, d['text'][i]) or re.match(text_everify2, d['text'][i]) or re.match(text_everify3, d['text'][i]) or re.match(text_everify4, d['text'][i]):
                    too_little += 1
 
        return too_little, index

    def display_image(image):
        # display image with marked boxes 
        b,g,r = cv2.split(image)
        rgb_img = cv2.merge([r,g,b])
        plt.figure(figsize=(16,12))
        plt.imshow(rgb_img)
        plt.title('SAMPLE DOCUMENT WITH WORD LEVEL BOXES')
        plt.show()

    def ups_signature(d, i):
        # check if it is UPS file, if so then look for signature given in a different way than usually
        n_boxes = len(d['text'])
        text = 'Signature'
        text_long = 'Signature Transaction ID:'
        for i in range(n_boxes):
            if re.match(text, d['text'][i]):
                if re.match(text_long, (d['text'][i] + ' ' + d['text'][i+1] + ' ' + d['text'][i+2])):
                    if len(d['text'][i+4]) > 10:
                        return True
                    else:
                        return False
                else:
                    return 'empty'
    
    def rectangles_rec(img_name):
        # look for rectangles that have information whether it is marked as signed or not in case of having no common signature
        # read image into array
        image_array = cv2.imread('C:\\Users\\danie\\Desktop\\UPS - Examples\\Images\\{}.jpg'.format(img_name))     # may be changed

        # convering image to gray scale
        gray_scale_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # image thresholding
        _, img_bin = cv2.threshold(gray_scale_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        img_bin = 255 - img_bin

        # Image.fromarray(img_bin).show()

        # set min width to detect horizontal lines
        line_min_width = 15
        # kernel to detect horizontal lines
        kernal_h = np.ones((1,line_min_width), np.uint8)
        # kernel to detect vertical lines
        kernal_v = np.ones((line_min_width,1), np.uint8)
        # horizontal kernel on the image
        img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
        # verical kernel on the image
        img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
        # combining the image
        img_bin_final=img_bin_h|img_bin_v
        # Image.fromarray(img_bin).show()
        final_kernel = np.ones((3,3), np.uint8)
        img_bin_final=cv2.dilate(img_bin_final,final_kernel,iterations=1)
        _, labels, stats,_ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

        quotients = []
        areas = 0
        for x,y,w,h,area in stats[2:]:
            if area >= 100:
                areas += 1
                cv2.rectangle(image_array,(x,y),(x+w,y+h),(255,255,0),2)
            
                area2 = 0
                black = np.array([0, 0, 0])

                for i in range(x, x+w):
                    for j in range(y, y+h):
                        if img_bin[j, i].all() != black.all():
                            area2 += 1
                
                quotient = area2/area
                if quotient > 0.2:
                    quotients.append(quotient)
              
        if not quotients:
            if areas != 0:
                return False
            else:
                return "empty"
        else:
            return True                

    def rectangles_rec_ups(img_name, index_line_pos, index_sign_line_pos):
        # look for rectangles that have information whether it is marked as signed or not in case of having no common signature
        # read image into array
        image_array = cv2.imread('path\\Images\\{}.jpg'.format(img_name))     # may be changed

        # convering image to gray scale
        gray_scale_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # image thresholding
        _, img_bin = cv2.threshold(gray_scale_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        img_bin = 255 - img_bin

        # Image.fromarray(img_bin).show()

        # set min width to detect horizontal lines
        line_min_width = 15
        # kernel to detect horizontal lines
        kernal_h = np.ones((1,line_min_width), np.uint8)
        # kernel to detect vertical lines
        kernal_v = np.ones((line_min_width,1), np.uint8)
        # horizontal kernel on the image
        img_bin_h = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_h)
        # verical kernel on the image
        img_bin_v = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernal_v)
        # combining the image
        img_bin_final=img_bin_h|img_bin_v
        # Image.fromarray(img_bin).show()
        final_kernel = np.ones((3,3), np.uint8)
        img_bin_final=cv2.dilate(img_bin_final,final_kernel,iterations=1)
        _, labels, stats,_ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

        quotients = []
        areas = 0
        for x,y,w,h,area in stats[2:]:
            if area >= 100:
                areas += 1
                cv2.rectangle(image_array,(x,y),(x+w,y+h),(255,255,0),2)
            
                area2 = 0
                area3 = 0
                white = np.array([255, 255, 255])
                black = np.array([0, 0, 0])

                for i in range(x, x+w):
                    for j in range(y, y+h):
                        # check if box is in the same line with index or index_sign and if it's x position is no further than 1000 pix to avoid catching No boxes
                        if y >= index_line_pos[0] - 50 and y <= index_line_pos[1] + 50 or y >= index_sign_line_pos[0] - 50 and y <= index_sign_line_pos[1] + 50:
                            if x < 1000:
                                if img_bin[j, i].all() != black.all():
                                    area2 += 1
                                if img_bin[j, i].all() != white.all():
                                    area3 += 1
                quotient = area2/area
                if quotient > 0.2:
                    quotients.append(quotient)
                
        if quotients:
            return True                

    def rect_mini(pdf_name, k):
        # look for boxes marked as signed with usage of rectangles_rec function. If found, then insert data in correct place
        img_name = "{}{}".format(pdf_name, k)
        signed = 0
        if rectangles_rec(img_name) == True:
            signed = 1
        return signed

    def rect_mini_ups(pdf_name, k,  index_line, index_sign_line):
        # look for boxes marked as signed with usage of rectangles_rec function. If found, then insert data in correct place
        img_name = "{}{}".format(pdf_name, k)
        signed = 0
        if rectangles_rec_ups(img_name,  index_line, index_sign_line) == True:
            signed = 1
        return signed

    def exhibit_words_loop(image, d):
        # loop through every found word and look for date and signature
        text = 'signature'      # text to be found inside file
        date = ''
        # delete empty values
        if row == 0:
            for i in range(20):
                try:
                    if len(d['text'][i]) == 0 or d['text'][i] == None:
                        for key in d.keys():
                            del d[key][i]
                except:
                    pass
        n_boxes = len(d['text'])
        index = 0
        index_sign = 0
        index_sign2 = 0
        index_printed = 0
        too_little = 0
        ups_index = 0
        text_ups = 'UPS'
        text_ups_long = 'UPS Pre-Employment'
        exhibit_letter = ''
        box_index = 0

        for i in range(n_boxes):
            # look for letter on exhibit page
            if re.search('exhibit', d['text'][i].lower()):
                if i < 5:
                    exhibit_letter = d['text'][i + 1].replace('12', '').replace('1', '')
                    if exhibit_letter == '4':
                        exhibit_letter = 'A'
                    
            if re.match(text_ups, d['text'][i]):
                try:
                    if re.match(text_ups_long, (d['text'][i] + ' ' + d['text'][i+1])):   
                        if ups_signature(d, i) == True:
                            ups_index = 1
                        elif ups_signature(d, i) == False:
                            ups_index = 2
                        else:
                            ups_index = 3
                        break
                    else:
                        pass
                except:
                    pass
            # condition to only pick boxes with a confidence > 30%
            if float(d['conf'][i]) > 30:
                if re.match(date_pattern, d['text'][i]) or re.match(date_pattern2, d['text'][i]) or re.match(date_pattern3, d['text'][i]) or re.match(date_pattern4, d['text'][i]):
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    # red
                    if i > 5:
                        index = i + 1
                        date = d['text'][i]   

                elif re.search(only_year, d['text'][i]):
                    new_date = d['text'][i - 2] + d['text'][i - 1] + d['text'][i] 
                    new_date2 = d['text'][i - 4] + d['text'][i - 3] + d['text'][i - 2] + d['text'][i - 1] + d['text'][i] 
                    
                    if i > 5:
                        if re.match(date_pattern, new_date) or re.match(date_pattern2, new_date) or re.match(date_pattern3, new_date) or re.match(date_pattern4, new_date):
                            date = new_date
                            index = i + 1
                            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    # red
                        elif re.match(date_pattern, new_date2) or re.match(date_pattern2, new_date2) or re.match(date_pattern3, new_date2) or re.match(date_pattern4, new_date2):
                            date = new_date2
                            index = i + 1
                            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    # red
                else:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)    # green
 
                # looking for signature
                if re.search(text, d['text'][i].lower()):
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    # red
                    if index_sign == 0:
                        index_sign = i + 1
                    else:
                        index_sign2 = i + 1

                if re.search('check', d['text'][i].lower()):
                    check_text = d['text'][i].lower() + d['text'][i + 1].lower() + d['text'][i + 2].lower()
                    if check_text == 'checktosign':
                        box_index = 1
            elif float(d['conf'][i]) > 10 and float(d['conf'][i]) <= 30: 
                if re.match(date_pattern, d['text'][i]) or re.match(date_pattern2, d['text'][i]) or re.match(date_pattern3, d['text'][i]) or re.match(date_pattern4, d['text'][i]):
                    too_little += 1
            else:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)    # blue
            
            # look for Printed Name with conf > 30 and if found then set variable 
            if re.match('Printed', d['text'][i]) and re.match('Name', d['text'][i + 1]):
                if float(d['conf'][i]) > 30 and float(d['conf'][i + 1]) > 30:
                    index_printed = i - 1
            # printing if found, if not look for separated date
            if index == 0 and i > 5:
                if re.match(date_pattern, d['text'][i]) or re.match(date_pattern2, d['text'][i]) or re.match(date_pattern3, d['text'][i]) or re.match(date_pattern4, d['text'][i]):
                    pass
                elif re.match(date_short_eu, d['text'][i]) or re.match(date_short_us, d['text'][i]):
                    try:
                        new_date = d['text'][i] + d['text'][i + 1] + d['text'][i + 2]
                        if re.match(date_pattern, new_date) or re.match(date_pattern2, new_date) or re.match(date_pattern3, new_date) or re.match(date_pattern4, new_date):
                            if re.match('^([0-2][0-9]|((19|20)\d\d))', d['text'][i + 2]):
                                index = i + 3
                                date = new_date
                    except:
                        pass
            # if date is in format Apr 23, 2021
            if d['text'][i].strip() in months:
                if re.match(date_month, d['text'][i + 1]):
                    date = d['text'][i] + d['text'][i + 1]
                    index = i + 2
                elif re.match(date_month, (d['text'][i + 1] + d['text'][i + 2])):
                    date = d['text'][i] + d['text'][i + 1] + d['text'][i + 2] 
                    index = i + 3
        return too_little, index, index_sign, image, ups_index, index_printed, date, exhibit_letter, box_index, index_sign2

    def exhibit_pages_loop(start, num, row, pdf_index):
        # loop through every page and look for date and signature with usage of different functions, like words_loop
        pdf_index = pdf_index
        exhibit_pages = []
        exhibit_dates = []
        exhibit_pages_signed = []
        exhibit_pages_notsigned = []
        big_signed = 0
        nonlocal failures   # to copy not signed file to a different directory    
        for k in range(start, num):   
            if k == 0:
                if pdf_name.endswith(".pdf"):   
                    file_name = file_name_func(k, file_format)
                else:
                    file_name = pdf_name
            else:
                file_name = file_name_func(k, file_format)       
            # image = cv2.imread(IMGS_DIR + file_name) 
            # remove lines from image
            image = lines_remover(file_name)
            # create copy in case of enlarging
            image_copy = image.copy() 
            image_copy2 = image.copy()       
            # read image 
            d = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DICT)
 
            # loop through every word
            too_little, index, index_sign, image, ups_index, index_printed, date, exhibit_letter, box_index, index_sign2 = exhibit_words_loop(image, d)
            # resize image if it's too little
            if too_little != 0 or date == '':
                d = resizing(image_copy)
                too_little, index, index_sign, image, ups_index, index_printed, date, exhibit_letter, box_index, index_sign2 = exhibit_words_loop(image_copy, d)
                if date == '':
                    d = shrinking(image_copy2)
                    too_little, index, index_sign, image, ups_index, index_printed, date, exhibit_letter, box_index, index_sign2 = exhibit_words_loop(image_copy, d)
                
            n_boxes = len(d['text'])
            signature = ''
            signed = 0

            # don't add any text except signature yes/no
            if index > 1:
                try:
                    if index_sign < n_boxes:
                        
                        if index < n_boxes:
                            if index_printed != 0:
                                if len(d['text'][index]) > 0 or len(d['text'][index_sign]) > 0 or len(d['text'][index_printed]) > 0:
                                    signature = 'Yes'
                                elif d['text'][index + 1] == "|":
                                    if len(d['text'][index + 2]) > 1:
                                        signature = 'Yes'
                                elif index < index_printed:
                                    if len(d['text'][index + 1]) > 1 and d['text'][index + 1].lower() != 'printed':
                                        signature = 'Yes'
                            else:
                                if len(d['text'][index]) > 0 or len(d['text'][index_sign]) > 0 or len(d['text'][index_sign + 1]) > 0 and d['text'][index_sign + 1].lower() != 'supplier':
                                    signature = 'Yes'
                                elif d['text'][index + 1] == "|":
                                    if len(d['text'][index + 2]) > 1:
                                        signature = 'Yes'   
                        else:    
                            if index_printed != 0:
                                if len(d['text'][index_sign]) > 0 or len(d['text'][index_printed]) > 0:
                                    signature = 'Yes'
                                elif d['text'][index + 1] == "|":
                                    if len(d['text'][index + 2]) > 1:
                                        signature = 'Yes'   
                            else:
                                # provide d['text'][index_sign + 1].lower() != 'supplier' to avoid empty lines like in UPS Daniel Pomerantz files, where in+1 is empty 
                                # and in+2 is electronically, but if it's supplier, than line is empty or not found.
                                if len(d['text'][index_sign]) > 0 or len(d['text'][index_sign + 1]) > 0 and d['text'][index_sign + 1].lower() != 'supplier':
                                    signature = 'Yes'
                                elif d['text'][index + 1] == "|":
                                    if len(d['text'][index + 2]) > 1:
                                        signature = 'Yes'            
                    else:
                        if index < n_boxes:
                            if index_printed != 0:
                                if len(d['text'][index]) > 0 or len(d['text'][index_printed]) > 0:
                                    signature = 'Yes'
                                elif d['text'][index + 1] == "|":
                                    if len(d['text'][index + 2]) > 1:
                                        signature = 'Yes'
                                elif index < index_printed:
                                    if len(d['text'][index + 1]) > 1 and d['text'][index + 1].lower() != 'printed':
                                        signature = 'Yes'
                            else:
                                if len(d['text'][index]) > 0:
                                    signature = 'Yes'
                                elif d['text'][index + 1] == "|":
                                    if len(d['text'][index + 2]) > 1:
                                        signature = 'Yes'
                        else:    
                            if index_printed != 0:
                                if len(d['text'][index_printed]) > 0:
                                    signature = 'Yes'
                            elif d['text'][index + 1] == "|":
                                if len(d['text'][index + 2]) > 1:
                                    signature = 'Yes'    
                except:
                    try:
                        signed = rect_mini(pdf_name, k)
                        big_signed = signed
                    except:    
                        pass
            
            elif index_sign != 0:
                if k == (num-1):
                    # check if last page is signed without date
                    if (index_sign + 1) < n_boxes and (index_sign2 + 1) < n_boxes:
                        if len(d['text'][index_sign]) > 0 and d['text'][index_sign].lower() != 'supplier' or len(d['text'][index_sign + 1]) > 0 and d['text'][index_sign + 1].lower() != 'supplier':
                            signed = 1
                            big_signed = signed
                        elif len(d['text'][index_sign2]) > 0 and d['text'][index_sign2].lower() != 'date:' or len(d['text'][index_sign2 + 1]) > 0 and d['text'][index_sign2 + 1].lower() != 'date:':
                            signed = 1
                            big_signed = signed
                        else:
                            signed = rect_mini(pdf_name, k)
                            big_signed = signed   
                    else:
                        signed = rect_mini(pdf_name, k)
                        big_signed = signed 
                else:
                    signed = rect_mini(pdf_name, k)
                    big_signed = signed
            elif ups_index != 0:
                if ups_index == 1:
                    signature = 'Yes'
            try:
                if d['text'][index - 4].lower() == 'printed':
                    if len(d['text'][index - 8]) > 0 and d['text'][index - 8].lower() != '' and d['text'][index - 8].lower() != 'signature':
                        signature = 'Yes'
            except:
                pass

            if index_printed != 0 and signed == 0:
                if d['text'][index_printed-1] == '|' and len(d['text'][index_printed-2]):
                    if d['text'][index_printed-3] == date or d['text'][index_printed-4] == date or d['text'][index_printed-5] == date:
                        signed = 1
                        signature = 'Yes'
                        big_signed = signed
            # check if there is a box to be checked
            if box_index != 0 and signed == 0:
                signed = rect_mini(pdf_name, k)
                big_signed = signed
            # check if document is signed or not
            # add letters of signed documents (Exhibit 12A, 12B...)
            if len(exhibit_letter) > 0:
                exhibit_pages.append(exhibit_letter)
            # check if signed by date
            if len(date) > 0 and signature == 'Yes':
                if len(exhibit_dates) < len(exhibit_pages):
                    exhibit_dates.append(date)
                    # add document as completed
                    if len(exhibit_dates) == len(exhibit_pages):
                        if exhibit_pages[-1] not in exhibit_pages_signed:
                            exhibit_pages_signed.append(exhibit_pages[-1])
            if signed == 1 and len(exhibit_dates) == 3 and len(exhibit_pages) == 4:
                exhibit_pages_signed.append(exhibit_pages[-1])
                exhibit_dates.append(exhibit_dates[0])
            # add document as not completed
            if len(exhibit_pages) > (len(exhibit_dates) + 1) :
                if exhibit_pages[-2] not in exhibit_pages_notsigned:
                    exhibit_pages_notsigned.append(exhibit_pages[-2])
                    exhibit_pages.pop(-2)
            if signed == 0 and index != 0 and index_sign != 0 and index_sign2 != 0:
                if d['text'][index-2].lower() == 'date:' or d['text'][index-2].lower() == 'dare':
                    if len(d['text'][index_sign]) > 0 or len(d['text'][index_sign2]) > 0:
                        signed = 1
                        big_signed = signed
                elif index_printed > index and len(d['text'][index_printed - 1]) > 0 and d['text'][index_printed - 1] != date:
                    signed = 1
                    big_signed = signed
            if k == (num-1):
                if len(exhibit_pages) == 0 and big_signed > 0:
                    signed = big_signed
                if len(exhibit_pages) > len(exhibit_dates) :
                    if exhibit_pages[-1] not in exhibit_pages_notsigned:
                        exhibit_pages_notsigned.append(exhibit_pages[-1])
                df.loc[row, ['File Name']] = pdf_name

                if len(exhibit_pages_signed) > 0 or len(exhibit_pages_notsigned) > 0:
                    if len(exhibit_pages_signed) > 0:
                        df.loc[row, ['Found']] = str(sorted(exhibit_pages_signed)).replace('[', '').replace(']', '')
                    if len(exhibit_pages_notsigned) > 0:
                        df.loc[row, ['Not Found']] = str(sorted(exhibit_pages_notsigned)).replace('[', '').replace(']', '')
                      
                elif signed != 0:
                    df.loc[row, ['Found']] = 'Signed'
                else:
                    if signature == 'Yes':
                        df.loc[row, ['Found']] = 'Signed'
                    else:
                        df.loc[row, ['Not Found']] = 'Not signed'
                if len(exhibit_dates) > 0:
                    df.loc[row, ['Date']] = exhibit_dates[0]
                elif len(date) > 0:
                    df.loc[row, ['Date']] = date

                row += 1  

        if len(exhibit_pages_notsigned) > 0:
            failures += 1   # to copy not signed file to a different directory    
        return d
    
    def everify_words_loop(image, d):
        # loop through every found word and look for date and signature 
        n_boxes = len(d['text'])
        index = 0
        index_not = 0
        too_little = 0
        text_report = 'report'      # text to be found inside file
        text_report_long = 'reportstatus'
        text_complete = 'complete'
        text_employ = 'employment'
        text_employ_long = 'employmentauthorized'
        date = ''
        for i in range(n_boxes):  
            # condition to only pick boxes with a confidence > 30%
            if float(d['conf'][i]) > 30:    
                # looking for report status
                if re.match(date_pattern, d['text'][i]) or re.match(date_pattern2, d['text'][i]) or re.match(date_pattern3, d['text'][i]) or re.match(date_pattern4, d['text'][i]):
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    # red
                    if i > 5:
                        date = d['text'][i]
                elif re.match(date_short_eu, d['text'][i]) or re.match(date_short_us, d['text'][i]):
                    try:
                        new_date = d['text'][i] + d['text'][i + 1] + d['text'][i + 2]
                        if re.match(date_pattern, new_date) or re.match(date_pattern2, new_date) or re.match(date_pattern3, new_date) or re.match(date_pattern4, new_date):
                            if re.match('^([0-2][0-9]|((19|20)\d\d))', d['text'][i + 2]):
                                index = i + 3
                                date = new_date
                    except:
                        pass
                # if date is in format Apr 23, 2021
                elif d['text'][i].strip() in months:
                    if re.match(date_month, d['text'][i + 1]):
                        date = d['text'][i] + d['text'][i + 1]
                        index = i + 2
                    elif re.match(date_month, (d['text'][i + 1] + d['text'][i + 2])):
                        date = d['text'][i] + d['text'][i + 1] + d['text'][i + 2] 
                        index = i + 3
                        
                if re.match(text_report, d['text'][i].lower()):
                    new_text = d['text'][i] + d['text'][i+1]
                    if re.search(text_report_long, new_text.lower()):
                        if re.search(text_complete, d['text'][i+2].lower()):
                            index = i + 2    
                        else:
                            index_not = i + 2
                            
                elif re.match(text_employ, d['text'][i].lower()):
                    new_text = d['text'][i] + d['text'][i+1]
                    if re.search(text_employ_long, new_text.lower()):                  
                        if d['text'][i+2].lower() != 'result' and d['text'][i+2].lower() != 'result.':
                            index = i + 2                   
                        else:
                            index_not = i + 2                           
                    else:
                        index_not = i + 2
                        
                elif re.search('verify', d['text'][i].lower()):
                    if re.match(text_complete, d['text'][i+1].lower()):
                        if d['text'][i+1].lower() != 'not':
                            index = i + 2                           
                        else:
                           index_not = i + 2              
                    else:
                        try:
                            if re.search(text_complete, d['text'][i+2].lower()):
                                if d['text'][i+1].lower() != 'not' and d['text'][i+2].lower() != 'incomplete':
                                    index = i + 2
                                else:
                                    index_not = i + 2                            
                        except:
                            pass

            elif float(d['conf'][i]) > 10 and float(d['conf'][i]) <= 30: 
                if re.match(text_report, d['text'][i].lower()):
                    new_text = d['text'][i] + d['text'][i+1]
                    if re.search(text_report_long, new_text.lower()):
                        too_little += 1
                elif re.match(text_employ, d['text'][i].lower()):
                    new_text = d['text'][i] + d['text'][i+1]
                    if re.search(text_employ_long, new_text.lower()):
                        too_little += 1

        return too_little, index, image, index_not, date

    def everify_pages_loop(start, num, row, pdf_index):
        # loop through every page and look for date and signature with usage of different functions, like words_loop
        pdf_index = pdf_index
        signed = 0
        nonlocal failures   # to copy not signed file to a different directory
        for k in range(start, num):   
            if k == 0:
                if pdf_name.endswith(".pdf"):   
                    file_name = file_name_func(k, file_format)
                else:
                    file_name = pdf_name
            else:
                file_name = file_name_func(k, file_format)   
            # remove lines from image
            image = lines_remover(file_name)
            # create copy in case of enlarging
            image_copy = image.copy()       
            # read image 
            d = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DICT)
            # loop through every word
            too_little, index, image, index_not, date = everify_words_loop(image, d)
            
            # resize image if it's too little
            if too_little != 0:
                d = resizing(image_copy)
                too_little, index, image, index_not, date = everify_words_loop(image_copy, d)
            
            # if date exists, look for signature in 2 ways: one step to the right from index or one step to the right from 'Signature'
            if index > 1:
                signed += 1 
        df.loc[row, ['File Name']] = pdf_name
        if signed > 0:
            df.loc[row, ['Found']] = 'Signed'
            df.loc[row, ['Date']] = date 
        elif index_not != 0:
            df.loc[row, ['Not Found']] = 'Not signed'

            failures += 1   # to copy not signed file to a different directory
        row += 1   
            
        return d

    def ups_words_loop(image, d):
        # loop through every found word and look for date and signature
        date = ''
        # delete empty values
        if row == 0:
            for i in range(20):
                try:
                    if len(d['text'][i]) == 0 or d['text'][i] == None:
                        for key in d.keys():
                            del d[key][i]
                except:
                    pass
        n_boxes = len(d['text'])
        index = 0
        index_sign = 0
        index_printed = 0
        too_little = 0
        ups_index = 0
        text_everify1 = 'e-verify'
        text_everify2 = 'everify'

        for i in range(n_boxes): 
            # condition to only pick boxes with a confidence > 30%
            if float(d['conf'][i]) > 30:
                if re.match(date_pattern, d['text'][i]) or re.match(date_pattern2, d['text'][i]) or re.match(date_pattern3, d['text'][i]) or re.match(date_pattern4, d['text'][i]):
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    # red
                    if i > 5:
                        date = d['text'][i]
                elif re.match(date_short_eu, d['text'][i]) or re.match(date_short_us, d['text'][i]):
                    try:
                        new_date = d['text'][i] + d['text'][i + 1] + d['text'][i + 2]
                        if re.match(date_pattern, new_date) or re.match(date_pattern2, new_date) or re.match(date_pattern3, new_date) or re.match(date_pattern4, new_date):
                            if re.match('^([0-2][0-9]|((19|20)\d\d))', d['text'][i + 2]):
                                index = i + 3
                                date = new_date
                    except:
                        pass

                if re.match(text_everify1, d['text'][i].lower()) or re.match(text_everify2, d['text'][i].lower()):
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)    # red
                    if d['text'][i+1].lower() == 'completed' or d['text'][i+1].lower() == 'completed?':
                        index = i + 1
                    elif d['text'][i+2].lower() == 'completed' or d['text'][i+2].lower() == 'completed?':
                        index = i + 2
                    elif d['text'][i+1].lower() == 'process':
                        index_sign = i + 11
                else:
                    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)    # green
                
            elif float(d['conf'][i]) > 10 and float(d['conf'][i]) <= 30: 
                if re.match(text_everify1, d['text'][i].lower()) or re.match(text_everify2, d['text'][i].lower()):
                    too_little += 1
            else:
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)    # blue

        return too_little, index, index_sign, image, ups_index, index_printed, date

    def ups_pages_loop(start, num, row, pdf_index):
        # loop through every page and look for date and signature with usage of different functions, like words_loop
        pdf_index = pdf_index
        signed = 0
        nonlocal failures   # to copy not signed file to a different directory
        for k in range(start, num):
            if k == 0:
                if pdf_name.endswith(".pdf"):   
                    file_name = file_name_func(k, file_format)
                else:
                    file_name = pdf_name
            else:
                file_name = file_name_func(k, file_format)
            image = lines_remover(file_name)
            # create copy in case of enlarging
            image_copy = image.copy()       
            # read image 
            d = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DICT)
            # loop through every word
            too_little, index, index_sign, image, ups_index, index_printed, date = ups_words_loop(image, d)
            # resize image if it's too little
            if too_little != 0:
                d = resizing(image_copy)
                too_little, index, index_sign, image, ups_index, index_printed, date = ups_words_loop(image_copy, d)

            n_boxes = len(d['text'])
            # if date exists, look for signature in 2 ways: one step to the right from index or one step to the right from 'Signature'
            marked_list = ['x', 'y', 'v', 'xyes', '_xyes', 'xx', 'x_yes__no', 'x_yes', 'y_', '_x', '_x_yes', 'x_yes___no', 'vv', 'ves', 'v_', '_x_',
                '_x__yes', '_x__']
            if index > 1:
                try:
                    if index_sign < n_boxes:
                        if d['text'][index+1].lower() in marked_list:
                            signed += 1
                        elif d['text'][index+1].lower() == 'yes':
                            if len(d['text'][index+2].lower()) != 0:
                                if d['text'][index+2].lower() in marked_list:
                                    signed += 1
                                elif d['text'][index+2].lower() == 'or' or d['text'][index+2].lower() == 'i-9':
                                    signed += 1
                            else:
                                if d['text'][index+3].lower() == 'or' or d['text'][index+3].lower() == 'i-9':
                                    signed += 1                                 
                        elif len(d['text'][index+1].lower()) == 0:
                            if d['text'][index+2].lower() == 'yes':
                                if (d['text'][index+3].lower()) != 0:
                                    if d['text'][index+3].lower() == 'or' or d['text'][index+3].lower() == 'i-9':
                                        signed += 1                                         
                                else:
                                    if d['text'][index+4].lower() == 'or' or d['text'][index+4].lower() == 'i-9':
                                        signed += 1           
                        if d['text'][index_sign+1].lower() in marked_list:
                            signed += 1
                        elif d['text'][index_sign+1].lower() == 'yes':
                            if len(d['text'][index_sign+2].lower()) != 0:
                                if d['text'][index_sign+2].lower() in marked_list:
                                    signed += 1
                                else:
                                    if d['text'][index_sign+3].lower() == 'or' or d['text'][index_sign+3].lower() == 'i-9':
                                        signed += 1 
                            # new functionality
                            elif len(d['text'][index_sign+2].lower()) == 0 and d['text'][index_sign+3].lower() == 'i-9':
                                signed += 1                                            
                        elif len(d['text'][index_sign+1].lower()) == 0:
                            if d['text'][index_sign+2].lower() == 'yes':
                                if (d['text'][index_sign+3].lower()) != 0:
                                    if d['text'][index_sign+3].lower() == 'or' or d['text'][index_sign+3].lower() == 'i-9':
                                        signed += 1                                         
                                else:
                                    if d['text'][index_sign+4].lower() == 'or' or d['text'][index_sign+4].lower() == 'i-9':
                                        signed += 1   
                        if d['text'][index_sign+1].lower() == 'date' or d['text'][index_sign+1].lower() == 'date.':
                            if d['text'][index_sign+2].lower() in marked_list:
                                signed += 1
                            elif d['text'][index_sign+2].lower() == 'yes' and d['text'][index_sign+3].lower() != 'no' and d['text'][index_sign+4].lower() != 'no' and d['text'][index_sign+5].lower() != 'no':
                                signed += 1
             
                except:
                    try:
                        pdf_index = rect_mini(pdf_name, k)
                    except:    
                        pass
            if k == 0:
                if signed == 0:
                    index_line = d['top'][index]
                    index_sign_line = d['top'][index_sign]
                    try:
                        index_line_pos, index_sign_line_pos = lines_position(d, index_line, index_sign_line)
                        signed = rect_mini_ups(pdf_name, k, index_line_pos, index_sign_line_pos)
                    except:
                        pass

        df.loc[row, ['File Name']] = pdf_name
        if signed > 0:
            df.loc[row, ['Found']] = 'Signed'
            df.loc[row, ['Date']] = date
        else:
            df.loc[row, ['Not Found']] = 'Not signed'

            failures += 1   # to copy not signed file to a different directory
        
        row += 1   

        return d   

    def file_name_func(k, file_format):
        # process file name based on file format
        if file_format == 0:         
            file_name = "{}{}.jpg".format(pdf_name, k)
        elif file_format == 1:
            file_name = "{}.jpg".format(pdf_name)
        elif file_format == 2:
            file_name = pdf_name
        elif file_format == 3:
            file_name = pdf_name    
        elif file_format == 4:
            file_name = pdf_name 

        return file_name

    def lines_position(d, index_line, index_sign_line):
        # get lines coordinates for further checking checked boxes
        data = {}
        for i in range(len(d['line_num'])):
            txt = d['text'][i]
            block_num = d['block_num'][i]
            line_num = d['line_num'][i]
            top, left = d['top'][i], d['left'][i]
            width, height = d['width'][i], d['height'][i]
            if not (txt == '' or txt.isspace()):
                tup = (txt, left, top, width, height)
                if block_num in data:
                    if line_num in data[block_num]:
                        data[block_num][line_num].append(tup)
                    else:
                        data[block_num][line_num] = [tup]
                else:
                    data[block_num] = {}
                    data[block_num][line_num] = [tup]

        linedata = {}
        idx = 0
        for _, b  in data.items():
            for _, l in b.items():
                linedata[idx] = l
                idx += 1
        line_idx = 1
        index_line_pos, index_sign_line_pos = (0, 0), (0, 0)
        for _, line in linedata.items():
            xmin, ymin = line[0][1], line[0][2]
            xmax, ymax = (line[-1][1] + line[-1][3]), (line[-1][2] + line[-1][4])
            line_idx += 1
            if ymax + 30 >= index_line and ymin - 30 <= index_line:
                index_line_pos = (ymin, ymax)
            elif ymax + 30 >= index_sign_line and ymin - 30 <= index_sign_line:
                index_sign_line_pos = (ymin, ymax)

        return index_line_pos, index_sign_line_pos

    def pages_loop(num, row):
        # loop through every page and look for date and signature with usage of different functions, like words_loop
        nonlocal pdf_name

        for k in range(num):   
            file_name = file_name_func(k, file_format)
            image = cv2.imread(IMGS_DIR + file_name) 
            if file_format == 0:
                if type(image) is np.ndarray:
                    pass
                else:
                    new_name = pdf_name.replace('-', '').replace('–', '').replace('+', '')
                    shutil.copy(directory + '/' + pdf_name, directory + '/' + new_name)
                    file_name = new_name
                    page = convert_from_path(directory + '/' + file_name, poppler_path=poppler_path)
                    num = 0
                    for page in pages:
                        page.save(r"path\Images\{}{}.jpg".format(file_name, num))       # may be changed
                        num += 1

                    file_name = "{}{}.jpg".format(file_name, k)
                    pdf_name = file_name
            image = lines_remover(file_name)
            # create copy in case of enlarging
            image_copy = image.copy()

            # read image 
            d = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DICT)
           
           # loop through every word 
            too_little, index = words_loop(image, d)

            if too_little != 0:
                d = resizing(image_copy)
                too_little, index = words_loop(image_copy, d)
            if index != 0:
                break

        df.loc[row, ['File Name']] = pdf_name
        start = 0
        if index == 0:
            df.loc[row, ['Document Type']] = 'Not Found'
            d = everify_pages_loop(start, num, row, pdf_index)
        elif index == 1:
            df.loc[row, ['Document Type']] = 'E-Verify'
            d = everify_pages_loop(start, num, row, pdf_index)
        elif index == 2:
            df.loc[row, ['Document Type']] = 'UPS Onboarding'
            d = ups_pages_loop(start, num, row, pdf_index)
        elif index == 3:
            df.loc[row, ['Document Type']] = 'Exhibit'
            d = exhibit_pages_loop(start, num, row, pdf_index)

        return d
    
    d = pages_loop(num, row)

    # Check if file is signed properly. If so, copy it to Propers folder, else copy it to Failures folder.
    if failures != 0:
        copy(directory + '/' + pdf_name, IMG_FAIL_DIR)
    else:
        copy(directory + '/' + pdf_name, IMG_PROPER_DIR)

    return df 

def file_loop(directory):
    new_df = pd.DataFrame(columns=['File Name', 'Document Type', 'Found', 'Not Found', 'Date'])

    row = 0
    count = 0
    for file in os.listdir(directory):
        # if count == 2:
        #     break
        # count += 1
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"): 
            file_format = 0
            new_df = new_df.append(pdf_recognizer(filename, row, directory, file_format))
            continue
        elif filename.endswith(".jpg"): 
            file_format = 1
            new_df = new_df.append(pdf_recognizer(filename, row, directory, file_format))
        elif filename.endswith(".PNG"): 
            file_format = 2
            new_df = new_df.append(pdf_recognizer(filename, row, directory, file_format))
        elif filename.endswith(".GIF"): 
            file_format = 3
            new_df = new_df.append(pdf_recognizer(filename, row, directory, file_format))
        elif filename.endswith(".doc") or filename.endswith(".docx"):
            # convert('{}/{}'.format(directory, filename) , '{}/{}.pdf'.format(directory, filename))
            doc = aw.Document('{}/{}'.format(directory, filename))
            doc.save('{}/{}.pdf'.format(directory, filename))
            file_format = 0
            filename = filename + '.pdf'
            new_df = new_df.append(pdf_recognizer(filename, row, directory, file_format))
        else:
            continue
    current_hour = datetime.datetime.now().strftime('%H_%M_%S')        
    file_path = 'path/Summary_files_uipath_{}.xlsx'.format(current_hour)
    
    excel_file = new_df.to_excel(file_path, index=False)

    return file_path
    # return excel_file

file_loop("path\\N\\")

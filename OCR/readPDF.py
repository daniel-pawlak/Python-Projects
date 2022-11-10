import json
import re
import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from pytesseract import Output

custom_config = r'--oem 1 --psm 6'
"""
Sets file path for pytesseract since it is not installed globally on machine.
"""
def setTesseractFilePath(directory: str):
    pytesseract.pytesseract.tesseract_cmd = directory

"""
Converts passed in pdf into a series of images that can be used for OCR, using poppler library.

@return The list of images containing images for each page of the pdf
"""
def convert_pdf_to_image(filePath: str, path_to_poppler: str, save_path: str) -> list:
    pdf_images = convert_from_path(filePath, poppler_path=path_to_poppler)
    image_counter = 0
    img_filepath = []

    for page in pdf_images:
        page_filepath = f"{save_path}/Page {image_counter}.jpg"
        page.save(page_filepath)

        img_filepath.append(page_filepath)
        image_counter += 1

    return img_filepath

"""
Pre-processes the image by turning it into greyscale & adding thresholding so it's easier to read for 
tesseract.

@return Numpy array containing data about the transformed image.
"""
def preprocess_image(image : str) -> np.ndarray:
    read_img = cv2.imread(image)
    greyscale_img = cv2.cvtColor(read_img, cv2.COLOR_BGR2GRAY) # Add greyscaling
    threshholded_image = cv2.threshold(greyscale_img, 0, 255, cv2.THRESH_TOZERO)[1] # Add thresholding 

    return threshholded_image

"""
Place bounding boxes over required information and then extract what's needed.

@param image - String filepath for the image
"""
def place_bounding_boxes(image: str):
    print(image)
    read_img = preprocess_image(image)

    tesseract_dict = pytesseract.image_to_data(read_img, output_type=Output.DICT)

    for i in range(len(tesseract_dict['text'])):
        if int(float(tesseract_dict['conf'][i])) > 60:
            if tesseract_dict['text'][i] == 'Fresenius':
                (x, y, w, h) = (tesseract_dict['left'][i], tesseract_dict['top'][i], tesseract_dict['width'][i], tesseract_dict['height'][i])
                read_img = cv2.rectangle(read_img, (x,y), (x+w, y+h), (0, 0,255),2)

    cv2.imshow('img', read_img)
    cv2.waitKey(0)


def remove_blank_entries(text_arr : list):
    return list(filter(lambda x : x.strip() != '', text_arr))

def resizing(image: np.ndarray) -> np.ndarray:
    # resize image with given variables to make it more readable
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)      # reshape image, make it bigger and easier to read
    return image 

"""
Parsing logic for alstom pdf's specifically, extracts the following
    - Client Name
    - Period of employment

@param Images - A string containing the filepath for the image.
"""
def parse_alstom(image: str):
    client_info = []

    read_img = preprocess_image(image)
    tesseract_dict = pytesseract.image_to_data(read_img, config=custom_config, output_type=Output.DICT, lang="deu") # 17 & 18
    tesseract_dict['text'] = remove_blank_entries(tesseract_dict['text'])
    
    first_name = tesseract_dict['text'][16]
    last_name = tesseract_dict['text'][17]
    time_period = f"{tesseract_dict['text'][19]} {tesseract_dict['text'][20]}"

    client_info.append(first_name)
    client_info.append(last_name)
    client_info.append(time_period)

    return client_info

"""
Parsing logic for Fresenius PDF's Specifically, extracts the following
    - Client Name
    - Name Of Associate
    - Period of employment
    - Shift hours
    - Late night shift hours
    - Overtime 100%

@param Images - A string filepath for the image
@return list
"""
def parse_fresenius(image: str) -> list:
    assoc_name = ('', '')
    client_name = ('', '', '')
    time_period = ''
    shift_details = []

    # Trying out bounding boxes logic
    read_img = preprocess_image(image)
    tesseract_dict = pytesseract.image_to_data(read_img, config=custom_config, output_type=Output.DICT, lang="deu")

    #Filter all empty entries within the list
    tesseract_dict['text'] = remove_blank_entries(tesseract_dict['text'])
    
    if len(tesseract_dict['text']) == 3:
        #It's a blank page
        print("Blank page")
        return ['blank']
    else:
        text_arr = tesseract_dict['text']
        # Find Fresenius name
        for word in range(len(text_arr)):
            if text_arr[word] == 'Fresenius':
               client_name = (text_arr[word], text_arr[word + 1], text_arr[word + 2])
            elif text_arr[word].lower().strip() == "pers.nr.":
                word += 2
                assoc_name = [text_arr[word], text_arr[word+1]]
                word += 1

            elif re.match("\d\.\d+\.\d+-\d+\.\d+\.\d+", text_arr[word]):
                time_period = text_arr[word]                

            elif text_arr[word].lower() == "endsaldo":
                loopCounter = word 

                #Find ZGG index
                while text_arr[loopCounter].lower() != "zgg":
                    loopCounter += 1

                # Get all info in shift tables
                while loopCounter < len(text_arr):
                    inner_list = []
                    if "+/-" in text_arr[loopCounter]:
                        break
                    else:
                        while not re.match("\d+.\d+.\d{4}", text_arr[loopCounter]):
                            inner_list.append(text_arr[loopCounter])
                            loopCounter += 1

                        # Append the date to the list as well
                        inner_list.append(text_arr[loopCounter])
                        shift_details.append(inner_list)
                    loopCounter += 1
        print(shift_details)
        name_string = f"{client_name[0]} {client_name[1]} {client_name[2]}"

        # Print Extracted Details
        print(f"Client Name: {name_string}")

        assoc_string = ""
        for word in assoc_name:
            assoc_string += word + " "

        client_details = []
        client_details.append(name_string)
        client_details.append(assoc_string)
        client_details.append(time_period)

        for shift in shift_details:
            elem = " ".join(shift)
            client_details.append(elem)

        print(f"Associate Name: {assoc_string}")
        print(f"Time Period: " + time_period)

        return client_details 
"""
Test function for different methods of preprocessing
"""
def split_table(image: np.ndarray, roi_filePath: str) -> None:
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image, (7,7), 0)
    inverted_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
    dilate = cv2.dilate(inverted_img, kernel, iterations=1)
    contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])

    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if (h >= 100 and h <= 500) and w >= 1000:
            roi = image[y: y+h, x:x+w]
            cv2.imwrite(f"{roi_filePath}roi.jpg", roi)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
#    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
#    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)    # green #

#    cv2.rectangle(image, (202,112), (496, 137), (0, 255, 0), 2)
#    cv2.rectangle(image, (290, 231), (426, 257), (0, 255, 0), 2)
#    cv2.rectangle(image, (712, 231), (957, 259), (0, 255, 0), 2)

def parse_knorr(image: str, roi_filePath: str) -> list:
    read_img = cv2.imread(image)

    read_img = preprocess_image(image)
    tesseract_dict = pytesseract.image_to_data(read_img, config=custom_config, output_type=Output.DICT, lang="deu")
    tesseract_dict['text'] = remove_blank_entries(tesseract_dict['text'])

    text_list = tesseract_dict['text']
#    print(text_list)
    seite_num = tesseract_dict['text'][-3]

    if int(seite_num) > 1:
        return ["Page 2"]
    #Find Time Period
    vom_index = text_list.index("vom")
    time_period = f"{text_list[vom_index + 1]} {text_list[vom_index+2]} {text_list[vom_index+3]}"

    #Find associate name
    assoc_num_index = text_list.index("Personalnummer:")
    assoc_name = (text_list[assoc_num_index + 2], text_list[assoc_num_index + 3])

    #Find Client Name
    client_name_index = text_list.index("Personalbereich")
    client_name = (text_list[client_name_index + 1], text_list[client_name_index + 2 ])

    # Split the table from the rest of the PDF
    split_table(read_img, roi_filePath)
    
    table_image = cv2.imread(f"{roi_filePath}roi.jpg")

    grey_table = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY) # Add greyscaling
    thresh_table = cv2.threshold(grey_table, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove all Horizontal lines in the table
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(thresh_table, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(table_image, [c], -1, (255,255,255), 5)
   
    # Remove all Vertical lines in the table
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    remove_vertical = cv2.morphologyEx(thresh_table, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(table_image, [c], -1, (255,255,255), 5)

    #Double the size of the image on the table
    table_image = resizing(table_image)

    table_dict = pytesseract.image_to_data(table_image, config='--oem 1 --psm 6', output_type=Output.DICT, lang="deu")
    table_dict['text'] = remove_blank_entries(table_dict['text'])

    normal_hours = ''
    shift_hours = ''
    late_shift_hours = ''
    overtime_50 =''
    overtime_100 = ''

    for word in range(len(table_dict['text'])):
        if table_dict['text'][word].lower() == "produktivstunden" and normal_hours == '':
            normal_hours = table_dict['text'][word + 1]
        elif table_dict['text'][word].lower() == "2." and table_dict['text'][word + 1].lower() == "schichtzulage":
            shift_hours = table_dict['text'][word + 2]
        elif table_dict['text'][word].lower() == "3." and table_dict['text'][word + 1].lower() == "schichtzulage":
            late_shift_hours = table_dict['text'][word + 2]
        elif table_dict['text'][word] in ["USTD", "ÜSTD"]:
            if table_dict['text'][word + 1] == "bez.":
                if table_dict['text'][word + 2] == "50%":
                    overtime_50 = table_dict['text'][word + 3]
                elif table_dict['text'][word + 2] == "100%":
                    overtime_100 = table_dict['text'][word + 3]
        
    assoc_string = f"{assoc_name[0]} {assoc_name[1]}"
    client_string = f"{client_name[0]} {client_name[1]}"

    print(f"Time period: {time_period}")
    print(f"Associate Name: {assoc_string}")
    print(f"Client Name: {client_string}")

    print(f"Produktivstunden: {normal_hours}")
    print(f"2. Schichtzulage: {shift_hours}")
    print(f"3. Schichtzulage: {late_shift_hours}")
    print(f"USTD bez. 50%: {overtime_50}")
    print(f"USTD bez. 100%: {overtime_100}")

    return [assoc_string, time_period, normal_hours, shift_hours, late_shift_hours, overtime_50, overtime_100]
#    return [time_period, assoc_string, client_string, normal_hours, shift_hours, late_shift_hours, overtime_50, overtime_100]

"""
- Loop over images
- Keep going until a new client page is found.
- Return all extracted details, and page range, determined by image name.

Arguments: Entire image array, Starting index for which images to read first
Return: Tuple (list of extracted details, Page numbers)
"""
def parse_lam(images: list, starting_index: int) -> list:

    time_period = ''
    assoc_name = [] 
    extern_id = ''
    normal_hours = ''
    work_from_home_days = {}
    ending_index = len(images) - 1
    wfh_count = 0

    for elem in range(starting_index, len(images)):
        # If the current page does not have the associate name that's been found already
        image = images[elem]
        read_img = preprocess_image(image)
        rotate_img = cv2.rotate(read_img, cv2.ROTATE_90_CLOCKWISE)

        print(f"Reading Image: {image}")
        img_data = pytesseract.image_to_data(rotate_img, config=custom_config, output_type=Output.DICT, lang="deu")
        img_data['text'] = remove_blank_entries(img_data['text'])
        img_text = img_data['text']
        #print(img_text)

        if len(assoc_name) != 0 and not all(name in img_text for name in assoc_name):
            ending_index = elem - 1
            break

        for loopCounter in range(len(img_text)):

            curr_word = img_text[loopCounter]

            if curr_word.lower() == "druck-periode:":
                if time_period == "":
                    time_period = img_text[loopCounter + 1] + img_text[loopCounter + 2] + img_text[loopCounter + 3]

                if len(assoc_name) == 0: 
                    assoc_counter = loopCounter + 4
                    curr_word = img_text[assoc_counter]

                    while curr_word != "/" and assoc_counter < len(img_text):
                        curr_word = img_text[assoc_counter]

                        if curr_word != "/":
                            assoc_name.append(curr_word)
                        
                        assoc_counter += 1

                    loopCounter += assoc_counter
            elif curr_word.lower() == "pnr:":
                extern_id = img_text[loopCounter + 1]
            elif curr_word.lower() == "periodensumme":
                normal_hours = img_text[loopCounter + 1]
            elif curr_word.lower() == "summe" and img_text[loopCounter + 1].lower() == "woche" and img_text[loopCounter+2] == "9":
                loopCounter += 5

                curr_word = img_text[loopCounter]
                prev_letter = ''

                while curr_word.lower() != "summe":
                    curr_word = img_text[loopCounter]

                    if len(curr_word) == 1 and img_text[loopCounter + 2].lower() == "work":
                        wfh_count += 1
                        prev_letter = curr_word

                        if curr_word in work_from_home_days:
                            work_from_home_days[curr_word].append(img_text[loopCounter+5])
                        else:
                            work_from_home_days[curr_word] = [img_text[loopCounter + 5]]
                        loopCounter += 11
                    elif curr_word.lower() == "work":
                        wfh_count += 1
                        work_from_home_days[prev_letter].append(img_text[loopCounter+3])
                        loopCounter += 4
                    else:
                        loopCounter += 1


    print(f"Time Period: {time_period}")
    print(f"Associate Name: {' '.join(assoc_name)}")
    print(f"External Identification Number: {extern_id}")
    print(f"Normal Hours: {normal_hours}")
    print(f"{work_from_home_days}")
    work_from_home_Json = json.dumps(work_from_home_days)


    return [' '.join(assoc_name), time_period, extern_id, normal_hours, work_from_home_Json, str(wfh_count), str(ending_index)]

setTesseractFilePath('C:\\Users\\RPA.BOT18\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe')
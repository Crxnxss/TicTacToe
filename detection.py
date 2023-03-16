import cv2
import numpy as np
from math import *
import time



def find_position(a, b):
    """Return the cell number"""
    
    first_line = 100
    second_line = 180
    
    if a < first_line and b < first_line:
        return 1
    if a < first_line and b < second_line and b > first_line:
        return 2
    if a < first_line and b > second_line:
        return 3
    if a > first_line and a < second_line and b < first_line:
        return 4
    if a > first_line and a < second_line and b < second_line and b > first_line:
        return 5
    if a > first_line and a < second_line and b > second_line :
        return 6
    if a > second_line and b < first_line:
        return 7
    if a > second_line and b < second_line and b > first_line:
        return 8
    if a > second_line and b > second_line:
        return 9
    


def replace_cell(cell_played):
    """Inverse matrix"""
    if cell_played == 1:
        return 1    
    if cell_played == 2:
        return 4
    if cell_played == 3:
        return 7
    if cell_played == 4:
        return 2
    if cell_played == 5:
        return 5
    if cell_played == 6:
        return 8
    if cell_played == 7:
        return 3
    if cell_played == 8:
        return 6
    if cell_played == 9:
        return 9

    
    
def main_function(cells_played):
    """"""

    cap = cv2.VideoCapture(0)
    list_result = []

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 200)
        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 20000:
                
                largest_contour = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(largest_contour)
                
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                
                perimeter = cv2.arcLength(largest_contour, True)
                approx = cv2.approxPolyDP(largest_contour, 0.02 * perimeter, True)
                
                if len(approx) == 4:
                    
                    grid_corners = approx.reshape(4, 2)

                    x_min, y_min = np.min(grid_corners, axis=0)
                    x_max, y_max = np.max(grid_corners, axis=0)
                    roi = frame[y_min:y_max, x_min:x_max]
                    
                    cv2.imshow('Morpion', roi)

                    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    roi_blurred = cv2.GaussianBlur(roi_gray, (5, 5), 0)
                    roi_edged = cv2.Canny(roi_blurred, 50, 200)
                    roi_contours, roi_hierarchy = cv2.findContours(roi_edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
                        
                    detected_circles = cv2.HoughCircles(roi_edged, 
                                cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                            param2 = 30, minRadius = 1, maxRadius = 40)
                                
                    if detected_circles is not None:
                        detected_circles = np.uint16(np.around(detected_circles))
                        for i in range(0, len(detected_circles[0])):
                            
                            a, b, _ = detected_circles[0][i]
                            
                            cell = find_position(a, b)
                            
                            if len(cells_played) > 0:
                                if not cells_played.count(cell) > 0:
                                    list_result.append(cell)
                            else:
                                list_result.append(cell)
                                
                        if len(list_result) >= 75:
                            idx_element = 0
                            for element in list_result:
                                if list_result.count(element) > idx_element:
                                    idx_element = list_result.count(element)
                                    cell_played = element
                            list_result = []
                            return cell_played
                            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    


    





        
        
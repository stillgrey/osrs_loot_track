import PIL
from PIL import Image
import sys
from chardict import CHARACTER_DICT


val = (239, 16, 32, 255)
#val = (0, 0, 255, 255) #getting alphabet

letter_dict = {}


#count = 0

class letter_line:
    def __init__(self, V_bottom):
        self.y_bottom = V_bottom
        self.y_top = V_bottom-10
        self.line_letters = []
    def check_range(self, letter, pix_list):
        inrange_count = 0
        for coord in pix_list:
            if coord[1] > self.y_top and coord[1] < self.y_bottom:
                inrange_count+=1
        if inrange_count >= 4:
            return True
        return False
            
    def add_letter(self, letter, leftmost, rightmost):
        position = 0
        for i in range(len(self.line_letters)):
            if self.line_letters[i][1] > leftmost:
                break
            position+=1
        self.line_letters.insert(position, (letter, leftmost, rightmost))
        
    def get_string(self):
        char_list = []
        prev_char_rightmost = self.line_letters[0][1]
        for character in self.line_letters:
            if character[1]-prev_char_rightmost > 3:
                if character[0].isdigit() and prev_char.isdigit():
                    pass
                else:
                    char_list += ' '
            char_list += character[0]
            prev_char = character[0]
            prev_char_rightmost = character[2]
        return "".join(char_list)

        
            
        

def sort_tuple_list(tup_list):
    sorted_tuple_list = []
    for tup in tup_list:
        pass

def normalize_values(coord_list):
    x_coords = []
    y_coords = []
    for coord in coord_list:
        x_coords+=[coord[0]]
        y_coords+= [coord[1]]
    min_x = min(x_coords)
    min_y = min(y_coords)
    normalized_coord_list = []
    for coord in coord_list:
        normalized_coord_list += [(coord[0]-min_x, coord[1]-min_y)]
    #normalized_coord_list.sort()
    return normalized_coord_list

def get_adjacent((x, y), cur_adj, bottom_y, im):
    if bottom_y - y >= 9:
        possible_adj = [(x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y)]
    else:
        possible_adj = [(x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]  
    new_adj = []
    for pixel in possible_adj:
        if im.getpixel(pixel) == val and pixel not in cur_adj and pixel not in new_adj:
            new_adj+=[pixel]
    for pixel in new_adj:
        new_adj+=get_adjacent(pixel, new_adj+cur_adj, bottom_y, im)
    return new_adj
            
def construct_letter(x, y, im):
    adjacent_pixels = [(x, y)]
    adjacent_pixels+=get_adjacent((x, y), adjacent_pixels, y, im)
    letter = None
    adjacent_pixels_normalized = normalize_values(adjacent_pixels)
    try:
        if adjacent_pixels_normalized is not None:
            #print adjacent_pixels
            pixel_string = str(adjacent_pixels_normalized)
            letter = CHARACTER_DICT[pixel_string]
    except KeyError:
        pass

    
    
    return (adjacent_pixels, letter, adjacent_pixels_normalized)


def get_valuable_drop_strings(image_path):
    im = PIL.Image.open(image_path)
    line_list = []

    y_range = range(im.size[1])[::-1]
    x_range = range(im.size[0])
    checked_pixels = []
    backlog = []
    min_V_y = 0
    for y in y_range:
        if y < min_V_y:
            break
        for x in x_range:
            if (x, y) not in checked_pixels:
                if im.getpixel((x, y)) == val:
                    adj_pixels, letter, apn = construct_letter(x, y, im)

                    if letter != None and letter != 'V':
                        if line_list == []:
                            backlog+=[(adj_pixels, letter, apn)]
                        else:
                            for a_line in line_list:
                                if a_line.check_range(letter, adj_pixels):
                                    x_letter_coords = []
                                    for coord in adj_pixels:
                                        x_letter_coords+= [coord[0]]
                                    a_line.add_letter(letter, min(x_letter_coords), max(x_letter_coords))
                                    break
                            while backlog != []:
                                prev_char = backlog.pop()
                                x_letter_coords = []
                                
                                for a_line in line_list:
                                    if a_line.check_range(prev_char[1], prev_char[0]):
                                        x_letter_coords = []
                                        for coord in prev_char[0]:
                                            x_letter_coords+= [coord[0]]
                                        a_line.add_letter(prev_char[1], min(x_letter_coords), max(x_letter_coords))
                                        break
                                    
                                
                        
                    #print apn
                    
                    #Generate Valuable Loot lines
                    if line_list == [] and letter == 'V':
                        v_pixels = adj_pixels
                        x_V_coords = []
                        y_V_coords = []
                        for coord in v_pixels:
                            x_V_coords+= [coord[0]]
                            y_V_coords+= [coord[1]]
                        cur_V_left = min(x_V_coords)
                        cur_V_bottom = max(y_V_coords)
                        min_V_y = cur_V_bottom-20
                        while (cur_V_bottom != None):
                            line_list+=[letter_line(cur_V_bottom)]
                            line_list[len(line_list)-1].add_letter(letter, cur_V_left, cur_V_left+4)
                            cur_V_bottom-=14
                            
                            
                            if im.getpixel((cur_V_left+2, cur_V_bottom)) == val:
                                v_pixels, new_V, apn = construct_letter(cur_V_left+2, cur_V_bottom, im)
                            else:
                                cur_V_bottom = None
                                break
                            if new_V != 'V':
                                cur_V_bottom = None
                                break
                            
                            
                            x_V_coords = []
                            y_V_coords = []
                            for coord in v_pixels:
                                x_V_coords+= [coord[0]]
                                y_V_coords+= [coord[1]]
                            cur_V_bottom = max(y_V_coords)
                            min_V_y = cur_V_bottom-20
                            
                            
                    checked_pixels+=adj_pixels
    completed_strings = []
    for myline in line_list:
        completed_strings += [myline.get_string()]
    return completed_strings
    

'''                
                    if len(adj_pixels) > 5:
                        try:
                            ld[str(apn)]
                        except KeyError:
                            print "(%d, %d)" % (x, y)
                            ld[str(apn)] = raw_input("Character ?")
    f = open("chardict.py", "wb")
    f.write("CHARACTER_DICT = " + str(ld))
    f.close()

'''

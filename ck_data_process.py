import os
import dlib  # face recognition
import cv2  # image processing


def get_file_path(root_path, file_list, dir_list):
    # Gets all the file names and directory names in this directory
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # Gets the path to a directory or file
        dir_file_path = os.path.join(root_path, dir_file)
        # Determine whether the path is a file or a path
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            # Recursively get the path to all files and directories
            get_file_path(dir_file_path, file_list, dir_list)
        else:
            file_list.append(dir_file_path)


def distance(p1, p2):
    dis = pow((shape.part(p1).x - shape.part(p2).x), 2) + pow((shape.part(p1).y - shape.part(p2).y), 2)
    return dis


def distance2(x1, y1, x2, y2):
    dis = pow(x1 - x2, 2) + pow(y1 - y2, 2)
    return dis


# Store all file paths
file_list = []
# Store all file paths
dir_list = []
nameFolder = 'surprise'
root_path = r"E:/ck/" + nameFolder + "/"
get_file_path(root_path, file_list, dir_list)

f = open(root_path + "/../" + nameFolder + "data.csv", "w", encoding="utf-8")
f.write("D1,D2,D3,D4,D5,D6,Expression\n")
f.close()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

for filename in file_list:
    print(filename)
    im_rd = cv2.imread(filename)
    cv2.imshow('aa', im_rd)
    cv2.waitKey(1)
    try:
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
        img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)
    except:
        img_gray = im_rd

    rect = dlib.rectangle(0, 0, im_rd.shape[0], im_rd.shape[1])  # startX, startY, endX, endY
    shape = predictor(img_gray, rect)
    D1 = distance(20, 25)
    D2 = distance2((shape.part(20).x + shape.part(25).x) / 2, (shape.part(20).y + shape.part(25).y) / 2,
                   (shape.part(42).x + shape.part(47).x) / 2, (shape.part(42).y + shape.part(47).y) / 2)
    D3 = distance2((shape.part(38).x + shape.part(45).x) / 2, (shape.part(38).y + shape.part(45).y) / 2,
                   (shape.part(42).x + shape.part(47).x) / 2, (shape.part(42).y + shape.part(47).y) / 2)
    D4 = distance(52, 58)
    D5 = distance(49, 55)
    D6 = distance(52, 58)
    # D6 = distance2((shape.part(49).x + shape.part(55).x) / 2, (shape.part(49).y + shape.part(55).y) / 2,
    #               shape.part(52).x, shape.part(52).y)
    print(D1)
    # 写入文件
    f = open(root_path + "/../" + nameFolder + "data.csv", "a", encoding="utf-8")
    f.write(
        str(D1) + ',' + str(D2) + ',' + str(D3) + ',' + str(D4) + ',' + str(D5) + ',' + str(
            D6) + ',' + nameFolder + '\n')
    f.close()

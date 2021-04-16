import dlib  # face recognition
import cv2  # image processing


class face_emotion():

    def __init__(self):
        # Use the feature extractor get_frontal_face_detector
        self.detector = dlib.get_frontal_face_detector()
        # dlib's 68-point model'
        self.predictor = dlib.shape_predictor("predictor/shape_predictor_68_face_landmarks.dat")
        # Create CV2 camera object, it will automatically switch to the external camera
        self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture("2.mp4")  # read video
        # Set the video parameter, propId set the video parameter, value set the parameter value
        self.cap.set(3, 480)

    def distance2(self, x1, y1, x2, y2):  # Calculate the square of the Euclidean distance between two points
        dis = pow(x1 - x2, 2) + pow(y1 - y2, 2)
        return dis

    def learning_face(self, mode, fileName):
        def distance(p1, p2):  # Calculate the square of the Euclidean distance between two points
            dis = pow((shape.part(p1).x - shape.part(p2).x), 2) + pow((shape.part(p1).y - shape.part(p2).y), 2)
            return dis

        if mode == 0:  # mode selection
            self.cap = cv2.VideoCapture(0)  # open camera
        else:
            self.cap = cv2.VideoCapture(fileName)  # open video
        # parameter initialization
        areaLastFace = 1
        count_nan = 0
        count_warning = 0
        count_break = 0
        status_code = 0  # 0Natural 1Sad

        while (self.cap.isOpened()):
            flag, im_rd = self.cap.read()
            k = cv2.waitKey(1)
            # Take gray scale to adapt
            try:
                try:
                    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
                    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)
                except:
                    img_gray = im_rd
                    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)  # length and width of the Gaussian kernel
            except:
                break
            # scanning human face
            faces = self.detector(img_gray, 0)
            # 字体
            font = cv2.FONT_HERSHEY_SIMPLEX

            if (len(faces) != 0):
                # checking 68-point face
                areaMaxFace = 0
                for i in range(len(faces)):  # Choose the largest face
                    if faces[i].area() > areaMaxFace:
                        areaMaxFace = faces[i].area()
                        indexMax = i
                    print("第" + str(i) + "个脸面积：" + str(faces[i].area()))
                print("最大脸面积：" + str(faces[indexMax].area()) + "\n")  # Print out the largest face
                print(faces[indexMax])
                for i in range(len(faces)):
                    for k, d in enumerate(faces):  # enumerate
                        # Box all faces
                        # Use a red rectangle to frame the face
                        cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                        # 计算人脸热别框边长
                        self.face_width = d.right() - d.left()
                        if indexMax != k:  # deal with only the largest faces
                            continue
                        if (faces[indexMax].area() / areaLastFace) < 0.3:  # enter the wait status
                            count_nan += 1
                            if count_nan >= 10:
                                areaLastFace = faces[indexMax].area()  # Accept the latest maximum face area
                                count_nan = 0
                            continue
                        else:
                            areaLastFace = faces[indexMax].area()
                        # Use the predictor to get the coordinates of 68 points of data
                        shape = self.predictor(img_gray, d)
                        # Circles show each feature point
                        for i in range(68):
                            cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (0, 255, 0), -1, 8)
                        # calculate D2、D3、D4、D5
                        D2 = self.distance2((shape.part(20).x + shape.part(25).x) / 2,
                                            (shape.part(20).y + shape.part(25).y) / 2,
                                            (shape.part(42).x + shape.part(47).x) / 2,
                                            (shape.part(42).y + shape.part(47).y) / 2) / faces[k].area()
                        D3 = (distance(45, 47) + distance(44, 48) + distance(39, 41) + distance(38, 42)) / 4 / faces[
                            k].area()
                        D4 = distance(52, 58) / faces[k].area()
                        D5 = distance(49, 55) / faces[k].area()

                        print(D2, D3, D4, D5)

                        th4 = 0.038845
                        th5 = 0.059244
                        th2 = 0.017198
                        th3 = 0.12
                        th5_2 = 0.0334201
                        # discussing thresholds
                        if D4 < th4 and D5 < th5 and D2 > th2 and D5 > th5_2 or D3 < th3:
                            status_code = 1  # Sad
                            cv2.putText(im_rd, "Sad", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
                        else:
                            status_code = 0  # Happy
                            cv2.putText(im_rd, "Natural", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)

                # face amount
                cv2.putText(im_rd, "Faces: " + str(len(faces)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            else:

                cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                status_code = 0
            # window display
            cv2.imshow('Caring System', im_rd)
            k = cv2.waitKey(10)
            while 1:
                if count_warning != 0:
                    count_break += 1
                    if count_break >= 10:
                        count_warning = 0
                        count_break = 0
                if status_code == 0:  # Natural
                    break
                elif status_code == 1:  # Sad
                    count_warning += 1
                    # print("angry")
                    if count_warning <= 5:
                        break
                    # if SAD mood was found for 5 consecutive times, a record was added

                    count_warning += 10
                kk = cv2.waitKey(10)
                if 1:  # exit the recording mode automatically
                    count_warning = 0
                    break
            # If in image mode, pause here to avoid errors
            if mode == 2:
                input()
        # Release the camera/video source
        self.cap.release()
        # delete the window
        cv2.destroyAllWindows()


if __name__ == "__main__":  # main function
    my_face = face_emotion()    # # instantiation
    my_face.learning_face(0, "test_data/6.mp4")

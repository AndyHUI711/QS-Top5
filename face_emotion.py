import dlib  # face recognition
import cv2  # image processing
import time


class face_emotion():

    def __init__(self):
        # # Use the feature extractor get_frontal_face_detector
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
        flag_e = 0
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
        count_all = [0] * 4
        tic = time.perf_counter()
        while (self.cap.isOpened()):
            if time.perf_counter() - tic >= 15:  # quit after 15 sec
                break
            flag, im_rd = self.cap.read()
            k = cv2.waitKey(1)
            # Take gray scale to adapt
            try:
                try:
                    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
                    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)
                except:
                    img_gray = im_rd
                    img_gray = cv2.GaussianBlur(img_gray, (3, 3), 0)
            except:
                break
            # scanning human face
            faces = self.detector(img_gray, 0)
            # font
            font = cv2.FONT_HERSHEY_SIMPLEX

            if (len(faces) != 0):
                # # checking 68-point face
                areaMaxFace = 0
                for i in range(len(faces)):  # # Choose the largest face
                    if faces[i].area() > areaMaxFace:
                        areaMaxFace = faces[i].area()
                        indexMax = i
                    print("第" + str(i) + "个脸面积：" + str(faces[i].area()))
                print("最大脸面积：" + str(faces[indexMax].area()) + "\n")
                print(faces[indexMax])
                for i in range(len(faces)):
                    for k, d in enumerate(faces):  # enumerate
                        # Box all faces
                        # Use a red rectangle to frame the face
                        cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                        # Calculate the edge length of the frame of the human face heat
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


                        th1 = 0.038845
                        th2 = 0.059244
                        th3 = 0.082031
                        th4 = 0.017198

                        # discussing thresholds
                        if (D4 > th1 and D5 > th2) or (D4 <= th1 and D5 > th2):
                            status_code = 2  # Happy
                            cv2.putText(im_rd, "Happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
                        elif D4 > th1 and D5 <= th3:
                            status_code = 1  # Sad
                            cv2.putText(im_rd, "Sad", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.8,
                                        (0, 0, 255), 2, 4)
                        elif D4 <= th1 and D5 <= th2 and D2 <= th4:  # adjust th3
                            status_code = 3  # Anger
                            cv2.putText(im_rd, "Angry", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)
                        else:
                            status_code = 4  # Natural
                            cv2.putText(im_rd, "Nature", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                        (0, 0, 255), 2, 4)

                # face amount
                cv2.putText(im_rd, "Faces: " + str(len(faces)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                # if no human face
                cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                status_code = 0
            # window display
            cv2.imshow('Caring System', im_rd)
            k = cv2.waitKey(10)
        # counting
            count_all[status_code - 1] += 1
        # Release the camera/video source
        self.cap.release()
        # delete the window
        cv2.destroyAllWindows()
        if sum(count_all) >= 10:    # if count > 10, valid detection
            flag_e = count_all.index(max(count_all)) + 1    # find the most frequently appeared mood
        else:
            flag_e = 0  # NONE_FACE
        print('ALL_COUNT = [Sad, Happy, Angry, Natural]' + str(count_all))
        if flag_e == 1:
            return 'Sad'
        elif flag_e == 2:
            return 'Happy'
        elif flag_e == 3:
            return 'Angry'
        elif flag_e == 4:
            return 'Natural'
        else:
            return 'NONE_FACE'

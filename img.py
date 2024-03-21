import cv2
import numpy as np


class Image:
    img_original = cv2.imread("london.jpg")
    img_edited = cv2.imread("london_ed.jpg")

    def __init__(self):

        self.gs_o, self.gs_e = self.gray_scale()

        self.frame = []
        self.coords = []

        self.new_img = np.zeros(shape=Image.img_edited.shape, dtype=np.uint8)

        self.alpha = np.zeros(shape=(Image.img_edited.shape[0], Image.img_edited.shape[1]), dtype=np.uint8)




    def gray_scale(self):
        arr_o = np.zeros(shape=(Image.img_original.shape[0], Image.img_original.shape[1]))
        arr_e = np.zeros(shape=(Image.img_edited.shape[0], Image.img_edited.shape[1]))

        shape_o = Image.img_original.shape
        shape_e = Image.img_edited.shape

        b1,g1,r1 = np.split(Image.img_original, 3, axis=2)
        b2,g2,r2 = np.split(Image.img_edited, 3, axis=2)


        if shape_o == shape_e:
            arr_o = b1*0.144 + g1*0.587 + r1*0.299
            arr_e = b2*0.144 + g2*0.587 + r2*0.299

        else: pass

        return arr_o, arr_e

    def compare(self):
        frame = [(0,0), (self.gs_e.shape)]
        threshold_main = 13

        self.iterate(threshold_main,frame)

        frame1,frame2,frame3,biggest_frame = self.frames()

        threshold_object = 10
        self.iterate(threshold_object,frame1, frame_status=True)
        self.iterate(threshold_object+10,frame2, frame_status=True)
        self.iterate(threshold_object,frame3, frame_status=True)


        self.fill(frame1)
        self.fill(frame2)
        self.fill(frame3)


        rgba_img = np.dstack((self.new_img, self.alpha[:, :, np.newaxis]))
        biggest = rgba_img[biggest_frame[0][0]+1:biggest_frame[1][0],biggest_frame[0][1]+1:biggest_frame[1][1]]
        return rgba_img,biggest


    def frames(self):
        arr = [[self.coords[0]]]

        for i in range(len(self.coords)):
            for j in range(len((arr))):
                diff_x = abs(arr[j][0][0]-self.coords[i][0])
                diff_y = abs(arr[j][0][1]-self.coords[i][1])

                if diff_x< 150 and diff_y <150:
                    arr[j].append(self.coords[i])
                    break

            else:
                arr.append([self.coords[i]])

        object1 = np.asarray(arr[0])
        object2 = np.asarray(arr[1])
        object3 = np.asarray(arr[2])

        min_x1, min_y1 = np.min(object1, axis=0)
        max_x1, max_y1 = np.max(object1, axis=0)

        min_x2, min_y2 = np.min(object2, axis=0)
        max_x2, max_y2 = np.max(object2, axis=0)

        min_x3, min_y3 = np.min(object3, axis=0)
        max_x3, max_y3 = np.max(object3, axis=0)

        biggest = self.find_biggest_obj([(min_x1, min_y1), (max_x1,max_y1)], [(min_x2, min_y2), (max_x2,max_y2)], [(min_x3, min_y3), (max_x3,max_y3)])

        return [(min_x1, min_y1), (max_x1,max_y1)], [(min_x2, min_y2), (max_x2,max_y2)], [(min_x3, min_y3), (max_x3,max_y3)],biggest


    def iterate(self, threshold, object, frame_status = False):

        x1 = object[0][0]
        y1 = object[1][0]
        x2 = object[0][1]
        y2 = object[1][1]

        for i in range(x1, y1):
            for j in range(x2, y2):

                diff = abs(self.gs_o[i][j]-self.gs_e[i][j])

                if diff> threshold :
                    self.alpha[i][j] = 255
                    self.new_img[i][j] = Image.img_edited[i][j]
                    self.coords.append((i,j))

                else:
                    self.alpha[i][j] = 0
                    self.new_img[i][j] = (0, 0, 0)

                if frame_status:
                    self.new_img[x1][j] = (0, 255, 0)
                    self.new_img[y1][j] = (0, 255, 0)
                    self.alpha[x1][j] = 0
                    self.alpha[y1][j] = 0

                if frame_status:
                    self.new_img[i][x2] = (0, 255, 0)
                    self.new_img[i][y2] = (0, 255, 0)
                    self.alpha[i][x2] = 0
                    self.alpha[i][y2] = 0


    def fill(self, frame):

        y1 = frame[0][0] +1
        y2 = frame[1][0] -1
        x1 = frame[0][1] +1
        x2 = frame[1][1] -1

        for j in range(y1,y2):
            start, end = 0,0

            for i in range (x1,x2):

                if any(self.new_img[j][i]) and start ==0:
                    start = i

                elif any(self.new_img[j][i]):
                    end = i

            for k in range(start,end):


                self.alpha[j][k] = 255
                self.new_img[j][k] = Image.img_edited[j][k]



    def find_biggest_obj(self, obj1, obj2, obj3):

        diff_x1 = abs(obj1[0][0]-obj1[1][0])
        diff_y1 = abs(obj1[0][1]-obj1[1][1])
        area1 = diff_x1*diff_y1

        diff_x2 = abs(obj2[0][0]-obj2[1][0])
        diff_y2 = abs(obj2[0][1]-obj2[1][1])
        area2 = diff_x2*diff_y2

        diff_x3 = abs(obj3[0][0]-obj3[1][0])
        diff_y3 = abs(obj3[0][1]-obj3[1][1])
        area3 = diff_x3*diff_y3

        arr = np.array([area1, area2, area3])
        max = np.argmax(arr)

        if max == 0: return obj1
        elif max == 1: return obj2
        elif max == 2: return obj3




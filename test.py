import cv2
import matplotlib.pyplot as plt
from typing import Sequence 
from cv2 import DMatch, KeyPoint 
from cv2.typing import MatLike, Point
import numpy as np
from math import sqrt
from time import sleep

class FaceFinder:
    def __init__(self, device_id_rgb, device_id_thermal):
        self.face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.video_capture_rgb = cv2.VideoCapture(device_id_rgb)
        # self.video_capture_thermal = cv2.VideoCapture(device_id_thermal)
        self.video_capture_thermal = self.video_capture_rgb

    def detectBoundingBox(self, vid):
        gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
        for (x, y, w, h) in faces:
            cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
        return faces

    def distance(self, point1: Point, point2: Point) -> Point:
        r2 = (point1[0] - point2[0], point1[1] - point2[1])
        return r2

    def detect(self):
        # result, video_frame1 = self.video_capture_rgb.read()
        # sleep(2)
        # result, video_frame2 = self.video_capture_thermal.read()
        video_frame1 = cv2.imread("./f1.png")
        video_frame2 = cv2.imread("./f2.png")
        # if result is False:
        #     self.video_capture.release()
        #     return None, None

        # faces = self.detectBoundingBox(video_frame)
        # return faces, video_frame

        #query image
        gray_image1 = cv2.cvtColor(video_frame1, cv2.COLOR_BGR2GRAY)
        #training image
        gray_image2 = cv2.cvtColor(video_frame2, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB.create()
        key1: Sequence[KeyPoint]
        des1: MatLike

        key2: Sequence[KeyPoint]
        des2: MatLike

        key1, des1 = orb.detectAndCompute(gray_image1, None)
        key2, des2 = orb.detectAndCompute(gray_image2, None)

        matcher = cv2.DescriptorMatcher.create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(des1, des2, None)
        # Sort matches by score
        # matches.sort(key=lambda x: x.distance, reverse=False)
        matches = sorted(matches, key=lambda x: x.distance, reverse=False)
        
        # Remove not so good matches
        numGoodMatches = int(len(matches) * 0.15)
        matches:Sequence[DMatch] = matches[:numGoodMatches]
        
        query_points = [key1[match.queryIdx].pt for match in matches]
        training_points = [key2[match.trainIdx].pt for match in matches]

        print(query_points[0])
        print(training_points[0])
        print(self.distance(query_points[0], training_points[0]))
        positional_vectors = []
        for i in range(0, len(query_points)):
            positional_vectors.append(self.distance(query_points[i], training_points[i]))
        
        average_x = sum(pt[0] for pt in positional_vectors)/len(positional_vectors)
        average_y = sum(pt[1] for pt in positional_vectors)/len(positional_vectors)
        # trans_matrix = np.float32([[1,0,average_x], [0,1,average_y]])
        trans_matrix = np.float32([[1,0,average_x], [0,1,average_y]])
        img3 = cv2.warpAffine(gray_image2, trans_matrix, (gray_image2.shape[1], gray_image2.shape[0]))
        print(img3.shape)
        print(gray_image2.shape)
        print(gray_image1.shape)
        # plt.imshow(img3)
        # plt.show()
        plt.imshow(cv2.addWeighted(gray_image1,0.4, img3,0.1,0))
        plt.show()



        # np_query = np.array(query_points).reshape(-1,1,2)
        # np_train = np.array(training_points)
        # print(np_query.shape)
        # print(np_train.shape)

        
        # Draw top matches
        # imMatches = cv2.drawMatches(gray_image1, key1, gray_image2, key2, matches, None)
        # plt.imshow(imMatches)
        # plt.show()


if __name__ == '__main__':
    finder = FaceFinder(0,0)

    finder.detect()
    # if type(faces) == None or type(video_frame) == None:
    #     exit()

    # im1 = plt.imshow(video_frame)
    # plt.ion()
    # while True:
    #     faces, video_frame = finder.detect()
    #     if type(faces) == None or type(video_frame) == None:
    #         break
    #     print(faces)
    #     im1.set_data(video_frame)
    #     plt.pause(0.1)
    # cv2.destroyAllWindows()

import cv2
import matplotlib.pyplot as plt

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

    def detect(self):
        result, video_frame1 = self.video_capture_rgb.read()
        result, video_frame2 = self.video_capture_thermal.read()
        # if result is False:
        #     self.video_capture.release()
        #     return None, None

        # faces = self.detectBoundingBox(video_frame)
        # return faces, video_frame

        gray_image1 = cv2.cvtColor(video_frame1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(video_frame2, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB.create()
        key1, des1 = orb.detectAndCompute(gray_image1, None)
        key2, des2 = orb.detectAndCompute(gray_image2, None)

        matcher = cv2.DescriptorMatcher.create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(des1, des2, None)
        matches = [x for x in matches]

        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)
        
        # Remove not so good matches
        numGoodMatches = int(len(matches) * 0.15)
        matches = matches[:numGoodMatches]
        
        # Draw top matches
        imMatches = cv2.drawMatches(gray_image1, key1, gray_image2, key2, matches, None)
        plt.imshow(imMatches)
        plt.show()


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

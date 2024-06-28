import unittest
from function import openai_request
import cv2

class OpenAIRequestUnitTest(unittest.TestCase):
	def test_send_request_image(self):
		# Read the image using OpenCV
		image = cv2.imread("test/data/test_images/frame_0.jpg")
		# Put image in list because this function takes in a list of images
		analysis = openai_request.analyze_images([image])


		self.assertIsNotNone(analysis)
		self.assertIn("content", analysis)
		content = analysis["content"]
		self.assertTrue("sandwich" in content)
		self.assertTrue("video" in content)

	def test_send_request_multiple_images(self):
		image_list = []
		for i in range(10):
			image_path = f"test/data/test_images/frame_{i}.jpg"
			image = cv2.imread(image_path)
			image_list.append(image)
		analysis = openai_request.analyze_images(image_list)

		self.assertIsNotNone(analysis)
		self.assertIn("content", analysis)

		content = analysis["content"]
		self.assertTrue("sandwich" in content)
		self.assertTrue("video" in content)

if __name__ == '__main__':
	unittest.main()

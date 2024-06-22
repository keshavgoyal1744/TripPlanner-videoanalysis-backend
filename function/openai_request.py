import requests
import cv2
import json
import settings
from openai import OpenAI
import base64

def analyze_images(images: list):
	# Convert the image to JPG format
	# Convert the images to JPG format
	base_64_list = []
	for image in images:
		_, image_jpg = cv2.imencode('.jpg', image)
		base_64_list.append(base64.b64encode(image_jpg.tobytes()).decode('utf-8'))

	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {settings.openapi_key}"
	}

	content = []
	content.append(
		{
			"type": "text",
			"text": "These images are chronological sequence of a TikTok video. Analyze the content of this video in one paragraph only."
		})
	
	for base64_image in base_64_list:
		content.append(
			{
				"type": "image_url",
				"image_url": {
					"detail": "low", # details low is around 20 tokens, while detail high is around 900 tokens
					"url": f"data:image/jpeg;base64,{base64_image}"
				}
			})

	payload = {
		"model": "gpt-4o",
		"messages": [
			{
				"role": "user",
				"content": content
			}
		],
		"max_tokens": 300
	}

	# Find API request object here https://platform.openai.com/docs/guides/vision
	response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

	return response.json()["choices"][0]["message"]["content"]
import base64
from mimetypes import guess_type
from openai import AzureOpenAI




class ImageProcessor:
    def __init__(self, api_key, azure_endpoint, api_version):
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint
        self.api_version = api_version
        self.client = AzureOpenAI(api_key=self.api_key, azure_endpoint=self.azure_endpoint, api_version=self.api_version)

    def local_image_to_data_url(self, image_path):

        mime_type, _ = guess_type(image_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'  

        # reading and encoding the image file
        with open(image_path, "rb") as image_file:
            base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

        # data URL
        return f"data:{mime_type};base64,{base64_encoded_data}"

    def describe_image(self, image_path):
        #  the local image to a data URL
        data_url = self.local_image_to_data_url(image_path)

        #  API request to get the image description
        response = self.client.chat.completions.create(
            model="gpt-4-vision",
            messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", 
                     "text": f"""You are trained to interpret images about people and make responsible assumptions about them. Describe the image in detail, if the image is blank, white, or no meaningful description can be provided, answer with "No description for this image """},
                    {
                    "type": "image_url",
                    "image_url": {
                        "url" : data_url, 
                    },
                    },
                ],
                }
            ],
            max_tokens=100,
            temperature=0
            )
        

        return response.choices[0].message.content

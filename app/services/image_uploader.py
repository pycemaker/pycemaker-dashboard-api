import json
import os
import random
import string
import time
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, delete_app, storage
import os

load_dotenv('.env')


class ImageUploader:

    def __init__(self):
        self.firebase_settings = json.loads(
            os.environ.get("FIREBASE_SETTINGS"))
        # self.firebase_settings = os.path.dirname(os.path.dirname(
        #     os.path.dirname(os.path.abspath(__file__)))) + "/firebase-settings.json"
        self.cred = credentials.Certificate(self.firebase_settings)
        self.app = initialize_app(
            self.cred, {'storageBucket': 'pycemaker.appspot.com'})

    def uploadImage(self, image):
        # new_name = str(datetime.utcnow().strftime('%Y%m%d%H%M%S%f-'))
        new_name = str(int(time.time()*1000)) + "-"
        new_name = new_name + ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(10))
        new_name = new_name + os.path.splitext(image)[1]

        bucket = storage.bucket()
        blob = bucket.blob("images/" + new_name)
        blob.upload_from_filename(image)
        blob.make_public()

        print("your file url", blob.public_url)
        return blob.public_url

    def uploadBytesImage(self, image):
        # new_name = str(datetime.utcnow().strftime('%Y%m%d%H%M%S%f-'))
        new_name = str(int(time.time()*1000)) + "-"
        new_name = new_name + ''.join(random.SystemRandom().choice(
            string.ascii_letters + string.digits) for _ in range(10))
        new_name = new_name + ".png"

        bucket = storage.bucket()
        blob = bucket.blob("images/" + new_name)
        # blob.upload_from_filename(image)
        blob.upload_from_file(image, content_type='image/png')
        blob.make_public()

        print("your file url", blob.public_url)
        return blob.public_url

    def close(self):
        delete_app(self.app)

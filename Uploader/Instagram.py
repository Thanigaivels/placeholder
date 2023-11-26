import os, json, sys
from pathlib import Path
from instagrapi import Client

insta_client = None
CWD = os.path.dirname(__file__)

class InstaUploader:
    def __init__(self, profile):
        try:
            cookie_file = f'{profile["user"]}.json'
            if os.path.exists(cookie_file):
                cl = Client(json.load(open(cookie_file)))
            else:
                cl = Client()
                cl.login(profile['user'], profile['password'])
            json.dump(cl.get_settings(), open(cookie_file, 'w'), indent=4)
            self.client = cl
        except Exception as e:
            print("Something went wrong when creating insta client...\n", e)
            sys.exit(1)
        self.source = "insta"
        self.username = profile['user']

    def upload(self, file_path, caption, thumbnail):
        content = file_path
        insta_client = self.client

        _status = None
        if caption is None or len(caption) > 1500:
            caption = '''Look at this amazing video\n #instagood #trending #reels'''
        else:
            caption = caption.replace("gommala", self.username)

        if file_path.endswith('jpg') or file_path.endswith('jpeg'):
            _status = insta_client.photo_upload(content, caption)
        elif file_path.endswith('mp4'):
            if thumbnail != None and os.path.exists(thumbnail):
                _status = insta_client.video_upload(content, caption=caption, thumbnail=thumbnail)
            else:
                _status = insta_client.video_upload(content, caption)

        print("is uploaded? ", _status is not None)
        return _status is not None
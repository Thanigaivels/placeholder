import os, requests

from PIL import Image
from io import BytesIO
import ffmpeg, json
from Uploader import Instagram
from Utils import storage_handler, configs

CWD = os.path.dirname(__file__)

def mention_id(new_image, user_name):
    pass

def process_image(image, add_mention, profile):
    pass

def create_tittle_and_caption_txt(post, path, file_name):
    pass

def download_image(url, file_name):
    path = os.path.join(CWD, "../cache/images")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    file_name = os.path.join(path, file_name + ".jpeg")
    if not os.path.exists(file_name):
        print('downloading file', file_name)
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image_name = file_name
        print(image_name)
        image.save(image_name)
    else:
        print("File already exists and not downloaded")
    return file_name

def download_video(video_url, audio_url, file_name):
    path = os.path.join(CWD, "../cache/videos")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    file_name = video_url.split("/")[-1]
    video_filename = file_name + '.mp4'
    audio_filename = file_name + '.mp3'

    print('Downloading video file...')
    video_content = requests.get(video_url, stream=True)
    with open(os.path.join(path, video_filename), 'wb') as f:
        f.write(video_content.content)

    print('Downloading audio file...')
    audio_content = requests.get(audio_url)
    if audio_content.status_code == 200:
        with open(os.path.join(path, audio_filename), 'wb') as f:
            f.write(audio_content.content)
    else:
        print("Problem downloading audio. So skipping this post.")
        return False

    return merge_audio_with_video(video_filename, audio_filename)

def merge_audio_with_video(video_file_name, audio_file_name):
    input_path = os.path.join(CWD, "../cache/videos")
    output_path = os.path.join(CWD, "../cache/tmp")
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)

    input_video = ffmpeg.input(os.path.join(input_path, video_file_name))
    added_audio = ffmpeg.input(os.path.join(input_path, audio_file_name))
    o_path = os.path.join(output_path, video_file_name)
    ffmpeg.concat(input_video, added_audio, v=1, a=1).output(o_path).run(overwrite_output=True)
    return o_path

def start_upload():
    data = storage_handler.fetch_post_data()
    post_url = data[3]
    post_attrib = data[4]
    post_type = data[7]
    caption = data[5]
    title = data[6]
    file_name = data[2]
    
    downloaded_path = ""

    print(post_type)
    if "reel" == post_type:
        post_urls = post_attrib['content']
        video_url = post_urls[0]
        audio_url = post_urls[1]
        downloaded_path = download_video(video_url, audio_url, file_name)
    elif "image" == post_type:
        downloaded_path = download_image(post_url, file_name)
    print(downloaded_path)
    if downloaded_path == False:
        print("Problem with post. So, marking as 'Pending' and proceeding with the next one.")
        storage_handler.update_job_status(data[0], 'Pending')
        start_upload()
    else:
        uploader = Instagram.InstaUploader(configs.get_insta_profile('profile_1'))
        result = uploader.upload(downloaded_path, caption, None)
        # Need to update job status
        if (result == True):
            storage_handler.update_job_status(data[0])
        print(result)
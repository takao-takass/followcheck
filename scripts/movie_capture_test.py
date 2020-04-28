import cv2
import os,math
from PIL import Image, ImageDraw

def save_all_frames(video_path, dir_path, basename, ext='jpg'):

    # 動画ファイルの読み込み
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    # 動画のフレームレートと長さ(秒)を取得する
    allFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # 画像として保存するフレームの位置を取得する
    captureFrameTiming = math.floor(allFrames / 7)
    captureFrameList = []
    for num in range(1,6):
        captureFrameList.append(captureFrameTiming * num)
    
    # 動画のフレームをサムネイル画像として保存する
    n = 0
    while True:
        video.set(cv2.CAP_PROP_POS_FRAMES, captureFrameList[0])
        ret, frame = video.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(4), ext), frame)
            n += 1
            del captureFrameList[0]
            if len(captureFrameList) == 0:
                return
        else:
            return

save_all_frames(
    'D://followcheck_dev/followcheck/followcheck/fcmedia/tweetmedia/yukin0128/sample.mp4',
    'D://followcheck_dev/followcheck/followcheck/fcmedia/tweetmedia/thumbs/',
    'sample_video_img')
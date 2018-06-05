import random
import string

import cv2
import numpy as np
import redis

from Core.abstract_classes import SharedStorage


def encodeimage(image, quality_val=85):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    ret, imgbuf_enc = cv2.imencode("*.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality_val])
    if not ret:
        return b""
    return imgbuf_enc.tobytes()


def decodeimage(buffer):
    if buffer is None:
        return None
    imgbuf_enc = np.frombuffer(buffer, dtype=np.uint8)
    img = cv2.imdecode(imgbuf_enc, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

class RedisSharedStorage(SharedStorage):
    def __init__(self, host="localhost", port=6379):
        self._redis = redis.StrictRedis(host=host, port=port)

    def get(self, key):
        val = self._redis.get(key)
        return val

    def set(self, key, data):
        self._redis.set(key, data, ex=10)

    def uniqueKey(self):
        while True:
            name_red = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            if self._redis.get(name_red) is None:
                break
        return name_red

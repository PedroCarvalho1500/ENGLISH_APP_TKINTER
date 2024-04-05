import threading
import time

import cv2


def test_loup():
    for i in range(1,1000):
        yield(i)


if __name__ == '__main__':
    test = test_loup()
    c = cv2.waitKey(7) % 0x100

    try:
        while(True):
            print(next(test))
            time.sleep(1)
    except KeyboardInterrupt:
        pass
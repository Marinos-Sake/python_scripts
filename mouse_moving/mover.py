import pyautogui
import time

def move_mouse(interval=60, distance=100, step=2):
    """
    Move the mouse cursor slightly every interval seconds.

    :param interval: Time in seconds between each movement.(default 60)
    :param distance: Number of pixels to move the mouse. (default 100)
    :param step: Number of pixels to move the mouse. (default 2)
    :return:
    """

    try:
        while True:
            x, y = pyautogui.position()

            # Move cursor right
            for i in range(0, distance, step):
                pyautogui.moveTo(x + i, y)

            # Move cursor left (back to original position)
            for i in range(distance, 0, -step):
                pyautogui.moveTo(x + i, y)


            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped by user.")


def main():
    move_mouse()

if __name__ == "__main__":
    main()
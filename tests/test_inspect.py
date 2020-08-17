import os
import time
import pyautogui
from multiprocessing import Process

basetest = 'tests/base.py'


def run_process(command):
    output = os.popen(command).read()
    if 'Traceback (most recent call last):' in output:
        raise RuntimeError(output)
    return output


def _test_code():
    run_process(f'python -m code < {basetest} 2>&1')


def _test_idle():
    with open(basetest) as f:
        source = f.read()

    p = Process(target=lambda: run_process('idle 2>&1'))
    p.start()
    assert p.is_alive()
    time.sleep(1)
    for line in source.splitlines():
        if line.startswith('    '):
            pyautogui.typewrite('\b', interval=0.05)
            time.sleep(0.06)
        pyautogui.typewrite(line + '\n', interval=0.05)
        time.sleep(0.3)
    time.sleep(0.1)
    pyautogui.typewrite('exit()\n', interval=0.05)
    time.sleep(0.2)
    pyautogui.press('enter')
    p.join()


def test_blender():
    with open(basetest) as f:
        source = f.read()

    p = Process(target=lambda: run_process('optirun blender --python-use-system-env 2>&1'))
    p.start()
    assert p.is_alive()

    time.sleep(2.6)
    pyautogui.press('esc')
    time.sleep(0.4)
    pyautogui.click(x=1125, y=50)
    time.sleep(0.4)
    pyautogui.click(x=100, y=800)
    time.sleep(0.3)

    if 0:
        for line in source.splitlines():
            if line.startswith('    '):
                pyautogui.typewrite('\b\b\b\b', interval=0.05)
                time.sleep(0.06)
            pyautogui.typewrite(line + '\n', interval=0.05)
            time.sleep(0.3)

        time.sleep(1)

    pyautogui.click(x=1040, y=80)
    time.sleep(0.3)
    pyautogui.click(x=1040, y=200)
    time.sleep(0.2)

    last_line = ''
    for line in source.splitlines():
        ll = last_line.startswith('    ') and all(_ not in last_line for _ in ['return', 'pass'])
        if line.startswith('    ') or ll:
            pyautogui.typewrite('\b', interval=0.06)
            time.sleep(0.06)
        pyautogui.typewrite(line + '\n', interval=0.06)
        time.sleep(0.12)
        last_line = line

    pyautogui.click(x=1200, y=80)
    time.sleep(1)
    pyautogui.click(x=1200, y=80)
    time.sleep(1)

    pyautogui.hotkey('ctrl', 's')
    time.sleep(0.8)
    pyautogui.click(x=450, y=640)
    time.sleep(0.8)
    pyautogui.click(x=1510, y=935)
    time.sleep(0.8)

    pyautogui.click(x=1200, y=80)
    time.sleep(1)
    pyautogui.click(x=1200, y=80)
    time.sleep(1)

    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.2)
    pyautogui.click(x=845, y=600)

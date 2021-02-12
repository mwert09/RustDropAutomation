import math
import webbrowser
import os
import twitch
import time

url = 'http://twitch.tv'
webbrowser.register('chrome', None,
                    webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
browserExe = "chrome.exe"
stream_data = []
WATCH_TIME = 130
current_streamer = ""
streamer_number = -1
helix = twitch.Helix('client-id', 'client-secret')
rust_game_id = helix.game(name="Rust").id


def first_check():
    with open('data.txt', 'r') as data:
        lines = data.readlines()
        for line in lines:
            if " False\n" in line:
                return True
    return False


def print_status():
    with open('data.txt', 'r') as data:
        lines = data.readlines()
        for line in lines:
            print(line)


def start_timer():
    global streamer_number
    if streamer_number == 9:  
        should_watch = first_check()
        if not should_watch:
            print("You've got everything")
            return
        streamer_number = -1
        os.remove("data.txt")
        with open('data.txt', 'w') as data:
            for streamer in stream_data:
                current_streamer_data = f"{streamer[0]}-{streamer[1]}-{streamer[2]}"
                data.write(current_streamer_data)
        return
    streamer_number += 1
    current_streamer = stream_data[streamer_number][0]
    if helix.user(current_streamer).is_live and stream_data[streamer_number][2] == " False\n" and helix.user(
            current_streamer).stream.game_id == rust_game_id:
        current_url = f"{url}/{current_streamer}"
        webbrowser.get('chrome').open_new(current_url)
        count_down(WATCH_TIME * 60, current_streamer)
    else:
        start_timer()


def count_down(count, current_streamer):
    while count >= 0:
        count_min = math.floor(count / 60)
        count_second = count % 60
        if count_second < 10:
            count_second = f"0{count_second}"
        os.system('cls')
        print(f"{str(current_streamer)} - {count_min}:{count_second}")
        if count > 0:
            time.sleep(1)
            count -= 1
        elif count <= 0:
            os.system("taskkill /f /im " + browserExe)
            os.remove("data.txt")
            stream_data[streamer_number][2] = " True\n"
            with open('data.txt', 'w') as data:
                for streamer in stream_data:
                    current_streamer_data = f"{streamer[0]}-{streamer[1]}-{streamer[2]}"
                    data.write(current_streamer_data)
            print_status()
            start_timer()


with open('data.txt', 'r') as data:
    lines = data.readlines()
    for line in lines:
        current_stream = line.split('-')
        stream_data.append(current_stream)

should_watch = first_check()
if should_watch:
    print_status()
    start_timer()
else:
    print("You've got everything")

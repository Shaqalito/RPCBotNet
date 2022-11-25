from pypresence import Client
import atexit
import subprocess
import os



def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call)
    last_line = output.strip().split(b'\r\n')[-1]
    return last_line.lower().startswith(f"{process_name.lower()}".encode())


if not process_exists("Discord.exe"):
    print("Discord is not running... Starting Discord.")
    subprocess.call(f"{os.getenv('LOCALAPPDATA')}\\Discord\\Update.exe --processStart Discord.exe")
else:
    print("Discord Running... Starting RPC")

RPC = Client(client_id=962841674017562656, client_secret="qpAk99uJIYpxfagIug_DuBjm5d0mf5k8")    # Initialize client with client ID and Secret
atexit.register(RPC.offline_remote)
RPC.start()  # Start client, have a handshake (response heartbeat from discord).
RPC.initiate_token_auth()


def vcs(data):
    print(f"VOICE : {data.get('hostname')} | Average ping: {data.get('average_ping')} | Last Ping: {data.get('last_ping')}")
def sps(data):
    print(data)
def notif(data):
    message = data["message"]
    print(f"-----\nNEW NOTIF\n{message['author']['username']}#{message['author']['discriminator']} - {message['timestamp']}\n{message['content']}\n\nATTACHMENTS: {message['attachments']}\nEMBEDS: {message['embeds']}\n-----\n")

register_list = [
    {
        "cmd": "VOICE_CONNECTION_STATUS",
        "func": vcs,
        "args": None
    },
    {
        "cmd": "NOTIFICATION_CREATE",
        "func": notif,
        "args": None
    },
    {
        "cmd": "SPEAKING_START",
        "func": sps,
        "args": {"channel_id": "550333783308501058"}
    }
]

RPC.online_remote(register_list)

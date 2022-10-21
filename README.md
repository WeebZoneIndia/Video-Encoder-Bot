# Video Encoder Bot
A telegram bot to convert and compress videos into x265/x264 format via ffmpeg.

### Configuration

**Basics**
- `API_ID` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `API_HASH` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` - Get it by creating a bot on [https://t.me/BotFather](https://t.me/BotFather)

**Authorization**
`Every Var can have space as seperator for multiple user/chat.`
- `OWNER_ID` - A user can have full access to bot throught this var.
- `SUDO_USERS` - Chat identifier of the sudo user.
- `EVERYONE_CHATS` - Chat identifier of the user who can't touch bot code.

**Log Channel**
- `LOG_CHANNEL` - for bot logs (user and group id will also work!)

**Database**
- `SESSION_NAME`
- `MONGO_URI` - A mongo db url for settings, addchat etc.

**Google Drive**
- `INDEX_URL` - Index url for drive uploads
- `DRIVE_DIR` - Google Drive folder id where uploads will be placed.

**Optional**
- `DOWNLOAD_DIR` - (Optional) Temporary download directory to keep downloaded files.
- `ENCODE_DIR` - (Optional) Temporary encode directory to keep encoded files.

### Configuring Encoding Format
To change the ffmpeg profile edit them in [ffmpeg.py](/VideoEncoder/utils/ffmpeg.py)

### Installing Requirements
Install the required Python Modules and Latest FFMPEG in your machine.
```sh
apt update && apt-get install software-properties-common -y && apt-get update && add-apt-repository -y ppa:savoury1/ffmpeg4 && apt-get install -y ffmpeg && add-apt-repository -y ppa:savoury1/ffmpeg5 && apt-get install -y ffmpeg && pip3 install -r requirements.txt
```

### Deployment
With python 3.9.2 or later.
first make repo folder workdir then
```sh
apt update && apt install -y --no-install-recommends git wget aria2 curl busybox python3 python3-pip p7zip-full p7zip-rar unzip mkvtoolnix ffmpeg
pip3 install --no-cache-dir -r requirements.txt
chmod +x extract
bash run.sh
```

### For Drive
`Place token.pickle and credentials.json on workdir`

### Deployment via Docker
**Install docker**
```sh
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic nightly" && apt-cache policy docker-ce && sudo apt install docker-ce -y
```
**Start docker build**
- restart always
- docker name is encoder
```sh
sudo docker build . --no-cache -t encoder && sudo docker run --restart always --name encoder encoder
```

**Stop Docker for Major Change**
- this only need if update docker file or requirements only or else use update in bot
```sh
sudo docker stop encoder && sudo docker rm encoder
```

### Credits
- [ShannonScott](https://gist.github.com/ShannonScott) for [transcode_h265.py](https://gist.github.com/ShannonScott/6d807fc59bfa0356eee64fad66f9d9a8)
- [viperadnan-git](https://github.com/viperadnan-git/video-encoder-bot) for queue logic etc.

### Copyright & License
- Copyright &copy; 2022 &mdash; [WeebTime](https://github.com/WeebTime)
- Licensed under the terms of the [GNU Affero General Public License Version 3 &dash; 29 June 2007](./LICENSE)
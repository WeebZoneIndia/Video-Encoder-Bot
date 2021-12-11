# Video-Encoder-Bot
 a telegram bot for compressing/encoding videos in h264 format.

### Configuration
Add values in environment variables or add them in [config.env.example](/VideoEncoder/config.env.example) and rename file to `config.env`.

**Basics**
- `API_ID` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `API_HASH` - Get it by creating an app on [https://my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` - Get it by creating a bot on [https://t.me/BotFather](https://t.me/BotFather)

**Authorization**
- `SUDO_USERS` - Chat identifier of the sudo user. For multiple users use space as seperator.

**Encode Settings**
- `RESOLUTION` - [Click Here](https://weeb-zone.blogspot.com/p/encode-telegram-bot-guide.html)
- `PRESET` - [Click Here](https://weeb-zone.blogspot.com/p/encode-telegram-bot-guide.html)
- `TUNE` - [Click Here](https://weeb-zone.blogspot.com/p/encode-telegram-bot-guide.html)
- `AUDIO` - [Click Here](https://weeb-zone.blogspot.com/p/encode-telegram-bot-guide.html)
- `CRF` - [Click Here](https://weeb-zone.blogspot.com/p/encode-telegram-bot-guide.html)

**Optional**
- `DOC_THUMB` - (Optional) Thumbnail for document
- `UPLOAD_AS_DOC` - (Optional) Uploads Video as doc if `1` else `0`.
- `DOWNLOAD_DIR` - (Optional) Temporary download directory to keep downloaded files.
- `ENCODE_DIR` - (Optional) Temporary encode directory to keep encoded files.

### Configuring Encoding Format
To change the ffmpeg profile edit them in [ffmpeg.py](/VideoEncoder/utils/ffmpeg.py)

### Deployment
With python3.7 or later.
```
pip3 install --no-cache-dir -r requirements.txt
bash run.sh
```

### Credits
- [ShannonScott](https://gist.github.com/ShannonScott) for [transcode_h265.py](https://gist.github.com/ShannonScott/6d807fc59bfa0356eee64fad66f9d9a8)
- [viperadnan-git](https://github.com/viperadnan-git/video-encoder-bot) for queue etc.

### Copyright & License
- Copyright &copy; 2021 &mdash; [WeebTime](https://github.com/WeebTime)
- Licensed under the terms of the [GNU AFFERO GENERAL PUBLIC LICENSE](./LICENSE)
# Torrent / YouTube Leecher 🔥🤖

A Torrent, youtube-dl Leecher, and Uploader!

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [COPYING](./COPYING) for more details.

## installing

### The Eas(iest) Way

- Install Docker by following the [official docker docs](https://docs.docker.com/engine/install/debian/)

- Start docker daemon [skip if already running]:
```sh
dockerd
```
- Build Docker image:
```sh
docker build . -t public-leech
```
- Run the image:
```sh
docker run public-leech
```

It is not recommended to use "sudo", un-necessarily, in a GNU/Linux system.
GNU/Linux Permissions are highly customisable, and it is generally not required to have "ROOT" permission, ~~unless you know what you are doing~~.
You can still install all the dependencies in your system [with ROOT permissions], but please be aware of the potential issues when doing so. The installed packages may conflict with the system package manager's installed packages, which can cause trouble down the road and errors when upgrading conflicting packages.
**You have been warned.**


### The Legacy Way
Simply clone the repository and run the main file:

```sh
git clone https://github.com/SpEcHiDe/PublicLeech.git
cd PublicLeech
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
python3 -m tobrot
```

### Variable Explanations

##### Mandatory Variables

* `TG_BOT_TOKEN`: Create a bot using [@BotFather](https://telegram.dog/BotFather), and get the Telegram API token.

* `APP_ID`
* `API_HASH`: Get these two values from [my.telegram.org/apps](https://my.telegram.org/apps).
  * N.B.: if Telegram is blocked by your ISP, try our [Telegram bot](https://telegram.dog/UseTGXBot) to get the IDs.

* `AUTH_CHANNEL`:
Create a Super Group in Telegram, add `@GoogleIMGBot` to the group, and send /id in the chat, to get this value.
You can add multiple IDs seperated by space.

##### Optional Configuration Variables

* `SHOULD_USE_BUTTONS`: because, [BlameTelegram](https://t.me/c/1494623325/5603)

* `ARIA_TWO_STARTED_PORT`: The port on which aria2c daemon must START. This should be an integer, between 1001 and 65535.

* `EDIT_SLEEP_TIME_OUT`: The number of seconds to sleep after editing a Telegram message.

* `MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START`: The number of seconds to wait before auto-cancelling a dead link.

* `FINISHED_PROGRESS_STR`: any character(s) that might be displayed in the progress string.

* `UN_FINISHED_PROGRESS_STR`: any character(s) that might be displayed in the progress string.

* `TG_OFFENSIVE_API`: ~~DO NOT USE THIS~~.

* `R_CLONE_CONF_URI`:
![a help, maybe](https://telegra.ph/file/073bcbc0b69b03d75ea04.jpg)

* `R_CLONE_DEST`: Destination folder for rclone copying. Set your path starting with '/'. Or just leave '/' to set root folder

* `DOWNLOAD_LOCATION`: optional download directory, where the temporary downloads should ideally reside.

* `MAX_FILE_SIZE`: The maximum file_size allowed by Telegram [BOT API](https://core.telegram.org/bots/api), kept for [legacy purposes](https://t.me/c/1235155926/33801).

* `TG_MAX_FILE_SIZE`: The maximum file_size, allowed by Telegram [API](https://core.telegram.org/api).

* `FREE_USER_MAX_FILE_SIZE`: The file_size that was [supposed to be allowed](https://t.me/c/1331081386/147445) by the bot.

* `MAX_TG_SPLIT_FILE_SIZE`: The file_size at which it should be splitted if the file_size is greater than  `TG_MAX_FILE_SIZE`.

* `CHUNK_SIZE`: ~~not used~~, kept for [legacy purposes](https://t.me/c/1235155926/33801).

* `MAX_MESSAGE_LENGTH`: The maximum message length, allowed by [Telegram](https://t.me/c/1097142020/1224).

* `PROCESS_MAX_TIMEOUT`: ~~not used~~, kept for [legacy purposes](https://t.me/c/1235155926/33801).

* `SP_LIT_ALGO_RITH_M`: allowed values can be `hjs` or `rar`.
  - VIDEO files are not affected based on this value.

* `DIS_ABLE_ST_GFC_COMMAND_I`: setting this to ANYTHING will enable `/exec` and `/eval` commands.


## Available Commands

* The available commands depends on the ENVironment / CONfig variables that is set by you.
* You can read the [Commandi](./tobrot/dinmamoc.py) file, to know about the ENVironment variables to use.
* You can read the [Loilacaztion](./tobrot/amocmadin.py) file, to know about the ENVironment variables to use.


## How to Use?

* send any link, and click on the available buttons.

* if you have disabled `SHOULD_USE_BUTTONS`, you can read the [Commandi](./tobrot/dinmamoc.py) file, to know about the commands.
  - [COMMANDI_LEECH](./tobrot/dinmamoc.py#L23) can take multiple arguments
    * `archive`: if you want a `.tar.gz` file, in your Telegram Chat.
    * `leech_rc_0`: if you want to mirror to an rClone supported host, `0` is an example, and should be replaced with the index of your required host, in your uploaded `rclone.conf` file.

* if file is larger than `TG_MAX_FILE_SIZE`, [read this](https://t.me/c/1434259219/113).

* if file is a TAR archive, [read this](https://t.me/c/1434259219/104) to know how to uncompress.


## Issues or Feature Requests

* search for known issues, [here](https://t.me/c/1434259219/118) or in the [GitHub Issues](https://github.com/SpEcHiDe/PublicLeech/issues).

* add issues / feature requests, [here](https://github.com/SpEcHiDe/PublicLeech/issues/new).

* the GitHub Issue Tracker is only for Issue / Feature Requests. For any support, please use the Telegram Group.

## Credits, and Thanks to

* [me](https://GitHub.com/SpEcHIDe/PublicLeech)
* [Dan Tès](https://telegram.dog/haskell) for his [Pyrogram Library](https://github.com/pyrogram/pyrogram)
* [Robots](https://telegram.dog/Robots) for their [@UploadBot](https://telegram.dog/UploadBot)
* [@AjeeshNair](https://telegram.dog/AjeeshNait) for his [torrent.ajee.sh](https://torrent.ajee.sh)
* [@gotstc](https://telegram.dog/gotstc), @aryanvikash, [@HasibulKabir](https://telegram.dog/HasibulKabir) for their TORRENT groups
* [rClone Team](https://github.com/rclone/rclone)
* [gautamajay52](https://github.com/gautamajay52/TorrentLeech-Gdrive)
* [![CopyLeft](https://telegra.ph/file/b514ed14d994557a724cb.jpg)](https://telegra.ph/file/fab1017e21c42a5c1e613.mp4 "CopyLeft Credit Video")

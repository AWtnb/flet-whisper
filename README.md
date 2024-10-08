# README

[whisper](https://github.com/openai/whisper) を使って日本語の文字起こしをするGUIアプリケーション（[Flet](https://flet.dev/) 製）。

> [!NOTE]
> このソフトは [ffmpeg](https://ffmpeg.org/) を必要とします。PCにはfmpegがインストールされていて、なおかつffmpegのパスがユーザー環境変数に追加されている必要があります。

## USAGE

`okoshi.exe` 単体で動きます。適当なフォルダに配置してから、ファイルをダブルクリックして起動してください。
黒い画面がしばらく（数十秒～）表示されたあと、メイン画面が立ち上がります。

![img](./images/main-image.png)

### 初回起動時のみ必要な操作

おそらく初回の起動時に、Windows からの警告が表示されます。有効化するには下記の操作をしてください。

1. 「PC が保護されました」という表示の場合は「詳細情報」をクリック。

    ![img](./images/warning-1.png)

1. 表示される「実行」ボタンをクリックするとアプリが起動します。

    ![img](./images/warning-2.png)

### 2回目以降

1. `対象の音声ファイル` と `出力フォルダ` を指定する
1. `Quality` のドロップダウンリストから文字起こしの品質を指定する
    - medium（高品質）以上を指定すると処理に数時間～数日かかることがあります
1. `文字起こしを実行する` のボタンを押すと処理が開始します
    - 実行中はボタンなどが反応しなくなります
    - 黒い画面に進捗が表示されます
    - メイン画面も黒い画面も閉じずにそのまま待機してください
    - 実行中はPCがとても重くなるので注意してください
1. `mail` にメールアドレスを指定すると、文字起こしが完了した段階でメールで通知します
    - メールには文字起こし結果のテキストファイルが添付されます
    - メール通知後もプログラムを実行したPCには音声ファイルとテキストファイルが残っているので、適宜片付けてください
1. 黒い画面かメイン画面のどちらかを閉じるとプログラムが終了します

## Build (for developper)

Create `.env` into `assets` folder and set your mail setting.

```
.\
├─main.py
└─assets
    └─.env
```

`.env` :

```
SENDER_ADDRESS=●●
CC_ADDRESS=●●
SENDER_PASSWORD=●●
SMTP_HOST=●●
SMTP_PORT=●●
```

Create venv.

```
python -m venv .venv
```

Install packages:

```
python -m pip install flet
python -m pip install python-dotenv
python -m pip install openai-whisper
```


Build pyinstaller locally (`.exe` generated with pip-installed pyinstaller is often considered as virus by security soft):

1. `git clone https://github.com/pyinstaller/pyinstaller`
1. `cd .\pyinstaller\bootloader\`
1. `python .\waf all`
    - Build would fail, but it is ignorable.
    - Visual Studio C++ compiler is required for build.
        - It can be installed with [Scoop](https://scoop.sh/) : `scoop install vcredist2015` .
    - In my environment, 2015 and 2022 were installed. If just installing vcredist2015 results in error, try installing the latest version as well.
1. `cd ..` (move to `pyinstaller` directory)
1. `pip install .`
1. Delete `pyinstaller` folder.
    - This folder is used only for package build and no longer used.



### Build `okoshi.exe`

1. Enter venv ([skippable on VSCode](https://github.com/microsoft/vscode-python/wiki/Activate-Environments-in-Terminal-Using-Environment-Variables))

    ```
    .\.venv\Scripts\activate
    ```

1. Run:

    ```
    pyinstaller --onefile --name okoshi --collect-data whisper --add-data "assets\.env;assets" .\main.py
    ```

    - If error was raised around pathlib, uninstall it: `python -m pip uninstall pathlib -y`
    - After build, re-install: `python -m pip install pathlib`

1. Exit from venv ([skippable on VSCode](https://github.com/microsoft/vscode-python/wiki/Activate-Environments-in-Terminal-Using-Environment-Variables))

    ```
    deactivate
    ```

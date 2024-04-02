# README

[Flet](https://flet.dev/) GUI application for Japanese dictation with [whisper](https://github.com/openai/whisper).
This software requires [ffmpeg](https://ffmpeg.org/), which must be installed on your PC and the ffmpeg path must be added to the user environment variable.

[whisper](https://github.com/openai/whisper) を使って日本語の文字起こしをするGUIアプリケーション（[Flet](https://flet.dev/) 製）。
このソフトは [ffmpeg](https://ffmpeg.org/) を必要とします。PCにはfmpegがインストールされていて、なおかつffmpegのパスがユーザー環境変数に追加されている必要があります。

## BUILD

1. Find `whisper` folder inside Python site-packages folder and copy them into `assets` folder.

    ```
    .\
    ├─main.py
    └─assets
        └─whisper
            ├─...
            ︙
    ```

1. Remove pathlib module for pyinstaller compatibility:

    ```
    python -m pip uninstall pathlib
    ```

1. Run:

    ```
    pyinstaller --onefile --name okoshi --add-data "assets\whisper;whisper" .\main.py
    ```

1. Re-install pathlib:

    ```
    python -m pip install pathlib
    ```

---

When running a build using pyinstaller installed with `pip install pyinstaller`, the generated `.exe` file may be considered a virus by Windows Defender.
In this case, using a locally built pyinstaller may solve the problem.

Steps:

1. `git clone https://github.com/pyinstaller/pyinstaller`
1. `cd .\pyinstaller\bootloader\`
1. `python .\waf all`
    + Visual Studio C++ compiler is required for build.
        + It can be installed with [Scoop](https://scoop.sh/) : `scoop install vcredist2015` .
    + In my environment, 2015 and 2022 were installed. If just installing vcredist2015 results in error, try installing the latest version as well.
1. `cd ..` (move to `pyinstaller` directory)
1. `pip install .`

This will build pyinstaller in the python site-package folder.
The folder used for the build is no longer used, so you can delete it.
# README

[Flet](https://flet.dev/) GUI application for Japanese dictation with [whisper](https://github.com/openai/whisper).

[whisper](https://github.com/openai/whisper) を使って日本語の文字起こしをするGUIアプリケーション（[Flet](https://flet.dev/) 製）。


This software requires [ffmpeg](https://ffmpeg.org/), which must be installed on your PC and the ffmpeg path must be added to the user environment variable.

このソフトは [ffmpeg](https://ffmpeg.org/) を必要とします。PCにはfmpegがインストールされていて、なおかつffmpegのパスが[ユーザー環境変数に追加](https://engrholiday.jp/win/surface-env-path/#:~:text=%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%81%AE%EF%BC%BB%E8%A9%B3%E7%B4%B0%E6%83%85%E5%A0%B1%EF%BC%BD%E3%82%88%E3%82%8A,%E6%96%B0%E8%A6%8F%E3%80%91%E3%82%92%E3%82%AF%E3%83%AA%E3%83%83%E3%82%AF%E3%81%97%E3%81%BE%E3%81%99%E3%80%82)されている必要があります。

## BUILD

1. Find `whisper` folder inside Python site-packages folder and copy them into `assets` folder.

    ```
    .\
    │  main.py
    │
    └─assets
        └─whisper
            └─...
    ```

1. `python -m pip uninstall pathlib`
1. `pyinstaller --onefile --name okoshi --add-data "assets\whisper;whisper" .\main.py`
1. `python -m pip install pathlib`

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
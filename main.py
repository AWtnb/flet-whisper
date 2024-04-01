import os

import flet as ft
import whisper


def main(page: ft.Page):
    page.title = "whisper dictation"
    page.theme_mode = "light"

    target_file_path = ft.Ref[ft.Text]()
    output_folder_path = ft.Ref[ft.Text]()
    quality_selector = ft.Ref[ft.Dropdown]()
    message_to_user = ft.Ref[ft.Text]()
    progress_ring = ft.Ref[ft.ProgressRing]()

    ui_rows = []

    ###################################
    # file picker
    ###################################

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            target_file_path.current.value = e.files[0].path
            output_folder_path.current.value = os.path.dirname(
                target_file_path.current.value
            )
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    def show_file_picker(_: ft.FilePickerResultEvent):
        file_picker.pick_files(
            allow_multiple=False, file_type="custom", allowed_extensions=["m4a", "mp3"]
        )

    file_pick_row = ft.Row(
        controls=[
            ft.ElevatedButton("対象の音声ファイル", on_click=show_file_picker),
            ft.Text(ref=target_file_path),
        ]
    )
    ui_rows.append(file_pick_row)

    ###################################
    # folder picker
    ###################################

    def on_folder_picked(e: ft.FilePickerResultEvent):
        if e.path:
            output_folder_path.current.value = e.path
            page.update()

    folder_picker = ft.FilePicker(on_result=on_folder_picked)
    page.overlay.append(folder_picker)

    def show_pick_folder(_: ft.FilePickerResultEvent):
        folder_picker.get_directory_path()

    folder_pick_row = ft.Row(
        controls=[
            ft.ElevatedButton("出力フォルダ", on_click=show_pick_folder),
            ft.Text(ref=output_folder_path),
            ft.Text(
                value="※同名のファイルがあった場合は上書きされます",
                color=ft.colors.BLUE_GREY_400,
            ),
        ]
    )
    ui_rows.append(folder_pick_row)

    ###################################
    # main dictation
    ###################################

    quality_select_row = ft.Row(
        controls=[
            ft.Dropdown(
                ref=quality_selector,
                label="Quality",
                options=[
                    ft.dropdown.Option(key="base", text="base（簡易版）"),
                    ft.dropdown.Option(key="small", text="small（低品質）"),
                    ft.dropdown.Option(key="medium", text="medium（高品質）"),
                    ft.dropdown.Option(key="large", text="large（最高品質）"),
                ],
                value="base",
            ),
            ft.Text(
                value="高品質になるほど処理に時間がかかります。",
                color=ft.colors.BLUE_GREY_400,
            ),
        ]
    )
    ui_rows.append(quality_select_row)

    def dictate():
        out_basename = os.path.splitext(
            os.path.basename(target_file_path.current.value)
        )[0]
        out_path = os.path.join(output_folder_path.current.value, out_basename + ".txt")
        model = whisper.load_model(quality_selector.current.value)
        result = model.transcribe(
            target_file_path.current.value, verbose=True, language="ja"
        )
        lines = []
        for segment in result["segments"]:
            lines.append(segment["text"])
        with open(out_path, mode="w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    ###################################
    # execute button
    ###################################

    def execute_convert(_: ft.FilePickerResultEvent):
        if not target_file_path.current.value or not output_folder_path.current.value:
            return
        message_to_user.current.value = "文字起こし中です。画面を閉じずにお待ちください（高品質以上は数時間かかることがあります）"
        ui_controls.disabled = True
        progress_ring.current.visible = True
        page.update()
        dictate()
        ui_controls.disabled = False
        progress_ring.current.visible = False
        message_to_user.current.value = "文字起こしが完了しました！"
        page.update()

    execute_row = ft.Row(
        controls=[
            ft.FilledButton("文字起こしを実行する", on_click=execute_convert),
            ft.Text(
                ref=message_to_user,
                value="高品質以上は処理に数時間かかることがありますのでご注意ください。",
            ),
            ft.ProgressRing(ref=progress_ring, visible=False),
        ]
    )

    ui_rows.append(execute_row)

    ###################################
    # render page
    ###################################

    ui_rows = [
        ft.Text(
            "github.com/AWtnb/flet-whisper",
            style="labelSmall",
            weight="bold",
            color=ft.colors.BLUE_900,
        )
    ] + ui_rows
    ui_controls = ft.Column(controls=ui_rows)
    page.add(ui_controls)


ft.app(target=main)

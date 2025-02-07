import os
import re
import subprocess
import argparse

def format_filename(filename):
    # ランダムな8桁の数字と括弧()を削除
    new_filename = re.sub(r"\b\d{8}\b", "", filename)
    new_filename = re.sub(r"[\(\)]", "", new_filename).strip(" _-")
    return new_filename if new_filename else filename

def convert_ts_to_mp4(input_folder):
    if not os.path.exists(input_folder):
        print(f"❌ 指定されたフォルダが存在しません: {input_folder}")
        return

    ts_files = [f for f in os.listdir(input_folder) if f.endswith(".ts")]

    if not ts_files:
        print("⚠️ TSファイルが見つかりません。")
        return

    for ts_file in ts_files:
        input_path = os.path.join(input_folder, ts_file)
        base_name = os.path.splitext(ts_file)[0]  # .ts を除去
        formatted_name = format_filename(base_name)  # ファイル名を変換
        output_file = formatted_name + ".mp4"  # .mp4 に変更
        output_path = os.path.join(input_folder, output_file)

        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            output_path
        ]

        print(f"🎬 変換中: {ts_file} → {output_file}")
        try:
            subprocess.run(command, check=True)
            print(f"✅ 変換成功: {output_file}")

            os.remove(input_path)  # 変換後に元の .ts を削除
            print(f"🗑️ {ts_file} を削除しました。")
        except subprocess.CalledProcessError as e:
            print(f"❌ 変換失敗: {ts_file} ({e})")

    print("🎉 すべての変換が完了しました！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="指定フォルダ内の .ts ファイルを .mp4 に変換し、元の .ts を削除するツール")
    parser.add_argument("directory", help="変換する .ts ファイルがあるフォルダを指定してください")
    args = parser.parse_args()

    convert_ts_to_mp4(args.directory)

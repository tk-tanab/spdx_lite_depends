import glob
import lzma
import os
import re
import subprocess
import sys
import tarfile


# debianファイルを展開
def extend_deb(deb_file):
    # 展開先のディレクトリに移動
    os.chdir("./tmp")

    subprocess.run(
        ["ar", "-x", deb_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    # debファイル展開後のオブジェクト一覧を取得
    tar_files = [f for f in os.listdir() if ".tar" in f]

    for tar_file in tar_files:
        # 展開用のディレクトリを作成
        dir_name = tar_file.split(".", 1)[0]
        os.mkdir(dir_name)

        # .tar.zstファイルが展開された場合は，.tarファイルに変更
        tar_name, extension = tar_file.rsplit(".", 1)
        if extension == "zst":
            subprocess.run(
                ["zstd", "-d", tar_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            tar_file = tar_name

        # tarファイルの展開
        try:
            with tarfile.open(tar_file, "r:*") as tar:
                tar.extractall(dir_name)
        except Exception as e:
            print(e)

    # 元のディレクトリに戻る
    os.chdir("..")

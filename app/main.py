import glob
import os
import shutil

import control_to_spdx_json
import extend
import foss_api
import json_to_tv
import merge_json
import tv_to_json

if __name__ == "__main__":
    # ディレクトリを設定
    os.chdir(os.path.dirname(__file__))
    os.chdir("..")

    deb_files = glob.glob("./package_for_analyze/*.deb")

    for deb_file in deb_files:
        os.makedirs("./tmp", exist_ok=True)
        extend.extend_deb("." + deb_file)

        copyright_spdx = "./tmp/copyright.spdx"
        try:
            copyright_file = [
                p
                for p in glob.glob("./tmp/**/copyright", recursive=True)
                if os.path.isfile(p)
            ][0]
            foss_api.foss_api(copyright_file, copyright_spdx)
            copyright_json = tv_to_json.tv_to_json(copyright_spdx)
        except IndexError:
            # copyrightファイルがないとき
            foss_api.foss_api(deb_file, copyright_spdx)
            copyright_json = tv_to_json.tv_to_json(copyright_spdx)

        control_json = "./tmp/control.json"
        control_file = [
            p
            for p in glob.glob("./tmp/**/control", recursive=True)
            if os.path.isfile(p)
        ][0]
        control_to_spdx_json.control_to_spdx_json(control_file, control_json)

        spdx_template_json = "./spdx_template.json"
        file_name = os.path.basename(deb_file)
        user_name = "Taketo"

        spdx_json = merge_json.merge_json(
            copyright_json, control_json, spdx_template_json, file_name, user_name
        )

        json_to_tv.json_to_tv(spdx_json)

        shutil.rmtree("./tmp")

import json
import os


# json形式のSPDXをTagValue形式に変換
def json_to_tv(spdx_json):
    # spdxファイルを読む
    with open(spdx_json, mode='r', encoding='utf-8') as f:
        spdx_dict = json.load(f)

    tv_text = ""

    for info_name, info_list in spdx_dict.items():
        if info_name != "preamble":
            tv_text += "##-------------------------\n"
            tv_text += ("## " + info_name + '\n') 
            tv_text += "##-------------------------\n\n"
        for elem_dict in info_list:
            for tag, value_list in elem_dict.items():
                for value in value_list:
                    tv_text += (tag + ': ' + value + '\n')
            else:
                tv_text += '\n'

    spdx_file = './spdx_generated/' + os.path.splitext(os.path.basename(spdx_json))[0] + '.spdx'
    with open(spdx_file, mode='w') as f:
        f.write(tv_text)

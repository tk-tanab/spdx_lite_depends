import json
import re


def make_tv(lines, json_dict):
    # 初期値
    json_dict["Relationship"] = []
    json_dict["Dependencies"] = []

    # 1行ずつ分解
    for line in lines:
        if line and (not line[0].isspace()) and (": " in line):
            field, value = split_fv(line, lines)
            make_json(field, value, json_dict)


# fieldとvalueに分割する
def split_fv(line, lines):
    field, value = line.split(": ", 1)
    # valueが<text>すなわち複数行にまたがれる形式だった場合
    if field == "Description":
        value = "<text>" + value
        for text in lines[lines.index(line) + 1 :]:
            if text[0].isspace():
                value += "\n"
                value += text
            else:
                break
        value += "</text>"
    return field, value


# controlのfield,valueに対応してSPDXのtag,valueを作成
def make_json(field, value, json_dict):
    if field == "Package":
        json_dict["PackageName"] = [value]
        json_dict["SPDXID"] = ["SPDXRef-" + value]

    elif field == "Version":
        json_dict["PackageVersion"] = [value]

    elif field == "Homepage":
        json_dict["PackageHomePage"] = [value]

    elif field == "Description":
        json_dict["PackageComment"] = [value]

    elif field == "Depends":
        make_dependency_list(value, json_dict, " RUNTIME_DEPENDENCY_OF ")

    elif field == "Suggests":
        make_dependency_list(value, json_dict, " OPTIONAL_DEPENDENCY_OF ")

    elif field == "Pre-Depends":
        make_dependency_list(value, json_dict, " BUILD_DEPENDENCY_OF ")


# 依存関係にあるパッケージ群をリスト化・整形して"Relationship"と"Dependencies"に入力
def make_dependency_list(value, json_dict, relation_name):
    dependencies = [i for i in re.split(",| |[|]|\(.*?\)", value) if i]
    for depend in dependencies:
        json_dict["Relationship"].append(
            "SPDXRef-" + depend + relation_name + json_dict["SPDXID"][0]
        )
    json_dict["Dependencies"] += dependencies


# controlを擬似spdxのjson形式に変換
def control_to_spdx_json(control_file, control_json):
    # controlファイルを読む
    with open(control_file, mode="r", encoding="utf-8") as f:
        line_strip = [s.strip("\n") for s in f.readlines()]

    json_dict = {}

    make_tv(line_strip, json_dict)

    with open(control_json, mode="w", encoding="utf-8") as f:
        json.dump(json_dict, f, indent=4)

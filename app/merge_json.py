import json
import uuid

# spdxファイルの雛形をcopyrightのjsonで埋める
def fill_template(template_dict, copyright_dict):
    for info_name, info_list in template_dict.items():
        if info_list != []:
            for tag in info_list[0].keys():
                if tag in copyright_dict[info_name][0]:
                    info_list[0][tag] = copyright_dict[info_name][0][tag]

    template_dict["License Information"] = copyright_dict["License Information"]
    template_dict["Package Information"][0]["PackageLicenseDeclared"] = copyright_dict["File Information"][0]["LicenseInfoInFile"]
    template_dict["Package Information"][0]["PackageCopyrightText"] = copyright_dict["File Information"][0]["FileCopyrightText"]
    template_dict["Package Information"][0]["PackageLicenseComments"] = [copyright_dict["Package Information"][0]["PackageLicenseComments"][0].replace("licenseInfoInFile", "PackageLicenseDeclared")]
    if len(template_dict["Package Information"][0]["PackageLicenseDeclared"]) == 1:
        template_dict["Package Information"][0]["PackageLicenseConcluded"] = template_dict["Package Information"][0]["PackageLicenseDeclared"]
    else:
        template_dict["Package Information"][0]["PackageLicenseConcluded"] = ["NOASSERTION"]


# spdxファイルにcontrolファイルの情報を結合
def merge_control(spdx_dict, control_dict):
    spdx_dict["Document Information"][0]["DocumentName"] = [control_dict["PackageName"][0] + "_" + control_dict["PackageVersion"][0]]
    spdx_dict["Document Information"][0]["DocumentNamespace"] = ["http://spdx.org/spdxdocs/" + spdx_dict["Document Information"][0]["DocumentName"][0] + '-' + str(uuid.uuid4())]
    spdx_dict["Package Information"][0]["PackageName"] = control_dict["PackageName"]
    spdx_dict["Package Information"][0]["PackageVersion"] = control_dict["PackageVersion"]
    spdx_dict["Package Information"][0]["SPDXID"] = control_dict["SPDXID"]
    spdx_dict["Package Information"][0]["PackageComment"] = control_dict["PackageComment"]

    spdx_dict["Package Information"][1]["Relationship"] = [spdx_dict["Document Information"][0]["SPDXID"][0] + " DESCRIBES " + spdx_dict["Package Information"][0]["SPDXID"][0]]
    spdx_dict["Package Information"][1]["Relationship"] += control_dict["Relationship"]

    for depend in control_dict["Dependencies"]:
        elem_dict = {}
        elem_dict["PackageName"] = [depend]
        elem_dict["SPDXID"] = ["SPDXRef-" + depend]
        elem_dict["PackageDownloadLocation"] = ["NOASSERTION"]
        elem_dict["PackageLicenseConcluded"] = ["NOASSERTION"]
        elem_dict["PackageLicenseDeclared"] = ["NOASSERTION"]
        elem_dict["PackageCopyrightText"] = ["NOASSERTION"]
        elem_dict["FilesAnalyzed"] = ["false"]
        spdx_dict["Dependency Packages Information"].append(elem_dict)

# spdxファイルの微調整
def adjust_spdx(spdx_dict, file_name, user_name):
    spdx_dict["Creation Information"][0]["Creator"] = [
                "Tool: SPDX Lite + dependencies",
                "Tool: FOSSology",
                "Person: " + user_name
            ]
    spdx_dict["Package Information"][0]["PackageFileName"] = [file_name]

# copyrightのjsonとcontrolのjsonをspdxファイルの雛形にそって結合
def merge_json(copyright_json, control_json, spdx_template_json, file_name, user_name):
    # copyrightファイルを読む
    with open(copyright_json, mode='r', encoding='utf-8') as f:
        copyright_dict = json.load(f)

    # controlファイルを読む
    with open(control_json, mode='r', encoding='utf-8') as f:
        control_dict = json.load(f)

    # spdxファイルの雛形を読む
    with open(spdx_template_json, mode='r', encoding='utf-8') as f:
        spdx_dict = json.load(f)

    fill_template(spdx_dict, copyright_dict)
    merge_control(spdx_dict, control_dict)
    adjust_spdx(spdx_dict, file_name, user_name)
    spdx_json = "./tmp/" + file_name + ".json"
    with open(spdx_json, mode='w', encoding='utf-8') as f:
        json.dump(spdx_dict, f, indent=4)
    return spdx_json
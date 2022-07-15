# spdx_lite_depends
## 使い方
SPDXファイルを作成したいDebianパッケージ群をspdx_generatedの下に置き，
`poetry install && poetry run python app/main.py`を実行すると，package_for_analyzeの下に対応するSPDXファイル群が生成される．

## How to use
Place the Debian packages for which you want to create SPDX files under spdx_generated and run main.py under app to generate the corresponding SPDX files under package_for_analyze.

## 環境構築
### VSCode + devcontainer (推奨)
DockerとDocker Composeをインストールしていれば，VSCode経由で開発環境を開くことができます．
詳しくは: https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container

### GitHub Codespaces
[GitHub Codespaces](https://github.co.jp/features/codespaces)に登録していれば，Codespaces経由で開くことができます．

### 自前で設定
- fossologyのコンテナを立てます．　詳しくは: https://github.com/OpenChain-Project/Japan-WG-General/blob/master/Compliance-Tooling/FOSSology/Installation/using_docker_debian_jp.md
- Python 3.10 と Pythonライブラリのpoetry を導入します．
- `poetry install`で必要な依存ライブラリをダウンロードします．

# followcheck
- followcheckのバッチ処理です。
- Twitterからツイートをフェッチしたり、添付されている画像・動画をサーバーのDISKにキャッシュしたりします。

# バッチ処理の内容
- fc_compress_media.sh
    - 画像ファイルの品質を落としてファイルサイズを減らすバッチ処理。
- fc_create_remlist.sh
    - リムられリストを作成するバッチ処理。
    - フォローをリムーブしたユーザーを検出します。
- fc_create_thumbs.sh
    - キャッシュした画像と動画から、画面表示用のサムネイル画像を作成するバッチ処理。
- fc_delete_checked_tweets.sh
    - 既読したツイートを削除するバッチ処理。
- fc_delete_olddata.sh
    - 一時期使っていたデータお掃除ツール。
- fc_download_medias.sh
    - ツイートに添付されている画像・動画をサーバーにキャッシュするバッチ処理。
- fc_update_tweets.sh
    - ツイートをフェッチするバッチ処理。
- fc_download_tweets.sh
    - ツイートをフェッチするバッチ処理。（初回フェッチ用）
- fc_exists_media_file.sh
    - 不具合により誤削除してしまった画像・動画を再キャッシュするバッチ処理。
- fc_repair_users.sh
    - ユーザ情報を修復するバッチ処理。
- fc_update_reluser.sh
    - データベースに登録されているTwitterアカウントの情報を最新にするバッチ処理。

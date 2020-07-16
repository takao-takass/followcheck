-- --------------------------------------------------------
-- ホスト:                          192.168.1.6
-- サーバーのバージョン:                   8.0.19 - MySQL Community Server - GPL
-- サーバー OS:                      Linux
-- HeidiSQL バージョン:               10.3.0.5771
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- followcheck のデータベース構造をダンプしています
CREATE DATABASE IF NOT EXISTS `followcheck` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `followcheck`;

--  テーブル followcheck.code の構造をダンプしています
CREATE TABLE IF NOT EXISTS `code` (
  `type` varchar(30) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'コードの種類',
  `value` varchar(250) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'コードの値',
  `used_count` int unsigned NOT NULL DEFAULT '0' COMMENT '使用回数',
  `disabled` tinyint unsigned NOT NULL DEFAULT '0' COMMENT '使用不可',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '削除',
  PRIMARY KEY (`type`,`value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招待コードなどのパスワード以外の認証に用いるコードを管理する。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.exec_id_manage の構造をダンプしています
CREATE TABLE IF NOT EXISTS `exec_id_manage` (
  `exec_id` varchar(14) COLLATE utf8mb4_general_ci NOT NULL COMMENT '実行ID',
  `exec_count` int unsigned NOT NULL COMMENT '実行回数（n回目）',
  `create_datetime` datetime NOT NULL COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='実行IDを管理する。\r\n前回実行した時の実行IDを特定するために用いる。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.followers の構造をダンプしています
CREATE TABLE IF NOT EXISTS `followers` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `exec_id` varchar(14) COLLATE utf8mb4_general_ci NOT NULL COMMENT '実行ID',
  `follower_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォロワーユーザID',
  `create_datetime` datetime NOT NULL COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`exec_id`,`follower_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='フォロワーのユーザを利用者ごとに管理する。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.follow_eachother の構造をダンプしています
CREATE TABLE IF NOT EXISTS `follow_eachother` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `follow_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォローユーザID',
  `undisplayed` tinyint NOT NULL DEFAULT '0' COMMENT '非表示',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`follow_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='相互フォローのユーザ\r\n';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.friends の構造をダンプしています
CREATE TABLE IF NOT EXISTS `friends` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `exec_id` varchar(14) COLLATE utf8mb4_general_ci NOT NULL COMMENT '実行ID',
  `follow_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォロワーユーザID',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`exec_id`,`follow_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='フォローしているユーザのリストを利用者ごとに管理する。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.groups の構造をダンプしています
CREATE TABLE IF NOT EXISTS `groups` (
  `group_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'グループID',
  `service_user_id` varchar(12) COLLATE utf8mb4_general_ci NOT NULL COMMENT '利用者ID',
  `group_name` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterのアカウントID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` smallint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='グループを管理する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.group_users の構造をダンプしています
CREATE TABLE IF NOT EXISTS `group_users` (
  `group_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'グループID',
  `user_id` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterユーザID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` smallint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`group_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='グループに属するTwitterユーザを管理する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.hashtags の構造をダンプしています
CREATE TABLE IF NOT EXISTS `hashtags` (
  `hashtag_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'タグID',
  `tagtext` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'テキスト',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='これまでに検出したハッシュタグを登録する。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.profile_icons の構造をダンプしています
CREATE TABLE IF NOT EXISTS `profile_icons` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterのユーザID',
  `sequence` int NOT NULL DEFAULT '0' COMMENT '同一ユーザID内の連番',
  `url` varchar(150) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'アイコン画像のURL',
  `directory_path` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '画像ファイルのディレクトリ',
  `file_name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '画像ファイルの名前',
  `completed` tinyint NOT NULL DEFAULT '0' COMMENT '0:未完了、1:完了',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Twitterアカウントのプロフィールアイコン';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.queue_create_thumbs の構造をダンプしています
CREATE TABLE IF NOT EXISTS `queue_create_thumbs` (
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='サムネイル作成処理の待ち行列';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.relational_users の構造をダンプしています
CREATE TABLE IF NOT EXISTS `relational_users` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `disp_name` varchar(80) COLLATE utf8mb4_general_ci NOT NULL COMMENT '画面表示名',
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT '名前',
  `thumbnail_url` varchar(150) COLLATE utf8mb4_general_ci DEFAULT '' COMMENT 'サムネイル画像URL',
  `description` varchar(300) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '紹介文',
  `theme_color` varchar(6) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'テーマカラー',
  `follow_count` int unsigned NOT NULL DEFAULT '0' COMMENT 'フォロー数',
  `follower_count` int unsigned NOT NULL DEFAULT '0' COMMENT 'フォロワー数',
  `icecream` tinyint NOT NULL DEFAULT '0' COMMENT '1：凍結・削除されたアカウント」',
  `icecream_datetime` datetime DEFAULT NULL COMMENT '凍結された日時',
  `verify_datetime` datetime DEFAULT NULL COMMENT '凍結チェックをした日時',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='フォローまたはフォロワーの最新のユーザ情報を管理する。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.remove_users の構造をダンプしています
CREATE TABLE IF NOT EXISTS `remove_users` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `remove_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'リムーブされたユーザID',
  `day_old` int unsigned NOT NULL DEFAULT '0' COMMENT '経過日数',
  `followed` tinyint NOT NULL DEFAULT '0' COMMENT 'フォローしている(1:YES 0:NO)',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`remove_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='リムーブされたユーザのリストを利用者ごとに管理する。\r\n再フォローされたときは論理削除される。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.sequences の構造をダンプしています
CREATE TABLE IF NOT EXISTS `sequences` (
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'シーケンス名',
  `value` bigint NOT NULL DEFAULT '0' COMMENT '値',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='連番を管理する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.service_users の構造をダンプしています
CREATE TABLE IF NOT EXISTS `service_users` (
  `service_user_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT '利用者名',
  `mailaddress` varchar(100) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='このアプリケーションを使用するユーザ（利用者）を管理する。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.threads の構造をダンプしています
CREATE TABLE IF NOT EXISTS `threads` (
  `prosess_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '処理名称(バッチファイル名)',
  `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'スレッドID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`prosess_name`,`thread_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='バッチ処理のスレッドを登録する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.token の構造をダンプしています
CREATE TABLE IF NOT EXISTS `token` (
  `sign` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ipaddress` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `expire_datetime` datetime DEFAULT NULL,
  `create_datetime` datetime DEFAULT NULL,
  `update_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`sign`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='トークン';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.tweets の構造をダンプしています
CREATE TABLE IF NOT EXISTS `tweets` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterユーザID',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `tweet_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートしたユーザのID',
  `body` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '本文',
  `tweeted_datetime` datetime NOT NULL COMMENT 'ツイート日時',
  `favolite_count` int unsigned NOT NULL DEFAULT '0' COMMENT 'お気に入り数',
  `retweet_count` int unsigned NOT NULL DEFAULT '0' COMMENT 'リツイート数',
  `replied` tinyint NOT NULL DEFAULT '0' COMMENT 'リプライしたツイート',
  `retweeted` tinyint NOT NULL DEFAULT '0' COMMENT 'リツイートされたツイート',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.tweet_hashtags の構造をダンプしています
CREATE TABLE IF NOT EXISTS `tweet_hashtags` (
  `tweet_id` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `hashtag_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'タグID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`tweet_id`,`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='ツイートとハッシュタグを紐づける。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.tweet_medias の構造をダンプしています
CREATE TABLE IF NOT EXISTS `tweet_medias` (
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
  `type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアタイプ',
  `sizes` varchar(30) COLLATE utf8mb4_general_ci NOT NULL COMMENT '対応サイズ',
  `bitrate` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '動画ビットレート',
  `file_name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ファイル名',
  `directory_path` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ディレクトリパス',
  `thumb_file_name` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'サムネイルファイル名',
  `thumb_directory_path` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'サムネイルディレクトリパス',
  `download_error` tinyint NOT NULL DEFAULT '0' COMMENT 'ダウンロードエラー有無',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.tweet_take_users の構造をダンプしています
CREATE TABLE IF NOT EXISTS `tweet_take_users` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterユーザID',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '状態',
  `taked_datetime` datetime DEFAULT NULL COMMENT '取得完了日時',
  `continue_tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '取得継続に使うツイートID',
  `include_retweet` tinyint NOT NULL DEFAULT '1' COMMENT 'リツイートもダウンロードする',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全てのツイートを取得するユーザを管理する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.tweet_urls の構造をダンプしています
CREATE TABLE IF NOT EXISTS `tweet_urls` (
  `tweet_id` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(200) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'URL',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='ツイートされたURLを登録する';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.unfollowbacked の構造をダンプしています
CREATE TABLE IF NOT EXISTS `unfollowbacked` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `unfollowbacked_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォロバ待ちユーザID',
  `day_old` int unsigned NOT NULL DEFAULT '0' COMMENT '経過日数',
  `undisplayed` tinyint NOT NULL DEFAULT '0' COMMENT '非表示',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`unfollowbacked_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='フォロバ待ちユーザのリストを利用者ごとに管理する。\r\n相互フォローになった場合は削除される。';

-- エクスポートするデータが選択されていません

--  テーブル followcheck.users_accounts の構造をダンプしています
CREATE TABLE IF NOT EXISTS `users_accounts` (
  `service_user_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID(Twitter)',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='利用者のTwitterアカウントを登録する';

-- エクスポートするデータが選択されていません

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

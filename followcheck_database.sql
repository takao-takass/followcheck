CREATE DATABASE `followcheck` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;


-- followcheck.code definition

CREATE TABLE `code` (
  `type` varchar(30) NOT NULL COMMENT 'コードの種類',
  `value` varchar(250) NOT NULL COMMENT 'コードの値',
  `used_count` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '使用回数',
  `disabled` tinyint(3) unsigned NOT NULL DEFAULT 0 COMMENT '使用不可',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '削除',
  PRIMARY KEY (`type`,`value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='招待コードなどのパスワード以外の認証に用いるコードを管理する。';


-- followcheck.exec_id_manage definition

CREATE TABLE `exec_id_manage` (
  `exec_id` varchar(14) NOT NULL COMMENT '実行ID',
  `exec_count` int(10) unsigned NOT NULL COMMENT '実行回数（n回目）',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='実行IDを管理する。\r\n前回実行した時の実行IDを特定するために用いる。';


-- followcheck.follow_eachother definition

CREATE TABLE `follow_eachother` (
  `user_id` varchar(70) NOT NULL COMMENT 'ユーザID',
  `follow_user_id` varchar(70) NOT NULL COMMENT 'フォローユーザID',
  `undisplayed` tinyint(4) NOT NULL DEFAULT 0 COMMENT '非表示',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`follow_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='相互フォローのユーザ\r\n';


-- followcheck.followers definition

CREATE TABLE `followers` (
  `user_id` varchar(70) NOT NULL COMMENT 'ユーザID',
  `exec_id` varchar(14) NOT NULL COMMENT '実行ID',
  `follower_user_id` varchar(70) NOT NULL COMMENT 'フォロワーユーザID',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`exec_id`,`follower_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='フォロワーのユーザを利用者ごとに管理する。';


-- followcheck.friends definition

CREATE TABLE `friends` (
  `user_id` varchar(70) NOT NULL COMMENT 'ユーザID',
  `exec_id` varchar(14) NOT NULL COMMENT '実行ID',
  `follow_user_id` varchar(70) NOT NULL COMMENT 'フォロワーユーザID',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`exec_id`,`follow_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='フォローしているユーザのリストを利用者ごとに管理する。';


-- followcheck.matching_directories definition

CREATE TABLE `matching_directories` (
  `directory` varchar(200) NOT NULL,
  PRIMARY KEY (`directory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- followcheck.profile_icons definition

CREATE TABLE `profile_icons` (
  `user_id` varchar(70) NOT NULL COMMENT 'TwitterのユーザID',
  `sequence` int(11) NOT NULL DEFAULT 0 COMMENT '同一ユーザID内の連番',
  `url` varchar(150) NOT NULL COMMENT 'アイコン画像のURL',
  `directory_path` varchar(100) DEFAULT NULL COMMENT '画像ファイルのディレクトリ',
  `file_name` varchar(100) DEFAULT NULL COMMENT '画像ファイルの名前',
  `completed` tinyint(4) NOT NULL DEFAULT 0 COMMENT '0:未完了、1:完了',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`sequence`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Twitterアカウントのプロフィールアイコン';


-- followcheck.relational_users definition

CREATE TABLE `relational_users` (
  `user_id` varchar(70) NOT NULL COMMENT 'ユーザID',
  `disp_name` varchar(80) NOT NULL COMMENT '画面表示名',
  `name` varchar(50) NOT NULL COMMENT '名前',
  `thumbnail_url` varchar(150) DEFAULT '' COMMENT 'サムネイル画像URL',
  `description` varchar(300) DEFAULT NULL COMMENT '紹介文',
  `theme_color` varchar(6) DEFAULT NULL COMMENT 'テーマカラー',
  `follow_count` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'フォロー数',
  `follower_count` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'フォロワー数',
  `location` varchar(100) DEFAULT NULL,
  `icecream` tinyint(4) NOT NULL DEFAULT 0 COMMENT '1：凍結・削除されたアカウント」',
  `icecream_datetime` datetime DEFAULT NULL COMMENT '凍結された日時',
  `not_found` tinyint(4) NOT NULL DEFAULT 0,
  `protected` tinyint(4) NOT NULL DEFAULT 0 COMMENT '鍵垢',
  `verify_datetime` datetime DEFAULT NULL COMMENT '凍結チェックをした日時',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='フォローまたはフォロワーの最新のユーザ情報を管理する。';


-- followcheck.remove_users definition

CREATE TABLE `remove_users` (
  `user_id` varchar(70) NOT NULL COMMENT 'ユーザID',
  `remove_user_id` varchar(70) NOT NULL COMMENT 'リムーブされたユーザID',
  `day_old` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '経過日数',
  `followed` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'フォローしている(1:YES 0:NO)',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`remove_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='リムーブされたユーザのリストを利用者ごとに管理する。\r\n再フォローされたときは論理削除される。';


-- followcheck.sequences definition

CREATE TABLE `sequences` (
  `name` varchar(50) NOT NULL COMMENT 'シーケンス名',
  `value` bigint(20) NOT NULL DEFAULT 0 COMMENT '値',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '1：削除を示す'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='連番を管理する';


-- followcheck.service_users definition

CREATE TABLE `service_users` (
  `service_user_id` varchar(10) NOT NULL COMMENT 'サービス利用者ID',
  `name` varchar(50) NOT NULL COMMENT '利用者名',
  `mailaddress` varchar(100) NOT NULL DEFAULT '0',
  `password` varchar(255) NOT NULL DEFAULT '',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='このアプリケーションを使用するユーザ（利用者）を管理する。';


-- followcheck.threads definition

CREATE TABLE `threads` (
  `prosess_name` varchar(50) NOT NULL COMMENT '処理名称(バッチファイル名)',
  `thread_id` varchar(30) NOT NULL COMMENT 'スレッドID',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  PRIMARY KEY (`prosess_name`,`thread_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='バッチ処理のスレッドを登録する';


-- followcheck.token definition

CREATE TABLE `token` (
  `sign` varchar(255) NOT NULL,
  `service_user_id` varchar(10) DEFAULT NULL,
  `ipaddress` varchar(40) DEFAULT NULL,
  `expire_datetime` datetime DEFAULT NULL,
  `create_datetime` datetime DEFAULT current_timestamp(),
  `update_datetime` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`sign`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='トークン';


-- followcheck.tweet_take_users definition

CREATE TABLE `tweet_take_users` (
  `service_user_id` varchar(10) NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) NOT NULL COMMENT 'TwitterユーザID',
  `status` varchar(1) NOT NULL DEFAULT '0' COMMENT '状態',
  `taked_datetime` datetime DEFAULT NULL COMMENT '取得完了日時',
  `continue_tweet_id` varchar(50) DEFAULT NULL COMMENT '取得継続に使うツイートID',
  `include_retweet` tinyint(4) NOT NULL DEFAULT 1 COMMENT 'リツイートもダウンロードする',
  `not_tweeted_longtime` tinyint(4) NOT NULL DEFAULT 0 COMMENT '長期間ツイートしていないユーザ',
  `high_priority` tinyint(1) NOT NULL DEFAULT 0,
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  `show_kept` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`service_user_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='全てのツイートを取得するユーザを管理する';


-- followcheck.unfollowbacked definition

CREATE TABLE `unfollowbacked` (
  `user_id` varchar(70) NOT NULL COMMENT 'ユーザID',
  `unfollowbacked_user_id` varchar(70) NOT NULL COMMENT 'フォロバ待ちユーザID',
  `day_old` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '経過日数',
  `undisplayed` tinyint(4) NOT NULL DEFAULT 0 COMMENT '非表示',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`unfollowbacked_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='フォロバ待ちユーザのリストを利用者ごとに管理する。\r\n相互フォローになった場合は削除される。';


-- followcheck.user_config definition

CREATE TABLE `user_config` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `config_id` int(11) NOT NULL,
  `value` int(11) DEFAULT NULL,
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `user_config_service_user_id_IDX` (`service_user_id`,`config_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;


-- followcheck.users_accounts definition

CREATE TABLE `users_accounts` (
  `service_user_id` varchar(10) NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) NOT NULL COMMENT 'ユーザID(Twitter)',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='利用者のTwitterアカウントを登録する';


-- followcheck.shown_tweets definition

CREATE TABLE `shown_tweets` (
  `sign` varchar(255) NOT NULL,
  `user_id` varchar(70) NOT NULL COMMENT 'TwitterユーザID',
  `tweet_id` varchar(100) NOT NULL,
  `tweeted_datetime` datetime NOT NULL,
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`sign`,`user_id`,`tweet_id`),
  KEY `shown_tweets_sign_IDX` (`sign`,`tweet_id`) USING BTREE,
  CONSTRAINT `shown_tweets_FK` FOREIGN KEY (`sign`) REFERENCES `token` (`sign`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- followcheck.tweets definition

CREATE TABLE `tweets` (
  `service_user_id` varchar(10) NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) NOT NULL COMMENT 'TwitterユーザID',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `tweet_user_id` varchar(70) NOT NULL COMMENT 'ツイートしたユーザのID',
  `body` varchar(1000) DEFAULT NULL COMMENT '本文',
  `arranged_body` varchar(200) DEFAULT NULL COMMENT '整形本文',
  `tweeted_datetime` datetime NOT NULL COMMENT 'ツイート日時',
  `favolite_count` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'お気に入り数',
  `retweet_count` int(10) unsigned NOT NULL DEFAULT 0 COMMENT 'リツイート数',
  `replied` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'リプライしたツイート',
  `retweeted` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'リツイートされたツイート',
  `is_media` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'メディアが添付されている',
  `media_ready` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'メディアを表示する準備が出来ている',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  `kept` bit(1) NOT NULL DEFAULT b'0',
  `shown` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`),
  KEY `user_id` (`user_id`),
  KEY `tweets_service_user_id_IDX` (`service_user_id`,`tweet_id`) USING BTREE,
  KEY `tweets_tweeted_datetime_IDX` (`tweeted_datetime`) USING BTREE,
  CONSTRAINT `tweets_FK` FOREIGN KEY (`service_user_id`, `user_id`) REFERENCES `tweet_take_users` (`service_user_id`, `user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';


-- followcheck.existing_media_thumbs definition

CREATE TABLE `existing_media_thumbs` (
  `service_user_id` varchar(10) NOT NULL DEFAULT '0',
  `user_id` varchar(70) NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) NOT NULL COMMENT 'メディアURL',
  `type` varchar(30) NOT NULL COMMENT 'メディアタイプ',
  `sizes` varchar(30) NOT NULL COMMENT '対応サイズ',
  `bitrate` varchar(15) DEFAULT NULL COMMENT '動画ビットレート',
  `file_name` varchar(100) DEFAULT NULL COMMENT 'ファイル名',
  `directory_path` varchar(100) DEFAULT NULL COMMENT 'ディレクトリパス',
  `thumb_file_name` varchar(100) DEFAULT NULL COMMENT 'サムネイルファイル名',
  `thumb_directory_path` varchar(100) DEFAULT NULL COMMENT 'サムネイルディレクトリパス',
  `download_error` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'ダウンロードエラー有無',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  KEY `tweet_id` (`tweet_id`),
  CONSTRAINT `existing_media_thumbs_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`) REFERENCES `tweets` (`service_user_id`, `user_id`, `tweet_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';


-- followcheck.existing_tweet_medias definition

CREATE TABLE `existing_tweet_medias` (
  `service_user_id` varchar(10) NOT NULL DEFAULT '0',
  `user_id` varchar(70) NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) NOT NULL COMMENT 'メディアURL',
  `type` varchar(30) NOT NULL COMMENT 'メディアタイプ',
  `sizes` varchar(30) NOT NULL COMMENT '対応サイズ',
  `bitrate` varchar(15) DEFAULT NULL COMMENT '動画ビットレート',
  `file_name` varchar(100) DEFAULT NULL COMMENT 'ファイル名',
  `directory_path` varchar(100) DEFAULT NULL COMMENT 'ディレクトリパス',
  `thumb_file_name` varchar(100) DEFAULT NULL COMMENT 'サムネイルファイル名',
  `thumb_directory_path` varchar(100) DEFAULT NULL COMMENT 'サムネイルディレクトリパス',
  `download_error` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'ダウンロードエラー有無',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  KEY `tweet_id` (`tweet_id`),
  CONSTRAINT `existing_tweet_medias_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`) REFERENCES `tweets` (`service_user_id`, `user_id`, `tweet_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';


-- followcheck.tweet_medias definition

CREATE TABLE `tweet_medias` (
  `service_user_id` varchar(10) NOT NULL DEFAULT '0',
  `user_id` varchar(70) NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) NOT NULL COMMENT 'メディアURL',
  `type` varchar(30) NOT NULL COMMENT 'メディアタイプ',
  `sizes` varchar(30) NOT NULL COMMENT '対応サイズ',
  `bitrate` varchar(15) DEFAULT NULL COMMENT '動画ビットレート',
  `file_name` varchar(100) DEFAULT NULL COMMENT 'ファイル名',
  `directory_path` varchar(100) DEFAULT NULL COMMENT 'ディレクトリパス',
  `file_size` int(11) NOT NULL DEFAULT 0,
  `thumb_file_name` varchar(100) DEFAULT NULL COMMENT 'サムネイルファイル名',
  `thumb_directory_path` varchar(100) DEFAULT NULL COMMENT 'サムネイルディレクトリパス',
  `thumb_file_size` int(11) NOT NULL DEFAULT 0,
  `download_error` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'ダウンロードエラー有無',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  KEY `tweet_id` (`tweet_id`),
  CONSTRAINT `tweet_medias_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`) REFERENCES `tweets` (`service_user_id`, `user_id`, `tweet_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';


-- followcheck.losted_tweet_medias definition

CREATE TABLE `losted_tweet_medias` (
  `service_user_id` varchar(10) NOT NULL DEFAULT '0',
  `user_id` varchar(70) NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) NOT NULL COMMENT 'メディアURL',
  `type` varchar(30) NOT NULL COMMENT 'メディアタイプ',
  `sizes` varchar(30) NOT NULL COMMENT '対応サイズ',
  `bitrate` varchar(15) DEFAULT NULL COMMENT '動画ビットレート',
  `file_name` varchar(100) DEFAULT NULL COMMENT 'ファイル名',
  `directory_path` varchar(100) DEFAULT NULL COMMENT 'ディレクトリパス',
  `thumb_file_name` varchar(100) DEFAULT NULL COMMENT 'サムネイルファイル名',
  `thumb_directory_path` varchar(100) DEFAULT NULL COMMENT 'サムネイルディレクトリパス',
  `download_error` tinyint(4) NOT NULL DEFAULT 0 COMMENT 'ダウンロードエラー有無',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL COMMENT '更新日時',
  `deleted` tinyint(4) NOT NULL DEFAULT 0 COMMENT '論理削除',
  `losted_datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `download_entried` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  KEY `tweet_id` (`tweet_id`),
  CONSTRAINT `losted_tweet_medias_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`, `url`) REFERENCES `tweet_medias` (`service_user_id`, `user_id`, `tweet_id`, `url`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;


-- followcheck.queue_compress_medias definition

CREATE TABLE `queue_compress_medias` (
  `service_user_id` varchar(10) NOT NULL DEFAULT '0',
  `user_id` varchar(70) NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) NOT NULL COMMENT 'メディアURL',
  `status` varchar(1) NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `error_text` text DEFAULT NULL COMMENT 'エラーテキスト',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  CONSTRAINT `queue_compress_medias_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`, `url`) REFERENCES `tweet_medias` (`service_user_id`, `user_id`, `tweet_id`, `url`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='メディア圧縮処理の待ち行列';


-- followcheck.queue_create_thumbs definition

CREATE TABLE `queue_create_thumbs` (
  `service_user_id` varchar(10) NOT NULL DEFAULT '0',
  `user_id` varchar(70) NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) NOT NULL COMMENT 'メディアURL',
  `status` varchar(1) NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `error_text` text DEFAULT NULL COMMENT 'エラーテキスト',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  CONSTRAINT `queue_create_thumbs_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`, `url`) REFERENCES `tweet_medias` (`service_user_id`, `user_id`, `tweet_id`, `url`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='サムネイル作成処理の待ち行列';


-- followcheck.queue_download_medias definition

CREATE TABLE `queue_download_medias` (
  `service_user_id` varchar(10) NOT NULL DEFAULT '0',
  `user_id` varchar(70) NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) NOT NULL COMMENT 'メディアURL',
  `status` varchar(1) NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `error_text` text DEFAULT NULL COMMENT 'エラーテキスト',
  `create_datetime` datetime NOT NULL DEFAULT current_timestamp() COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新日時',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  CONSTRAINT `queue_download_medias_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`, `url`) REFERENCES `tweet_medias` (`service_user_id`, `user_id`, `tweet_id`, `url`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
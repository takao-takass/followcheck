CREATE TABLE `tweet_medias` (
  `service_user_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
  `type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアタイプ',
  `sizes` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '対応サイズ',
  `bitrate` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '動画ビットレート',
  `file_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ファイル名',
  `directory_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ディレクトリパス',
  `thumb_file_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'サムネイルファイル名',
  `thumb_directory_path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'サムネイルディレクトリパス',
  `download_error` tinyint NOT NULL DEFAULT '0' COMMENT 'ダウンロードエラー有無',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`,`url`),
  KEY `tweet_id` (`tweet_id`),
  CONSTRAINT `tweet_medias_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`) REFERENCES `tweets` (`service_user_id`, `user_id`, `tweet_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する'
;
CREATE TABLE `delete_tweets` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterユーザID',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`),
  KEY `delete_tweets_FK` (`service_user_id`,`user_id`,`tweet_id`),
  CONSTRAINT `delete_tweets_FK` FOREIGN KEY (`service_user_id`, `user_id`, `tweet_id`) REFERENCES `tweets` (`service_user_id`, `user_id`, `tweet_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='既読のツイートを登録する'
;
ALTER TABLE followcheck_dev.tweet_medias ADD CONSTRAINT tweet_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id) REFERENCES followcheck_dev.tweets(service_user_id,user_id,tweet_id) ON DELETE CASCADE
;
ALTER TABLE followcheck_dev.losted_tweet_medias ADD CONSTRAINT losted_tweet_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck_dev.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck_dev.queue_compress_medias ADD CONSTRAINT queue_compress_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck_dev.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck_dev.queue_create_thumbs ADD CONSTRAINT queue_create_thumbs_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck_dev.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck_dev.queue_download_medias ADD CONSTRAINT queue_download_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck_dev.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck_dev.tweets ADD CONSTRAINT tweets_FK FOREIGN KEY (service_user_id,user_id) REFERENCES followcheck_dev.tweet_take_users(service_user_id,user_id) ON DELETE CASCADE
;
DROP TABLE followcheck_dev.deletable_tweets
;
DROP TABLE followcheck_dev.queue_delete_tweets
;
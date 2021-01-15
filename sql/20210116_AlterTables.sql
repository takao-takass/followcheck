CREATE TABLE `shown_tweets` (
  `sign` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `tweet_id` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`sign`,`tweet_id`),
  CONSTRAINT `shown_tweets_FK` FOREIGN KEY (`sign`) REFERENCES `token` (`sign`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
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
ALTER TABLE followcheck.tweet_medias ADD CONSTRAINT tweet_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id) REFERENCES followcheck.tweets(service_user_id,user_id,tweet_id) ON DELETE CASCADE
;
ALTER TABLE followcheck.losted_tweet_medias ADD CONSTRAINT losted_tweet_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck.queue_compress_medias ADD CONSTRAINT queue_compress_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck.queue_create_thumbs ADD CONSTRAINT queue_create_thumbs_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck.queue_download_medias ADD CONSTRAINT queue_download_medias_FK FOREIGN KEY (service_user_id,user_id,tweet_id,url) REFERENCES followcheck.tweet_medias(service_user_id,user_id,tweet_id,url) ON DELETE CASCADE
;
ALTER TABLE followcheck.tweets ADD CONSTRAINT tweets_FK FOREIGN KEY (service_user_id,user_id) REFERENCES followcheck.tweet_take_users(service_user_id,user_id) ON DELETE CASCADE
;
DROP TABLE followcheck.deletable_tweets
;
DROP TABLE followcheck.queue_delete_tweets
;
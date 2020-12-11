-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 192.168.1.6    Database: followcheck
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Keywords`
--

DROP TABLE IF EXISTS `Keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Keywords` (
  `id` int NOT NULL,
  `create_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `checked_tweets`
--

DROP TABLE IF EXISTS `checked_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `checked_tweets` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`service_user_id`,`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='既読のツイートを登録する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `code`
--

DROP TABLE IF EXISTS `code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `code` (
  `type` varchar(30) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'コードの種類',
  `value` varchar(250) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'コードの値',
  `used_count` int unsigned NOT NULL DEFAULT '0' COMMENT '使用回数',
  `disabled` tinyint unsigned NOT NULL DEFAULT '0' COMMENT '使用不可',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '削除',
  PRIMARY KEY (`type`,`value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='招待コードなどのパスワード以外の認証に用いるコードを管理する。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deletable_tweets`
--

DROP TABLE IF EXISTS `deletable_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deletable_tweets` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  PRIMARY KEY (`service_user_id`,`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `exec_id_manage`
--

DROP TABLE IF EXISTS `exec_id_manage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exec_id_manage` (
  `exec_id` varchar(14) COLLATE utf8mb4_general_ci NOT NULL COMMENT '実行ID',
  `exec_count` int unsigned NOT NULL COMMENT '実行回数（n回目）',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='実行IDを管理する。\r\n前回実行した時の実行IDを特定するために用いる。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `follow_eachother`
--

DROP TABLE IF EXISTS `follow_eachother`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow_eachother` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `follow_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォローユーザID',
  `undisplayed` tinyint NOT NULL DEFAULT '0' COMMENT '非表示',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`follow_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='相互フォローのユーザ\r\n';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `followers` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `exec_id` varchar(14) COLLATE utf8mb4_general_ci NOT NULL COMMENT '実行ID',
  `follower_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォロワーユーザID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`exec_id`,`follower_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='フォロワーのユーザを利用者ごとに管理する。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `friends`
--

DROP TABLE IF EXISTS `friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friends` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `exec_id` varchar(14) COLLATE utf8mb4_general_ci NOT NULL COMMENT '実行ID',
  `follow_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォロワーユーザID',
  `create_datetime` datetime NOT NULL COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`exec_id`,`follow_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='フォローしているユーザのリストを利用者ごとに管理する。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_users`
--

DROP TABLE IF EXISTS `group_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_users` (
  `group_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'グループID',
  `user_id` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterユーザID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` smallint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`group_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='グループに属するTwitterユーザを管理する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `group_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'グループID',
  `service_user_id` varchar(12) COLLATE utf8mb4_general_ci NOT NULL COMMENT '利用者ID',
  `group_name` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterのアカウントID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` smallint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='グループを管理する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hashtags`
--

DROP TABLE IF EXISTS `hashtags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hashtags` (
  `hashtag_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'タグID',
  `tagtext` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'テキスト',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='これまでに検出したハッシュタグを登録する。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `keep_tweets`
--

DROP TABLE IF EXISTS `keep_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keep_tweets` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`service_user_id`,`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='キープされたツイート';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profile_icons`
--

DROP TABLE IF EXISTS `profile_icons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profile_icons` (
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `queue_compress_medias`
--

DROP TABLE IF EXISTS `queue_compress_medias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `queue_compress_medias` (
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `error_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'エラーテキスト',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='メディア圧縮処理の待ち行列';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `queue_create_thumbs`
--

DROP TABLE IF EXISTS `queue_create_thumbs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `queue_create_thumbs` (
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `error_text` text COLLATE utf8mb4_general_ci COMMENT 'エラーテキスト',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='サムネイル作成処理の待ち行列';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `queue_delete_tweets`
--

DROP TABLE IF EXISTS `queue_delete_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `queue_delete_tweets` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `tweeted_datetime` datetime NOT NULL COMMENT 'ツイートが投稿された日時',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `error_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'エラーテキスト',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`),
  KEY `thread_id` (`thread_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='ツイート削除処理のキュー';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `queue_download_medias`
--

DROP TABLE IF EXISTS `queue_download_medias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `queue_download_medias` (
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
  `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '処理を担当しているスレッドID',
  `error_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'エラーテキスト',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `relational_users`
--

DROP TABLE IF EXISTS `relational_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `relational_users` (
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `remove_users`
--

DROP TABLE IF EXISTS `remove_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `remove_users` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `remove_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'リムーブされたユーザID',
  `day_old` int unsigned NOT NULL DEFAULT '0' COMMENT '経過日数',
  `followed` tinyint NOT NULL DEFAULT '0' COMMENT 'フォローしている(1:YES 0:NO)',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`remove_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='リムーブされたユーザのリストを利用者ごとに管理する。\r\n再フォローされたときは論理削除される。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sequences`
--

DROP TABLE IF EXISTS `sequences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sequences` (
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'シーケンス名',
  `value` bigint NOT NULL DEFAULT '0' COMMENT '値',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='連番を管理する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `service_users`
--

DROP TABLE IF EXISTS `service_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `service_users` (
  `service_user_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT '利用者名',
  `mailaddress` varchar(100) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0',
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='このアプリケーションを使用するユーザ（利用者）を管理する。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `threads`
--

DROP TABLE IF EXISTS `threads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `threads` (
  `prosess_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '処理名称(バッチファイル名)',
  `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'スレッドID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`prosess_name`,`thread_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='バッチ処理のスレッドを登録する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token` (
  `sign` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ipaddress` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `expire_datetime` datetime DEFAULT NULL,
  `create_datetime` datetime DEFAULT NULL,
  `update_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`sign`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='トークン';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweet_hashtags`
--

DROP TABLE IF EXISTS `tweet_hashtags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_hashtags` (
  `tweet_id` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `hashtag_id` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'タグID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`tweet_id`,`hashtag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='ツイートとハッシュタグを紐づける。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweet_medias`
--

DROP TABLE IF EXISTS `tweet_medias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_medias` (
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
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`tweet_id`,`url`),
  KEY `tweet_id` (`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweet_medias_cp`
--

DROP TABLE IF EXISTS `tweet_medias_cp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_medias_cp` (
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
  `message` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweet_take_users`
--

DROP TABLE IF EXISTS `tweet_take_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_take_users` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterユーザID',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '状態',
  `taked_datetime` datetime DEFAULT NULL COMMENT '取得完了日時',
  `continue_tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '取得継続に使うツイートID',
  `include_retweet` tinyint NOT NULL DEFAULT '1' COMMENT 'リツイートもダウンロードする',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='全てのツイートを取得するユーザを管理する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweet_urls`
--

DROP TABLE IF EXISTS `tweet_urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_urls` (
  `tweet_id` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `url` varchar(200) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'URL',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '1：削除を示す',
  PRIMARY KEY (`tweet_id`,`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='ツイートされたURLを登録する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tweets`
--

DROP TABLE IF EXISTS `tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweets` (
  `service_user_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TwitterユーザID',
  `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
  `tweet_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートしたユーザのID',
  `body` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '本文',
  `arranged_body` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '整形本文',
  `tweeted_datetime` datetime NOT NULL COMMENT 'ツイート日時',
  `favolite_count` int unsigned NOT NULL DEFAULT '0' COMMENT 'お気に入り数',
  `retweet_count` int unsigned NOT NULL DEFAULT '0' COMMENT 'リツイート数',
  `replied` tinyint NOT NULL DEFAULT '0' COMMENT 'リプライしたツイート',
  `retweeted` tinyint NOT NULL DEFAULT '0' COMMENT 'リツイートされたツイート',
  `is_media` tinyint NOT NULL DEFAULT '0' COMMENT 'メディアが添付されている',
  `media_ready` tinyint NOT NULL DEFAULT '0' COMMENT 'メディアを表示する準備が出来ている',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`,`tweet_id`),
  KEY `user_id` (`user_id`),
  KEY `tweets_service_user_id_IDX` (`service_user_id`,`tweet_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='取得したツイートを登録する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unfollowbacked`
--

DROP TABLE IF EXISTS `unfollowbacked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unfollowbacked` (
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID',
  `unfollowbacked_user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'フォロバ待ちユーザID',
  `day_old` int unsigned NOT NULL DEFAULT '0' COMMENT '経過日数',
  `undisplayed` tinyint NOT NULL DEFAULT '0' COMMENT '非表示',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`user_id`,`unfollowbacked_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='フォロバ待ちユーザのリストを利用者ごとに管理する。\r\n相互フォローになった場合は削除される。';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_config`
--

DROP TABLE IF EXISTS `user_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_config` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `service_user_id` varchar(10) COLLATE utf8mb4_bin NOT NULL,
  `config_id` int NOT NULL,
  `value` int DEFAULT NULL,
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `user_config_service_user_id_IDX` (`service_user_id`,`config_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users_accounts`
--

DROP TABLE IF EXISTS `users_accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_accounts` (
  `service_user_id` varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'サービス利用者ID',
  `user_id` varchar(70) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ユーザID(Twitter)',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
  `deleted` tinyint NOT NULL DEFAULT '0' COMMENT '論理削除',
  PRIMARY KEY (`service_user_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='利用者のTwitterアカウントを登録する';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'followcheck'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-10 17:24:33

DROP TABLE tweet_medias_cp;

ALTER TABLE tweet_medias ADD user_id varchar(70)  NOT NULL DEFAULT '0' FIRST;
ALTER TABLE tweet_medias ADD service_user_id varchar(10) NOT NULL DEFAULT '0' FIRST;
ALTER TABLE tweet_medias DROP PRIMARY KEY;
ALTER TABLE tweet_medias ADD PRIMARY KEY (service_user_id, user_id, tweet_id, url);

ALTER TABLE queue_download_medias ADD user_id varchar(70)  NOT NULL DEFAULT '0' FIRST;
ALTER TABLE queue_download_medias ADD service_user_id varchar(10) NOT NULL DEFAULT '0' FIRST;
ALTER TABLE queue_download_medias DROP PRIMARY KEY;
ALTER TABLE queue_download_medias ADD PRIMARY KEY (service_user_id, user_id, tweet_id, url);

ALTER TABLE queue_compress_medias ADD user_id varchar(70)  NOT NULL DEFAULT '0' FIRST;
ALTER TABLE queue_compress_medias ADD service_user_id varchar(10) NOT NULL DEFAULT '0' FIRST;
ALTER TABLE queue_compress_medias DROP PRIMARY KEY;
ALTER TABLE queue_compress_medias ADD PRIMARY KEY (service_user_id, user_id, tweet_id, url);

ALTER TABLE queue_create_thumbs ADD user_id varchar(70)  NOT NULL DEFAULT '0' FIRST;
ALTER TABLE queue_create_thumbs ADD service_user_id varchar(10) NOT NULL DEFAULT '0' FIRST;
ALTER TABLE queue_create_thumbs DROP PRIMARY KEY;
ALTER TABLE queue_create_thumbs ADD PRIMARY KEY (service_user_id, user_id, tweet_id, url);


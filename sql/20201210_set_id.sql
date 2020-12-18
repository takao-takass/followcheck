UPDATE tweet_medias tm
      ,tweets tw
SET tm.service_user_id = tw.service_user_id
   ,tm.user_id  = tw.user_id
WHERE tm.tweet_id = tw.tweet_id;

COMMIT;

UPDATE queue_compress_medias qcm
      ,tweet_medias tm
SET qcm.service_user_id = tm.service_user_id
   ,qcm.user_id = tm.user_id
WHERE qcm.tweet_id = tm.tweet_id
AND   qcm.url = tm.url;

COMMIT;

UPDATE queue_create_thumbs qcm
      ,tweet_medias tm
SET qcm.service_user_id = tm.service_user_id
   ,qcm.user_id = tm.user_id
WHERE qcm.tweet_id = tm.tweet_id
AND qcm.url = tm.url;

COMMIT;

UPDATE queue_download_medias qcm
      ,tweet_medias tm
SET qcm.service_user_id = tm.service_user_id
   ,qcm.user_id = tm.user_id
WHERE qcm.tweet_id = tm.tweet_id
AND qcm.url = tm.url;

COMMIT;
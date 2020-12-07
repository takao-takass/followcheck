import sys, hashlib, config, cv2
from PIL import Image
from classes import logger, thread, databeses, exceptions


class DownloadMedias:

    @staticmethod
    def run():

        """
        CREATE TABLE `queue_download_medias` (
          `tweet_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ツイートID',
          `url` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'メディアURL',
          `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT 'キューのステータス',
          `thread_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '処理を担当しているスレッドID',
          `error_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'エラーテキスト',
          `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登録日時',
          `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
          PRIMARY KEY (`tweet_id`,`url`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC
        """

        try:
            # スレッドIDの発行
            log = logger.ThreadLogging('-')
            thread_id = thread.ThreadId().CreateThread('download_medias.py', 1)

            # サムネイルの作成
            log = logger.ThreadLogging(thread_id)
            log.info("メディア情報を確認しています...")

            # 処理予約をする。
            db = databeses.DbConnection(log)
            db.execute(
                " UPDATE queue_download_medias"
                " SET thread_id = %(thread_id)s"
                " WHERE `status` = 0"
                " AND thread_id IS NULL "
                " LIMIT 5000",
                {
                    'thread_id': thread_id
                }
            )
            db.commit()

            download_medias = db.execute(
                " SELECT A.tweet_id,A.url,C.disp_name,A.sizes,A.`type` "
                " FROM queue_download_medias qdm"
                " INNER JOIN tweet_medias tm"
                " ON qdm.tweet_id = tm.tweet_id"
                " AND qdm.url = tm.url "
                " INNER JOIN tweets tw"
                " ON tm.tweet_id = tw.tweet_id"
                " INNER JOIN relational_users ru"
                " ON tw.user_id = ru.user_id"
                " WHERE qdm.thread_id = %(thread_id)s",
                {
                    'thread_id': thread_id
                }
            )

            for download_media in download_medias:
                
                splited_usls = download_media['url'].split('/')
                filename = splited_usls[len(splited_usls)-1].split('?')[0]




                # download_mediaws_bk.py および create_thumbnail.py を参考に実装する。









        except exceptions.UncreatedThreadException:
            # スレッドの作成ができない時は処理終了
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()

        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread('download_medias.py', thread_id)


# 処理実行
DownloadMedias.run()

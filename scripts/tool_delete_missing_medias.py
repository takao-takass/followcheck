import os
import sys
import config

from classes import logger, thread, databeses, exceptions


# DBから削除されたがストレージに残留しているメディアファイルを削除する
class DeleteMissingMedias:

    @staticmethod
    def run():

        try:
            # スレッドIDの発行
            thread_id = thread.ThreadId().CreateThread('delete_missing_medias.py', 1)
            log = logger.ThreadLogging(thread_id)
            db = databeses.DbConnection(log)

            # チェックテーブルから対象のディレクトリを取得する
            # テーブルが空の場合はディレクトリリストを取得して登録する
            matching_directories = db.fetch(
                " SELECT directory "
                " FROM matching_directories"
                , {}
            )

            if len(matching_directories) == 0:
                file_directories = os.listdir(path=config.STRAGE_MEDIAS_PATH)
                directories = [f for f in file_directories if os.path.isdir(os.path.join(config.STRAGE_MEDIAS_PATH, f))]

                for directory in directories:
                    db.execute(
                        " INSERT INTO matching_directories ("
                        "     directory"
                        " ) VALUES ("
                        "     %(directory)s"
                        " )"
                        , {
                            'directory': directory,
                        }
                    )
                    db.commit()
                
                matching_directories = db.fetch(
                    " SELECT directory "
                    " FROM matching_directories"
                    , {}
                )

            directory_count = 1
            for matching_directory in matching_directories:

                # ディレクトリパスを条件にレコードをすべて取得
                # また、ディレクトリ内のファイルリストを取得する
                log.info(f"SEARCH DIRECTORY ({ directory_count }/{ len(matching_directories) }) : { matching_directory['directory'] }")
                file_directories = os.listdir(path=config.STRAGE_MEDIAS_PATH + matching_directory['directory'])
                files = [f for f in file_directories if os.path.isfile(os.path.join(config.STRAGE_MEDIAS_PATH + matching_directory['directory'], f))]

                matching_files = db.fetch(
                    " SELECT file_name"
                    " FROM profile_icons"
                    " WHERE directory_path = %(directory_path)s"
                    , {
                        'directory_path': config.STRAGE_ICON_PATH + matching_directory['directory'] + '/',
                    }
                )
                matching_files = matching_files + db.fetch(
                    " SELECT file_name"
                    " FROM tweet_medias"
                    " WHERE directory_path = %(directory_path)s"
                    , {
                        'directory_path': config.STRAGE_MEDIAS_PATH + matching_directory['directory'] + '/',
                    }
                )
                matching_files = matching_files + db.fetch(
                    " SELECT thumb_file_name as file_name"
                    " FROM tweet_medias"
                    " WHERE thumb_directory_path = %(directory_path)s"
                    , {
                        'directory_path': config.STRAGE_MEDIAS_PATH + matching_directory['directory'] + '/',
                    }
                )
                matching_file_names = [f['file_name'] for f in matching_files]

                # マッチングする。マッチングしないファイルは削除する。
                for file_name in files:
                    if file_name in matching_file_names:
                        log.info(f'MATCHING OK! : {file_name}')
                    else:
                        log.info(f'MATCHING MISS! DELETED!!: {file_name}')
                        os.remove(config.STRAGE_MEDIAS_PATH + matching_directory['directory'] + '/' + file_name)

                # 終了したディレクトリはテーブルから削除。
                db.execute(
                    " DELETE FROM matching_directories"
                    " WHERE directory = %(directory)s"
                    , {
                        'directory': matching_directory['directory'],
                    }
                )
                db.commit()

                directory_count = directory_count + 1


        except exceptions.UncreatedThreadException:
            # スレッドの作成ができない時は処理終了
            sys.exit()

        except Exception as e:
            log.error(e)
            sys.exit()

        finally:
            if 'thread_id' in locals():
                log.info('プロセスを終了します。')
                thread.ThreadId().ExitThread('delete_missing_medias.py', thread_id)


# 処理実行
DeleteMissingMedias.run()

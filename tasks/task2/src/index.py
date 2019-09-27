import json
from typing import Any

from logger.get_logger import get_logger
from metadata_creator import main

logger = get_logger(__name__)


def handler(event: dict, context: Any) -> None:
    """
    Lambdaで実行される関数
    :param event: 渡されたEvent。ここから色々な情報を取得する
    :param context: Lambdaの実行に関する情報が入ったインスタンス。今回の処理では使用しない
    :return:
    """

    try:
        logger.info('event', event)
        main(event)
    except Exception as e:
        # 意図しない例外が発生した場合の処理
        logger.error(f'Exception occurred: {e}', exc_info=True)
    return

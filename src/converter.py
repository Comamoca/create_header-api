import base64
from io import BytesIO

from loguru import logger
from PIL import Image


def toBase64(img: Image, format="png") -> str:
    """画像データをBase64文字列に変換する
    :returns: str

    """
    buffer = BytesIO()
    img.save(buffer, format)
    img_str = base64.b64encode(buffer.getvalue()).decode("ascii")
    logger.info("テキスト -> Base64 変換処理が完了")

    return img_str


def toImage(img_str):
    if "base64," in img_str:
        # DARA URI の場合、data:[<mediatype>][;base64], を除く
        img_str = img_str.split(",")[1]
    img_raw = base64.b64decode(img_str)
    img = Image.open(BytesIO(img_raw))
    logger.info("Base64 -> 画像データ 変換処理が完了")

    return img

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pilmoji import Pilmoji
from pathlib import Path
from loguru import logger

from src import converter as conv

from collections import namedtuple

import tweepy
import dotenv
import os

# import urllib.error
# import urllib.request
#
# from tempfile import NamedTemporaryFile


class TwitterAPIError(Exception):
    """Docstring for ResponceError. """
    def __str__(self):
        return ("Twitter APIの応答が不適切です。引数を確認して下さい。")

    def __init__(self):
        """TODO: to be defined. """


User = namedtuple(
    "User",
    [
        "name",
        "twitter_id",
        "icon_url",
        "youtube_name",
        "instagram_name",
        "facebook_name",
    ],
)

Header = namedtuple("Header", ["basePath", "user"])

Font = namedtuple("Font", ["name", "path"])


def _get_user_data(twitter_id: str) -> tuple[str, str]:

    """TODO: get user data

    :twiter_id: TwitterのID Ex. @Comamoca_
    :returns: (アイコンのURL, ユーザーの表示名)

    """

    def get_dotenv():
        dotenv.load_dotenv()
        logger.debug("環境設定の読み込み完了")
        KEY = os.environ.get("API_KEY")
        SECRET = os.environ.get("API_SECRET")
        TOKEN = os.environ.get("TOKEN")
        SECRET_TOKEN = os.environ.get("SECRET_TOKEN")
        BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
        return (KEY, SECRET, TOKEN, SECRET_TOKEN, BEARER_TOKEN)

        # def dl_img(url):{{{
        #     fp = NamedTemporaryFile()
        #     try:
        #         with urllib.request.urlopen(url) as web_file:
        #             data = web_file.read()
        #             # 一時ファイルに保存
        #             fp.write(data)
        #     except urllib.error.URLError as e:
        #         print(e)
        #
        return fp

    #
    #
    # def load_tmpfile(fp):
    #     fp.seek(0)
    #     b = fp.read()
    #     return b}}}

    def get_datas(
        api_keys: tuple[str, str, str, str, str], id_str: str
    ) -> tuple[str, str]:
        fields = [
            "description",
            "name",
            "username",
            "public_metrics",
            "profile_image_url",
            "verified",
        ]

        fields_str = ",".join(fields)

        logger.debug("Twitterクライアントオブジェクトの生成が完了")
        client = tweepy.Client(
            bearer_token=api_keys[4],
            consumer_key=api_keys[0],
            consumer_secret=api_keys[1],
            access_token=api_keys[2],
            access_token_secret=[3],
        )

        logger.info("Twitter APIにアクセス開始")
        usr = client.get_user(
            username=id_str,
            user_fields=fields_str,
        )
        logger.info("ユーザー情報を取得しました。")
        # print(usr)

        try:
            url = usr.data.profile_image_url
            name = usr.data.name
        except AttributeError:
            logger.exception("例外が発生")
            raise TwitterAPIError

        return (url, name)

    url, username = get_datas(get_dotenv(), twitter_id)

    return (url, username)


# fp = dl_img("https://pbs.twimg.com/profile_images/\
# 1505613048236498947/rI0hpagN.png")
# get_icon_url(get_dotenv()

# ================= ここから画像処理 =================

# def icon_round(icon):{{{
#     mask = Image.new("L", icon_size, 0)
#     draw = ImageDraw.Draw(mask)
#     icon.putalpha(0)
#
#     draw = ImageDraw.Draw(icon)
#     draw.ellipse((0, 0, 200, 200), fill=(0, 0, 0))
#     draw.ellipse((
#                   0,
#                   0,
#                   200, 200),
#                  fill=255)
#
#     mask = mask.filter(ImageFilter.GaussianBlur(5))
#
#     # result = icon.copy()
#     # result.putalpha(mask)
#     return icon
#
#
# def crop_icon(pil_img, blur_radius, offset=0):
#     offset = blur_radius * 2 + offset
#     mask = Image.new("L", pil_img.size, 0)
#     draw = ImageDraw.Draw(mask)
#     draw.ellipse((
#                   offset,
#                   offset,
#                   pil_img.size[0] - offset, pil_img.size[1] - offset),
#                  fill=255)
#
#     mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
#
#     # result = pil_img.copy()
#     # result.putalpha(mask)
#
#     return pil_img
#

# croped = icon_round(icon)
#
# print(type(croped))
# # 画像に追加する文字列を指定}}}


def make_header(user: User,
                icon: Image,
                twitter_id_font: Font,
                sns_name_font: Font,
                header: Header,
                word: str) -> Image:

    """ヘッダー画像を生成する。

    :user: ユーザーデータ
    :returns: 画像データ

    """
    # user = get_user_data(id_str, youtube_name, instagram_name, facebook_name)

    url, uname = _get_user_data(user.twitter_id)
    inputfile = header.basePath

    img = Image.open(Path(inputfile).resolve())
    logger.info("ヘッダー画像の読み込み完了")
    copied = img.copy()

    # TODO: 画像をJson経由で取得する
    icon.load()
    logger.info("アイコンデータを取得完了")

    imagesize = copied.size
    # draw = ImageDraw.Draw(copied)

    icon_size = (200, 200)
    resized = icon.resize(icon_size)
    copied.paste(resized, (320, 150))

    twitter_id_font = ImageFont.truetype(twitter_id_font.path, 50)
    sns_name_font = ImageFont.truetype(sns_name_font.path, 30)
    sns_id_font = ImageFont.truetype(sns_name_font.path, 20)
    logger.info("フォントデータの読み込み完了")

    def draw_text(draw, text: str, font, x, y):
        with Pilmoji(draw) as pil:
            pil.text(
                (
                 x,
                 y,
                ),
                text,
                font=font,
                fill="#FFF",
            )
        logger.debug(f"文字の書き込み処理 テキスト: {text}が完了")

    def draw_id_word(img, id_str: str, one_word: str,
                     id_font, word_font) -> None:
        draw_text(img, id_str, id_font, int(imagesize[0] / 2), 100)
        draw_text(img, one_word, word_font, int(imagesize[0] / 2 + 20), 150)
        logger.info("Twitterユーザー名と一言の書き込みが完了")

    def draw_more_sns(img, sns_name, id_str: str, y) -> None:
        span = 100
        draw_text(img, sns_name, sns_name_font,
                  int(imagesize[0] / 2 - span), y)
        draw_text(img, id_str, sns_id_font,
                  int(imagesize[0] / 2 - span), y + 30)
        logger.info("SNS情報の書き込みが完了")

    # ==== テスト画像の生成処理 ====
    draw_id_word(copied,
                 user.name,
                 word,
                 twitter_id_font,
                 sns_id_font)

    sns_names = [
        ("Youtube", user.youtube_name),
        ("Instagram", user.instagram_name),
        ("Facebook", user.facebook_name),
    ]

    y = 190
    for sns, name in sns_names:
        if len(name) == 0:
            continue
        draw_more_sns(copied, sns, name, y)
        y += 100

    # ファイルを保存
    # copied.save("out.png", "PNG", quality=100, optimize=True)
    return copied


def create(
         icon_str: str,
         twitter_id: str,
         word: str,
         youtube_name: str,
         insta_name: str,
         fbook_name: str,
         header_path: str = "./media/sample/header_1.png") -> str:
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    """必要だと思われる情報

    Twitter ID (@~~~)
    Youtube, INstam FBookのユーザ名 -> デフォルトは空文字(表示しない)
    一言 -> デフォルトは空文字(表示しない)
    """
    tw_id = "Comamoca_"
    url, name = _get_user_data(tw_id)

    user = User(
        name=name,
        twitter_id=tw_id,
        icon_url=url,
        youtube_name=youtube_name,
        instagram_name=insta_name,
        facebook_name=fbook_name,
    )

    icon = conv.toImage(icon_str)

    niconico_font = Font("ニコニコフォント", "./media/sample/fonts/nicokaku_v1.ttf")
    jk_font = Font("JKゴシック", "./media/sample/fonts/JKG-L_3.ttf")
    # emoji_font = Font("Noto_emoji",
    #                   "./media/sample/fonts/NotoColorEmoji.ttf")

    header = Header(basePath=header_path, user=user)
    img = make_header(user, icon, header=header, word=word,
                      twitter_id_font=niconico_font,
                      sns_name_font=jk_font)

    str_img = conv.toBase64(img)

    return str_img


if __name__ == "__main__":
    """必要だと思われる情報

    Twitter ID (@~~~)
    Youtube, INstam FBookのユーザ名 -> デフォルトは空文字(表示しない)
    一言 -> デフォルトは空文字(表示しない)
    """
    tw_id = "Comamoca_"
    url, name = _get_user_data(tw_id)

    user = User(
        name=name,
        twitter_id=tw_id,
        icon_url=url,
        youtube_name="",
        instagram_name="",
        facebook_name="",
    )

    niconico_font = Font("ニコニコフォント", "./media/sample/fonts/nicokaku_v1.ttf")
    jk_font = Font("JKゴシック", "./media/sample/fonts/JKG-L_3.ttf")
    # emoji_font = Font("Noto_emoji",
    #                   "./media/sample/fonts/NotoColorEmoji.ttf")

    with open("./icon.txt", "r") as f:
        logger.debug("テストデータの読み込み開始")
        txt = f.read()
        logger.debug("完了")

    icon = conv.toImage(txt)

    header = Header(basePath="./media/sample/header_1.png", user=user)
    img = make_header(user, icon, header, "一言")

    img.save("out.png", "PNG", quality=100, optimize=True)

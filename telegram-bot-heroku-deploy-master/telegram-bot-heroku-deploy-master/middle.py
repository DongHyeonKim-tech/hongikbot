import logging
import telegram
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1612750464:AAHzrMCUR24yJYLnTto5laTwSqBUdxiJU6E", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("piracy", piracy))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="홍익대학교 세종캠퍼스 정보알리미 챗봇입니다!\n원하시는 서비스를 클릭해주세요.\n\n각 학과 홈페이지 주소 및 정보: /site\n금주 학식 식단: /menu\n학사 일정(복학, 개강 등): /schedule\n정규학기 수강신청 일정: /sugang\n계절학기 수강신청 일정: /seasonal\n기타 학교 정보(학사행정, 학교기관, 프린터, 증명발급 등): /other",
    )


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Currently I am in Alpha stage, help me also!')


def piracy(update, context):
    update.message.reply_text('Ahhan, FBI wants to know your location!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


BOT_TOKEN = "1612750464:AAHzrMCUR24yJYLnTto5laTwSqBUdxiJU6E"
bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# on different commands - answer in Telegram
# dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("piracy", piracy))


def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id=update.effective_user.id, action=ChatAction.TYPING
    )


def menu_cb_button(update, context):
    context.bot.send_chat_action(
        menu_chat_id=update.effective_user.id, menu_action=ChatAction.TYPING
    )


def schedule_cb_button(update, context):
    context.bot.send_chat_action(
        schedule_chat_id=update.effective_user.id, schedule_action=ChatAction.TYPING
    )


def sugang_cb_button(update, context):
    context.bot.send_chat_action(
        sugang_chat_id=update.effective_user.id, sugang_action=ChatAction.TYPING
    )


def seasonal_cb_button(update, context):
    context.bot.send_chat_action(
        seasonal_chat_id=update.effective_user.id, seasonal_action=ChatAction.TYPING
    )


def other_cb_button(update, context):
    context.bot.send_chat_action(
        other_chat_id=update.effective_user.id, other_action=ChatAction.TYPING
    )


def information_task_buttons(update, context):
    task_buttons = [
        [
            InlineKeyboardButton("상경대학", callback_data="상경대학"),
            InlineKeyboardButton("과학기술대학", callback_data="과학기술대학"),
        ],
        [
            InlineKeyboardButton("조형대학", callback_data="조형대학"),
            InlineKeyboardButton("융합전공", callback_data="융합전공"),
        ],
        [InlineKeyboardButton(
            "게임학부,광고홍보학부,캠퍼스자율,산업스포츠", callback_data="기타")],
    ]
    reply_markup = InlineKeyboardMarkup(task_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="대학/학과를 선택해주세요.\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


def menu_task_buttons(update, context):
    menu_buttons = [
        [InlineKeyboardButton(
            "학교식단 사이트 바로가기", callback_data="식단 바로가기")],
        [
            InlineKeyboardButton("월요일", callback_data="월요일"),
            InlineKeyboardButton("화요일", callback_data="화요일"),
        ],
        [
            InlineKeyboardButton("수요일", callback_data="수요일"),
            InlineKeyboardButton("목요일", callback_data="목요일"),
        ],
        [
            InlineKeyboardButton("금요일", callback_data="금요일"),
            InlineKeyboardButton("이번주", callback_data="이번주"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(menu_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="학식은 현재 코로나로 인해 B동 식당에서만 운영중이며 운영시간은 11:30~14:00입니다.\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


def schedule_task_buttons(update, context):
    schedule_buttons = [
        [InlineKeyboardButton("학사일정 사이트 바로가기", callback_data="학사일정 바로가기")],
        [
            InlineKeyboardButton("복학신청기간", callback_data="복학"),
            InlineKeyboardButton("휴학신청기간", callback_data="휴학"),
        ],
        [
            InlineKeyboardButton("수강과목 사전선택 기간", callback_data="사전선택"),
            InlineKeyboardButton("수강신청기간", callback_data="수강신청"),
        ],
        [
            InlineKeyboardButton("개강", callback_data="개강"),
            InlineKeyboardButton("종강", callback_data="종강"),
        ],
        [
            InlineKeyboardButton("계절학기", callback_data="계절학기"),
            InlineKeyboardButton("학위수여식", callback_data="학위수여식"),
        ],
        [InlineKeyboardButton("전체일정(21-1학기)", callback_data="전체일정")],
    ]
    reply_markup = InlineKeyboardMarkup(schedule_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="일정을 선택해주세요.\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


def sugang_task_buttons(update, context):
    sugang_buttons = [
        [InlineKeyboardButton("수강신청 사이트 바로가기", callback_data="수강신청 바로가기")],
        [
            InlineKeyboardButton("수강신청 전체 일정", callback_data="수강신청 전체 일정"),
            InlineKeyboardButton("담아두기 전체 일정", callback_data="담아두기 전체 일정"),
        ],
        [
            InlineKeyboardButton("1학년", callback_data="1"),
            InlineKeyboardButton("2학년", callback_data="2"),
        ],
        [
            InlineKeyboardButton("3학년", callback_data="3"),
            InlineKeyboardButton("4,5학년", callback_data="4,5"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(sugang_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="일정 혹은 학년을 선택해주세요.\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


def seasonal_task_buttons(update, context):
    seasonal_buttons = [
        [
            InlineKeyboardButton(
                "수강신청 사이트 바로가기", callback_data="계절학기 수강신청 바로가기"),
            InlineKeyboardButton("수강신청 전체 일정", callback_data="계절학기일정"),
        ],
        [
            InlineKeyboardButton("1차 수강신청 일정", callback_data="계절1차수강"),
            InlineKeyboardButton("2차 수강신청 일정", callback_data="계절2차수강"),
        ],
        [
            InlineKeyboardButton("수강철회", callback_data="계절철회정정"),
            InlineKeyboardButton("폐강 과목 수강생 수강정정기간",
                                 callback_data="계절폐강정정"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(seasonal_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="20-2 동계 계절학기 기간: 12. 28(월) ~ 2021. 1. 20(수).\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


def other_task_buttons(update, context):
    other_buttons = [
        [
            InlineKeyboardButton("학사행정 사이트 바로가기", callback_data="학사행정"),
            InlineKeyboardButton("클래스넷 사이트 바로가기", callback_data="클래스넷"),
        ],
        [
            InlineKeyboardButton("행정기관 사이트 바로가기", callback_data="행정기관"),
            InlineKeyboardButton("부속기관 사이트 바로가기", callback_data="부속기관"),
        ],
        [
            InlineKeyboardButton("인터넷 증명발급 사이트 바로가기",
                                 callback_data="인터넷증명발급(학생)"),
            InlineKeyboardButton("공용프린터 안내 사이트 바로가기",
                                 callback_data="공용프린터 사용안내"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(other_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="*각 서비스 상세 안내\n1.학사행정: 계절학기, 휴/복학, 장학금 등의 규정 및 종류\n2.행정기관: 교무입시팀, 학생복지팀, 기숙사, 산학협력단 등\n3.부속기관: 도서관, 전산실, 취업진로지원/학생상담/교수학습지원 등\n4.증명발급: 재학/수료/졸업예정/성적증명서 등 발급 및 발급안내\n5.공용프린터: 공용프린터 위치 및 사용시간 안내\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


task_buttons_handler = CommandHandler("site", information_task_buttons)
button_callback_handler = CallbackQueryHandler(cb_button)
dp.add_handler(task_buttons_handler)
dp.add_handler(button_callback_handler)

menu_task_buttons_handler = CommandHandler("menu", menu_task_buttons)
menu_button_callback_handler = CallbackQueryHandler(menu_cb_button)
dp.add_handler(menu_task_buttons_handler)
dp.add_handler(menu_button_callback_handler)

schedule_task_buttons_handler = CommandHandler(
    "schedule", schedule_task_buttons)
schedule_button_callback_handler = CallbackQueryHandler(schedule_cb_button)
dp.add_handler(schedule_task_buttons_handler)
dp.add_handler(schedule_button_callback_handler)

sugang_task_buttons_handler = CommandHandler("sugang", sugang_task_buttons)
sugang_button_callback_handler = CallbackQueryHandler(sugang_cb_button)
dp.add_handler(sugang_task_buttons_handler)
dp.add_handler(sugang_button_callback_handler)

seasonal_task_buttons_handler = CommandHandler(
    "seasonal", seasonal_task_buttons)
seasonal_button_callback_handler = CallbackQueryHandler(seasonal_cb_button)
dp.add_handler(seasonal_task_buttons_handler)
dp.add_handler(seasonal_button_callback_handler)

other_task_buttons_handler = CommandHandler("other", other_task_buttons)
other_button_callback_handler = CallbackQueryHandler(other_cb_button)
dp.add_handler(other_task_buttons_handler)
dp.add_handler(other_button_callback_handler)
# on noncommand i.e message - echo the message on Telegram
dp.add_handler(MessageHandler(Filters.text, echo))

# log all errors
dp.add_error_handler(error)

updater.start_polling()
updater.idle()

if __name__ == '__main__':
    main()

# 사용 라이브러리
import os
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import time
import pymysql
import telegram
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, bot
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler

# 봇 토큰 기본 정보

BOT_TOKEN = "1612750464:AAHzrMCUR24yJYLnTto5laTwSqBUdxiJU6E"
bot = telegram.Bot(token=BOT_TOKEN)

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="홍익대학교 세종캠퍼스 정보알리미 챗봇입니다!\n원하시는 서비스를 클릭해주세요.\n\n각 학과 홈페이지 주소 및 정보: /site\n금주 학식 식단: /menu\n학사 일정(복학, 개강 등): /schedule\n정규학기 수강신청 일정: /sugang\n계절학기 수강신청 일정: /seasonal\n기타 학교 정보(학사행정, 학교기관, 프린터, 증명발급 등): /other",
    )
    ###


PORT = int(os.environ.get("PORT", 5000))

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

# Mysql 데이터 가져오기-각 학부 정보
dept = ["상경대학", "과학기술대학", "조형대학", "융합전공", "기타"]
dept_num = ["1", "2", "3", "4", "5"]

connect = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="xkzlxkzl1!",
    db="chatbot",
    charset="utf8mb4",
)

dept_info_list = []

for i in range(0, len(dept)):
    cur = connect.cursor(pymysql.cursors.DictCursor)
    query = (
        "SELECT DEPT_NAME, DEPT_LOC, DEPT_PH, DEPT_URL FROM TBL_DEPT WHERE DEPT_NO LIKE '"
        + dept_num[i]
        + "%'"
    )
    cur.execute(query)
    rows = cur.fetchall()
    connect.commit()

    for row in rows:
        dept_info = {
            "DEPT_NAME": row["DEPT_NAME"],
            "DEPT_LOC": row["DEPT_LOC"],
            "DEPT_PH": row["DEPT_PH"],
            "DEPT_URL": row["DEPT_URL"],
        }
        dept_info_list.append(dept_info)

dept_DF = pd.DataFrame(dept_info_list)
code_dept_business = ""
code_dept_sci_tech = ""
code_dept_art = ""
code_dept_else1 = ""
code_dept_else2 = ""
if dept_DF.empty == False:
    for i in range(0, 4):
        code_dept_business = (
            code_dept_business
            + "\n\n"
            + dept_DF.DEPT_NAME.iloc[i]
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
            + "\n"
            + dept_DF.DEPT_URL.iloc[i]
        )
    for i in range(4, 15):
        code_dept_sci_tech = (
            code_dept_sci_tech
            + "\n\n"
            + dept_DF.DEPT_NAME.iloc[i]
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
            + "\n"
            + dept_DF.DEPT_URL.iloc[i]
        )
    for i in range(15, 21):
        code_dept_art = (
            code_dept_art
            + "\n\n"
            + dept_DF.DEPT_NAME.iloc[i]
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
            + "\n"
            + dept_DF.DEPT_URL.iloc[i]
        )
    for i in range(21, 25):
        code_dept_else1 = (
            code_dept_else1
            + "\n\n"
            + dept_DF.DEPT_NAME.iloc[i]
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
            + "\n"
            + dept_DF.DEPT_URL.iloc[i]
        )
    for i in range(25, 27):
        code_dept_else2 = (
            code_dept_else2
            + "\n\n"
            + dept_DF.DEPT_NAME.iloc[i]
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
            + "\n"
            + dept_DF.DEPT_URL.iloc[i]
        )
code_dept = [
    code_dept_business,
    code_dept_sci_tech,
    code_dept_art,
    code_dept_else2,
    code_dept_else1,
]

# 식단 크롤링
req = requests.get("http://sj.hongik.ac.kr/site/food/food_menu.html")
html = req.content
soup = BeautifulSoup(html, "html.parser")


def get_text_list(tag_list):
    return [tag.text for tag in tag_list]


menu_list = get_text_list(soup.select("div.foodmenu"))
date_list = get_text_list(soup.find_all("th", {"strong": ""})[2:8])

sikdan_list = []
for date, menu in zip(date_list, menu_list):
    sikdan = {"date": date, "menu": menu}
    sikdan_list.append(sikdan)

sikdan_DF = pd.DataFrame(sikdan_list)
code_html = ""
if sikdan_DF.empty == False:
    for i in range(0, len(sikdan_DF)):
        code_html = code_html + "\n\n" + \
            sikdan_DF.date.iloc[i] + sikdan_DF.menu.iloc[i]
        if i == 4:
            break

# 학사일정 크롤링
req_sche = requests.get(
    "http://sejong.hongik.ac.kr/contents/www/cor/calendar.html")
html_sche = req_sche.content
soup_sche = BeautifulSoup(html_sche, "html5lib")

list_day = soup_sche.find_all(name="td", attrs={"valign": "middle"})
half_number = len(list_day) / 2
type(int(half_number))

calendar_list = []
for index in range(20, int(half_number) + 1):
    date = list_day[index * 2 - 2].find().text
    schedule = list_day[index * 2 - 1].find().text
    schedule_obj = {
        "date": date,
        "schedule": schedule,
    }
    calendar_list.append(schedule_obj)
    if index == 41:
        break

calendar_DF = pd.DataFrame(calendar_list)

code_html_schedule = ""
if calendar_DF.empty == False:
    for i in range(0, len(calendar_DF)):
        code_html_schedule = (
            code_html_schedule
            + "\n"
            + calendar_DF.schedule.iloc[i]
            + " : "
            + calendar_DF.date.iloc[i]
        )
# 학교 홈페이지 정보 GUI


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
        [InlineKeyboardButton("게임학부,광고홍보학부,캠퍼스자율,산업스포츠", callback_data="기타")],
    ]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="대학/학과를 선택해주세요.\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


# 학교 식단  GUI


def menu_task_buttons(update, context):
    menu_buttons = [
        [InlineKeyboardButton("학교식단 사이트 바로가기", callback_data="식단 바로가기")],
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


# 학교 일정 GUI


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


# 수강신청 GUI


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


# 계절학기 GUI


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
            InlineKeyboardButton("폐강 과목 수강생 수강정정기간", callback_data="계절폐강정정"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(seasonal_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="20-2 동계 계절학기 기간: 12. 28(월) ~ 2021. 1. 20(수).\n\n첫 화면으로 돌아가기: /start",
        reply_markup=reply_markup,
    )


# 기타 GUI


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


# 학교 홈페이지 정보 GUI


def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id=update.effective_user.id, action=ChatAction.TYPING
    )

    # 각 학과 정보
    for i in range(0, len(dept)):
        if data == dept[i]:
            context.bot.edit_message_text(
                text=code_dept[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="뒤로가기: /site\n첫 화면으로 돌아가기: /start".format(
                    data),
            )

    # 학교 식단
    if data == "식단 바로가기":
        context.bot.edit_message_text(
            text="[학교식단 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/cafe_2.html)\n\n뒤로가기: /menu\n첫 화면으로 돌아가기: /start",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
    if data == "이번주":
        context.bot.edit_message_text(
            text=code_html,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /menu\n첫 화면으로 돌아가기: /start".format(
                data),
        )
    Food = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    for i in range(0, len(Food)):
        if data == Food[i]:
            context.bot.edit_message_text(
                text=sikdan_DF.date.iloc[i] + sikdan_DF.menu.iloc[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="뒤로가기: /menu\n첫 화면으로 돌아가기: /start".format(
                    data),
            )
    # 학사일정
    if data == "학사일정 바로가기":
        context.bot.edit_message_text(
            text="[학사일정 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/calendar_1.html) \n\n뒤로가기: /schedule\n첫 화면으로 돌아가기: /start",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
    if data == "복학":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[0]
            + " 기간은 "
            + calendar_DF.date.iloc[0]
            + "입니다."
            + "\n"
            + calendar_DF.schedule.iloc[15]
            + " 기간은 "
            + calendar_DF.date.iloc[15]
            + "입니다.",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data),
        )
    if data == "휴학":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[4]
            + " 기간은 "
            + calendar_DF.date.iloc[4]
            + "입니다."
            + "\n"
            + calendar_DF.schedule.iloc[20]
            + " 기간은 "
            + calendar_DF.date.iloc[20]
            + "입니다.",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data),
        )
    if data == "사전선택":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[1]
            + " 기간은 "
            + calendar_DF.date.iloc[1]
            + "입니다."
            + "\n"
            + calendar_DF.schedule.iloc[16]
            + " 기간은 "
            + calendar_DF.date.iloc[16]
            + "입니다.",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data),
        )
    if data == "수강신청":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[3]
            + " 기간은 "
            + calendar_DF.date.iloc[3]
            + "입니다."
            + "\n"
            + calendar_DF.schedule.iloc[21]
            + " 기간은 "
            + calendar_DF.date.iloc[21]
            + "입니다",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data),
        )
    if data == "개강":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[5]
            + " 기간은 "
            + calendar_DF.date.iloc[5]
            + "입니다.",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data
            ),
        )
    if data == "종강":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[9]
            + " 기간은 "
            + calendar_DF.date.iloc[9]
            + "입니다.",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data
            ),
        )
    if data == "계절학기":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[12]
            + " 기간은 "
            + calendar_DF.date.iloc[12]
            + "입니다.",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data
            ),
        )
    if data == "학위수여식":
        context.bot.edit_message_text(
            text=calendar_DF.schedule.iloc[17]
            + " 기간은 "
            + calendar_DF.date.iloc[17]
            + "입니다.",
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data
            ),
        )
    if data == "전체일정":
        context.bot.edit_message_text(
            text=code_html_schedule,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="뒤로가기: /schedule\n첫 화면으로 돌아가기: /start".format(
                data),
        )
    # 수강신청
    # 각 학년 수강신청 기간
    sign = ["1", "2", "3", "4,5"]
    sign_time = [
        "8.25(화) 14:00~17:00",
        "8.25(화) 09:00~12:00",
        "8.25(화) 09:00~12:00",
        "8.24(화) 14:00~17:00",
        "8.24(화) 09:00~12:00",
    ]
    for i in range(0, len(sign)):
        if data == sign[i]:
            context.bot.edit_message_text(
                text=sign[i]
                + "학년 수강신청 기간은 "
                + sign_time[i]
                + "입니다.\n\n뒤로가기: /sugang\n첫 화면으로 돌아가기: /start",
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
            )
    # 전체 수강신청, 담아두기 기간 및 수강신청 바로가기
    sign_else = ["수강신청 전체 일정", "담아두기 전체 일정", "수강신청 바로가기"]
    sign_else_content = [
        "1학년: 8.25(화) 14:00~17:00\n2학년: 8.25(화) 09:00~12:00\n3학년: 8.24(화) 14:00~17:00\n4,5학년: 8.24(화) 09:00~12:00\n\n전체학년 추가: 8.26(수) 09:00 ~ 8.27(목) 17:00\n정정: 9.1(화) 09:00 ~ 9. 7(월) 17:00\n철회: 9.8(화) 09:00 ~ 9. 9(수) 17:00\n폐강과목 수강생 정정기간: 9. 10(목) 폐강과목 공지 이후 ~ 9.11(금) 17:00\n\n첫 화면으로 돌아가기: /start",
        "1차 담아두기 기간: 7.28(화) 09:00 ~ 8.4(화) 17:00\n2차 담아두기 기간: 8.10(월) 09:00 ~ 8.14(금) 17:00\n\n첫 화면으로 돌아가기: /start",
        "[수강신청 사이트 바로가기](https://sugang.hongik.ac.kr/cn1000.jsp)\n\n뒤로가기: /sugang\n첫 화면으로 돌아가기: /start",
    ]
    for i in range(0, len(sign_else)):
        if data == sign_else[i]:
            context.bot.edit_message_text(
                text=sign_else_content[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode="Markdown",
            )
    # 계절학기
    seasonal = ["계절1차수강", "계절2차수강", "계절철회정정",
                "계절폐강정정", "계절학기일정", "계절학기 수강신청 바로가기"]
    seasonal_content = [
        "1,2학년: 12. 09(수) 09:00 ~ 17:00\n3학년: 12. 08(화) 09:00 ~ 17:00\n4,5학년: 12. 07(월) 09:00 ~ 17:00\n전체: 12. 10(목) 09:00 ~ 17:00\n1차 수강료 납부: 12. 11(금) 09:00 ~ 12. 15(화) 16:00\n※ 1차 수강료를 납부하지 않으면 1차 수강신청내역은 일괄 삭제\n\n첫 화면으로 돌아가기: /start",
        "2차 수강신청: 12. 16(수) 09:00 ~ 17:00\n2차 수강료 납부: 12. 17(목) 09:00 ~ 12. 18(금) 16:00\n※ 2차 수강료를 납부하지 않으면 2차 수강신청 내역은 일괄 삭제\n계절학기에는 수강신청 정정 허가원이 없으므로 유의\n\n첫 화면으로 돌아가기: /start",
        "수강철회: 12. 21(월) 09:00 ~ 12. 22(화) 17:00\n※ 추가 수강신청이나 정정은 되지 않고 철회만 가능\n철회한 내역에 대해 기납부한 수강료는 전액 환불처리\n\n첫 화면으로 돌아가기: /start",
        "폐강과목 수강생 정정기간: 12. 23(수) 15:00 ~ 12. 24(목) 17:00까지\n온라인 정정 : 수강신청페이지 > 폐강과목 수강정정\n\n첫 화면으로 돌아가기: /start",
        "*1차 수강신청\n1,2학년: 12. 09(수) 09:00 ~ 17:00\n3학년: 12. 08(화) 09:00 ~ 17:00\n4,5학년: 12. 07(월) 09:00 ~ 17:00\n전체: 12. 10(목) 09:00 ~ 17:00\n\n*2차 수강신청\n2차 수강신청: 12. 16(수) 09:00 ~ 17:00\n\n첫 화면으로 돌아가기: /start",
        " [동계 계절학기 수강신청 사이트 바로가기](https://sugang.hongik.ac.kr/cn1000.jsp)\n\n뒤로가기: /seosonal첫 화면으로 돌아가기: /start",
    ]
    for i in range(0, len(seasonal)):
        if data == seasonal[i]:
            context.bot.edit_message_text(
                text=seasonal_content[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode="Markdown",
            )
    # Other
    other = ["클래스넷", "학사행정", "행정기관", "부속기관", "인터넷증명발급(학생)", "공용프린터 사용안내"]
    other_content = [
        "[클래스넷 사이트 바로가기](https://www.hongik.ac.kr/login.do)",
        "[학사행정 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/scholarship.html)",
        "[행정기관 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/stration.html)",
        "[부속기관 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/attachedd.html)",
        "[증명서 발급](http://hongik.certpia.com/default.asp)",
        "[공용프린터 사용안내 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/printer.html)",
    ]
    for i in range(0, len(other)):
        if data == other[i]:
            context.bot.edit_message_text(
                text=other_content[i] +
                "\n\n뒤로가기: /other\n첫 화면으로 돌아가기: /start",
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode="Markdown",
            )


# cb_button
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


# handler
task_buttons_handler = CommandHandler("site", information_task_buttons)
button_callback_handler = CallbackQueryHandler(cb_button)
dispatcher.add_handler(task_buttons_handler)
dispatcher.add_handler(button_callback_handler)


menu_task_buttons_handler = CommandHandler("menu", menu_task_buttons)
menu_button_callback_handler = CallbackQueryHandler(menu_cb_button)
dispatcher.add_handler(menu_task_buttons_handler)
dispatcher.add_handler(menu_button_callback_handler)

schedule_task_buttons_handler = CommandHandler(
    "schedule", schedule_task_buttons)
schedule_button_callback_handler = CallbackQueryHandler(schedule_cb_button)
dispatcher.add_handler(schedule_task_buttons_handler)
dispatcher.add_handler(schedule_button_callback_handler)

sugang_task_buttons_handler = CommandHandler("sugang", sugang_task_buttons)
sugang_button_callback_handler = CallbackQueryHandler(sugang_cb_button)
dispatcher.add_handler(sugang_task_buttons_handler)
dispatcher.add_handler(sugang_button_callback_handler)

seasonal_task_buttons_handler = CommandHandler(
    "seasonal", seasonal_task_buttons)
seasonal_button_callback_handler = CallbackQueryHandler(seasonal_cb_button)
dispatcher.add_handler(seasonal_task_buttons_handler)
dispatcher.add_handler(seasonal_button_callback_handler)

other_task_buttons_handler = CommandHandler("other", other_task_buttons)
other_button_callback_handler = CallbackQueryHandler(other_cb_button)
dispatcher.add_handler(other_task_buttons_handler)
dispatcher.add_handler(other_button_callback_handler)

# updater.start_polling(timeout=1, clean=True)
updater.start_webhook(listen="0.0.0.0", port=int(
    PORT), url_path='1612750464:AAHzrMCUR24yJYLnTto5laTwSqBUdxiJU6E')
updater.bot.setWebhook("https://hongikbot11.herokuapp.com/" +
                       '1612750464:AAHzrMCUR24yJYLnTto5laTwSqBUdxiJU6E')
updater.idle()

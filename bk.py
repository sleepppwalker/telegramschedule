import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram import types

bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_name = 'database.db'

async def get_schedule_for_group(group_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT start_day, lessonname, teachername, auditory, start_time, end_time, date, comment_to_day, pod_groups FROM schedule WHERE groupname=?", (group_name,))
    schedule_data = cursor.fetchall()
    conn.close()
    return schedule_data

async def get_schedule_for_teacher(teacher_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT start_day, lessonname, groupname, auditory, start_time, end_time, date, teachername, pod_groups FROM schedule WHERE teachername=?", (teacher_name,))
    schedule_data = cursor.fetchall()
    conn.close()
    return schedule_data

async def get_schedule_for_auditory(auditory_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT start_day, lessonname, groupname, auditory, start_time, end_time, date, teachername, pod_groups FROM schedule WHERE auditory=?", (auditory_name,))
    schedule_data = cursor.fetchall()
    conn.close()
    return schedule_data

def get_groups_by_course(course):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT groupname FROM schedule WHERE course=?", (course,))
    groups = cursor.fetchall()
    conn.close()
    return groups

def format_schedule_message(schedule_data):
    formatted_message = ''
    current_day = None
    day_schedule_exists = False 

    for row in schedule_data:
        date_start = row[0]
        lessonname = row[1]
        teachername = row[2]
        auditory = row[3]
        time_start = row[4]
        time_end = row[5]
        date = row[6]
        comment_to_day = row[7]
        pod_groups = row [8]

        if current_day != date_start:
            if current_day is not None and not day_schedule_exists:
                formatted_message += "Для выбранного дня нет расписания.😞\n\n"
            current_day = date_start
            day_schedule_exists = False
            formatted_message += f"<b>📅{current_day}:</b> <b>{date}</b>\n"

            if comment_to_day:
                formatted_message += f"Комментарий на день: {comment_to_day}\n"
            else:
                formatted_message += ""

        formatted_message += f"\n🕓Время: {time_start} - {time_end}\n"
        formatted_message += f"📖Предмет: {lessonname}\n🧑‍🏫Преподаватель: {teachername}\n🏛Аудитория: {auditory}\n"
        if pod_groups:
            formatted_message += f"👥Подгруппа: {pod_groups}\n"
        else:
            formatted_message +="\n"
        day_schedule_exists = True

    if not day_schedule_exists:
        formatted_message += "Для выбранного дня нет расписания.😞\n"

    return formatted_message

def format_schedule_message_teacher(schedule_data_teacher):
    formatted_message_teacher = ''
    current_day = None
    for row in schedule_data_teacher:
        date_start = row[0]
        lessonname = row[1]
        groupname = row[2]
        auditory = row[3]
        time_start = row[4]
        time_end = row[5]
        date = row[6]
        teachername = row[7]
        pod_groups = row [8]
        
        if current_day != date_start:
            if formatted_message_teacher:
                formatted_message_teacher += '\n\n'
            current_day = date_start
            formatted_message_teacher += f"<b>📅{current_day}:</b> <b>{date}</b> \n<b>🧑‍🏫Преподаватель: {teachername}</b>\n"

        formatted_message_teacher += f"\n🕓Время: {time_start} - {time_end}\n"
        formatted_message_teacher += f"📖Предмет: {lessonname}\n👥Группа: {groupname}\n🏛Аудитория: {auditory}\n"
        if pod_groups:
            formatted_message_teacher += f"👥Подгруппа: {pod_groups}\n"
        else:
            formatted_message_teacher +="\n"
    
    return formatted_message_teacher

def format_schedule_message_auditory(schedule_data_auditory):
    formatted_message_auditory = ''
    current_day = None
    for row in schedule_data_auditory:
        date_start = row[0]
        lessonname = row[1]
        groupname = row[2]
        auditory = row[3]
        time_start = row[4]
        time_end = row[5]
        date = row[6]
        teachername = row[7]
        pod_groups = row [8]
        
        if current_day != date_start:
            if formatted_message_auditory:
                formatted_message_auditory += '\n\n'
            current_day = date_start
            formatted_message_auditory += f"<b>📅{current_day}:</b> <b>{date}</b> \n<b>🏛Аудитория: {auditory}</b>\n"
        
        formatted_message_auditory += f"\n🕓Время: {time_start} - {time_end}\n"
        formatted_message_auditory += f"📖Предмет: {lessonname}\n👥Группа: {groupname}\n🧑‍🏫Преподаватель: {teachername}\n"
        if pod_groups:
            formatted_message_auditory += f"👥Подгруппа: {pod_groups}\n"
        else:
            formatted_message_auditory +="\n"
    
    return formatted_message_auditory

def sort_schedule_by_day(schedule_data):
    sorted_schedule = {}
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for row in schedule_data:
        date_start = row[0]
        if date_start not in sorted_schedule:
            sorted_schedule[date_start] = []
        sorted_schedule[date_start].append(row)
    
    sorted_schedule = {day: sorted_schedule.get(day, []) for day in days_of_week}
    
    return sorted_schedule

def get_groups():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT groupname FROM schedule")
    groups = cursor.fetchall()
    conn.close()
    return groups

def get_teachers():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT teachername FROM schedule")
    teachers = cursor.fetchall()
    conn.close()
    return teachers

def get_auditories():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT auditory FROM schedule")
    auditories = cursor.fetchall()
    conn.close()
    return auditories

button_teacher = KeyboardButton('Поиск по преподавателю')
button_group = KeyboardButton('Поиск по группе')
button_auditory = KeyboardButton('Поиск по аудитории')
greet_kb = ReplyKeyboardMarkup()
greet_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_teacher).add(button_group).add(button_auditory)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    help_text = "Привет! Этот бот предоставляет расписание занятий для групп, преподавателей и аудиторий.\n\n" \
                "Вы можете использовать следующие команды:\n" \
                "/start - начать использование бота\n" \
                "Поиск по группе - выберите курс и группу для просмотра расписания по дням недели\n" \
                "Поиск по преподавателю - выберите преподавателя для просмотра его расписания\n" \
                "Поиск по аудитории - выберите аудиторию для просмотра расписания занятий\n" \
                "Выберите одну из доступных команд."
    await message.reply(help_text, reply_markup=greet_kb)

def check_subscription_status(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT subscribed FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        subscribed = bool(result[0])
    else:
        subscribed = False
    return subscribed

@dp.message_handler(text=['Поиск по преподавателю'])
async def start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    teachers = get_teachers()
    for teacher in teachers:
        keyboard.add(types.InlineKeyboardButton(text=teacher[0], callback_data=f'show_teacher_schedule:{teacher[0]}'))
    await message.reply("🧑‍🏫 Выберите преподавателя:", reply_markup=keyboard)

@dp.message_handler(text=['Поиск по аудитории'])
async def start_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    auditories = get_auditories()
    for auditory in auditories:
        keyboard.add(types.InlineKeyboardButton(text=auditory[0], callback_data=f'show_auditory_schedule:{auditory[0]}'))
    await message.reply("📖 Выберите аудиторию:", reply_markup=keyboard)

@dp.message_handler(text=['Поиск по группе'])
async def start_group_search(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton(text='1 курс', callback_data='select_course:1'),
        types.InlineKeyboardButton(text='2 курс', callback_data='select_course:2')
    )
    keyboard.row(
        types.InlineKeyboardButton(text='3 курс', callback_data='select_course:3'),
        types.InlineKeyboardButton(text='4 курс', callback_data='select_course:4')
    )
    await message.reply("🎓 Выберите курс:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('select_course:'))
async def select_course(callback_query: types.CallbackQuery):
    course = callback_query.data.split(':')[1]
    keyboard = types.InlineKeyboardMarkup()
    groups = get_groups_by_course(course)
    if groups:
        for group in groups:
            keyboard.add(types.InlineKeyboardButton(text=group[0], callback_data=f'show_group_schedule:{group[0]}'))
        await callback_query.message.answer("📖 Выберите группу:", reply_markup=keyboard)
    else:
        await callback_query.message.answer("Для выбранного курса нет доступных групп. 🧐")
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('show_group_schedule:'))
async def show_group_schedule(callback_query: types.CallbackQuery):
    group_name = callback_query.data.split(':')[1]
    keyboard = types.InlineKeyboardMarkup()
    days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for day in days_of_week:
        keyboard.add(types.InlineKeyboardButton(text=day, callback_data=f'select_day:{day}:{group_name}'))
    await callback_query.message.answer("📅 Выберите день недели:", reply_markup=keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('show_teacher_schedule:'))
async def show_teacher_schedule(callback_query: types.CallbackQuery):
    teacher_name = callback_query.data.split(':')[1]
    schedule_data_teacher = await get_schedule_for_teacher(teacher_name)
    if schedule_data_teacher:
        formatted_message_teacher = format_schedule_message_teacher(schedule_data_teacher)
        await callback_query.message.answer(formatted_message_teacher, parse_mode=types.ParseMode.HTML)
    else:
        await callback_query.message.answer("Для выбранного преподавателя нет расписания. 😞")
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('show_auditory_schedule:'))
async def show_teacher_schedule(callback_query: types.CallbackQuery):
    auditory_name = callback_query.data.split(':')[1]
    schedule_data_auditory = await get_schedule_for_auditory(auditory_name)
    if schedule_data_auditory:
        formatted_message_auditory = format_schedule_message_auditory(schedule_data_auditory)
        await callback_query.message.answer(formatted_message_auditory, parse_mode=types.ParseMode.HTML)
    else:
        await callback_query.message.answer("В выбранной аудитории нет занятий. 📖")
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith('select_day:'))
async def select_day(callback_query: types.CallbackQuery):
    day = callback_query.data.split(':')[1]
    group_name = callback_query.data.split(':')[2]
    schedule_data = await get_schedule_for_group(group_name)
    sorted_schedule = sort_schedule_by_day(schedule_data)
    if day in sorted_schedule:
        day_schedule_data = sorted_schedule[day]
        formatted_message = format_schedule_message(day_schedule_data)
        await callback_query.message.answer(formatted_message, parse_mode=types.ParseMode.HTML)
    else:
        await callback_query.message.answer("Расписание для выбранного дня недоступно. 😞")
    await callback_query.answer()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)

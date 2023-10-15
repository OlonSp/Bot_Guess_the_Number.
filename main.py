from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import random

BOT_TOKEN = 'Your bot token'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPT = 7

user = {}

async def Process_Start_Command(message: Message):
    await message.answer("Привет, давай сыграем в игру, я загадаю число от 1 до 100, а ты побробуешь отгадать\nИграем?")
    if message.from_user.id not in user:
        user[message.from_user.id] = {
            "in_game": False,
            "attepmt_left": None,
            "random_number": None,
            "all_game": 0,
            "win_game": 0
            }

async def Process_Help_Command(message: Message):
    await message.answer("Я бот - угадай число, я загадываю число от 1 до 100, а ты пробуешь его отгадать, у тебя будет всего 5 попыток.\n"
                        "Если ты пришёл в первый раз напиши /start, чтобы зарегестрироваться и иметь возможность играть.\n"
                        "Напиши /cancel если захочешь покинуть игру, /stat - чтобы увидеть свою статистику ")

async def Process_cancel_Command(message: Message):
    if user[message.from_user.id]["in_game"]:
        user[message.from_user.id]["in_game"] = False
        await message.answer("Жаль, напиши да, если захочешь сыграть")
    else:
        await message.answer("Так мы и так не играем, напиши да чтобы сыграть")

async def Process_stat(message: Message):
    if not(user[message.from_user.id]["in_game"]):
        await message.answer(f"Ты сыграл со мной {user[message.from_user.id]['all_game']} раз, из них победных - {user[message.from_user.id]['win_game']}")
    else:
        await message.answer("Мы сейчас играем, напиши число от 1 до 100")

async def Process_Yes(message: Message):
    if user[message.from_user.id]["in_game"]:
        await message.answer("Мы уже играем, введите число от 1 до 100")
    else:
        user[message.from_user.id]["in_game"] = True
        user[message.from_user.id]["attepmt_left"] = ATTEMPT
        user[message.from_user.id]["random_number"] = random.randint(1, 100)
        await message.answer("Угадай моё число от 1 до 100")

async def Process_No(message: Message):
    if user[message.from_user.id]["in_game"]:
        await message.answer("Мы уже играем, напиши число от 1 до 100")
    else:
        await message.answer("Жаль, напиши да, если захочешь сыграть")

async def Process_game(message: Message):
    if user[message.from_user.id]["in_game"]:
        if int(message.text) == user[message.from_user.id]["random_number"]:
            user[message.from_user.id]["all_game"] += 1
            user[message.from_user.id]["in_game"] = False
            user[message.from_user.id]["win_game"] += 1
            await message.answer("Ты победил!!!!Ура!!!\nХочешь ещё сыграть?")
        elif (int(message.text) <= user[message.from_user.id]["random_number"]):
            user[message.from_user.id]["attepmt_left"] -= 1
            await message.answer("Моё число больше")
        elif (int(message.text) >= user[message.from_user.id]["random_number"]):
            user[message.from_user.id]["attepmt_left"] -= 1
            await message.answer("Моё число меньше")

        if (user[message.from_user.id]["attepmt_left"] == 0):
            await message.answer("Ты проиграл! Моё число: " + str(user[message.from_user.id]["random_number"] + "."))
            user[message.from_user.id]["all_game"] += 1
            user[message.from_user.id]["in_game"] = False
    else:
        await message.answer("Я не понимаю, что ты пишешь. Напиши да или нет")

async def Process_other_message(message: Message):
    if user[message.from_user.id]["in_game"]:
        await message.answer("Введите число от 1 до 100")
    else:
        await message.answer("Я не понимаю, что ты пишешь. Напиши да или нет")

dp.message.register(Process_Start_Command, Command(commands='start'))
dp.message.register(Process_Help_Command, Command(commands='help'))
dp.message.register(Process_stat, Command(commands='stat'))
dp.message.register(Process_cancel_Command, Command(commands='cancel'))
dp.message.register(Process_Yes, F.text.lower().in_(["да", "погнали", "давай", "давай сыграем", "играем"]))
dp.message.register(Process_No, F.text.lower().in_(["нет", "не хочу", "неа", "отказываюсь"]))
dp.message.register(Process_game, lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.message.register(Process_other_message)

if __name__ == '__main__':
    dp.run_polling(bot)

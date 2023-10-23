from aiogram import Bot, Dispatcher, F
from aiogram.types import ContentType, Message
from aiogram.filters import Command, CommandStart
from random import randint

# bot game
BOT_TOKEN = ''
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5
user = {'in_game': False,
        'num': None,
        'attempts': None,
        'total_games': 0,
        'wins': 0}
keys1 = ['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']
keys2 = ['нет', 'не', 'не хочу', 'не буду']
def random_num() -> int:
    return randint(1, 100)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!\nНе хочешь поиграть в игру угать число?\n/help - подробные правила.')

@dp.message(Command(commands='help'))
async def start(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )

@dp.message(Command(commands='stat'))
async def stat(message: Message):
    await message.answer(f'Всего игр: {user["total_games"]}\n'
                   f'Победы: {user["wins"]}.')
    if user['in_game']:
        await message.answer('Ты в игре.\n'
                             f'Осталось {user["attempts"]} попытки.')
    else:
        await message.answer('Сыграем?')


@dp.message(Command(commands='cancel'))
async def cancel(message: Message):
    user['in_game'] = False if user['in_game'] else user['in_game']
    if user['in_game']:
        await message.answer('А мы итак с вами не играем.\n'
                             'Может, сыграем разок?')
    else:
        await message.answer('Игра закончилась.\n'
                             'Если захотите сыграть снова '
                             '- напишите об этом.')


@dp.message(F.text.lower().in_(keys1))
async def game(message: Message):
    if user['in_game']:
        await message.answer('Пока мы играем в игру я могу '
                            'реагировать только на числа от 1 до 100 '
                            'и команды /cancel и /stat')
    else:
        user['in_game'] = True
        user['attempts'] = ATTEMPTS
        user['num'] = random_num()
        await message.answer('Число от 1 до 100 загадано.\n'
                             'Попробуй угадать!')

@dp.message(F.text.lower().in_(keys2))
async def no_game(message:Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n'
                             'Захотите - напишите.')

    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and int(x.text) in range(1, 101))
async def game_on(message: Message):
    if user['in_game']:
        if int(message.text) == user['num']:
            user['in_game'] = False
            user['total_games'] += 1
            user['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > user['num']:
            user['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < user['num']:
            user['attempts'] -= 1
            await message.answer('Мое число больше')

        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {user["num"]}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def any(message: Message):
    if user['in_game']:
        await message.answer('Ты сейчас в игре, жду от тебя число от 1 до 100.')

    else:
        await message.answer('Действуй согласно инструкциям, мои дествия ограничены.')


if __name__ == '__main__':
    dp.run_polling(bot)


class BotEmoji:
    green_checkmark = '\U00002705'
    green_circle = '\U0001F7E2'
    red_cross = '\U0000274C'
    red_circle = '\U0001F534 '
    sparkles = '\U00002728'
    star = '\U00002B50'
    trophy = '\U0001F3C6'
    like = '\U0001F44D'
    dislike = '\U0001F44E'
    biceps = '\U0001F4AA'
    party_popper = '\U0001F389'
    stop_sign = '\U0001f6d1'
    hundred_points = '\U0001F4AF'
    waving_hand = '\U0001F44B'
    writing_hand = '\U0000270D'
    eyes = '\U0001F440'
    menu = '\U00002630'
    books = '\U0001F4DA'
    graduation_cap = '\U0001F393'


class BotVocabulary:
    command_start = f'Приветствую! {BotEmoji.waving_hand} Меня зовут Василий Питонов и я помогу Вам подготовиться к ЕГЭ по информатике {BotEmoji.sparkles}\n' \
        + 'Со мной Вы можете потренироваться решать задания, предполагающие выбор варианта ответа или краткий ответ. ' \
        + f'Все задания взяты из открытого банка заданий ЕГЭ и разбиты по соответствующим категориям и подкатегориям. Выберите одну из них и давайте начнём {BotEmoji.biceps}\n' \
        + f'Также не забывайте использовать {BotEmoji.menu} меню в левой нижней части экрана для навигации.'
    command_menu = f'Вы находитесь в меню выбора заданий. Выберите категорию {BotEmoji.books}'
    choose_subcategory = f'Хороший выбор!{BotEmoji.like}\nТеперь выберите подкатегорию или вернитесь назад для выбора другой категории {BotEmoji.writing_hand}'
    command_statistic = 'Это сообщение выводится при команде statistic' 
    message_poll = f'{BotEmoji.stop_sign} Вам нужно выбрать один из вариантов ответа на поставленный вопрос.'
    message_success = f'{BotEmoji.green_circle} Правильно! Продолжайте в том же духе!'
    message_failure = f'{BotEmoji.red_circle} Неправильно! Запомните, в чём была ошибка, чтобы больше её не допускать.'

    @classmethod
    def message_no_more_questions(cls, result, numbers, subcategory_name):
        return f'Поздравляем! {BotEmoji.party_popper}\n'\
                + f'Вы завершили все задания в подкатегории «{subcategory_name}» с результатом {result} из {numbers} {BotEmoji.hundred_points}\n\n' \
                + f'Хотите сбросить текущий прогресс и начать решать задания сначала или вернуться в главное меню для выбора другой категории?'

        
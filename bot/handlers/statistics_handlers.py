from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from ..models import Results, Assignment
from ..keyboards.statistics_keyboards import make_statistics_keyboard
from ..keyboards.factories import StatisticCategoryCallbackFactory
from ..services.vocabulary import BotVocabulary

router = Router()


@router.message(Command(commands=['results']))
async def start_command(message: Message, state: FSMContext):
    """
    Обработчик команды /results отправляет сообщение с общей статистикой 
    пользователя по разделам и инлайн-клавиатурой со статистикой по каждому
    из разделом с возможностью сброса прогресса.
    """
    await state.clear()
    
    results_success = await Results.objects.filter(
        user__user_id=message.from_user.id, 
        status=True
    ).acount()
    results_failure = await Results.objects.filter(
        user__user_id=message.from_user.id, 
        status=False
    ).acount()
    all_assignments = await Assignment.objects.all().acount()
    
    await message.answer(
        text=BotVocabulary.results(
            results_success=results_success, 
            results_failure=results_failure, 
            all_assignments=all_assignments
        ),
        reply_markup=await make_statistics_keyboard(message.from_user.id)
    )
    

@router.callback_query(StatisticCategoryCallbackFactory.filter())
async def restart_category(
    callback: CallbackQuery, 
    callback_data: StatisticCategoryCallbackFactory
):
    """
    Обработчик нажатия инлайн-кнопки сброса прогресса по разделу, при наличии 
    результатов пользователя по нему, удаляет его результаты. 
    """
    result = await Results.objects.filter(
        user__user_id=callback.from_user.id
    ).afirst()
    if result:
        await Results.objects.filter(
            user__user_id=callback.from_user.id,
            category__id=callback_data.category_id
        ).adelete()
        
        await callback.message.edit_reply_markup(
            reply_markup=await make_statistics_keyboard(callback.from_user.id)
        )
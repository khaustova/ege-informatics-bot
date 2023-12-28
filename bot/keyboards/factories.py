from aiogram.filters.callback_data import CallbackData


class CategoryCallbackFactory(CallbackData, prefix='category'):
    category_id: int
    
class StatisticCategoryCallbackFactory(CallbackData, prefix='delete_category'):
    category_id: int

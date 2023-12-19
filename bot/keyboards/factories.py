from aiogram.filters.callback_data import CallbackData


class CategoryCallbackFactory(CallbackData, prefix='category'):
    category_id: int
    
    
class SubcategoryCallbackFactory(CallbackData, prefix='subcategory'):
    subcategory_id: int
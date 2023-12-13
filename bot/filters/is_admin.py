from aiogram.filters import BaseFilter
from aiogram.types import Message
from ..models import User

class IsAdmin(BaseFilter):
    
    async def __call__(self, message: Message) -> bool:
        user = await User.objects.aget(user_id=message.from_user.id)
        return user.is_admin
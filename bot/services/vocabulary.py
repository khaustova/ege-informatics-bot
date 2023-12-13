from ..models import Quiz

class BotVocabulary:
    async def start():
        quiz = await Quiz.objects.aget(id=1)
        return quiz.question
from asgiref.sync import sync_to_async
from random import randint  
from django.db.models import Subquery, OuterRef
from django.db.models.aggregates import Count
from .models import Assignment, Results, Category, Subcategory


@sync_to_async
def get_question(user_id):
    questions = Assignment.objects.exclude(
        pk__in=Subquery(
            Results.objects.filter(
                user__user_id=user_id, 
                question=OuterRef('pk')
            ).values('question')
        )
    )
    
    if questions.all().exists():
        count = questions.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return questions.all()[random_index]
    
    return None


@sync_to_async
def get_categories():
    return list(Category.objects.all().values())


@sync_to_async
def get_subcategories(category_id):
    return list(Subcategory.objects.filter(category__id=category_id).values())
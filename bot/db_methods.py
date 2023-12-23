from asgiref.sync import sync_to_async
from random import shuffle
from django.db.models import Subquery, OuterRef
from .models import Assignment, Results, Category, Subcategory


@sync_to_async
def get_assignments_ids(user_id: int, subcategory_id: int) -> list[int]:
    assignments: Assignment = Assignment.objects.filter(
        subcategory__id=subcategory_id).exclude(
            pk__in=Subquery(
                Results.objects.filter(
                    user__user_id=user_id, 
                    question=OuterRef('pk')
                ).values('question')
            )
    ).values()
    
    assignments_ids: list[str] = []
    for assignment in assignments:
        assignments_ids.append(str(assignment['id']))
        
    shuffle(assignments_ids)
    
    return '_'.join(assignments_ids)


@sync_to_async
def get_categories():
    return list(Category.objects.all().values())


@sync_to_async
def get_subcategories(category_id):
    return list(Subcategory.objects.filter(category__id=category_id).values())
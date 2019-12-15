from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return

    for cat in instance.category.all():
        slug = cat.slug

        new_count = 0
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()

        Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    for c in Category.objects.all():
        Category.objects.filter(slug=c.slug).update(todos_count=0)

    cat_counter = Counter()  
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            cat_counter[cat.slug] += 1

    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)

all_priority_counter = {}

@receiver(post_save, sender=TodoItem)
def priority_low_counter(sender, instance, created, using, update_fields, raw, **kwargs):

    priority_counter = Counter()
    for t in TodoItem.objects.all():
        if t.priority == 3:
            priority_counter['Низкий приоритет'] += 1

    all_priority_counter['Низкий приоритет'] = priority_counter['Низкий приоритет']

@receiver(post_save, sender=TodoItem)
def priority_medium_counter(sender, instance, created, using, update_fields, raw, **kwargs):

    priority_counter = Counter()
    for t in TodoItem.objects.all():
        if t.priority == 2:
            priority_counter['Средний приоритет'] += 1

    all_priority_counter['Средний приоритет'] = priority_counter['Средний приоритет']

@receiver(post_save, sender=TodoItem)
def priority_high_counter(sender, instance, created, using, update_fields, raw, **kwargs):

    priority_counter = Counter()
    for t in TodoItem.objects.all():
        if t.priority == 1:
            priority_counter['Высокий приоритет'] += 1

    all_priority_counter['Высокий приоритет'] = priority_counter['Высокий приоритет']
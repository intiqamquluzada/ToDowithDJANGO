from django.db import models
from services.mixin import DateMixin, SlugMixin
from services.choices import TODO_STATUS
from services.generator import Generator
from django.contrib.auth import get_user_model
User = get_user_model()


class Todo(DateMixin, SlugMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    task_name = models.CharField(max_length=200)
    deadline = models.DateField()
    status = models.CharField(max_length=100, choices=TODO_STATUS, default='Uncompleted')

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Generator.create_slug_shortcode(size=15, model_=Todo)
        super(Todo, self).save(*args, **kwargs)

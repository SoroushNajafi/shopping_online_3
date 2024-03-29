from django.db import models


class Contact(models.Model):
    name = models.CharField(verbose_name='Name', max_length=200)
    email = models.EmailField(verbose_name='E-mail')
    message = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.name}: {self.email}'

from django.db import models
from django.contrib.auth.models import User

CATEGORIES = (
    ('N', 'Nature'),
    ('F', 'Food'),
    ('A', 'Animals'),
    ('S', 'Structure'),
    ('P', 'People'),
    ('L', 'Life')
)

class Contest(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    end_date = models.DateField()
    photo_url = models.CharField(max_length=150, default='https://via.placeholder.com/300x300')

    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    photo_url = models.CharField(max_length=150, default='https://i.imgur.com/IcvbvO5.jpg')
    category = models.CharField(
        max_length=1,
        choices=CATEGORIES,
        default='N'
    )
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

class Like(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(null=True,blank=True,upload_to='post_pics/')
    creation_date = models.DateTimeField(auto_now_add=True)
    amount_of_likes = models.IntegerField(default=0)
    amount_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.creator} posted: '{self.description[0:6]}...'"


class Comment(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    value = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    amount_of_likes = models.IntegerField(default=0)
    

    def __str__(self):
        return f"{self.creator} comments: '{self.value[0:6]}...'"

class Like(models.Model):
    like_owner = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.like_owner} liked post: {self.post}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField('Profile',symmetrical=False,blank=True)
    image = models.ImageField(null=True,blank=True,upload_to='profile_pics/')
    
    

    

    


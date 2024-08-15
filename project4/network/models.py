from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Creatpost(models.Model):
    postcontent = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authorofpost")
    datecreated = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H %M %S')}"
    
class Follower (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="following")
    userfollowers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__ (self):
        return f"{self.user} is following {self.userfollowers}"
    
class Likepost (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="usewholiked")
    post = models.ForeignKey(Creatpost,on_delete=models.CASCADE, related_name="postliked")

    def __str__ (self):
        return f"{self.user} liked {self.post}"
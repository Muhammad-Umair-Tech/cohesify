from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

import os

# Create your models here.
class User(AbstractUser):
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    # blank=True means that a User can have zero friends
    # symmetrical=True means that if A friends B, B automatically friends A
    profile_picture = models.ImageField(
        upload_to="cohesify/profile_pictures/",
        default="cohesify/default_content/default_profile_picture.png",
        blank=True
    )
    # blank=True means the user can register without a profile picture

    # A property is a method that can be accessed like a data attribute, allowing easy encapsulation and pre-computation
    @property
    def friends_count(self):
        return self.friends.count()
    
    @property
    def posts_count(self):
        return self.posts.count()
    
    @property
    def trimmed_firstname(self):
        name = self.first_name
        if len(name) > 5:
            name = self.first_name[:5] + "..."
        return name
    
    @property
    def liked_posts(self):
        user_likes = Like.objects.filter(liker=self)
        return [l.post for l in user_likes]
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)

    caption = models.TextField(max_length=1000)
    media = models.FileField(upload_to="cohesify/posts/", blank=True, null=False)

    @property
    def is_photo(self):
        return self.media.name.lower().endswith((
            ".png", ".jpg", ".jpeg", ".gif", ".webp"
        ))
    
    @property
    def is_video(self):
        return self.media.name.lower().endswith((
            ".mp4", ".mkv", ".mov", ".webm", ".avi"
        ))
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.id}. Auth: {self.author}, Created at {self.created_at}"
    

# Whenever a profile picture is updated, before these updates are saved in the DB
# a pre_save signal is sent. This function receives that signal, and deletes the
# previous profile picture if the new one is different

# Here, sender is a class, and the decorator always plugs the Post class as sender
@receiver(pre_save, sender=User)
def delete_old_media_on_update(sender, instance, **kwargs):
    if not instance.pk: # If the object doesn't exist
        return
    
    # Get the old profile pic if the sender exist
    try:
        old_media = sender.objects.get(pk=instance.pk).profile_picture
    except sender.DoesNotExist:
        return
    
    new_media = instance.profile_picture

    old_media_name = os.path.basename(old_media.name)
    if old_media and old_media != new_media and old_media_name != "default_profile_picture.png":
        old_media.delete(save=False) # Do not update the DB


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"By {self.liker} on {self.post}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return f"By {self.author} on {self.post}: {self.text}"




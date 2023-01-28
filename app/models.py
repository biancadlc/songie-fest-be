from django.db import models


class User(models.Model):  
    username = models.CharField(max_length=36)
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    email = models.CharField(max_length=36)
    password = models.CharField(max_length=16)
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username)


class MusicPost(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)


class Song(models.Model): 
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    music_post = models.ForeignKey(MusicPost, on_delete=models.CASCADE)
    play_count = models.IntegerField()
    date_published = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    music_post= models.ForeignKey(MusicPost, related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    date_published = models.DateTimeField(auto_now_add=True)
    

class Like(models.Model):
    # user = represents user who liked post, deleting user deletes like
    user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE)
    music_post = models.ForeignKey(MusicPost, related_name='like', on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    
    


# class Profile(models.Model): 
    # 1:1 relationship w/ Django User model
    # if User deleted, profile destroyed too
    # user = models.OneToOneField(User, on_delete=models.CASCADE) 
    # optional? for storing profile pic of user
    # image = models.ImageField(default='default.png', upload_to='profile_pics') 
    # use AutoSlugField, set it to make a slug from user field
    # slug = AutoSlugField(populate_from='user')
    # store small intro? blank=True means it can be left blank
    # bio = models.CharField(max_length=255, blank=True)
    # many to many w/ Profile model, can be left blank 
    # every user can have multiple friends & can be frends w/ multiple ppl
    # friends = models.ManyToManyField("Profile", blank=True)x     # stretch
    
    
    
            
    # define get_absolute_url toget the abs URL for that profile
    # def get_absolute_url(self):
    #     return "/users/{}".format(self.slug)      


    

    

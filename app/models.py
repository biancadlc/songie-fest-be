from django.db import models


class User(models.Model):  
    username = models.CharField(max_length=36)
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    email = models.CharField(max_length=36)
    password = models.CharField(max_length=16)
    date_published = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.username)


class MusicPost(models.Model):   
    user = models.ForeignKey(User, related_name='music_posts',on_delete=models.CASCADE, null=True) 
    date_published = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    
    def __str__(self):
        date = str(self.date_published).split(' ')[0]
        object_string = f"{self.user} posted on {date}"
        return object_string


class Song(models.Model): 
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    music_post = models.ForeignKey(MusicPost, related_name='songs', on_delete=models.CASCADE)
    play_count = models.IntegerField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        object_string = f'{self.title} by {self.artist}'
        return object_string


class Comment(models.Model):
    music_post= models.ForeignKey(MusicPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    date_published = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return str(self.text)

    # class Meta:
    #     ordering = ('date_published',)
        
    # def __str__(self):
    #     return 'Comment by {} on {}'.format(self.username, self.music_post)



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


    

    

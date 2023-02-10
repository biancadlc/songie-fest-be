from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token




class MyUserManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email), #turns email to lowercase
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):  
    username = models.CharField(max_length=36, unique=True)
    first_name = models.CharField(max_length=36)
    last_name = models.CharField(max_length=36)
    email = models.CharField(max_length=36, unique=True)
    # password = models.CharField(max_length=36)
    date_published = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] #anything you add 
    #here you need to ass to create_user param in usermanager
    objects = MyUserManager()

    def __str__(self):
        return str(self.username)
    
    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):  
        return True
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    


data = {
    'biancadlc': [
        {'id': 1,
        'likes_count': 9,
        'date_published': 'Feb',
        'songs': [
                    {'id': 4,
                    'title':'Yellow ',
                    'artist': 'Coldplay',
                    'frequency_count': 200 },
                    {'id': 5,
                    'title':'Rainbo ',
                    'artist': 'JustaGent',
                    'frequency_count': 90 }
                            ]
        },
        {'id': 2,
        'likes_count': 9,
        'date_published': 'april',
        'songs': [
            {'id': 6,
            'title':'Fix you ',
            'artist': 'Coldplay',
            'frequency_count': 8 },
            {'id': 7,
            'title':'Hold on ',
            'artist': 'jonas',
            'frequency_count': 400 }
            ]
        }],
    'thaolee': [
        {'id': 3,
        'likes_count': 9,
        'date_published': 'Feb',
        'songs': [
                {'id': 8,
                'title':'Yellow ',
                'artist': 'Coldplay',
                'frequency_count': 200 },
                {'id': 9,
                'title':'Rainbo ',
                'artist': 'JustaGent',
                'frequency_count': 90 }]
                },
        {'id': 4,
        'likes_count': 9,
        'date_published': 'april',
        'songs': [
                {'id': 10,
                'title':'Fix you ',
                'artist': 'Coldplay',
                'frequency_count': 8 },
                {'id': 11,
                'title':'Hold on ',
                'artist': 'jonas',
                'frequency_count': 400 }]
                }]
    }


class MusicPost(models.Model):   
    user = models.ForeignKey(User, related_name='music_posts',on_delete=models.CASCADE, null=True) 
    username = models.CharField(max_length=36, null=True)
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


    

    

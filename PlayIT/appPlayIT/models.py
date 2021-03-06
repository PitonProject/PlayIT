from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Pub(models.Model):
    name = models.TextField()
    street = models.TextField()
    number = models.IntegerField()
    city = models.TextField()
    zipCode = models.TextField(blank=True, null=True)
    stateOrProvince = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/pub/" + str(self.pk)

class User_Pub(models.Model):
    user = models.ForeignKey(User)
    pub = models.ForeignKey(Pub)
    class Meta:
        unique_together = ('user', 'pub')
    def __unicode__(self):
        return self.user.username + " - " +  self.pub.name

class Playlist(models.Model):
    pub = models.ForeignKey(Pub, related_name='playlists')
    name = models.TextField()
    user = models.ForeignKey(User, default=1)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/playlist/" + str(self.pk)

class Track(models.Model):
    spotify_id = models.TextField(primary_key=True)
    name = models.TextField()
    artist = models.TextField()
    #spotify_artist_id = models.TextField()
    album = models.TextField()
    #spotify_album_id = models.TextField()
    def __unicode__(self):
        return self.name + " - " + self.artist

class Playlist_Track(models.Model):
    playlist = models.ForeignKey(Playlist)
    track = models.ForeignKey(Track)
    user = models.ForeignKey(User)
    class Meta:
        unique_together = ('playlist', 'track')
    def __unicode__(self):
        return self.playlist.name + " - " +  self.track.name

class Review(models.Model):
    RATING_CHOICES = ((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'))
    rating = models.PositiveSmallIntegerField('Ratings (stars)', blank=False, default=3, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, default=1)
    date = models.DateField(default=date.today)
    pub = models.ForeignKey(Pub)
    def __unicode__(self):
        return self.pub.name + " - " + str(self.rating)
    def get_absolute_url(self):
        return "/pub/" + str(self.pub.pk)
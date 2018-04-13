from django.db import models
from django.utils.safestring import mark_safe


class Lyrics(models.Model):
    title = models.CharField(max_length=70)
    pub_date = models.DateField()
    text = models.TextField()
    written_by = models.CharField(max_length=800)
    remarks = models.CharField(max_length=100)
    replaced_new_lines = models.BooleanField()

    def __str__(self):
        return self.title

    def safe_text(self):
        return mark_safe(self.text)


class Correction(models.Model):
    by = models.CharField(max_length=70)
    date_time = models.DateTimeField()
    song_title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.by


class SubmittedLyrics(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=255)
    date = models.DateField()
    lyrics = models.TextField()
    replaced_new_lines = models.BooleanField()
    published = models.BooleanField()

    def __str__(self):
        return self.title

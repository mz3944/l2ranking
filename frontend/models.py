from datetime import datetime
import decimal

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from django.contrib.auth import models as auth_models
from django.db import models as db_models

class Category(db_models.Model):
    slug = db_models.SlugField(max_length=80, primary_key=True)
    name = db_models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

class Server(db_models.Model):
    name = db_models.CharField(max_length=80)
    description = db_models.TextField(max_length=250)
    category = db_models.ForeignKey(Category)
    website = db_models.URLField(max_length=80)
    banner = db_models.ImageField(upload_to='banners', blank=True)

    # Extra Info
    exp_rate = db_models.PositiveSmallIntegerField(default=1)
    sp_rate = db_models.PositiveSmallIntegerField(default=1)
    drop_rate = db_models.PositiveSmallIntegerField(default=1)
    spoil_rate = db_models.PositiveSmallIntegerField(default=1)
    custom = db_models.BooleanField(default=False)
    donation = db_models.BooleanField(default=False)

    # Stats
    vote_count = db_models.PositiveIntegerField(default=0)
    in_stat = db_models.PositiveIntegerField(default=0)
    out_stat = db_models.PositiveIntegerField(default=0)
    rating = db_models.DecimalField(default=0.0, max_digits=2, decimal_places=1)

    # Misc
    user = db_models.ForeignKey(auth_models.User)
    create_date = db_models.DateTimeField(default=datetime.now, editable=False)
    modify_date = db_models.DateTimeField(default=datetime.now, editable=False)

    def add_vote(self):
        self.vote_count += 1
        self.save()

    def __unicode__(self):
        return self.name

class Vote(db_models.Model):
    character = db_models.CharField(max_length=80)
    server = db_models.ForeignKey(Server)
    ip_address = db_models.IPAddressField()

    # Misc
    create_date = db_models.DateTimeField(default=datetime.now, editable=False)

    def __unicode__(self):
        return '%(server_name)s (%(ip_address)s) @ %(create_date)s' % {
            'server_name': self.server.name,
            'ip_address': self.ip_address,
            'create_date': self.create_date,
        }

class Review(db_models.Model):
    body = db_models.TextField(max_length=500)
    rating = db_models.PositiveSmallIntegerField(default=5)
    server = db_models.ForeignKey(Server)

    # Misc
    user = db_models.ForeignKey(auth_models.User)
    create_date = db_models.DateTimeField(default=datetime.now, editable=False)
    modify_date = db_models.DateTimeField(default=datetime.now, editable=False)

    def __unicode__(self):
        return self.server.name

class News(db_models.Model):
    title = db_models.CharField(max_length=80)
    body = db_models.TextField(max_length=1000)
    excerpt = db_models.TextField(max_length=200)

    # Misc
    create_date = db_models.DateTimeField(default=datetime.now, editable=False)
    modify_date = db_models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        verbose_name_plural = 'news'

    def __unicode__(self):
        return self.title

# Update server rating
@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def test(sender, **kwargs):
    obj = kwargs['instance']
    total_rating = 0
    reviews = Review.objects.filter(server=obj.server)
    for review in reviews:
        total_rating += review.rating

    # Avoid zero division
    if reviews.count() > 0:
        rating = round(decimal.Decimal(total_rating) / decimal.Decimal(reviews.count()), 1)
    else:
        rating = 0

    obj.server.rating = rating
    obj.server.save()
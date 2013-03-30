from django.contrib.auth import models as auth_models
from django.db import models as db_models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


class Category(db_models.Model):
    """
    Model represents server category.
    """

    slug = db_models.SlugField(max_length=80, primary_key=True)
    name = db_models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class Server(db_models.Model):
    """
    Model represents servers.
    """

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
    last_rank = db_models.IntegerField(default=0)

    # Misc
    user = db_models.ForeignKey(auth_models.User)
    create_date = db_models.DateTimeField(default=timezone.now, editable=False)
    modify_date = db_models.DateTimeField(default=timezone.now, editable=False)

    def is_owner(self, user_obj):
        if self.user == user_obj:
            return True
        return False

    def add_vote(self):
        self.vote_count += 1
        self.save()

    def __unicode__(self):
        return self.name


class Vote(db_models.Model):
    """
    Model represents server votes.
    """

    character = db_models.CharField(max_length=80)
    server = db_models.ForeignKey(Server)
    ip_address = db_models.IPAddressField()

    # Misc
    create_date = db_models.DateTimeField(default=timezone.now, editable=False)

    def __unicode__(self):
        return '%(server_name)s (%(ip_address)s) @ %(create_date)s' % {
            'server_name': self.server.name,
            'ip_address': self.ip_address,
            'create_date': self.create_date,
        }


class Review(db_models.Model):
    """
    Model represents server reviews.
    """

    RATE_CHOICES = (
        (1, u'Poor'),
        (2, u'Fair'),
        (3, u'Good'),
        (4, u'Very Good'),
        (5, u'Excellent'),
    )

    body = db_models.TextField(max_length=500)
    rating = db_models.PositiveSmallIntegerField(default=5, choices=RATE_CHOICES)
    server = db_models.ForeignKey(Server)

    # Misc
    user = db_models.ForeignKey(auth_models.User)
    create_date = db_models.DateTimeField(default=timezone.now, editable=False)
    modify_date = db_models.DateTimeField(default=timezone.now, editable=False)

    def __unicode__(self):
        return '%(server)s reviewed by %(user)s (%(user_rating)s/%(overall_rating)s)' % {
            'server': self.server.name,
            'user': self.user.username,
            'user_rating': self.rating,
            'overall_rating': self.server.rating,
        }


class News(db_models.Model):
    """
    Model represents news.
    """

    title = db_models.CharField(max_length=80)
    body = db_models.TextField(max_length=1000)
    excerpt = db_models.TextField(max_length=200)

    # Misc
    create_date = db_models.DateTimeField(default=timezone.now, editable=False)
    modify_date = db_models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name_plural = 'news'

    def __unicode__(self):
        return self.title


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_server_rating(sender, **kwargs):
    """
    Function updates server rating after review is created, updated or deleted.
    """

    obj = kwargs['instance']

    ratings = [review.rating for review in Review.objects.filter(server=obj.server)]
    rating = round(float(sum(ratings)) / len(ratings), 1) if len(ratings) > 0 else 0

    obj.server.rating = rating
    obj.server.save()
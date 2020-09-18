from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.storage import default_storage as storage


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        #img = Image.open(storage.open(self.image.path))

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if img.height > 180 or img.width > 180:
            output_size = (180, 180)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Contact(models.Model):
    user_from = models.ForeignKey(
        'auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        'auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))

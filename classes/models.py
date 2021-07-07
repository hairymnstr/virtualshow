from django.db import models
from django.db import IntegrityError
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import Group

from PIL import Image
from PIL import ExifTags
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
import os, cgi

# Create your models here.
class ShowSection(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True)
    static_content = models.TextField(blank=True)
    group = models.ForeignKey(Group)
    show_results = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and self.slug == "":
            self.slug = slugify(self.name[:ShowSection._meta.get_field('slug').max_length])
        super(ShowSection, self).save(*args, **kwargs)

class ShowClass(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    show_age = models.BooleanField()
    section = models.ForeignKey('ShowSection')
    
    class Meta:
        verbose_name_plural = "show classes"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id and self.slug == "":
            self.slug = slugify(self.name[:ShowClass._meta.get_field('slug').max_length])
        super(ShowClass, self).save(*args, **kwargs)

class EntryImage(models.Model):
    img = models.ImageField(upload_to="images")
    thumbnail = models.ImageField(upload_to="images", blank=True, null=True)
    entry = models.ForeignKey('ClassEntry')

    class Meta:
        ordering = ['entry__show_class', 'entry__place', 'entry__entry_no', 'pk']

    def index_in_entry(self):
        entry_images = EntryImage.objects.filter(entry__pk=self.entry.pk)
        for x in range(entry_images.count()):
            if entry_images[x].pk == self.pk:
                break
        return x+1

    def preview_tag(self):
        return f'<img src="{self.thumbnail.url}" alt=""/>'
    preview_tag.short_description = "Preview"
    preview_tag.allow_tags = True
    
    def image_name(self):
        return f"class{self.entry.show_class.pk:02d}_entry{self.entry.entry_no:03d}"
    
    def make_thumbnail(self):
        if not self.img:
            return
    
        if (not isinstance(self.img.file, UploadedFile)) and (self.thumbnail):
            return
      
        THUMBNAIL_SIZE = (600,600)
    
        if isinstance(self.img.file, UploadedFile):
            if self.img.file.content_type in ('image/jpeg', 'image/mpo'):
                pil_type = 'jpeg'
                file_extension = 'jpg'
                content_type = 'image/jpeg'
            elif self.img.file.content_type == 'image/png':
                pil_type = 'png'
                file_extension = 'png'
                content_type = 'image/png'
            else:
                raise Exception(f"Unhandled image type: {self.img.file.content_type}")
        else:
            if os.path.splitext(self.img.name)[1].strip(".").lower() == "jpg":
                pil_type = 'jpeg'
                file_extension = 'jpg'
                content_type = 'image/jpeg'
            else:
                pil_type = 'png'
                file_extension = 'png'
                content_type = 'image/png'
        
        image = Image.open(BytesIO(self.img.read()))
        
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                try:
                    exif=dict(image._getexif().items())

                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
                except (AttributeError, KeyError):
                    # no Exif tags on this image
                    # or no orientation tag on this image
                    pass
        
                break

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    
        temp = BytesIO()
        image.save(temp, pil_type)
        temp.seek(0)
    
        fd = SimpleUploadedFile(os.path.split(self.img.name)[-1], 
                            temp.read(), content_type=content_type)
    
        thumbnail_name = f"{self.image_name()}.preview.{file_extension}"

        if(os.path.exists(os.path.join(settings.MEDIA_ROOT, thumbnail_name))):
            os.remove(os.path.join(settings.MEDIA_ROOT, thumbnail_name))
        self.thumbnail.save(thumbnail_name, fd, save=False)
        
    def scale_image(self):
        if not isinstance(self.img.file, UploadedFile):
            return
    
        if self.img.file.content_type in ('image/jpeg', 'image/mpo'):
            pil_type = 'jpeg'
            file_extension = 'jpg'
        elif self.img.file.content_type == 'image/png':
            pil_type = 'png'
            file_extension = 'png'
        else:
            raise Exception(f"Unhandled image type: {self.img.file.content_type}")
    
        if hasattr(self.img.file, 'temporary_file_path'):
            image = Image.open(self.img.file.temporary_file_path())
        else:
            # thumbnail will have already read the file from memory
            self.img.file.seek(0)
            image = Image.open(BytesIO(self.img.file.read()))
    
        
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                try:
                    exif=dict(image._getexif().items())
                    
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
                except (AttributeError, KeyError):
                    # no Exif tags on this image
                    pass
                break
        
        
        image.thumbnail((1600, 1600), Image.ANTIALIAS)
    
        temp = BytesIO()
        image.save(temp, pil_type)
        temp.seek(0)
    
        fd = SimpleUploadedFile(f"{self.image_name()}.{file_extension}", 
                            temp.read(),
                            content_type=self.img.file.content_type)
    
        self.img.save(f"{self.image_name()}.{file_extension}", fd, save=False)
    
    def save(self, *args, **kwargs):
        self.make_thumbnail()
        self.scale_image()
        super(EntryImage, self).save(*args, **kwargs)

class ClassEntry(models.Model):
    FIRST_PLACE = 1
    SECOND_PLACE = 2
    THIRD_PLACE = 3
    BEST_GUINEA_PIG = 5
    CHAMPION_DAIRY = 6
    RESERVE_CHAMPION_DAIRY = 7
    CHAMPION_BEEF = 8
    RESERVE_CHAMPION_BEEF = 9
    COMMENDATION = 98
    UNPLACED = 99
    PLACE_CHOICES = (
        (FIRST_PLACE, 'First'),
        (SECOND_PLACE, 'Second'),
        (THIRD_PLACE, 'Third'),
        (BEST_GUINEA_PIG, 'Best Guinea Pig'),
        (CHAMPION_DAIRY, 'Champion Dairy'),
        (RESERVE_CHAMPION_DAIRY, 'Reserve Champion Dairy'),
        (CHAMPION_BEEF, 'Champion Beef'),
        (RESERVE_CHAMPION_BEEF, 'Reserve Champion Beef'),
        (COMMENDATION, 'Highly Commended'),
        (UNPLACED, 'Unplaced'),
    )
    title = models.CharField(max_length=50)
    caption = models.TextField(blank=True, null=True)
    show_class = models.ForeignKey('ShowClass')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    entrant = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True, help_text="Intended for judges comments")
    age = models.IntegerField(blank=True, null=True, help_text="Only displayed in classes with the Show Age option selected")
    entry_no = models.IntegerField(blank=True, help_text="Leave blank on new entries to take the next number")
    place = models.IntegerField(choices=PLACE_CHOICES, default=UNPLACED)

    class Meta:
        verbose_name_plural = "class entries"
        ordering = ["show_class", "place", "entry_no"]
        unique_together = (('show_class', 'entry_no'),)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.id:
            # update only
            super(ClassEntry, self).save(*args, **kwargs)
            return
        
        # new entry may need to try a coupld of times if there are multiple people creating entries
        retries = 0
        while not self.id:
            try:
                highest_entry = ClassEntry.objects.filter(show_class=self.show_class.pk).aggregate(models.Max('entry_no'))['entry_no__max']
                if not highest_entry == None:
                    self.entry_no = highest_entry + 1
                else:
                    self.entry_no = 1
                super(ClassEntry, self).save(*args, **kwargs)
            except IntegrityError as err:
                if retries == 10:
                    raise err
                retries += 1
                time.sleep(random.uniform(0.5, 1))

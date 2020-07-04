from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
import os, cgi

# Create your models here.
class ShowClass(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    img = models.ImageField(upload_to="images")
    thumbnail = models.ImageField(upload_to="images", blank=True, null=True)
    show_age = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "show classes"

    def preview_tag(self):
        return f'<img src="{self.thumbnail.url}"/>'
    preview_tag.short_description = "Preview"
    preview_tag.allow_tags = True

    def __str__(self):
        return self.name
    
    def make_thumbnail(self):
        if not self.img:
            return
    
        if (not isinstance(self.img.file, UploadedFile)) and (self.thumbnail):
            return
      
        THUMBNAIL_SIZE = (600,400)
    
        if isinstance(self.img.file, UploadedFile):
            if self.img.file.content_type == 'image/jpeg':
                pil_type = 'jpeg'
                file_extension = 'jpg'
                content_type = 'image/jpeg'
            elif self.img.file.content_type == 'image/png':
                pil_type = 'png'
                file_extension = 'png'
                content_type = 'image/png'
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
        
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    
        temp = BytesIO()
        image.save(temp, pil_type)
        temp.seek(0)
    
        fd = SimpleUploadedFile(os.path.split(self.img.name)[-1], 
                            temp.read(), content_type=content_type)
    
        thumbnail_name = "%s.preview.%s" % (os.path.splitext(fd.name)[0], file_extension)

        if(os.path.exists(os.path.join(settings.MEDIA_ROOT, thumbnail_name))):
            os.remove(os.path.join(settings.MEDIA_ROOT, thumbnail_name))
        self.thumbnail.save(thumbnail_name, fd, save=False)
        
    def scale_image(self):
        if not isinstance(self.img.file, UploadedFile):
            return
    
        if self.img.file.content_type == 'image/jpeg':
            pil_type = 'jpeg'
            file_extension = '.jpg'
        elif self.img.file.content_type == 'image/png':
            pil_type = 'png'
            file_extension = '.png'
    
        if hasattr(self.img.file, 'temporary_file_path'):
            image = Image.open(self.img.file.temporary_file_path())
        else:
            # thumbnail will have already read the file from memory
            self.img.file.seek(0)
            image = Image.open(BytesIO(self.img.file.read()))
    
        image.thumbnail((1600, 1600), Image.ANTIALIAS)
    
        temp = BytesIO()
        image.save(temp, pil_type)
        temp.seek(0)
    
        fd = SimpleUploadedFile(os.path.splitext(self.img.name)[0] + file_extension, 
                            temp.read(),
                            content_type=self.img.file.content_type)
    
        self.img.save(os.path.splitext(self.img.name)[0] + file_extension, fd, save=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name[:ShowClass._meta.get_field('slug').max_length])
        self.make_thumbnail()
        self.scale_image()
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
    
    def make_thumbnail(self):
        if not self.img:
            return
    
        if (not isinstance(self.img.file, UploadedFile)) and (self.thumbnail):
            return
      
        THUMBNAIL_SIZE = (600,600)
    
        if isinstance(self.img.file, UploadedFile):
            if self.img.file.content_type == 'image/jpeg':
                pil_type = 'jpeg'
                file_extension = 'jpg'
                content_type = 'image/jpeg'
            elif self.img.file.content_type == 'image/png':
                pil_type = 'png'
                file_extension = 'png'
                content_type = 'image/png'
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
        
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    
        temp = BytesIO()
        image.save(temp, pil_type)
        temp.seek(0)
    
        fd = SimpleUploadedFile(os.path.split(self.img.name)[-1], 
                            temp.read(), content_type=content_type)
    
        thumbnail_name = "%s.preview.%s" % (os.path.splitext(fd.name)[0], file_extension)

        if(os.path.exists(os.path.join(settings.MEDIA_ROOT, thumbnail_name))):
            os.remove(os.path.join(settings.MEDIA_ROOT, thumbnail_name))
        self.thumbnail.save(thumbnail_name, fd, save=False)
        
    def scale_image(self):
        if not isinstance(self.img.file, UploadedFile):
            return
    
        if self.img.file.content_type == 'image/jpeg':
            pil_type = 'jpeg'
            file_extension = '.jpg'
        elif self.img.file.content_type == 'image/png':
            pil_type = 'png'
            file_extension = '.png'
    
        if hasattr(self.img.file, 'temporary_file_path'):
            image = Image.open(self.img.file.temporary_file_path())
        else:
            # thumbnail will have already read the file from memory
            self.img.file.seek(0)
            image = Image.open(BytesIO(self.img.file.read()))
    
        image.thumbnail((1600, 1600), Image.ANTIALIAS)
    
        temp = BytesIO()
        image.save(temp, pil_type)
        temp.seek(0)
    
        fd = SimpleUploadedFile(os.path.splitext(self.img.name)[0] + file_extension, 
                            temp.read(),
                            content_type=self.img.file.content_type)
    
        self.img.save(os.path.splitext(self.img.name)[0] + file_extension, fd, save=False)
    
    def save(self, *args, **kwargs):
        self.make_thumbnail()
        self.scale_image()
        super(EntryImage, self).save(*args, **kwargs)

class ClassEntry(models.Model):
    FIRST_PLACE = 1
    SECOND_PLACE = 2
    THIRD_PLACE = 3
    COMMENDATION = 4
    UNPLACED = 99
    PLACE_CHOICES = (
        (FIRST_PLACE, 'First'),
        (SECOND_PLACE, 'Second'),
        (THIRD_PLACE, 'Third'),
        (COMMENDATION, 'Commendation'),
        (UNPLACED, 'Unplaced'),
    )
    title = models.CharField(max_length=50)
    caption = models.TextField(blank=True, null=True)
    show_class = models.ForeignKey('ShowClass')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    entrant = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True, help_text="Intended for judges comments")
    age = models.IntegerField(blank=True, null=True, help_text="Leave blank if you do not want to disclose!")
    entry_no = models.IntegerField(blank=True, help_text="Leave blank on new entries to take the next number")
    place = models.IntegerField(choices=PLACE_CHOICES, default=UNPLACED)

    class Meta:
        verbose_name_plural = "class entries"
        ordering = ["show_class", "place", "entry_no"]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            highest_entry = ClassEntry.objects.filter(show_class=self.show_class.pk).aggregate(models.Max('entry_no'))['entry_no__max']
            if not highest_entry == None:
                self.entry_no = highest_entry + 1
            else:
                self.entry_no = 1
        super(ClassEntry, self).save(*args, **kwargs)

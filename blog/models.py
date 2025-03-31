from django.db import models
from django.utils import timezone 
from account.models import Member
from django_prose_editor.fields import ProseEditorField
from slugify import slugify


# Create your models here.
class Post(models.Model):
    
    STATUS_CHOICES =(
        ('d' , 'پیش نویس'),
        ('p' , 'منتشر شده'),
    )
    
    title = models.CharField(max_length=100 , verbose_name='عنوان پست')
    slug = models.SlugField(max_length=100 ,unique=True,blank=True, allow_unicode=True, verbose_name='آدرس')
    image = models.ImageField(upload_to='Post_Images/' , blank=True , null=True , verbose_name="تصویر پست")
    description = ProseEditorField(verbose_name='محتوای مقاله')
    like = models.PositiveIntegerField(default=0 , verbose_name="لایک")
    view = models.PositiveIntegerField(default=0 , verbose_name="بازدید")
    publish = models.DateTimeField(default=timezone.now , verbose_name="زمان انتشار" )
    created = models.DateField(auto_now_add=True , verbose_name='تاریخ ساخت')
    updated = models.DateField(auto_now=True , verbose_name='تاریخ بروز رسانی')
    status = models.CharField(max_length=1 , choices=STATUS_CHOICES , verbose_name= "وضعیت")
    
    class Meta():
        verbose_name = "پست"
        verbose_name_plural = "پست ها"
        
    def save(self, *args, **kwargs):
        # تنظیم خودکار slug بر اساس title
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

    
class Comment(models.Model):

    post = models.ForeignKey(Post , on_delete= models.CASCADE , related_name="postcomment" , verbose_name='پست')
    user = models.ForeignKey(Member , on_delete=models.CASCADE , related_name='usercomment' , verbose_name='کاربر')
    content = ProseEditorField(max_length=500,verbose_name="متن کامنت")
    created = models.DateTimeField(auto_now_add=True , verbose_name='تاریخ ارسال')
    
    replay = models.ForeignKey('self',on_delete=models.CASCADE , related_name='replies', verbose_name='پاسخ' )

    class Meta():
        verbose_name = "نظر"
        verbose_name_plural = "نظرات" 
    def __str__(self):
        return f'کامنت {self.user}  روی {self.post}'
    
    def is_reply(self):
        return self.replay is not None

from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.subject or 'No Subject'}"


class Project(models.Model):
    proj_id = models.AutoField
    proj_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default="")
    proj_desc = models.CharField(max_length=300)
    proj_image = models.ImageField(default="")
    proj_file = models.FileField(default=None, upload_to='pf/images')
    pub_date = models.DateField(max_length=200, default=None)
    proj_link1 = models.URLField(default=None, max_length=200)
    proj_link2 = models.URLField(default=None, max_length=200)

    def __str__(self):
        return self.proj_name

from django.db import models


# from django.contrib.auth import get_user_model
# from django.db.models.loading import cache as model_cache
# if not model_cache.loaded:
#     model_cache.get_models()

# class Projdescription(EmbeddedDocument):
#     name = fields.StringField(max_length=400)
#
#     def __str__(self):
#         return self.name

# class ProjectManager(models.Manager):
#     pass


# Create your models here.
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

    # objects = ProjectManager()

    def __str__(self):
        return self.proj_name

# class Designation(EmbeddedDocument):
#     name = fields.StringField(required=True, max_length=250)
#
#     def __str__(self):
#         return self.name


# class Employee(Document):
#     name = fields.StringField(required=True, max_length=250)
#     username = fields.StringField(max_length=250)
#     email = fields.EmailField()
#     emp_id = fields.IntField()
#     designation = fields.EmbeddedDocumentField(Designation)
#     file = fields.FileField()
#
#     def __str__(self):
#         return self.name
#
#     # meta = {
#     #     'abstract': True
#     # }
#
#
# class Department(Document):
#     name = fields.StringField(required=True, max_length=250)
#     file = fields.FileField()
#
#     def __str__(self):
#         return self.name
#
#     # meta = {
#     #     'abstract': True
#     # }

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myportfolio.settings')
import django
django.setup()
from django.test import Client
c=Client()
resp1=c.post('/signup', {'username':'smoketestuser','fname':'Test','lname':'User','email':'smoketest@example.com','pass1':'TestPass123','pass2':'TestPass123'}, follow=True)
print('FIRST', resp1.status_code)
resp2=c.post('/signup', {'username':'smoketestuser','fname':'Test','lname':'User','email':'smoketest@example.com','pass1':'TestPass123','pass2':'TestPass123'}, follow=True)
print('SECOND', resp2.status_code)
print('\n---SECOND CONTENT PREVIEW---\n')
print(resp2.content.decode()[:800])

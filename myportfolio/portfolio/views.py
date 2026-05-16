from math import ceil

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from django.db import IntegrityError

from django.core.mail import send_mail
from django.conf import settings

from .models import Project, ContactMessage


# Create your views here.
def base(request):
    context = {}
    return render(request, 'pf/home.html', context)


def home(request):
    return render(request, 'pf/home.html')


def aboutme(request):
    return render(request, 'pf/aboutme.html')


def projects(request):
    allProjs = []
    if request.user.is_authenticated:
        catprojs = Project.objects.values('category')
        cats = {item['category'] for item in catprojs}
        for cat in cats:
            proj = Project.objects.filter(category=cat)
            n = len(proj)
            nSlides = n // 3 + ceil((n / 3) - (n // 3))
            allProjs.append([proj, range(1, nSlides), nSlides])
    return render(request, 'pf/projects.html', {'allProjs': allProjs})


def contactme(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not first_name or not email or not message:
            messages.error(request, 'Please fill in all required fields (First Name, Email, Message).')
            return redirect('contactme')

        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message,
        )

        full_subject = f"[Portfolio Contact] {subject or 'New Message'}"
        full_message = f"From: {first_name} {last_name} <{email}>\n\n{message}"

        try:
            send_mail(
                full_subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(
            request,
            f'Thanks {first_name}! Your message has been received. I\'ll get back to you soon.'
        )
        return redirect('contactme')

    return render(request, 'pf/contactme.html')


def resume(request):
    return render(request, 'pf/resume.html')


def documents(request):
    return render(request, 'pf/documents.html')


def search(request):
    if request.user.is_authenticated:

        query = request.GET['query']
        if len(query) > 78:
            allProjs = Project.objects.none()
        else:
            allPostsTitle = Project.objects.filter(category__icontains=query)
            allPostsContent = Project.objects.filter(proj_desc__icontains=query)
            allPostsName = Project.objects.filter(proj_name__icontains=query)
            allProjs = allPostsTitle.union(allPostsContent)
            allProjs = allProjs.union(allPostsName)

        if allProjs.count() == 0:
            messages.warning(request, "No search results found. Please refine your query")
        context = {'allProjs': allProjs, 'query': query}
        return render(request, 'pf/search.html', context)
    else:
        return redirect('projects')


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        next_url = request.POST.get('next', 'home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect(next_url)

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect(next_url)

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect(next_url)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username")
            return redirect(next_url)

        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
        except IntegrityError:
            messages.error(request, "Could not create user due to a database error. Please try a different username.")
            return redirect(next_url)

        messages.success(request, "Your account has been successfully created")
        return redirect(next_url)
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        next_url = request.POST.get('next', 'home')

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect(next_url)

    return HttpResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out... Thanks for visiting my Website")
    # return redirect('logout')
    return render(request, 'pf/logout.html')


def handler404(request, exception):
    return render(request, 'pf/404.html', status=404)

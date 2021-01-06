from math import ceil

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect

from .models import Project


# Create your views here.
def base(request):
    context = {}
    return render(request, 'pf/home.html', context)


def home(request):
    return render(request, 'pf/home.html')


def aboutme(request):
    return render(request, 'pf/aboutme.html')


def projects(request):
    if request.user.is_authenticated:
        allProjs = []
        catprojs = Project.objects.values('category')
        cats = {item['category'] for item in catprojs}
        for cat in cats:
            proj = Project.objects.filter(category=cat)
            n = len(proj)
            nSlides = n // 3 + ceil((n / 3) - (n // 3))
            allProjs.append([proj, range(1, nSlides), nSlides])
        context = {'allProjs': allProjs}
        return render(request, 'pf/projects.html', context)
    else:
        return render(request, 'pf/home2.html')


def contactme(request):
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
        return render(request, 'pf/home2.html')


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        # username should be under 10 characters
        if len(username) > 4:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')

        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')

        # passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')

    return HttpResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out... Thanks for visiting my Website")
    # return redirect('logout')
    return render(request, 'pf/logout.html')

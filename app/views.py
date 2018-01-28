from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from app.forms import TeacherForm, TeacherProfileForm, Student_DetailForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
from app.models import Student_Detail, Student_Allotment, Teacher, Teacher_Allotment, Room


def index(request):
    return render(request, 'index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = TeacherForm(data=request.POST)
        profile_form = TeacherProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = TeacherForm()
        profile_form = TeacherProfileForm()

    return render(request,
                  'register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    auth_logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')


@login_required
def student_upload(request):
    if request.method == 'POST':
        form = Student_DetailForm(request.POST, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            Student_Detail.objects.create(name=cd['name'], sap_id=cd['sap_id'], address=cd['address'],
                                          dob=cd['dob'], mobile_no=cd['mobile_no'], dept=cd['dept'],
                                          pic=request.FILES['pic'])
        form = Student_DetailForm()
        return render(request, 'student_upload.html', {'form': form})
    else:
        form = Student_DetailForm()
    return render(request, 'student_upload.html', {'form': form})


def upload_csv_room(request):
    data = {}
    if request.method == "GET":
        return render(request, "room-upload.html", data)
    # if not GET, then proceed
    csv_file = request.FILES["csv_file"]
    file_data = csv_file.read().decode("utf-8")

    lines = file_data.split("\n")
    # loop over the lines and save them in db. If error , store as string and then display
    for line in lines[:-1]:
        fields = line.split(",")
        Room.objects.create(room_name=fields[0], capacity=fields[1],
                            floor=fields[2])
    return HttpResponseRedirect(reverse('upload_csv_room'))


def upload_csv_studentallot(request):
    data = {}
    if request.method == "GET":
        return render(request, "room-upload.html", data)
    # if not GET, then proceed
    csv_file = request.FILES["csv_file"]
    file_data = csv_file.read().decode("utf-8")

    lines = file_data.split("\n")
    # loop over the lines and save them in db. If error , store as string and then display
    for line in lines[:-1]:
        fields = line.split(",")
        id = fields[0]
        s = Student_Detail.objects.filter(sap_id=id)
        print(s[0].name)
        Student_Allotment.objects.create(student=s[0], room_name=fields[1], date=fields[2], time=fields[3],
                                         exam=fields[4])
    return HttpResponseRedirect(reverse('upload_csv_studentallot'))


def upload_csv_teacherallot(request):
    data = {}
    if request.method == "GET":
        return render(request, "room-upload.html", data)
    # if not GET, then proceed
    csv_file = request.FILES["csv_file"]
    file_data = csv_file.read().decode("utf-8")

    lines = file_data.split("\n")
    # loop over the lines and save them in db. If error , store as string and then display
    for line in lines[:-1]:
        fields = line.split(",")
        id = fields[0]
        s = Teacher.objects.filter(sap_id=id)
        print(s[0])
        Teacher_Allotment.objects.create(
            teacher=s[0], room_name=fields[1], date=fields[2], time=fields[3])
    return HttpResponseRedirect(reverse('upload_csv_teacherallot'))

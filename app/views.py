from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from app.forms import TeacherForm, TeacherProfileForm, Student_DetailForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_protect
from app.models import Student_Detail, Student_Allotment, Teacher, Teacher_Allotment, Room
import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json
from PIL import Image
subscription_key = '5979034bfb134316b72d9625b0c320c5'
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

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

@csrf_protect
def hallticket(request):
    errors = []
    if request.method == "POST" :
        q = request.POST['q']
        print(q)
        student_details= Student_Detail.objects.filter(sap_id=q)
        print(student_details)
        ticket = Student_Allotment.objects.filter(student=student_details[0])
        return render(request, 'hallticket.html',
                          {'ticket': ticket, 'query': q})

        
    return render(request, 'hallticket.html',
              {'errors': errors})

def verify(request):
    if request.method=="POST":
        sap_sent=requests.POST['sap_id']
        img_sent=request.body
        student_details= Student_Detail.objects.filter(sap_id=sap_sent)
        print(student_details)
        img_store=student_details.pic

        detect(img_store,img_sent)



def test(request):
    student_details= Student_Detail.objects.filter(sap_id=60004150064)
    #print(student_details)
    
    #print(student_details[0].pic)
    img_sent=student_details[0].pic
    print(img_sent)
    (img_sent)
    detect(img_sent, img_sent)

    return render(request, 'test.html',
              {})






def detect(img_sent, img_store):

    headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
    }

  
    params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    #body1 = {'url': 'https://vignette.wikia.nocookie.net/harrypotter/images/c/c1/Harry%2Bpotter-Harry_Potter_HP4_01.jpg'}
    #body2 = {'url': 'https://images.pottermore.com/bxd3o8b291gf/3SQ3X2km8wkQIsQWa02yOY/25f258f21bdbe5f552a4419bb775f4f0/HarryPotter_WB_F4_HarryPotterMidshot_Promo_080615_Port.jpg'}
   
    try:
        #data1 = open('./img1.png', 'rb').read()
        #data2 = open('./img2.png', 'rb').read()

        #data1= Image.open(img_sent)
        #print(data1)
        #data2= Image.open(img_store)
        data1 = open(str(img_sent), 'rb').read()
        data2 = open(str(img_store), 'rb').read()


        response1 = requests.request('POST', uri_base + '/face/v1.0/detect',  data=img_sent, headers=headers, params=params)
        response2 = requests.request('POST', uri_base + '/face/v1.0/detect', data=img_store, headers=headers, params=params)
        print(response1)

        #print ('Response:')
        parsed1 = json.loads(response1.text)
        parsed2 = json.loads(response2.text)
        faceId1=parsed1[0]['faceId']
        faceId2=parsed2[0]['faceId']
        print(faceId1,faceId2)

        verify2(faceId1,faceId2)
        #print (json.dumps(parsed, sort_keys=True, indent=2))

    except Exception as e:
        print('Error:')
        print(e)


def verify2(faceId1,faceId2):


    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }


    params = urllib.parse.urlencode({
    })

    body = { 
        "faceId1": faceId1,
        "faceId2": faceId2,
    }

    try:
    
        response = requests.request('POST', uri_base + '/face/v1.0/verify', json=body, data=None, headers=headers, params=params)
        print(response)
        print ('Response:')
        parsed = json.loads(response.text)
        print(parsed)
        print (json.dumps(parsed, sort_keys=True, indent=2))
    except Exception as e:
        print('Error:')
        print(e)


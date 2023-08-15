
# from pyexpat.errors import messages
from django.shortcuts import redirect, render
from studentApp.forms import *
from django.contrib import messages
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'studentApp/home.html')

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'],)
            notes.save()
        messages.success(request,f"notes added from {request.user.username} successfully")
    else:

        form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'studentApp/notes.html',context)

@login_required 
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class note_details(DetailView):
    model=Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                 finished=request.POST['is_finished']
                 if finished == 'on':
                     finished = True
                 else:
                     finished = False
            except:
                 finished = False
            homeworks=HomeWork(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request,f"Homework added from {request.user.username}!!")

    else:

        form=HomeworkForm()
    homework=HomeWork.objects.filter(user=request.user)
    if len(homework)== 0:
        homework_done= True
    else:
        homework_done= False
    context={'homeworks':homework, 'homeworks_done':homework_done,'form':form}
    return render(request,'studentApp/homework.html',context)

@login_required
def update_homework(request,pk=None):
    homework=HomeWork.objects.get(id=pk)
    if homework.is_finished==True :
        homework.is_finished=False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None): #id
    HomeWork.objects.get(id=pk).delete()   #without primary key id=id
    return redirect('homework')

@login_required
def youtubeview(request): #pip insatll youtube-search-python
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
             'duration':i['duration'],
            'thumbnail':i['thumbnails'][0]['url'],
              'channel':i['channel']['name'],
                 'link':i['link'],
                 'views':i['viewCount']['short'],
            'published':i['publishedTime']
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={'form':form,'results':result_list}
        return render(request,'studentApp/youtube.html',context)
    else:        
        form=DashboardForm
    context={'form':form}
    return render(request,'studentApp/youtube.html',context)

@login_required
def booksview(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        
        result_list = []
        if "items" in answer:
            for item in answer["items"]:
                volume_info = item.get("volumeInfo", {})
                result_dict = {
                    "title": volume_info.get("title"),
                    "subtitle": volume_info.get("subtitle"),
                    "description": volume_info.get("description"),
                    "count": volume_info.get("pageCount"),
                    "categories": volume_info.get("categories"),
                    "rating": volume_info.get("averageRating"),
                    "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail"),
                    "preview": volume_info.get("previewLink")
                }
                result_list.append(result_dict)
        
        context = {
            "form": form,
            "results": result_list
        }
        return render(request, "studentApp/books.html", context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'studentApp/books.html', context)

    
def dictionaryview(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
        r = requests.get(url)
        answer = r.json()
        # print(answer[0]['meanings'][0]['definitions'][0])
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', [])
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
            
        except (KeyError, IndexError):
            context = {
                'form': form,
                'input': ''
            }
        print(context)
        return render(request, 'studentApp/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
        return render(request, 'studentApp/dictionary.html', context)

   
def wikiview(request): # pip install wikipedia
    if request.method == 'POST':
        text=request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'studentApp/wiki.html',context)
    else:
       form=DashboardForm()
    context={'form':form}
    return render(request,'studentApp/wiki.html',context)

def registerview(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!!")
            return redirect('login')  # Replace 'home' with the URL name of your home page
    else:
        form = UserRegistrationForm()
    return render(request, 'studentApp/register.html', {'forms': form})

@login_required
def profileview(request):
    homeworks=HomeWork.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    context={
        'homeworks':homeworks,
        'homework_done':homework_done
    }
    return render(request,'studentApp/profile.html',context)



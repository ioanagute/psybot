from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Chat, Entry
import openai
import pytz

openai.api_key = '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'

system_message = { "role": "system", "content": "You are a psychology expert. Keep your answers under 200 words." }

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def therapy_page(request):
    return render(request, 'therapy.html')

def journal_page(request):
    if request.method == 'POST':
        return add_journal_entry(request)
    elif request.method == 'GET':
        return get_journal_page(request)

def add_journal_entry(request):
    title = request.POST.get('title')
    tags = request.POST.get('tags')
    text = request.POST.get('text')

    entry = Entry(user=request.user, title=title, tags=tags, text=text)
    entry.save()
    return JsonResponse({ "id": entry.id, "created_at": format_date(entry.created_at, "Europe/Bucharest") })

def get_journal_page(request):
    search = request.GET.get('search', None)
    date = request.GET.get('date', None)
    tag = request.GET.get('tag', None)

    if search:
        searchFilter = Q(title__icontains=search) | Q(text__icontains=search)
    else:
        searchFilter = Q()

    if date:
        dateFilter = Q(created_at__date=date)
    else:
        dateFilter = Q()
    
    if tag:
        tagFilter = Q(tags__icontains=tag)
    else:
        tagFilter = Q()

    entries = Entry.objects.filter(Q(user=request.user), searchFilter, dateFilter, tagFilter)

    return render(request, 'journal.html', {'entries': entries})



def ask_openai(message, user):
    messages = [system_message]

    lastChats = Chat.objects.filter(user=user).order_by('-created_at')[:3]

    for chat in lastChats:
        messages.append({ "role": "user", "content": chat.message })
        messages.append({ "role": "assistant", "content": chat.response })

    messages.append({ "role": "user", "content": message })

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )

    answer = response.choices[0].message.content.strip()
    return answer

def psybot_page(request):
    if request.method == 'POST':
        return add_chat(request)
    elif request.method == 'GET':
        return get_chat_page(request)

def add_chat(request):
    message = request.POST.get('message')
    response = ask_openai(message, request.user)

    chat = Chat(user=request.user, message=message, response=response)
    chat.save()
    return JsonResponse({ 'id': chat.id, 'message': message, 'response': response, "created_at": format_date(chat.created_at, "Europe/Bucharest") })

def get_chat_page(request):
    search = request.GET.get('search', None)
    date = request.GET.get('date', None)

    if search:
        searchFilter = Q(message__icontains=search) | Q(response__icontains=search)
    else:
        searchFilter = Q()

    if date:
        dateFilter = Q(created_at__date=date)
    else:
        dateFilter = Q()

    chats = Chat.objects.filter(Q(user=request.user), searchFilter, dateFilter)
    return render(request, 'psybot.html', {'chats': chats})

def delete_chat(request):
    chat_id = request.POST.get('chat_id')
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()
    return JsonResponse({"message": "success"})

def delete_entry(request):
    entry_id = request.POST.get('entry_id')
    entry = get_object_or_404(Entry, id=entry_id)
    entry.delete()
    return JsonResponse({"message": "success"})

def format_date(input_date, target_timezone):
    target_tz = pytz.timezone(target_timezone)
    converted_date = input_date.astimezone(target_tz)
    formatted_date = converted_date.strftime("%b. %d, %Y, %I:%M %p").replace(" 0", " ").replace('AM', 'a.m.').replace('PM', 'p.m.')
    return formatted_date

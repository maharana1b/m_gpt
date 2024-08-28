from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        # Handle the chat message here
        message = request.POST.get('message')
        # Return a response if needed
    return render(request, 'chat.html')

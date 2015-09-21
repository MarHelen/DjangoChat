
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
#from django.template.defaulttags import csrf_token
#from django.views.decorators.csrf import requires_csrf_token, csrf_protect, ensure_csrf_cookie
#from django.core.context_processors import csrf

from .models import Message
from .forms import PostForm
from django.utils import timezone

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

#@csrf_token
def index(request):
    latest_message_list = Message.objects.order_by('post_time')
    unicode_list = [item.__unicode__ for item in latest_message_list]
    form = PostForm(request.POST)
    
    
    if request.method == 'POST':
        message_text = request.POST.get('message_text')
        response_data = {}
        new_mess = Message(message_text = message_text, post_time = timezone.now(), username="first")
        """ logging for new came message"""
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        message_for_log = 'first just wrote: %s' %(message_text)
        logger.info(message_for_log)
        new_mess.save()
        form = PostForm(request.POST)
    else:
        form = PostForm()
        
    template = loader.get_template('chat/index.html')
    
    context = RequestContext(request, {
                    'unicode_list': unicode_list,   
                    'form': form, })    
        
    return HttpResponse(template.render(context))
    #return render(context, 'chat/index.html', {'form': form})

""""
#@csrf_token
#@ensure_csrf_cookie
def new_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message_text')
        response_data = {}
        new_mess = Message(message_text = message_text, post_time = new_mess.created, username="first")
        #logging for new came message
        message_for_log = 'first just wrote: %s' %(message_text)
        logger.log(message_for_log)
        
        new_mess.save()
        #post = Post(text=post_text, author=request.user)
        #post.save()

        response_data['result'] = 'Create post successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:       
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

"""

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
#from django.contrib.sessions.models import Session
#from django.template.defaulttags import csrf_token
#from django.views.decorators.csrf import requires_csrf_token, csrf_protect, ensure_csrf_cookie
#from django.core.context_processors import csrf

from .models import Message
from .forms import PostForm
from django.utils import timezone

# import the logging library
import logging
import json
from datetime import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

#@csrf_token
def index(request):
    #latest_message_list = Message.objects.order_by('post_time')
    #unicode_list = [item.__unicode__ for item in latest_message_list]
    """ hack for storing datetime value in serializable value - convert to string time part as %M%S
                that's enough for time comparation in scale of seconds """    
    #request.session['update_time'] = timezone.now().strftime("%M%S")
    #form = PostForm(request.POST)
    response_data = {}
    response_data['error'] = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            message_t = form.cleaned_data['message_text']        
            time = timezone.now()
            new_mess = Message(message_text = message_t, post_time = time, username="first")
            #logging for new came message
            message_for_log = 'first just wrote: %s' %(message_t)
            logger.debug(message_for_log)       
            new_mess.save()
            #post = Post(text=post_text, author=request.user)
            response_data['result'] = 'Create post successful!'
            
        else:
            response_data['error'] = 'form is invalid'
        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
                 )        
    else:
        form = PostForm()
        
        
    template = loader.get_template('chat/index.html')
    context = RequestContext(request, {
                    #'unicode_list': unicode_list,   
                    'form': form, })    
        
    return HttpResponse(template.render(context))


#@csrf_token
#@ensure_csrf_cookie
""""
def new_message(request):
    #if request.method == 'POST':
    message_t = ''
    message_t = request.POST.get('the_post')
    response_data = {}
    new_mess = Message(message_text = message_t, post_time = new_mess.created, username="first")
    #logging for new came message
    message_for_log = 'first just wrote: %s' %(message_t)
    logger.log(message_for_log)       
    new_mess.save()
        #post = Post(text=post_text, author=request.user)
    response_data['result'] = 'Create post successful!'

    return HttpResponse(
           json.dumps(response_data),
           content_type="application/json"
       )
    #else:       
    #    return HttpResponse(
    #        json.dumps({"nothing to see": "this isn't happening"}),
    #        content_type="application/json"
    #    )

#"""

def content(request):
    response_data= {}
    if request.method == "GET":
        last_update = request.session.get('update_time', False)
        latest_message_list = Message.objects.filter(post_time.strftime("%M%S") > last_update).order_by('post_time')
        request.session['update_time'] = timezone.now().strftime("%M%S")
        #latest_message_list = [item for item in latest_message_list if item.post_time > last_update]
        if latest_message_list:
            unicode_list = [item.__unicode__ for item in latest_message_list]
            response_data['status'] = 'update succeeded'
        else: 
            response_data['status'] = 'nothing to update'
            unicode_list = []
        response_data['answer'] = unicode_list
    else:
        response_data['status'] = 'Something wrong with request'
         
        
    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )        
        
        

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
from SimpleChat.settings import *


import logging.config
logging.config.dictConfig(LOGGING)

# import the logging library
import logging
import json
from datetime import datetime
import datetime
import time



# Get an instance of a logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def index(request):
    """function designed for handling POST message requst, verifies, saves to db"""
    response_data = {}
    response_data['error'] = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            message_t = form.cleaned_data['message_text']        
            time = timezone.localtime(timezone.now())
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
    """ this function handles continues GET requsts for updating Chat box with new messages"""
    response_data= {}
    if request.method == "GET":
        last_update_id = int(request.GET.get('message_id', 0))
        
        #request list of all messages in the db
        latest_message_list = Message.objects.order_by('id')
        
        #filter messages list by model function to leave only newer than specified id
        latest_message_list = [item for item in latest_message_list if item.was_published_recently(last_update_id)]
        
        #logging for new-coming message
        message_for_log = 'The last outputted in GUI message has %s id' %(last_update_id)
        logger.debug(message_for_log)
        
        """" if latest_message_list is not empty, make unicode message list, save last message id, set status,
             if it's empty - last_message_id leavs the same, set status, make unicode list empty"""
        if latest_message_list:
            response_data['id'] = latest_message_list[-1].id
            unicode_list = [item.__unicode__() for item in latest_message_list]
            response_data['status'] = 'success'
        else: 
            response_data['id'] = last_update_id
            response_data['status'] = 'notmodified'
            unicode_list = []
            
        #make response data list
        response_data['answer'] = unicode_list
        
        #if request is not GET, status will be 'error'
    else:
        response_data['status'] = 'error'
    
    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )        
        
        
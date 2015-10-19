from django.db import models

import datetime
import time

from django.db import models
from django.utils import timezone


class Message(models.Model):
    
    """class for modeling main application db for storing users messages
       DB item contains user_name, message_text, post_time as main parametres"""
    
    username = models.CharField(max_length=30)
    message_text = models.CharField(max_length=250)
    post_time = models.DateTimeField('date published')
    
    def __unicode__(self):
        
        """ this method makes unicode string for sending to GUI, including post_time, user_name, message_text"""
        
        return '%s %s wrote: %s' %(self.post_time.strftime("%Y-%m-%d %H:%M:%S"), self.username, self.message_text)
    
    def was_published_recently(self, specified_id):
        
        """this method designed for creting filter by specified item id, returns TRUE if item.id is bigger"""
        
        return int(self.id) > specified_id    


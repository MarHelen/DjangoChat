from django.db import models

import datetime
import time
#import pytz

from django.db import models
from django.utils import timezone


class Message(models.Model):
    username = models.CharField(max_length=30)
    message_text = models.CharField(max_length=250)
    post_time = models.DateTimeField('date published')
    
    def __unicode__(self):       
        return '%s %s wrote: %s' %(self.post_time.strftime("%Y-%m-%d %H:%M:%S"), self.username, self.message_text)
    
    def was_published_recently(self, specified_id):
        return self.id > specified_id    
    #time.mktime(d.timetuple())


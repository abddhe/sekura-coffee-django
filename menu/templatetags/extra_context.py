from datetime import datetime,timedelta
from django.utils import timezone
from django import template
import re
from menu.models import Notification

register = template.Library()


class NotificationNode(template.Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        context[self.variable] = Notification.objects.filter(opened=False).order_by('-created_at')
        return ""


@register.tag("get_notification")
def get_notification(parser, token):
    return NotificationNode('notifications')


@register.filter('regex')
def regex(string, pattern):
    new_string = re.sub(pattern=pattern, repl='', string=string)
    return new_string


@register.filter('new')
def new(date):
    new_date = date + timedelta(minutes=5)
    if new_date > timezone.now():
        return True
    return False

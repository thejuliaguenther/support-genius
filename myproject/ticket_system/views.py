from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import RequestContext, loader
from django_twilio.decorators import twilio_view
from twilio.twiml import Response


def index(request):
    template = loader.get_template('ticket_system/dashboard.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def tickets(request):
    template = loader.get_template('ticket_system/tickets.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def one_ticket(request):
    template = loader.get_template('ticket_system/one_ticket.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

@twilio_view
def sms(request):
    name = request.POST.get('Body', '')
    msg = 'Hey %s, how are you today?' % (name)
    r = Response()  
    r.message('Hello from your Django app!')
    return r

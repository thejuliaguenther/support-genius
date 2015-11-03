
from django.http import HttpResponse
from django.template import RequestContext, loader

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


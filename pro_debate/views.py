from django.shortcuts import get_object_or_404, render

from .models import Position, Elaboration


def index(request):
    positions = Position.objects.order_by('id')[:50]
    context = {'positions': positions}
    return render(request, 'pro_debate/index.html', context)


def detail(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    children = Elaboration.objects.filter(child_of=position_id).order_by('tree_relation')

    context = {'position': position, 'children': children}
    return render(request, 'pro_debate/detail.html', context)
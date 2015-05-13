from django.shortcuts import get_object_or_404, render

from .models import Position, Elaboration


def index(request):
    # positions = Position.objects.filter().order_by('id')[:50]
    positions = Position.objects.exclude(elaboration_of_position__tree_relation='S').exclude(elaboration_of_position__tree_relation='C').order_by('id')[:50]

    context = {'positions': positions}
    return render(request, 'pro_debate/index.html', context)


def detail(request, position_id, parent_id):
    position = get_object_or_404(Position, pk=position_id)
    support_points = Elaboration.objects.filter(child_of=position_id, tree_relation='S')
    counter_points = Elaboration.objects.filter(child_of=position_id, tree_relation='C')

    parent = None

    if Position.objects.filter(pk=parent_id).first():
    	# Need a check to make sure the parent is indeed a parent
    	parent = Position.objects.get(pk=parent_id)

    context = {
    	'position': position, 
    	'support_points': support_points,
    	'counter_points': counter_points,
    	'parent': parent
	}
    return render(request, 'pro_debate/detail.html', context)
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Position, Elaboration, Manifestation


def index(request):
    positions = Position.objects.filter().order_by('id')
    # positions = Position.objects.filter().order_by('id')[:50]
    # positions = Position.objects.exclude(elaboration_of_position__tree_relation='S').exclude(elaboration_of_position__tree_relation='C').order_by('id')[:50]

    context = {
        'positions': positions
    }
    return render(request, 'pro_debate/index.html', context)


def detail(request, position_id):
    position = get_object_or_404(Position, pk=position_id)

    support_points = Elaboration.objects.filter(child_of=position_id, tree_relation='S')
    counter_points = Elaboration.objects.filter(child_of=position_id, tree_relation='C')

    get_parent = request.GET.get('parent')
    get_grandparent = request.GET.get('grandparent')

    parent = None
    elaboration_in_tree = None
    elaborations_in_other_trees = None

    if Position.objects.filter(pk=get_parent).first():
        # Could use a check to make sure the parent is indeed a parent
        parent = Position.objects.get(pk=get_parent)
        # Don't think I'm enforcing this at the DB level yet, but each
        # support/counter point gets one elaboration. So there should only
        # ever be one of these objects returned:
        elaboration_in_tree = Elaboration.objects.get(elaborates=position_id, child_of=get_parent)
        elaborations_in_other_trees = Elaboration.objects.filter(elaborates=position_id).exclude(child_of=get_parent)
    else:
        # If we're not in a tree, we can try getting the 'general' argument.
        # That term/pattern might not continue to exist as is.
        if Elaboration.objects.filter(elaborates=position_id, tree_relation='G').first():
            elaboration_in_tree = Elaboration.objects.get(elaborates=position_id, tree_relation='G')
        elaborations_in_other_trees = Elaboration.objects.filter(elaborates=position_id).exclude(tree_relation='G')


    context = {
        'position': position, 
        'support_points': support_points,
        'counter_points': counter_points,
        'parent': parent,
        'grandparent': get_grandparent,
        'elaboration_in_tree': elaboration_in_tree,
        'elaborations_in_other_trees': elaborations_in_other_trees
    }
    return render(request, 'pro_debate/detail.html', context)


def submit(request, position_id):
    position = request.POST['position'];
    elaboration = request.POST['elaboration'];
    tree_relation = request.POST['tree_relation'];
    child_of = request.POST['child_of'];
    grandchild_of = request.POST['grandchild_of'];

    new_position = Position.objects.create(position_statement=position)
    new_elaboration = Elaboration.objects.create(
        elaboration=elaboration,
        tree_relation=tree_relation,
        child_of=Position.objects.get(pk=child_of),
        elaborates=Position.objects.get(pk=position_id)
    )
    new_position.elaboration_of_position.add(new_elaboration)

    context = {
        'position_id': position_id,
        'error_message': "You didn't select a choice.",
    }

    parent_param = '?parent=%s' % child_of
    grandparent_param = '&grandparent=%s' % grandchild_of if grandchild_of else ''
    return HttpResponseRedirect(reverse('detail', args=(new_position.id,)) + parent_param + grandparent_param)
    # return render(request, 'pro_debate/detail.html', context) 


def submit_manifestation(request, position_id):
    url = request.POST['url'];
    title = request.POST['title'];
    notes = request.POST['notes'];
    parent = request.POST['parent'];
    grandparent = request.POST['grandparent'];

    current_position = Position.objects.get(pk=position_id);
    new_manifestation = Manifestation.objects.create(
        url=url,
        title=title,
        manifests=current_position,
        notes=notes
    )
    current_position.manifestation_set.add(new_manifestation)

    parent_param = '?parent=%s' % parent if parent else ''
    grandparent_param = '&grandparent=%s' % grandparent if grandparent else ''
    return HttpResponseRedirect(reverse('detail', args=(position_id,)) + parent_param + grandparent_param)
    # return render(request, 'pro_debate/detail.html', context) 


def add(request):
    position = request.POST['position'];
    elaboration = request.POST['elaboration'];

    new_position = Position.objects.create(position_statement=position)
    new_elaboration = Elaboration.objects.create(
        elaboration=elaboration,
        tree_relation='G',
        elaborates=Position.objects.get(pk=new_position.id)
    )
    new_position.elaboration_of_position.add(new_elaboration)

    return HttpResponseRedirect(reverse('detail', args=(new_position.id,)))
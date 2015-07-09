from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Position, Elaboration, Manifestation
from .forms import SupportCounterPointForm


def index(request):
    positions = Position.objects.filter().order_by('id')
    # positions = Position.objects.filter().order_by('id')[:50]
    # positions = Position.objects.exclude(elaboration_of_position__tree_relation='S').exclude(elaboration_of_position__tree_relation='C').order_by('id')[:50]

    invalid_submit = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SupportCounterPointForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # If valid, process the form. This is spun out into an object 
            # because we use the same logic in the detail view.
            redirect_info = process_form(form)
            # Redirect to the new position we created. I wanted to do this in
            # the process_form object but it didn't seem to work
            return HttpResponseRedirect(reverse('detail', args=(redirect_info['new_position'],)) + redirect_info['parent_param'] + redirect_info['grandparent_param'])
        else:
            invalid_submit = form.cleaned_data['tree_relation']
    # if not POST, create a blank form
    else:
        form = SupportCounterPointForm()

    context = {
        'positions': positions,
        'form': form,
        'invalid_submit': invalid_submit
    }
    return render(request, 'pro_debate/index.html', context)


def manifestation_index(request):
    manifestations = Manifestation.objects.filter().order_by('id')

    context = {
        'manifestations': manifestations
    }
    return render(request, 'pro_debate/manifestation_index.html', context)


def manifestation(request, manifestation_id):
    manifestation = get_object_or_404(Manifestation, pk=manifestation_id)

    context = {
        'manifestation': manifestation
    }
    return render(request, 'pro_debate/manifestation.html', context)


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


    invalid_submit = None

    # See notes in index view for commentary
    if request.method == 'POST':
        form = SupportCounterPointForm(request.POST)
        if form.is_valid():
            redirect_info = process_form(form)
            return HttpResponseRedirect(reverse('detail', args=(redirect_info['new_position'],)) + redirect_info['parent_param'] + redirect_info['grandparent_param'])
        else:
            invalid_submit = form.cleaned_data['tree_relation']
    else:
        grandparent_id = ""
        if parent:
            grandparent_id = parent.id

        form = SupportCounterPointForm(
            initial={
                'child_of': position.id,
                'grandchild_of': grandparent_id
            }
        )

    context = {
        'position': position, 
        'support_points': support_points,
        'counter_points': counter_points,
        'parent': parent,
        'grandparent': get_grandparent,
        'elaboration_in_tree': elaboration_in_tree,
        'elaborations_in_other_trees': elaborations_in_other_trees,
        'form': form,
        'invalid_submit': invalid_submit
    }
    return render(request, 'pro_debate/detail.html', context)


def process_form(form):
    # process the data in form.cleaned_data as required
    point = form.cleaned_data
    child_of_position = Position.objects.get(pk=point['child_of']) if point['child_of'] else None

    new_position = Position.objects.create(position_statement=point['position'])
    new_elaboration = Elaboration.objects.create(
        elaboration=point['elaboration'],
        tree_relation=point['tree_relation'],
        child_of=child_of_position,
        elaborates=Position.objects.get(pk=new_position.id)
    )
    new_position.elaboration_of_position.add(new_elaboration)

    if point['tree_relation'] != 'G':
        parent_param = '?parent=%s' % point['child_of'] if point['child_of'] else ''
        grandparent_param = '&grandparent=%s' % point['grandchild_of'] if point['grandchild_of'] else ''
    else:
        parent_param = ''
        grandparent_param = ''
    
    return_info = {
        'new_position': new_position.id,
        'parent_param': parent_param,
        'grandparent_param': grandparent_param
    }

    return return_info


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



from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Position, Elaboration, Manifestation
from .forms import SupportCounterPointForm, SubmitManifestationForm


def index(request):
    positions = Position.objects.filter().order_by('id')
    # positions = Position.objects.filter().order_by('id')[:50]
    # positions = Position.objects.exclude(elaboration_of_position__tree_relation='S').exclude(elaboration_of_position__tree_relation='C').order_by('id')[:50]

    which_form_is_invalid = None

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SupportCounterPointForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # If valid, process the form. This is spun out into an object 
            # because we use the same logic in the detail view.
            redirect_info = process_point_form(form)
            # Redirect to the new position we created. I wanted to do this in
            # the process_point_form object but it didn't seem to work
            return HttpResponseRedirect(reverse('detail', args=(redirect_info['new_position'],)) + redirect_info['parent_param'] + redirect_info['grandparent_param'])
        else:
            which_form_is_invalid = form.cleaned_data['tree_relation']
    # if not POST, create a blank form
    else:
        form = SupportCounterPointForm()

    context = {
        'positions': positions,
        'form': form,
        'which_form_is_invalid': which_form_is_invalid
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


    which_form_is_invalid = None

    grandparent_id = parent.id if parent else ""

    point_form = SupportCounterPointForm(
        initial={
            'child_of': position.id,
            'grandchild_of': grandparent_id
        },
    )
    manifestation_form = SubmitManifestationForm(
        initial={
            'manifests': position.id,
            'position_parent': get_parent,
            'position_grandparent': get_grandparent
        },
    )
    # See notes in index view for commentary
    if request.method == 'POST':
        # Named the submit buttons to check which form submitted. I don't know
        # if this is the best way to handle different forms in the same view.
        if 'submit-elaboration' in request.POST:
            point_form = SupportCounterPointForm(request.POST)
            if point_form.is_valid():
                redirect_info = process_point_form(point_form)
                return HttpResponseRedirect(reverse('detail', args=(redirect_info['new_position'],)) + redirect_info['parent_param'] + redirect_info['grandparent_param'])
            else:
                which_form_is_invalid = point_form.cleaned_data['tree_relation'] if 'tree_relation' in point_form.cleaned_data else ""
        elif 'submit-manifestation' in request.POST:
            manifestation_form = SubmitManifestationForm(request.POST)
            if manifestation_form.is_valid():
                redirect_info = process_manifestation(manifestation_form)
                return HttpResponseRedirect(reverse('detail', args=(position_id,)) + redirect_info['parent_param'] + redirect_info['grandparent_param'])
            else:
                which_form_is_invalid = "manifestation"


    context = {
        'position': position, 
        'support_points': support_points,
        'counter_points': counter_points,
        'parent': parent,
        'grandparent': get_grandparent,
        'elaboration_in_tree': elaboration_in_tree,
        'elaborations_in_other_trees': elaborations_in_other_trees,
        'point_form': point_form,
        'manifestation_form': manifestation_form,
        'which_form_is_invalid': which_form_is_invalid
    }
    return render(request, 'pro_debate/detail.html', context)


def process_point_form(form):
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


def process_manifestation(form):
    manifestation = form.cleaned_data

    new_manifestation = Manifestation.objects.create(
        url=manifestation['url'],
        title=manifestation['title'],
        notes=manifestation['notes'],
        manifests=Position.objects.get(pk=manifestation['manifests'])
    )

    parent_param = '?parent=%s' % manifestation['position_parent'] if manifestation['position_parent'] else ''
    grandparent_param = '&grandparent=%s' % manifestation['position_grandparent'] if manifestation['position_grandparent'] else ''
    
    return_info = {
        'parent_param': parent_param,
        'grandparent_param': grandparent_param
    }

    return return_info
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Position, Elaboration, Manifestation
from .forms import SupportCounterPointForm, SubmitManifestationForm
from taggit.models import Tag, TaggedItem


def index(request):
    positions = Position.objects.filter().order_by('-id')[:5]
    tags = Tag.objects.all()

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
            return HttpResponseRedirect(reverse('detail', args=(redirect_info['new_position'],)) + redirect_info['get_params'])
        else:
            which_form_is_invalid = form.cleaned_data['tree_relation']
    # if not POST, create a blank form
    else:
        form = SupportCounterPointForm()

    context = {
        'positions': positions,
        'point_form': form,
        'which_form_is_invalid': which_form_is_invalid,
        'tags': tags
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

    current_parent = request.GET.get('parent')
    current_grandparent = request.GET.get('grandparent')

    current_parent_param = '?parent=%s' % current_parent if current_parent else ''
    current_grandparent_param = '&grandparent=%s' % current_grandparent if current_grandparent else ''
    current_get_params = current_parent_param + current_grandparent_param

    parent = None
    elaboration_in_tree = None
    elaborations_in_other_trees = None

    if Position.objects.filter(pk=current_parent).first():
        # Could use a check to make sure the parent is indeed a parent
        parent = Position.objects.get(pk=current_parent)
        # Don't think I'm enforcing this at the DB level yet, but each
        # support/counter point gets one elaboration. So there should only
        # ever be one of these objects returned:
        elaboration_in_tree = Elaboration.objects.get(elaborates=position_id, child_of=current_parent)
        elaborations_in_other_trees = Elaboration.objects.filter(elaborates=position_id).exclude(child_of=current_parent)
    else:
        # If we're not in a tree, we can try getting the 'general' argument.
        # That term/pattern might not continue to exist as is.
        if Elaboration.objects.filter(elaborates=position_id, tree_relation='G').first():
            elaboration_in_tree = Elaboration.objects.get(elaborates=position_id, tree_relation='G')
        elaborations_in_other_trees = Elaboration.objects.filter(elaborates=position_id).exclude(tree_relation='G')


    which_form_is_invalid = None

    new_position_grandparent_id = parent.id if parent else ""

    # Prep a tag list to prepopulate the point forms
    tag_list = ""
    for tag in position.tags.all():
        tag_list = tag_list + tag.name + ", "

    point_form = SupportCounterPointForm(
        initial={
            'child_of': position.id,
            'grandchild_of': new_position_grandparent_id,
            'tags': tag_list
        },
    )
    manifestation_form = SubmitManifestationForm(
        initial={
            'manifests': position.id,
            'position_parent': current_parent,
            'position_grandparent': current_grandparent
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
                return HttpResponseRedirect(reverse('detail', args=(redirect_info['new_position'],)) + redirect_info['get_params'])
            else:
                which_form_is_invalid = point_form.cleaned_data['tree_relation'] if 'tree_relation' in point_form.cleaned_data else ""
        elif 'submit-manifestation' in request.POST:
            manifestation_form = SubmitManifestationForm(request.POST)
            if manifestation_form.is_valid():
                redirect_info = process_manifestation(manifestation_form)
                return HttpResponseRedirect(reverse('detail', args=(position_id,)) + redirect_info)
            else:
                which_form_is_invalid = "manifestation"


    context = {
        'position': position, 
        'support_points': support_points,
        'counter_points': counter_points,
        'current_get_params': current_get_params,
        'parent': parent,
        'grandparent': current_grandparent,
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
    tags = point['tags']

    new_position = Position.objects.create(position_statement=point['position'])
    new_position.tags.add(*tags)
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
        'get_params': parent_param + grandparent_param
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
    
    return_info = parent_param + grandparent_param

    return return_info


def tag_index(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    positions_with_tag = Position.objects.filter(tags=tag)

    context = {
        'tag': tag,
        'positions_with_tag': positions_with_tag
    }
    return render(request, 'pro_debate/tag_index.html', context)
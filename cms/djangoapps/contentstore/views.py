import json

from django.http import HttpResponse
from django_future.csrf import ensure_csrf_cookie
from fs.osfs import OSFS

from mitxmako.shortcuts import render_to_response
from xmodule.modulestore.django import modulestore


@ensure_csrf_cookie
def index(request):
    # TODO (cpennington): These need to be read in from the active user
    org = 'mit.edu'
    course = '6002xs12'
    name = '6.002_Spring_2012'
    course = modulestore().get_item(['i4x', org, course, 'course', name])
    weeks = course.get_children()
    return render_to_response('index.html', {'weeks': weeks})


def edit_item(request):
    item_id = request.GET['id']
    item = modulestore().get_item(item_id)
    return render_to_response('unit.html', {
        'contents': item.get_html(),
        'js_module': item.js_module_name(),
        'category': item.category,
        'name': item.name,
    })


def save_item(request):
    item_id = request.POST['id']
    data = json.loads(request.POST['data'])
    modulestore().update_item(item_id, data)
    return HttpResponse(json.dumps({}))


def temp_force_export(request):
    org = 'mit.edu'
    course = '6002xs12'
    name = '6.002_Spring_2012'
    course = modulestore().get_item(['i4x', org, course, 'course', name])
    fs = OSFS('../data-export-test')
    xml = course.export_to_xml(fs)
    with fs.open('course.xml', 'w') as course_xml:
        course_xml.write(xml)

    return HttpResponse('Done')

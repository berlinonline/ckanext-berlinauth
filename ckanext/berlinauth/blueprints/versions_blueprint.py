from flask import Blueprint
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base

versions_blueprint = Blueprint('versions_blueprint', __name__)

@versions_blueprint.route('/ckan-admin/versions')
def versions():
    # Call the existing CKAN action internally
    context = {'for_view': True}
    data_dict = {}
    status = toolkit.get_action('status_show')(context, data_dict)

    return base.render('versions.html', extra_vars={'status': status})


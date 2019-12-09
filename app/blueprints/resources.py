from flask import Blueprint, render_template, abort

bp = Blueprint('resources', __name__)


CLUSTER_ID = "clusteridentification"
OSM_ID = "osm"
SURVEY_ID = "surveytools"
GRID_MAPPING_ID = "ongridmapping"


RESOURCES_ATTRIBUTES = {
    CLUSTER_ID: {
        'title': 'Cluster Identification',
        'subtitle': 'How can I identify locations of settlements?',
        'description': 'When looking at energy access and rural electrification it is crucial to '
                       'understand where exactly the non- or undersupplied people are living and '
                       'in which settlement structure, e.g. in dispersed settlements or more '
                       'centralized village structures. This is also required for the development '
                       'of the most techno-economic feasible supply option, e.g. by mini-grids. '
                       'In order to understand those spatial population structures we used '
                       'datasets created from satellite imagery which detect buildings in a high '
                       'spatial resolution. We used those in order to create so-called population '
                       'clusters which we populate with additional information through remote '
                       'mapping of building footprints and surveys.',
        'image': 'img/img-5-resource-cluster.png'
    },
    OSM_ID: {
        'title': 'Mapping with OSM',
        'subtitle': 'How can I map a settlement in detail remotely? ',
        'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.',
        'image': 'img/img-6-resources-osm.png'
    },
    SURVEY_ID: {
        'title': 'Survey Tools',
        'subtitle': 'How can I visit a settlement and collect relevant data?',
        'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.',
        'image': 'img/img-7-resources-survey.png'
    },
    GRID_MAPPING_ID: {
        'title': 'On Grid Mapping',
        'subtitle': 'How can I track the grid?',
        'description': 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus.',
        'image': 'img/img-8-resources-og-mapping.png'
    },
}


@bp.route('/resources/')
@bp.route('/resources')
def index():
    return render_template('resources/index.html')


@bp.route('/resources/<resc_name>')
def selection(resc_name=None):
    if resc_name in RESOURCES_ATTRIBUTES.keys():
        return render_template('resources/selection.html', **RESOURCES_ATTRIBUTES[resc_name])
    else:
        abort(404)

from flask import Blueprint, render_template, abort, Markup, redirect, url_for

bp = Blueprint('resources', __name__)


CLUSTER_ID = "clusteridentification"
OSM_ID = "osm"
SURVEY_ID = "surveytools"
GRID_MAPPING_ID = "ongridmapping"


RESOURCES_ATTRIBUTES = {
    CLUSTER_ID: {
        'title': 'Cluster Identification',
        'subtitle': 'How can I identify locations of settlements?',
        'description': Markup(
            '''<p>When looking at energy access and rural electrification it is crucial to 
               understand where exactly the non- or undersupplied people are living and in
                which settlement structure they live, e.g. in dispersed settlements or 
               more centralized village structures. This is required in order to identify 
               a suitable electrification option such as by mini-grids, grid-connection or 
               stand-alone solution. In order to understand those spatial population 
               structures, we used openly available datasets derived from satellite 
               imagery to detect buildings in a high spatial resolution.</p>
               <p>More information on the detailed methodology behind the dataset is available at the <a href="https://www.ciesin.columbia.edu/data/hrsl/" target="_blank" rel="noreferrer">Center for International Earth Science Information Network</a> and at the <a href="https://dataforgood.fb.com/docs/methodology-high-resolution-population-density-maps-demographic-estimates/" target="_blank" rel="noreferrer">Facebook Connectivity Lab</a>.</p>
                <p>The lastest data download for Nigeria is available <a href="https://data.humdata.org/dataset/highresolutionpopulationdensitymaps-nga" target="_blank" rel="noreferrer">here</a>.</p>
                <p>The population clusters have been created by applying a <a href="https://CRAN.R-project.org/package=dbscan" target="_blank" rel="noreferrer">density-based clustering algorithm</a>, available in the open-source software environment <a href="https://www.r-project.org/" target="_blank" rel="noreferrer">R</a>.</p>
                <p>The population clusters have been derived in order to have discrete units with can be supplemented by additional attributes such as their area and their distance to power grid. In the webmap, these criteria can be filtered on, to provide you with a custom filter of clusters.</p>
                <p>Furthermore, these attributed population clusters form the basis for 
               further assessments, by filtering them according to their size and 
               distance to the grid a first selection has been derived for further 
               analysis, such as <a href="{}" target="_blank" rel="noreferrer">remote 
               mapping of building footprints</a>.</p>'''.format("/resources/osm")),
        'image': 'img/img-5-resource-cluster.png'
    },
    OSM_ID: {
        'title': 'Mapping with OSM',
        'subtitle': 'How can I map a settlement in detail remotely? ',
        'description': Markup('''Data on the Open Street Map (OSM) platform is utilised for off-grid areas in this project. This is detailed data of building outlines and any other geospatial datasets, generated either from on-site knowledge or from high resolution satellite imagery. If an off-grid area is not currently on the OSM database, it can be easily added.
        </br></br>
        Do you have an area of interest for an electrification project that you want to do further assessment on? Or do you want to contribute to data to assist electrification efforts in Nigeria? Check out the OSM tools below to help you get started:
        </br></br>
        <ul>
        <li>Create an OSM account on <a href="https://openstreetmap.org" rel="noreferrer"
        target="_blank">openstreetmap.org</a>.</li>
        <li>Read the beginner’s guide on <a href="https://learnosm.org/en/" rel="noreferrer" 
        target="_blank">
        learnosm.org</a> for an introduction.</li>
        <li><a href="https://josm.openstreetmap.de/" rel="noreferrer" target="_blank">JOSM</a> is a
         desktop application in which you can map areas of interest.</li>
        <li>The <a href="https://tasks.hotosm.org/" rel="noreferrer" target="_blank">
        HOT Tasking Manager</a> is used to manage tasks of areas to map. Get in touch and send
        us your OSM username if you want to be involved.</li>
        </ul>
        '''),
        'image': 'img/img-6-resources-osm.png'
    },
    SURVEY_ID: {
        'title': 'Survey Tools',
        'subtitle': 'How can I visit a settlement and collect relevant data?',
        'description': Markup('''Once a remote assessment of the satellite imagery has taken place,
        it is normally required that a potential location for electrification is visited and
        surveyed. Here more detailed information is collected to enable a more accurate demand
        assessment for the purposes of electrification. At Nigeria SE4ALL we have developed survey
        templates and tools to conduct the surveys.
        </br></br>
        Do you want to survey a potential location for electrification purposes? Or do you live in
        a settlement that you think could benefit from an electrification project, and want to
        share more information on this location to facilitate a project to happen?
        Check out the survey tools below to get started:
        </br></br>
        <ul>
        <li>To gather geospatial data about business locations, have a look at using
        <a href="http://fieldpapers.org/" rel="noreferrer" target="_blank">Field Papers</a> in
        conjunction with OSM data.</li>
        <li>A
        <a href="https://www.kobotoolbox.org/" rel="noreferrer" target="_blank">KoBoToolbox</a>
        questionnaire is also available. Get in touch with us and describe in a few sentences why
        you would like to collect the data, as well as sharing your KoBoToolbox username.
        You can then receive access to the questionnaires.</li>
        '''),
        'image': 'img/img-7-resources-survey.png'
    },
    GRID_MAPPING_ID: {
        'title': 'On Grid Mapping',
        'subtitle': 'How can I track the grid?',
        'description': 'The Medium Voltage (MV) grid data used by Nigeria SE4ALL is either primary data which is gathered first hand by the SE4ALL field team, or secondary data whose quality has been validated by the SE4ALL field team. Our aim is to maintain the most comprehensive grid data-set for Nigeria. To achieve this, we encourage anyone who may have more up-to date grid data, or additions to the grid data-set generated to get in touch and share their updates.',
        'image': 'img/img-8-resources-og-mapping.png'
    },
}


@bp.route('/resources/')
@bp.route('/resources')
def index():
    return redirect(url_for('landing', _anchor='landing-resources'))


@bp.route('/resources/<resc_name>')
def selection(resc_name=None):
    if resc_name in RESOURCES_ATTRIBUTES.keys():
        return render_template('resources/selection.html', **RESOURCES_ATTRIBUTES[resc_name])
    else:
        abort(404)

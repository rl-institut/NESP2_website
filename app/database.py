import os
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
import geoalchemy2
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")


DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=POSTGRES_USER,
    pw=POSTGRES_PW,
    url=POSTGRES_URL,
    db=POSTGRES_DB
)


PROGRESS_NUMBER_MAX = {
    'max_km_electricity': 'km electricity grid tracked',
    'max_villages': 'villages remotely mapped',
    'max_buildings': 'buildings mapped'
}
engine = create_engine(DB_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base(metadata=MetaData(schema='se4all', bind=engine))
BaseWeb = declarative_base(metadata=MetaData(schema='web', bind=engine))


class DlinesSe4all(Base):
    __table__ = Table('distribution_line_se4all', Base.metadata, autoload=True, autoload_with=engine)

class BoundaryAdmin(Base):
    __table__ = Table('boundary_adm1', Base.metadata, autoload=True, autoload_with=engine)

class GaugeMaximum(BaseWeb):
    __table__ = Table('ourprogress_maximums', BaseWeb.metadata, autoload=True, autoload_with=engine)


class MappedVillages(BaseWeb):
    __table__ = Table('ourprogress_villagesremotelymapped', BaseWeb.metadata, autoload=True,
                      autoload_with=engine)


class MappedBuildings(BaseWeb):
    __table__ = Table('ourprogress_buildingsmapped', BaseWeb.metadata, autoload=True,
                      autoload_with=engine)


def select_materialized_view(engine, view_name, schema=None, limit=None):
    if schema is not None:
        view_name = "{}.{}".format(schema, view_name)
    if limit is None:
        limit = ""
    else:
        limit = " LIMIT {}".format(limit)
    with engine.connect() as con:
        rs = con.execute('SELECT * FROM {}{};'.format(view_name, limit))
        data = rs.fetchall()
    return data


def query_electrified_km():
    res = select_materialized_view(engine, "ourprogress_kmelectricitygridtracked_value_v", schema="web")[0][0]
    return int(res)


def query_mapped_villages():
    res = select_materialized_view(engine, "ourprogress_villagesremotelymapped_value_v", schema="web")[0][0]
    return int(res)


def query_mapped_buildings():
    res = select_materialized_view(engine, "ourprogress_buildingsmapped_value_v", schema="web")[0][0]
    return int(res)


def query_gauge_maximum(desc):
    """Query the maximum value for a given progress gauge

    :param desc: the name of the variable under "Our progress in numbers" on the website
    :return: the maximum value as string
    """
    res = db_session.query(GaugeMaximum.maximum.label("max"))\
        .filter(GaugeMaximum.description.ilike("%{}%".format(desc))).first()
    return str(int(res.max))


def get_state_codes():
    res = db_session.query(
        BoundaryAdmin.adm1_pcode.label("code"),
        BoundaryAdmin.adm1_en.label("name")
    )
    return {r.name:r.code.lower() for r in res}


OG_CLUSTERS_COLUMNS = ('adm1_pcode', 'cluster_offgrid_id', 'area_km2',
    'building_count', 'percentage_building_area', 'grid_dist_km', 'geom')


def get_random_og_cluster(engine, view_code, schema="web", limit=20):
    """Select a random cluster from a given view

    :param engine: database engine
    :param view_name: the state code of the view formatted as "ngXYZ"
    :param schema: the name of the database schema
    :param limit: the number of villages to choose from
    :return: the information of one cluster : 'adm1_pcode', 'cluster_offgrid_id', 'area_km2',
    'building_count', 'percentage_building_area', 'grid_dist_km', 'geom'
    """

    if schema is not None:
        view_name = "{}.cluster_offgrid_{}_mv".format(schema, view_code)
    with engine.connect() as con:
        rs = con.execute('SELECT * FROM {} ORDER BY area_km2 LIMIT {};'.format(view_name, limit))
        data = rs.fetchall()
    single_cluster = data[random.randint(0, int(limit)-1)]
    return {key: single_cluster[key] for key in OG_CLUSTERS_COLUMNS}


def query_random_og_cluster(state_name, state_codes_dict):
    return get_random_og_cluster(engine=engine, view_code=state_codes_dict[state_name])

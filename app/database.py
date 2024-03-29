import os
import random
import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
import geoalchemy2.functions as func
from sqlalchemy import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from geojson import Point, Feature, FeatureCollection, LineString
from shapely.wkt import loads as loadswkt
from shapely.wkb import loads as loadswkb


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


DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
    user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB
)


PROGRESS_NUMBER_MAX = {
    "max_km_electricity": "km electricity grid tracked",
    "max_villages": "villages remotely mapped",
    "max_buildings": "buildings mapped",
}
engine = create_engine(DB_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


Base = declarative_base(metadata=MetaData(schema="se4all", bind=engine))
BaseWeb = declarative_base(metadata=MetaData(schema="web", bind=engine))


class DlinesSe4all(Base):
    __table__ = Table(
        "distribution_line_se4all", Base.metadata, autoload=True, autoload_with=engine
    )


class BoundaryAdmin(Base):
    __table__ = Table(
        "boundary_adm1", Base.metadata, autoload=True, autoload_with=engine
    )


class AdmStatus(Base):
    __table__ = Table(
        "boundary_adm1_status", Base.metadata, autoload=True, autoload_with=engine
    )


class GaugeMaximum(BaseWeb):
    __table__ = Table(
        "ourprogress_maximums", BaseWeb.metadata, autoload=True, autoload_with=engine
    )


class MappedVillages(BaseWeb):
    __table__ = Table(
        "ourprogress_villagesremotelymapped",
        BaseWeb.metadata,
        autoload=True,
        autoload_with=engine,
    )


class MappedBuildings(BaseWeb):
    __table__ = Table(
        "ourprogress_buildingsmapped",
        BaseWeb.metadata,
        autoload=True,
        autoload_with=engine,
    )


class GenerationAssets(Base):
    __table__ = Table(
        "generation_assets", Base.metadata, autoload=True, autoload_with=engine
    )


class PowerLines(Base):
    __table__ = Table(
        "osm_power_line", Base.metadata, autoload=True, autoload_with=engine
    )


class PowerStations(Base):
    __table__ = Table(
        "osm_power_substation", Base.metadata, autoload=True, autoload_with=engine
    )


class DashboardsData(Base):
    __table__ = Table(
        "generation_details", Base.metadata, autoload=True, autoload_with=engine
    )


def select_materialized_view(engine, view_name, schema=None, limit=None):
    if schema is not None:
        view_name = "{}.{}".format(schema, view_name)
    if limit is None:
        limit = ""
    else:
        limit = " LIMIT {}".format(limit)
    with engine.connect() as con:
        rs = con.execute("SELECT * FROM {}{};".format(view_name, limit))
        data = rs.fetchall()
    return data


def query_electrified_km():
    res = select_materialized_view(
        engine, "ourprogress_kmelectricitygridtracked_value_v", schema="web"
    )[0][0]
    return int(res)


def query_mapped_villages():
    res = select_materialized_view(
        engine, "ourprogress_villagesremotelymapped_value_v", schema="web"
    )[0][0]
    return int(res)


def query_mapped_buildings():
    res = select_materialized_view(
        engine, "ourprogress_buildingsmapped_value_v", schema="web"
    )[0][0]
    return int(res)


def query_gauge_maximum(desc):
    """Query the maximum value for a given progress gauge

    :param desc: the name of the variable under "Our progress in numbers" on the website
    :return: the maximum value as string
    """
    res = (
        db_session.query(GaugeMaximum.maximum.label("max"))
        .filter(GaugeMaximum.description.ilike("%{}%".format(desc)))
        .first()
    )
    return str(int(res.max))


def get_state_codes():
    res = db_session.query(
        BoundaryAdmin.adm1_pcode.label("code"), BoundaryAdmin.adm1_en.label("name")
    )
    return {r.name: r.code for r in res}


def query_available_og_clusters():
    """Look for state which have true set for both clusters and og_clusters"""
    res = (
        db_session.query(AdmStatus.adm1_pcode)
        .filter(AdmStatus.cluster_all & AdmStatus.cluster_offgrid)
        .all()
    )
    return [r.adm1_pcode for r in res]


def query_generation_assets():
    """Look for on and off grid generation assets"""

    res = db_session.query(
        GenerationAssets.name,
        func.ST_AsText(
            func.ST_Transform(
                func.ST_GeomFromWKB(GenerationAssets.geom, srid=3857), 4326
            )
        ).label("geom"),
        GenerationAssets.capacity_kw,
        GenerationAssets.asset_type,
        GenerationAssets.technology_type,
    )

    features = []
    for r in res:
        if r.geom is not None:
            gjson = Feature(
                geometry=Point(loadswkt(r.geom).coords[0]),
                properties={
                    "name": r.name,
                    "capacity_kw": r.capacity_kw,
                    "technology_type": r.technology_type,
                    "asset_type": r.asset_type,
                },
            )
            features.append(gjson)

    return FeatureCollection(features)


def query_dashboard_data():

    res = db_session.query(
        DashboardsData.technology,
        DashboardsData.start_year_of_operation,
        DashboardsData.capacity_mw,
        DashboardsData.capacity_regenerative_mw,
    )

    df = pd.DataFrame.from_records(
        [r for r in res],
        coerce_float=True,
        columns=[
            "technology",
            "start_year_of_operation",
            "capacity_mw",
            "capacity_regenerative_mw",
        ],
    )

    cum_cap = [12409]
    sum_cap = 12409

    cum_cap_re = [1930]
    sum_cap_re = 1930

    percent_renewable = [round(100 * sum_cap_re / sum_cap, 0)]

    years = [y for y in range(2020, 2031, 1)]

    for y in years[1:]:
        cap, cap_re = df.loc[
            df.start_year_of_operation == y, ["capacity_mw", "capacity_regenerative_mw"]
        ].sum()
        sum_cap = sum_cap + cap
        cum_cap.append(sum_cap)

        sum_cap_re = sum_cap_re + cap_re
        cum_cap_re.append(sum_cap_re)

        percent_renewable.append(round(100 * (sum_cap_re / sum_cap), 0))

    res = ["Hydro", "PV", "Wind"]
    re_type = {}
    for re in res:
        re_type[re] = []
        for y in years:
            re_type[re].append(
                int(
                    df.loc[
                        (df.technology == re) & (df.start_year_of_operation <= y),
                        "capacity_mw",
                    ].sum()
                )
            )

    return years, cum_cap, percent_renewable, re_type


def query_osm_power_lines():
    lines = db_session.query(func.ST_Transform(PowerLines.geom, 4326).label("geom"))

    features = []

    for r in lines:
        if r.geom is not None:
            features.append(
                Feature(geometry=LineString(loadswkb(bytes(r.geom.data)).coords),)
            )

    return FeatureCollection(features)


def query_osm_power_stations():
    res = db_session.query(
        func.ST_AsText(
            func.ST_Transform(func.ST_AsEWKB(PowerStations.geom), 4326)
        ).label("geom"),
        PowerStations.tags,
    )

    features = []

    for r in res:
        if r.geom is not None:
            features.append(
                Feature(geometry=Point(loadswkt(r.geom).coords[0]), properties=r.tags)
            )

    return FeatureCollection(features)


OG_CLUSTERS_COLUMNS = (
    "adm1_pcode",
    "cluster_offgrid_id",
    "area_km2",
    "building_count",
    "percentage_building_area",
    "grid_dist_km",
    "geom",
)


def get_random_og_cluster(engine, view_code, schema="web", limit=5):
    """Select a random cluster from a given view

    :param engine: database engine
    :param view_name: the state code of the view formatted as "ngXYZ"
    :param schema: the name of the database schema
    :param limit: the number of villages to choose from
    :return: the information of one cluster : 'adm1_pcode', 'cluster_offgrid_id', 'area_km2',
    'building_count', 'percentage_building_area', 'grid_dist_km', 'geom'
    """

    if schema is not None:
        view_name = "{}.cluster_offgrid_mv".format(schema, view_code)
    cols = ", ".join(OG_CLUSTERS_COLUMNS[:-1])
    cols = (
        cols + ", ST_AsGeoJSON(bounding_box) as geom, ST_AsGeoJSON(centroid) as lnglat"
    )
    with engine.connect() as con:
        rs = con.execute(
            "SELECT {} FROM {} WHERE adm1_pcode='{}' ORDER BY area_km2 DESC LIMIT {};".format(
                cols, view_name, view_code, limit
            )
        )
        data = rs.fetchall()
    single_cluster = data[random.randint(0, min([int(limit), len(data)]) - 1)]
    return {
        key: str(single_cluster[key])
        for key in OG_CLUSTERS_COLUMNS + ("geom", "lnglat")
    }


def query_random_og_cluster(state_name, state_codes_dict):
    """Protects from SQL injection by matching state_name in the state_codes_dict

    It is linked to /random-cluster endpoint via a post method
    """
    return get_random_og_cluster(engine=engine, view_code=state_codes_dict[state_name])


def filter_materialized_view(
    engine,
    view_name,
    schema="web",
    state_code=None,
    area=None,
    distance_grid=None,
    building=None,
    buildingfp=None,
    limit=None,
    keys=None,
):
    """

    :param engine:
    :param view_name: name of the view in the database (NOT A USER INPUT)
    :param schema: name of the schema in the database (NOT A USER INPUT)
    :param state_code: admin code of nigerian state (PROOFED USER INPUT)
    :param area: boundaries for settlement's area filter (USER INPUT)
    :param distance_grid: boundaries for settlement's distance to grid filter (USER INPUT)
    :param building: boundaries for settlement's building count filter (USER INPUT)
    :param buildingfp: boundaries for settlement's building percentage of area filter (USER INPUT)
    :param limit: boundaries for settlement area filter (NOT A USER INPUT)
    :param keys: list of columns to query values from (NOT A USER INPUT)
    :return: returned data from the query
    """

    # to hold query parameters
    values = {}

    if schema is not None:
        view_name = "{}.{}".format(schema, view_name)

    if limit is None:
        limit = ""
    else:
        values["limit"] = int(limit)
        limit = " LIMIT :limit"

    filter_cond = []

    if state_code is not None:
        key = "adm1_pcode"
        filter_cond += [f"{view_name}.{key} = :{key}"]
        values[key] = state_code

    if area is not None:
        key = "area_km2"
        val1 = key + "_1"
        val2 = key + "_2"
        filter_cond += [
            f"{view_name}.{key} >= :{val1}",
            f"{view_name}.{key} <= :{val2}",
        ]
        values[val1] = float(area[0])
        values[val2] = float(area[1])

    if distance_grid is not None:
        key = "grid_dist_km"
        val1 = key + "_1"
        val2 = key + "_2"
        filter_cond += [
            f"{view_name}.{key} >= :{val1}",
            f"{view_name}.{key} <= :{val2}",
        ]
        values[val1] = float(distance_grid[0])
        values[val2] = float(distance_grid[1])

    if building is not None:
        key = "building_count"
        val1 = key + "_1"
        val2 = key + "_2"
        filter_cond += [f"{view_name}.{key}>=:{val1}", f"{view_name}.{key}<=:{val2}"]
        values[val1] = int(round(float(building[0]), 0))
        values[val2] = int(round(float(building[1]), 0))

    if buildingfp is not None:
        key = "percentage_building_area"
        val1 = key + "_1"
        val2 = key + "_2"
        filter_cond += [f"{view_name}.{key}>=:{val1}", f"{view_name}.{key}<=:{val2}"]
        values[val1] = float(buildingfp[0])
        values[val2] = float(buildingfp[1])

    if keys is None:
        columns = "*"
    else:
        if not isinstance(keys, str):
            columns = ", ".join(keys)
        else:
            columns = "COUNT({})".format(keys)

    if len(filter_cond) > 0:
        filter_cond_str = " WHERE " + " AND ".join(filter_cond)
    else:
        filter_cond_str = ""

    with engine.connect() as con:
        query = "SELECT {} FROM {}{}{};".format(
            columns, view_name, filter_cond_str, limit
        )
        rs = con.execute(text(query), **values)
        data = rs.fetchall()
    return data


def convert_web_mat_view_to_light_json(records, cols):
    df = pd.DataFrame()

    for l in records:
        l = dict(l)
        geom = json.loads(l.pop("geom"))
        lnglat = json.loads(l.pop("lnglat"))

        l.update(
            {
                "lat": lnglat["coordinates"][1],
                "lng": lnglat["coordinates"][0],
                "bNorth": geom["coordinates"][0][2][1],
                "bSouth": geom["coordinates"][0][0][1],
                "bEast": geom["coordinates"][0][2][0],
                "bWest": geom["coordinates"][0][0][0],
            }
        )
        df = df.append(l, ignore_index=True)

    value_list = []
    for c in cols:
        value_list = value_list + df[c].to_list()

    return {
        "adm1_pcode": df["adm1_pcode"].unique()[0],
        "length": len(df.index),
        "columns": cols,
        "values": value_list,
    }


def query_filtered_clusters(
    state_name, state_codes_dict, area=None, distance_grid=None, limit=None, keys=None
):
    """

    :param state_name:
    :param state_codes_dict:
    :param area:
    :param distance_grid:
    :param limit:
    :param keys:
    :return:
    """

    if state_name in state_codes_dict:
        view_name = "cluster_all_mv"
        answer = filter_materialized_view(
            engine,
            view_name,
            schema="web",
            state_code=state_codes_dict[state_name],
            area=area,
            distance_grid=distance_grid,
            limit=limit,
            keys=keys,
        )
    else:
        print("Non existent state name: {}".format(state_name))
        answer = []
    return answer


def query_filtered_og_clusters(
    state_name,
    state_codes_dict,
    area=None,
    distance_grid=None,
    building=None,
    buildingfp=None,
    limit=None,
    keys=None,
):
    """

    :param state_name:
    :param state_codes_dict:
    :param area:
    :param distance_grid:
    :param building:
    :param buildingfp:
    :param limit:
    :param keys:
    :return:
    """

    if state_name in state_codes_dict:
        view_name = "cluster_offgrid_mv"
        answer = filter_materialized_view(
            engine,
            view_name,
            schema="web",
            state_code=state_codes_dict[state_name],
            area=area,
            distance_grid=distance_grid,
            building=building,
            buildingfp=buildingfp,
            limit=limit,
            keys=keys,
        )
    else:
        print("Non existent state name: {}".format(state_name))
        answer = []
    return answer

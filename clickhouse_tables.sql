create database project;

create table project.cafe
(
    id String,
    name String, 
    price_level Nullable(Float64),
    rating Nullable(Float64),
    types String,
    user_ratings_total Nullable(Float64),
    lat Float64,
    lng Float64,
    closest_metro String, 
    closest_metro_km Float64,
    n_nearest_museums Int64,
    n_nearest_art_galleries Int64,
    n_nearest_shopping_malls Int64,
    n_nearest_tourist_attractions Int64,
    n_nearest_same_establishments Int64,
    opportunity_take_away Int64,
    distance_to_center_km Float64,
    result Float64
)
ENGINE = ReplacingMergeTree()
PARTITION BY types
ORDER BY (id)
SETTINGS index_granularity=4096;



create table project.distr_cafe AS project.cafe
ENGINE = Distributed(awesome_cluster, project, cafe, rand())



SELECT 
    closest_metro,
    avg(user_ratings_total) as avg_ratings_count
FROM project.cafe
GROUP BY closest_metro
ORDER BY avg_ratings_count


CREATE MATERIALIZED VIEW project.mv_avg_ratings_by_metro
ENGINE = AggregatingMergeTree()
ORDER BY avg_ratings_count POPULATE AS
SELECT 
    closest_metro,
    avgState(user_ratings_total) as avg_ratings_count
FROM project.cafe
GROUP BY closest_metro


create table project.distr_mv_avg_ratings_by_metro AS project.mv_avg_ratings_by_metro
ENGINE = Distributed(awesome_cluster, project, mv_avg_ratings_by_metro)
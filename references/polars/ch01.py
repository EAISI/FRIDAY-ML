import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import subprocess
    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 1: Introducing Polars
    """)
    return


@app.cell
def _():
    import polars as pl
    pl.__version__  # The book is built with Polars version 1.20.0
    return (pl,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What Is This Thing Called Polars?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key Features
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key Concepts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Advantages
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why You Should Use Polars
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Performance
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Usability
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Popularity
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sustainability
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Polars Compared to Other Data Processing Packages
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why We Focus on Python Polars
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How This Book Is Organized
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## An ETL Showcase
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Extract
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Import packages
    """)
    return


@app.cell
def _(subprocess):
    # The command below builds the polars_geo plugin used in this chapter
    #! cd plugins/polars_geo && uv run maturin develop --release
    subprocess.call(['cd', 'plugins/polars_geo', '&&', 'uv', 'run', 'maturin', 'develop', '--release'])
    return


@app.cell
def _(get_ipython):
    # Reset the kernel to make the new plugin available

    # The code below will do this automatically when run in IPython
    get_ipython().kernel.do_shutdown(restart=True)
    return


@app.cell
def _():
    import polars_geo
    from plotnine import ggplot, aes, geom_point, geom_line, geom_bar, geom_histogram, facet_wrap, labs, theme_minimal, theme, element_text
    return aes, element_text, geom_point, ggplot, labs, theme


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Download and extract Citi Bike trips
    """)
    return


@app.cell
def _():
    # It might be needed to install `unzip` first if you're on Linux or macOS.
    # Linux:
    # sudo apt update && sudo apt install unzip
    # macOS:
    # brew install unzip
    # Windows:
    # Download the ZIP file manually and extract it (sorry)
    return


@app.cell
def _(subprocess):
    #! curl -sO https://s3.amazonaws.com/tripdata/202403-citibike-tripdata.zip
    subprocess.call(['curl', '-sO', 'https://s3.amazonaws.com/tripdata/202403-citibike-tripdata.zip'])
    #! unzip -o 202403-citibike-tripdata.zip "*.csv" -x "*/*" -d data/citibike/
    subprocess.call(['unzip', '-o', '202403-citibike-tripdata.zip', '*.csv', '-x', '*/*', '-d', 'data/citibike/'])
    #! rm -f 202403-citibike-tripdata.zip
    subprocess.call(['rm', '-f', '202403-citibike-tripdata.zip'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Read Citi Bike trips into a Polars DataFrame
    """)
    return


@app.cell
def _(subprocess):
    #! wc -l data/citibike/202403-citibike-tripdata.csv
    subprocess.call(['wc', '-l', 'data/citibike/202403-citibike-tripdata.csv'])
    #! head -n 6 data/citibike/202403-citibike-tripdata.csv
    subprocess.call(['head', '-n', '6', 'data/citibike/202403-citibike-tripdata.csv'])
    return


@app.cell
def _(pl):
    trips = pl.read_csv(  
        "data/citibike/202403-citibike-tripdata.csv",
        try_parse_dates=True,
        schema_overrides={
            "start_station_id": pl.String,
            "end_station_id": pl.String,
        },
    ).sort(  
        "started_at"
    )

    trips.height
    return (trips,)


@app.cell
def _(trips):
    print(trips[:, :4])
    print(trips[:, 4:8])
    print(trips[:, 8:])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Read in neighborhoods from GeoJSON
    """)
    return


@app.cell
def _(subprocess):
    #! python -m json.tool data/citibike/nyc-neighborhoods.geojson
    subprocess.call(['python', '-m', 'json.tool', 'data/citibike/nyc-neighborhoods.geojson'])
    return


@app.cell
def _(pl):
    neighborhoods = (
        pl.read_json("data/citibike/nyc-neighborhoods.geojson")
        .select("features")
        .explode("features")  
        .unnest("features")
        .unnest("properties")
        .select("neighborhood", "borough", "geometry")
        .unnest("geometry")
        .with_columns(polygon=pl.col("coordinates").list.first())
        .select("neighborhood", "borough", "polygon")
        .filter(pl.col("borough") != "Staten Island")  
        .sort("neighborhood")
    )

    neighborhoods
    return (neighborhoods,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus: Visualizing Neighborhoods and Stations
    """)
    return


@app.cell
def _(neighborhoods, pl):
    neighborhoods_coords = (
        neighborhoods.with_row_index("id")
        .explode("polygon")
        .with_columns(
            lon=pl.col("polygon").list.first(),
            lat=pl.col("polygon").list.last(),
        )
        .drop("polygon")
    )

    neighborhoods_coords
    return (neighborhoods_coords,)


@app.cell
def _(pl, trips):
    stations = (
        trips.group_by(station=pl.col("start_station_name"))
        .agg(  
            lon=pl.col("start_lng").median(),
            lat=pl.col("start_lat").median(),
        )
        .sort("station")
        .drop_nulls()
    )
    stations
    return (stations,)


@app.cell
def _(
    aes,
    element_rect,
    element_text,
    geom_point,
    geom_polygon,
    ggplot,
    guides,
    labs,
    neighborhoods_coords,
    scale_alpha_ordinal,
    scale_fill_brewer,
    scale_x_continuous,
    scale_y_continuous,
    stations,
    theme,
    theme_void,
):
    (
        ggplot(neighborhoods_coords, aes(x="lon", y="lat", group="id"))
        + geom_polygon(aes(alpha="neighborhood", fill="borough"), color="white")
        + geom_point(stations, size=0.1)
        + scale_x_continuous(expand=(0, 0))
        + scale_y_continuous(expand=(0, 0, 0, 0.01))
        + scale_alpha_ordinal(range=(0.3, 1))
        + scale_fill_brewer(type="qual", palette=2)
        + guides(alpha=False)
        + labs(
            title="New York City neighborhoods and Citi Bike stations",
            subtitle="2,143 stations across 106 neighborhoods",
            caption="Source: https://citibikenyc.com/system-data",
            fill="Borough",
        )
        + theme_void(base_size=14)
        + theme(
            dpi=300,
            figure_size=(7, 9),
            plot_background=element_rect(fill="white", color="white"),
            plot_caption=element_text(style="italic"),
            plot_margin=0.01,
            plot_title=element_text(ha="left"),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Transform
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Clean up columns
    """)
    return


@app.cell
def _(pl, trips):
    trips_1 = trips.select(bike_type=pl.col('rideable_type').str.split('_').list.get(0).cast(pl.Categorical), rider_type=pl.col('member_casual').cast(pl.Categorical), datetime_start=pl.col('started_at'), datetime_end=pl.col('ended_at'), station_start=pl.col('start_station_name'), station_end=pl.col('end_station_name'), lon_start=pl.col('start_lng'), lat_start=pl.col('start_lat'), lon_end=pl.col('end_lng'), lat_end=pl.col('end_lat')).with_columns(duration=pl.col('datetime_end') - pl.col('datetime_start'))
    trips_1.columns
    return (trips_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Clean up rows
    """)
    return


@app.cell
def _(pl, trips_1):
    trips_2 = trips_1.drop_nulls().filter((pl.col('datetime_start') >= pl.date(2024, 3, 1)) & (pl.col('datetime_end') < pl.date(2024, 4, 1))).filter(~((pl.col('station_start') == pl.col('station_end')) & (pl.col('duration').dt.total_seconds() < 5 * 60)))
    trips_2.height
    return (trips_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Add trip distance
    """)
    return


@app.cell
def _(pl, trips_2):
    trips_3 = trips_2.with_columns(distance=pl.concat_list('lon_start', 'lat_start').geo.haversine_distance(pl.concat_list('lon_end', 'lat_end')) / 1000)
    trips_3.select('lon_start', 'lon_end', 'lat_start', 'lat_end', 'distance', 'duration')
    return (trips_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Add borough and neighborhood
    """)
    return


@app.cell
def _(neighborhoods, pl, stations):
    stations_1 = stations.with_columns(point=pl.concat_list('lon', 'lat')).join(neighborhoods, how='cross').with_columns(in_neighborhood=pl.col('point').geo.point_in_polygon(pl.col('polygon'))).filter(pl.col('in_neighborhood')).unique('station').select('station', 'borough', 'neighborhood')
    stations_1
    return (stations_1,)


@app.cell
def _(pl, stations_1, trips_3):
    trips_4 = trips_3.join(stations_1.select(pl.all().name.suffix('_start')), on='station_start').join(stations_1.select(pl.all().name.suffix('_end')), on='station_end').select('bike_type', 'rider_type', 'datetime_start', 'datetime_end', 'duration', 'station_start', 'station_end', 'neighborhood_start', 'neighborhood_end', 'borough_start', 'borough_end', 'lat_start', 'lon_start', 'lat_end', 'lon_end', 'distance')
    return (trips_4,)


@app.cell
def _(trips_4):
    print(trips_4[:, :4])
    print(trips_4[:, 4:7])
    print(trips_4[:, 7:11])
    print(trips_4[:, 11:])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus: Visualizing Daily Trips per Borough
    """)
    return


@app.cell
def _(pl, trips_4):
    trips_per_day = trips_4.group_by_dynamic('datetime_start', group_by='borough_start', every='1d').agg(num_trips=pl.len())
    trips_per_day
    return (trips_per_day,)


@app.cell
def _(
    aes,
    element_line,
    element_rect,
    element_text,
    geom_area,
    ggplot,
    labs,
    scale_fill_brewer,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_tufte,
    trips_per_day,
):
    from mizani.labels import label_comma

    (
        ggplot(
            trips_per_day,
            aes(x="datetime_start", y="num_trips", fill="borough_start"),
        )
        + geom_area()
        + scale_fill_brewer(type="qual", palette=2)
        + scale_x_datetime(date_labels="%-d", date_breaks="1 day", expand=(0, 0))
        + scale_y_continuous(labels=label_comma(), expand=(0, 0))
        + labs(
            x="March 2024",
            fill="Borough",
            y="Trips per day",
            title="Citi Bike trips per day in March 2024",
            subtitle="On March 23, nearly 10 cm of rain fell in NYC",
        )
        + theme_tufte(base_size=14)
        + theme(
            axis_ticks_major=element_line(color="white"),
            figure_size=(8, 5),
            legend_position="top",
            plot_background=element_rect(fill="white", color="white"),
            plot_caption=element_text(style="italic"),
            plot_title=element_text(ha="left"),
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Load
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Write partitions
    """)
    return


@app.cell
def _(pl, trips_4):
    trips_parts = trips_4.sort('datetime_start').with_columns(date=pl.col('datetime_start').dt.date().cast(pl.String)).partition_by(['date'], as_dict=True, include_key=False)
    for key, df in trips_parts.items():
        df.write_parquet(f'data/citibike/trips-{key[0]}.parquet')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Verify
    """)
    return


@app.cell
def _(subprocess):
    #! ls -1 data/citibike/*.parquet
    subprocess.call(['ls', '-1', 'data/citibike/*.parquet'])
    return


@app.cell
def _(pl):
    pl.read_parquet("data/citibike/*.parquet").height
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus: Becoming Faster by Being Lazy
    """)
    return


@app.cell
def _(pl):
    trips_5 = pl.scan_csv('data/citibike/202403-citibike-tripdata.csv', try_parse_dates=True, schema_overrides={'start_station_id': pl.String, 'end_station_id': pl.String}).select(bike_type=pl.col('rideable_type').str.split('_').list.get(0), rider_type=pl.col('member_casual'), datetime_start=pl.col('started_at'), datetime_end=pl.col('ended_at'), station_start=pl.col('start_station_name'), station_end=pl.col('end_station_name'), lon_start=pl.col('start_lng'), lat_start=pl.col('start_lat'), lon_end=pl.col('end_lng'), lat_end=pl.col('end_lat')).with_columns(duration=pl.col('datetime_end') - pl.col('datetime_start')).drop_nulls().filter(~((pl.col('station_start') == pl.col('station_end')) & (pl.col('duration').dt.total_seconds() < 5 * 60))).with_columns(distance=pl.concat_list('lon_start', 'lat_start').geo.haversine_distance(pl.concat_list('lon_end', 'lat_end')) / 1000).collect()
    neighborhoods_1 = pl.read_json('data/citibike/nyc-neighborhoods.geojson').lazy().select('features').explode('features').unnest('features').unnest('properties').select('neighborhood', 'borough', 'geometry').unnest('geometry').with_columns(polygon=pl.col('coordinates').list.first()).select('neighborhood', 'borough', 'polygon').sort('neighborhood').filter(pl.col('borough') != 'Staten Island')
    stations_2 = trips_5.lazy().group_by(station=pl.col('station_start')).agg(lat=pl.col('lat_start').median(), lon=pl.col('lon_start').median()).with_columns(point=pl.concat_list('lon', 'lat')).drop_nulls().join(neighborhoods_1, how='cross').with_columns(in_neighborhood=pl.col('point').geo.point_in_polygon(pl.col('polygon'))).filter(pl.col('in_neighborhood')).unique('station').select(pl.col('station'), pl.col('borough'), pl.col('neighborhood')).collect()
    trips_5 = trips_5.join(stations_2.select(pl.all().name.suffix('_start')), on='station_start').join(stations_2.select(pl.all().name.suffix('_end')), on='station_end').select('bike_type', 'rider_type', 'datetime_start', 'datetime_end', 'duration', 'station_start', 'station_end', 'neighborhood_start', 'neighborhood_end', 'borough_start', 'borough_end', 'lat_start', 'lon_start', 'lat_end', 'lon_end', 'distance')
    trips_5.height
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()

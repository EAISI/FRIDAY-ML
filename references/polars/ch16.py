import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chapter 16: Visualizing Data
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
    ## NYC Bike Trips
    """)
    return


@app.cell
def _(pl):
    trips = pl.read_parquet("data/citibike/*.parquet")

    print(trips[:, :4])
    print(trips[:, 4:7])
    print(trips[:, 7:11])
    print(trips[:, 11:])
    return (trips,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Built-In Plotting with Altair
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Introducing Altair
    """)
    return


@app.cell
def _():
    import altair as alt
    return (alt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Methods in the Plot Namespaces
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plotting DataFrames
    """)
    return


@app.cell
def _(pl, trips):
    trips_speed = trips.select(
        pl.col("distance"),
        pl.col("duration").dt.total_seconds() / 3600,  
        pl.col("bike_type"),
    ).with_columns(speed=pl.col("distance") / pl.col("duration"))

    trips_speed
    return


@app.cell
def _():
    # This raises a MaxRowsError:
    # trips_speed.plot.scatter(
    #    x="distance",
    #    y="duration",
    #    color="bike_type:N",
    # )
    return


@app.cell
def _(pl, trips):
    trips_speed_1 = trips.filter(pl.col('station_start') == 'W 70 St & Amsterdam Ave').select(pl.col('distance'), pl.col('duration').dt.total_seconds() / 3600, pl.col('bike_type')).with_columns(speed=pl.col('distance') / pl.col('duration'))
    trips_speed_1
    return (trips_speed_1,)


@app.cell
def _(trips_speed_1):
    trips_speed_1.plot.scatter(x='distance', y='duration', color='bike_type:N')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Too Large to Handle
    """)
    return


@app.cell
def _(alt):
    alt.data_transformers.disable_max_rows()
    return


@app.cell
def _(alt):
    alt.data_transformers.enable("vegafusion")
    return


@app.cell
def _(trips):
    trips_type_counts = trips.group_by("rider_type", "bike_type").len()
    trips_type_counts
    return (trips_type_counts,)


@app.cell
def _(trips_type_counts):
    from IPython.display import display

    chart = trips_type_counts.plot.bar(
        x="rider_type", y="len", fill="bike_type:N"
    ).properties(
        width=300,
    )
    display(chart)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plotting Series
    """)
    return


@app.cell
def _(trips_speed_1):
    trips_speed_1['distance'].plot.kde()
    return


@app.cell
def _(trips_speed_1):
    trips_speed_1['distance'].plot.hist()
    return


@app.cell
def _(pl, trips):
    trips_hour_num_speed = (
        trips.sort("datetime_start")
        .group_by_dynamic("datetime_start", every="1h")
        .agg(
            num_trips=pl.len(),
            speed=(
                pl.col("distance") / (pl.col("duration").dt.total_seconds() / 3600)
            ).median(),
        )
        .filter(pl.col("datetime_start") > pl.date(2024, 3, 26))
    )

    trips_hour_num_speed
    return (trips_hour_num_speed,)


@app.cell
def _(trips_hour_num_speed):
    trips_hour_num_speed.plot.line(x="datetime_start", y="num_trips")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## pandas-Like Plotting with hvPlot
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Introducing hvPlot
    """)
    return


@app.cell
def _():
    import hvplot.polars
    import hvplot.pandas
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A First Plot
    """)
    return


@app.cell
def _(trips_speed_1):
    trips_speed_1.hvplot.scatter(x='distance', y='duration', color='bike_type', xlabel='distance (km)', ylabel='duration (h)', ylim=(0, 2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Methods in the hvPlot Namespace
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### pandas as Backup
    """)
    return


@app.cell
def _(pl, trips):
    trips_per_day_hour = (
        trips.sort("datetime_start")
        .group_by_dynamic("datetime_start", every="1h")
        .agg(pl.len())
    )
    return (trips_per_day_hour,)


@app.cell
def _():
    # This raises a ValueError:
    # trips_per_day_hour.hvplot.heatmap(
    #     x="datetime_start.hour", y="datetime_start.day", C="len", cmap="reds"
    # )
    return


@app.cell
def _(trips_per_day_hour):
    trips_per_day_hour.to_pandas().hvplot.heatmap(x='datetime_start.hour', y='datetime_start.day', C='len', cmap='reds')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Manual Transformations
    """)
    return


@app.cell
def _(trips_type_counts):
    trips_type_counts.hvplot.bar(
        x="rider_type",
        y="len",
        by="bike_type",
        ylabel="count",
        stacked=True,
        color=["orange", "green"],
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Changing the Plotting Backend
    """)
    return


@app.cell
def _(hvplot_1):
    hvplot_1.extension('matplotlib')
    return


@app.cell
def _(trips_type_counts):
    trips_type_counts.hvplot.bar(
        x="rider_type",
        y="len",
        by="bike_type",
        ylabel="count",
        stacked=True,
        color=["orange", "green"],
    )
    return


@app.cell
def _(hvplot_1):
    hvplot_1.extension('bokeh')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plotting Points on a Map
    """)
    return


@app.cell
def _(trips):
    trips.hvplot.points(
        x="lon_start",
        y="lat_start",
        datashade=True,
        geo=True,
        tiles="CartoLight",
        width=800,
        height=600,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Composing Plots
    """)
    return


@app.cell
def _(trips_hour_num_speed):
    (
        trips_hour_num_speed.hvplot.line(x="datetime_start", y="num_trips")
        + trips_hour_num_speed.hvplot.line(x="datetime_start", y="speed")
    ).cols(  
        1
    )
    return


@app.cell
def _(pl, trips_hour_num_speed):
    (
        trips_hour_num_speed.hvplot.line(x="datetime_start", y="num_trips")
        * trips_hour_num_speed.filter(pl.col("num_trips") > 9000).hvplot.scatter(
            x="datetime_start", y="num_trips", c="red", s=50
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Adding Interactive Widgets
    """)
    return


@app.cell
def _(pl, trips):
    trips_per_hour = (
        trips.sort("datetime_start")
        .group_by_dynamic("datetime_start", group_by="borough_start", every="1h")
        .agg(pl.len())
        .with_columns(date=pl.col("datetime_start").dt.date())
    )
    trips_per_hour
    return (trips_per_hour,)


@app.cell
def _(trips_per_hour):
    trips_per_hour.hvplot.line(
        x="datetime_start",
        by="borough_start",
        groupby="date",
        widget_location="left_top",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Publication-Quality Graphics with plotnine
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Introducing plotnine
    """)
    return


@app.cell
def _():
    from plotnine import ggplot, aes, geom_point, geom_line, geom_bar, geom_histogram, facet_wrap, labs, theme_minimal, theme, element_text
    return (
        aes,
        facet_wrap,
        geom_bar,
        geom_histogram,
        geom_line,
        geom_point,
        ggplot,
        labs,
        theme,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plots for Exploration
    """)
    return


@app.cell
def _(aes, geom_point, ggplot, trips_speed_1):
    ggplot(trips_speed_1, aes(x='distance', y='duration', color='bike_type')) + geom_point()
    return


@app.cell
def _(aes, geom_histogram, ggplot, trips_speed_1):
    ggplot(trips_speed_1, aes(x='distance')) + geom_histogram()
    return


@app.cell
def _(aes, geom_bar, ggplot, trips):
    ggplot(trips, aes(x="rider_type", fill="bike_type")) + geom_bar()
    return


@app.cell
def _(aes, geom_density, ggplot, trips_speed_1):
    ggplot(trips_speed_1, aes(x='distance', fill='bike_type')) + geom_density(alpha=0.7, color='none')
    return


@app.cell
def _(aes, geom_line, geom_point, ggplot, pl, trips_hour_num_speed):
    (
        ggplot(trips_hour_num_speed, aes(x="datetime_start", y="num_trips"))
        + geom_line(size=1, color="steelblue")
        + geom_point(
            data=trips_hour_num_speed.filter(pl.col("num_trips") > 9000),
            color="red",
            size=4,
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plots for Communication
    """)
    return


@app.cell
def _(pl, trips):
    trips_speed_2 = trips.group_by('neighborhood_start', 'neighborhood_end').agg(pl.col('duration').dt.total_seconds().median() / 60, pl.col('distance').median(), pl.col('borough_start').first(), pl.col('borough_end').first(), pl.len()).filter((pl.col('len') > 30) & (pl.col('distance') > 0.2) & (pl.col('neighborhood_start') != pl.col('neighborhood_end'))).with_columns(speed=pl.col('distance') / pl.col('duration')).sort('borough_start')
    trips_speed_2
    return (trips_speed_2,)


@app.cell
def _(
    aes,
    element_rect,
    geom_point,
    geom_smooth,
    ggplot,
    labs,
    pl,
    scale_color_brewer,
    theme,
    theme_tufte,
    trips_speed_2,
    xlim,
    ylim,
):
    ggplot(data=trips_speed_2.filter(pl.col('borough_start') == pl.col('borough_end')), mapping=aes(x='distance', y='duration', color='borough_end')) + geom_point(size=0.25, alpha=0.5) + geom_smooth(method='lowess', size=2, se=False, alpha=0.8) + xlim(0, 15) + ylim(0, 60) + scale_color_brewer(type='qualitative', palette='Set1') + labs(title='Trip distance and duration within each borough', x='Distance (km)', y='Duration (min)', color='Borough') + theme_tufte(base_size=14) + theme(figure_size=(8, 6), plot_background=element_rect(color='#ffffff'))
    return


@app.cell
def _(
    aes,
    facet_wrap,
    geom_point,
    geom_smooth,
    ggplot,
    labs,
    pl,
    scale_color_brewer,
    theme,
    theme_linedraw,
    trips_speed_2,
    xlim,
    ylim,
):
    ggplot(data=trips_speed_2.filter(pl.col('borough_start') != pl.col('borough_end')).with_columns(('From ' + pl.col('borough_start')).alias('borough_start')), mapping=aes(x='distance', y='duration', color='borough_end')) + geom_point(size=0.25, alpha=0.5) + geom_smooth(method='lowess', size=2, se=False, alpha=0.8) + xlim(0, 15) + ylim(0, 60) + scale_color_brewer(type='qualitative', palette='Set1') + facet_wrap('borough_start') + labs(title='Trip distance and duration cross borough', x='Distance (km)', y='Duration (min)', color='To Borough') + theme_linedraw(base_size=14) + theme(figure_size=(8, 6))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Styling DataFrames With Great Tables
    """)
    return


@app.cell
def _(pl, trips):
    import polars.selectors as cs

    busiest_stations = (
        trips.group_by(  
            station=pl.col("station_start"), date=pl.col("datetime_start").dt.date()
        )
        .agg(
            borough=pl.col("borough_start").first(),
            neighborhood=pl.col("neighborhood_start").first(),
            num_rides=pl.len(),
            percent_member=(pl.col("rider_type") == "member").mean(),
            percent_electric=(pl.col("bike_type") == "electric").mean(),
        )
        .sort("date")
        .group_by("station")
        .agg(
            cs.string().first(),
            cs.numeric().mean(),
            pl.col("num_rides").alias("rides_per_day"),  
        )
        .sort("num_rides", descending=True)
        .group_by("borough", maintain_order=True)
        .head(3)
    )

    busiest_stations
    return busiest_stations, cs


@app.cell
def _():
    from great_tables import GT
    return (GT,)


@app.cell
def _(GT, busiest_stations):
    GT(busiest_stations)
    return


@app.cell
def _(GT, busiest_stations, cs):
    from great_tables import style, md

    (
        GT(busiest_stations)
        .tab_stub(rowname_col="station", groupname_col="borough")  
        .cols_label(  
            neighborhood="Neighborhood",
            num_rides="Mean Daily Rides",
            percent_member="Members",
            percent_electric="E-Bikes",
            rides_per_day="Rides Per Day",
        )
        .tab_header(
            title="Busiest Bike Stations in NYC",
            subtitle="In March 2024, Per Borough",
        )
        .tab_stubhead(label="Station")
        .fmt_number(columns="num_rides", decimals=1)
        .fmt_percent(columns=cs.starts_with("percent_"), decimals=0)  
        .fmt_nanoplot(columns="rides_per_day", reference_line="mean")
        .data_color(columns="num_rides", palette="Blues")
        .tab_options(row_group_font_weight="bold")
        .tab_source_note(
            source_note=md(
                "Source: [NYC Citi Bike](https://citibikenyc.com/system-data)"
            )
        )
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()

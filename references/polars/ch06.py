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
    # Chapter 6: Reading and Writing Data
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
    ## Format Overview
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading CSV Files
    """)
    return


@app.cell
def _(subprocess):
    #! cat data/penguins.csv
    subprocess.call(['cat', 'data/penguins.csv'])
    return


@app.cell
def _(pl):
    penguins = pl.read_csv("data/penguins.csv")
    penguins
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Parsing Missing Values Correctly
    """)
    return


@app.cell
def _(pl):
    penguins_1 = pl.read_csv('data/penguins.csv', null_values='NA')
    penguins_1
    return (penguins_1,)


@app.cell
def _(penguins_1):
    penguins_1.null_count().transpose(include_header=True, column_names=['null_count'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading Files with Encodings Other Than UTF-8
    """)
    return


@app.cell
def _():
    # This raises a ComputeError:
    # pl.read_csv("data/directors.csv")
    return


@app.cell
def _(pl):
    pl.read_csv("data/directors.csv", encoding="EUC-CN")
    return


@app.cell
def _():
    import chardet


    def detect_encoding(filename: str) -> str:
        """Return the most probable character encoding for a file."""

        with open(filename, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result["encoding"]


    detect_encoding("data/directors.csv")
    return


@app.cell
def _(pl):
    pl.read_csv("data/directors.csv", encoding="EUC-JP")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading Excel Spreadsheets
    """)
    return


@app.cell
def _(pl):
    songs = pl.read_excel("data/top2000-2023.xlsx")  
    songs
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Working with Multiple Files
    """)
    return


@app.cell
def _(pl):
    pl.read_csv("data/stock/nvda/201?.csv")
    return


@app.cell
def _(pl):
    all_stocks = pl.read_csv("data/stock/**/*.csv")
    all_stocks
    return (all_stocks,)


@app.cell
def _():
    import calendar

    filenames = [
        f"data/stock/asml/{year}.csv"
        for year in range(1999, 2024)
        if calendar.isleap(year)
    ]

    filenames
    return (filenames,)


@app.cell
def _(filenames, pl):
    pl.concat(pl.read_csv(f) for f in filenames)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading Parquet
    """)
    return


@app.cell
def _(pl):
    # magic command not supported in marimo; please file an issue to add support
    # %%time
    trips = pl.read_parquet("data/taxi/yellow_tripdata_*.parquet")
    trips
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading JSON and NDJSON
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### JSON
    """)
    return


@app.cell
def _(subprocess):
    #! cat data/pokedex.json
    subprocess.call(['cat', 'data/pokedex.json'])
    return


@app.cell
def _(pl):
    pokedex = pl.read_json("data/pokedex.json")
    pokedex
    return (pokedex,)


@app.cell
def _(pokedex):
    (
        pokedex.explode("pokemon")
        .unnest("pokemon")
        .select("id", "name", "type", "height", "weight")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NDJSON
    """)
    return


@app.cell
def _(subprocess):
    #! cat data/wikimedia.ndjson
    subprocess.call(['cat', 'data/wikimedia.ndjson'])
    return


@app.cell
def _():
    from json import loads
    from pprint import pprint

    with open("data/wikimedia.ndjson") as f:
        pprint(loads(f.readline()))
    return


@app.cell
def _(pl):
    wikimedia = pl.read_ndjson("data/wikimedia.ndjson")
    wikimedia
    return (wikimedia,)


@app.cell
def _(wikimedia):
    (
        wikimedia.rename({"id": "edit_id"})
        .unnest("meta")
        .select("timestamp", "title", "user", "comment")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Other File Formats
    """)
    return


@app.cell
def _(pl):
    import pandas as pd

    url = "https://en.wikipedia.org/wiki/List_of_Latin_abbreviations"
    pl.from_pandas(pd.read_html(url, storage_options={"User-Agent": "Mozilla/5.0"})[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Querying Databases
    """)
    return


@app.cell
def _(pl):
    pl.read_database_uri(
        query="""
        SELECT
            f.film_id,
            f.title,
            c.name AS category,
            f.rating,
            f.length / 60.0 AS length
        FROM
            film AS f,
            film_category AS fc,
            category AS c
        WHERE
            fc.film_id = f.film_id
            AND fc.category_id = c.category_id
        LIMIT 10
        """,
        uri="sqlite:::data/sakila.db",
    )
    return


@app.cell
def _(pl):
    db = "sqlite:::data/sakila.db"
    films = pl.read_database_uri("SELECT * FROM film", db)
    film_categories = pl.read_database_uri("SELECT * FROM film_category", db)
    categories = pl.read_database_uri("SELECT * FROM category", db)

    (
        films.join(film_categories, on="film_id", suffix="_fc")
        .join(categories, on="category_id", suffix="_c")
        .select(
            "film_id",
            "title",
            pl.col("name").alias("category"),
            "rating",
            pl.col("length") / 60,
        )
        .limit(10)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Writing Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### CSV Format
    """)
    return


@app.cell
def _(all_stocks):
    all_stocks.write_csv("data/all_stocks.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Excel Format
    """)
    return


@app.cell
def _(all_stocks):
    all_stocks.write_excel("data/all_stocks.xlsx")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Parquet Format
    """)
    return


@app.cell
def _(all_stocks):
    all_stocks.write_parquet("data/all_stocks.parquet")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Other Considerations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()

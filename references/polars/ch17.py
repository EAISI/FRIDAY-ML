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
    # Chapter 17: Extending Polars
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
    ## User-Defined Functions in Python
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Applying a Function to Elements
    """)
    return


@app.cell
def _(pl):
    from textblob import TextBlob


    def analyze_sentiment(review):
        return TextBlob(review).sentiment.polarity


    reviews = pl.DataFrame(
        {
            "reviews": [
                "This product is great!",
                "Terrible service.",
                "Okay, but not what I expected.",
                "Excellent! I love it.",
            ]
        }
    )

    reviews.with_columns(
        sentiment_score=pl.col("reviews").map_elements(
            analyze_sentiment, return_dtype=pl.Float64
        )
    )
    return (TextBlob,)


@app.cell
def _(pl):
    ints = pl.DataFrame({"x": [1, 2, 3, 4]})


    def add_one(x):
        return x + 1


    ints.with_columns(
        pl.col("x")
        .map_elements(
            add_one,
            return_dtype=pl.Int64,
        )
        .alias("x + 1")
    )

    # Raises a PolarsInefficientMapWarning
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Applying a Function to a Series
    """)
    return


@app.cell
def _(pl):
    import polars.selectors as cs
    from scipy.special import softmax

    ml_dataset = pl.DataFrame(
        {
            "feature1": [0.3, 0.2, 0.4, 0.1, 0.2, 0.3, 0.5],
            "feature2": [32, 50, 70, 65, 0, 10, 15],
            "label": [1, 0, 1, 0, 1, 0, 0],
        }
    )

    ml_dataset.select(
        "label",
        cs.starts_with("feature").map_batches(
            lambda x: softmax(x.to_numpy()),
            return_dtype=pl.Float64,
        ),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Applying a Function to Groups
    """)
    return


@app.cell
def _(pl):
    from sklearn.preprocessing import StandardScaler


    def scale_temperature(group):
        scaler = StandardScaler()
        scaled_values = scaler.fit_transform(group[["temperature"]].to_numpy())
        return group.with_columns(
            pl.Series(values=scaled_values.flatten(), name="scaled_feature")
        )


    temperatures = pl.DataFrame(
        {
            "country": ["USA", "USA", "USA", "USA", "NL", "NL", "NL"],
            "temperature": [32, 50, 70, 65, 0, 10, 15],
        }
    )

    temperatures.group_by("country").map_groups(scale_temperature)
    return


@app.cell
def _(pl):
    temperatures_1 = pl.DataFrame({'country': ['USA', 'USA', 'USA', 'USA', 'NL', 'NL', 'NL'], 'temperature': [32, 50, 70, 65, 0, 10, 15]})
    for group, df in temperatures_1.group_by('country'):
        print(f'{group[0]}:\n{df}\n')
    return


@app.cell
def _(TextBlob, pl):
    from functools import lru_cache

    @lru_cache(maxsize=256)
    def analyze_sentiment_1(review):
        return TextBlob(review).sentiment.polarity
    reviews_1 = pl.DataFrame({'reviews': ['This product is great!', 'Terrible service.', 'Okay, but not what I expected.', 'Excellent! I love it.']})
    reviews_1.with_columns(sentiment_score=pl.col('reviews').map_elements(analyze_sentiment_1, return_dtype=pl.Float64))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Applying a Function to an Expression
    """)
    return


@app.cell
def _(pl):
    addresses = pl.DataFrame(
        {
            "address": [
                "Nieuwezijds Voorburgwal 147",
                "Museumstraat 1",
                "Oosterdok 2",
            ]
        }
    )


    def extract_house_number(input_expr: pl.Expr) -> pl.Expr:
        """Extract the house number from an address String"""
        return input_expr.str.extract(r"\d+", 0).cast(pl.Int64)


    addresses.with_columns(
        house_numbers=pl.col("address").pipe(extract_house_number)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Applying a Function to a DataFrame or LazyFrame
    """)
    return


@app.cell
def _(pl):
    small_numbers = pl.DataFrame({"ints": [2, 4, 6], "floats": [10.0, 20.0, 30.0]})


    def scale_the_input(
        df: pl.DataFrame | pl.LazyFrame, scale_factor: int
    ) -> pl.DataFrame | pl.LazyFrame:
        """Scales the input by the input factor"""
        return df * scale_factor


    small_numbers.pipe(scale_the_input, 5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Registering Your Own Namespace
    """)
    return


@app.cell
def _(pl):
    @pl.api.register_expr_namespace("celsius")  
    class Celsius:
        def __init__(self, expr: pl.Expr):  
            self._expr = expr

        def to_fahrenheit(self) -> pl.Expr:  
            return (self._expr * 9 / 5) + 32

        def to_kelvin(self) -> pl.Expr:
            return self._expr + 273.15
    return


@app.cell
def _(pl):
    temperatures_2 = pl.DataFrame({'celsius': [0, 10, 20, 30, 40]})
    temperatures_2.with_columns(fahrenheit=pl.col('celsius').celsius.to_fahrenheit())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Polars Plugins in Rust
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Prerequisites
    """)
    return


@app.cell
def _(subprocess):
    #! rustc --version
    subprocess.call(['rustc', '--version'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Anatomy of a Plugin Project
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Plugin
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Compiling the Plugin
    """)
    return


@app.cell
def _(subprocess):
    #! cd plugins/hello_world_plugin && uv run maturin develop --release
    subprocess.call(['cd', 'plugins/hello_world_plugin', '&&', 'uv', 'run', 'maturin', 'develop', '--release'])
    return


@app.cell
def _(get_ipython):
    # Reset the kernel to make the new plugin available

    # The code below will do this automatically when run in IPython
    get_ipython().kernel.do_shutdown(restart=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Performance Benchmark
    """)
    return


@app.cell
def _(pl):
    from hello_world_func import hello_world
    import time
    lots_of_strings = pl.DataFrame({'a': ['1', '2', '3', '4'] * 100000})
    times = []
    for i in range(10):
        t0 = time.time()
        out = lots_of_strings.with_columns(pl.col('a').str.replace_all('.*', 'Hello, world!'))
        t1 = time.time()
        times.append(t1 - t0)
    print(f'Polars native string replace:        {sum(times) / len(times):.5f}')
    times = []
    for i in range(10):
        t0 = time.time()
        out = lots_of_strings.with_columns(hello_world('a'))
        t1 = time.time()
        times.append(t1 - t0)
    print(f'Our custom made Hello world replace: {sum(times) / len(times):.5f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Register Arguments
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Working with multiple arguments as input
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Other register arguments
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Using a Rust Crate
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Use Case: geo
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Adding the geo crate
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### The Rust code
    """)
    return


@app.cell
def _(subprocess):
    #! cd plugins/polars_geo && uv run maturin develop --release
    subprocess.call(['cd', 'plugins/polars_geo', '&&', 'uv', 'run', 'maturin', 'develop', '--release'])
    return


@app.cell
def _(get_ipython):
    # Reset the kernel to make the new plugin available

    # The code below will do this automatically when run in IPython
    get_ipython().kernel.do_shutdown(restart=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### The Python code
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Making the custom namespace
    """)
    return


@app.cell
def _(pl):
    points_and_polygons = pl.DataFrame({'point': [[5.0, 5.0], [20.0, 20.0], [20.0, 20.0]], 'polygon': [[[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0]], [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0]], [[0.0, None], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]]})
    return (points_and_polygons,)


@app.cell
def _(pl, points_and_polygons):
    from plugins.polars_geo import polars_geo

    # Apply the point_in_polygon function
    points_and_polygons.with_columns(
        pl.col("point").geo.point_in_polygon(pl.col("polygon")).alias("in_polygon")
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

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
    # Chapter 3: Moving from pandas to Polars
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
    ## Animals
    """)
    return


@app.cell
def _(subprocess):
    #! cat data/animals.csv
    subprocess.call(['cat', 'data/animals.csv'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Similarities to Recognize
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Appearances to Appreciate
    """)
    return


@app.cell
def _():
    import pandas as pd
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Differences in Code
    """)
    return


@app.cell
def _(pd, pl):
    animals_pd = pd.read_csv("data/animals.csv", sep=",", header=0)
    animals_pl = pl.read_csv("data/animals.csv", separator=",", has_header=True)

    print(f"{type(animals_pd) = }")
    print(f"{type(animals_pl) = }")
    return animals_pd, animals_pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Differences in Display
    """)
    return


@app.cell
def _(animals_pd):
    animals_pd
    return


@app.cell
def _(animals_pl):
    animals_pl
    return


@app.cell
def _(animals_pd):
    animals_pd["animal"]
    return


@app.cell
def _(animals_pl):
    animals_pl.get_column("animal")
    return


@app.cell
def _(animals_pd):
    animals_pd_1 = animals_pd.drop(columns=['habitat', 'diet', 'features'])
    animals_pd_1
    return (animals_pd_1,)


@app.cell
def _(animals_pl):
    animals_pl_1 = animals_pl.drop('habitat', 'diet', 'features')
    animals_pl_1
    return (animals_pl_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concepts to Unlearn
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Index
    """)
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1.index
    return


@app.cell
def _(animals_pd_1):
    animals_agg_pd = animals_pd_1.groupby(['class', 'status'])[['weight']].mean()
    animals_agg_pd
    return (animals_agg_pd,)


@app.cell
def _(animals_agg_pd):
    animals_agg_pd.index
    return


@app.cell
def _(animals_agg_pd):
    animals_agg_pd.reset_index()
    return


@app.cell
def _(animals_pl_1, pl):
    animals_pl_1.group_by(['class', 'status']).agg(pl.col('weight').mean())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Axes
    """)
    return


@app.cell
def _():
    # This raises a KeyError:
    # animals_pd.drop("weight")
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1.drop('weight', axis=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Indexing and Slicing
    """)
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1[['animal', 'class']]
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1[animals_pd_1['status'] == 'endangered']
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1[:3]
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1['weight'] = animals_pd_1['weight'] * 1000
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1['weight']
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1['weight'] = animals_pd_1['weight'].sort_values()
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1['weight']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Eagerness
    """)
    return


@app.cell
def _(pl):
    lazy_query = (
        pl.scan_csv("data/animals.csv")
        .group_by("class")
        .agg(pl.col("weight").mean())
        .filter(pl.col("class") == "mammal")
    )
    return (lazy_query,)


@app.cell
def _(lazy_query):
    lazy_query.show_graph(optimized=False)
    return


@app.cell
def _(lazy_query):
    lazy_query.show_graph()
    return


@app.cell
def _(lazy_query):
    lazy_query.collect()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Relaxedness
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Syntax to Forget
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Common Operations Side By Side
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Removing duplicate values
    """)
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1.drop_duplicates(subset='class')
    return


@app.cell
def _(animals_pl_1):
    animals_pl_1.unique(subset='class')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Removing missing values
    """)
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1.dropna(subset='weight')
    return


@app.cell
def _(animals_pl_1):
    animals_pl_1.drop_nulls(subset='weight')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Sorting rows
    """)
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1.sort_values('weight', ascending=False)
    return


@app.cell
def _(animals_pl_1):
    animals_pl_1.sort('weight', descending=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Casting an existing column
    """)
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1.assign(lifespan=animals_pd_1['lifespan'].astype(float))
    return


@app.cell
def _(animals_pl_1, pl):
    animals_pl_1.with_columns(pl.col('lifespan').cast(pl.Float64))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Aggregating rows
    """)
    return


@app.cell
def _(animals_pd_1):
    animals_pd_1.groupby(['class', 'status'])[['weight']].mean()
    return


@app.cell
def _(animals_pl_1, pl):
    animals_pl_1.group_by('class', 'status').agg(pl.col('weight').mean())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## To and From pandas
    """)
    return


@app.cell
def _(animals_pd_1, pl):
    animals_pl_2 = pl.DataFrame(animals_pd_1)
    animals_pl_2
    return (animals_pl_2,)


@app.cell
def _(animals_pl_2):
    there_and_back_again_df = animals_pl_2.to_pandas()
    there_and_back_again_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()

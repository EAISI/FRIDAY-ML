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
    # Chapter 11: Filtering and Sorting Rows
    """)
    return


@app.cell
def _():
    import polars as pl
    pl.__version__  # The book is built with Polars version 1.20.0
    return (pl,)


@app.cell
def _(pl):
    tools = pl.read_csv("data/tools.csv")
    tools
    return (tools,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Filtering Rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtering Based on Expressions
    """)
    return


@app.cell
def _(pl, tools):
    tools.filter(pl.col("cordless") & (pl.col("brand") == "Makita"))
    return


@app.cell
def _(pl, tools):
    tools.filter(pl.col("cordless"), pl.col("brand") == "Makita")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtering Based on Column Names
    """)
    return


@app.cell
def _(tools):
    tools.filter("cordless")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtering Based on Constraints
    """)
    return


@app.cell
def _(tools):
    tools.filter(cordless=True, brand="Makita")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sorting Rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting Based on a Single Column
    """)
    return


@app.cell
def _(tools):
    tools.sort("price")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting in Reverse
    """)
    return


@app.cell
def _(tools):
    tools.sort("price", descending=True)
    return


@app.cell
def _():
    # This raises a TypeError:
    # tools.sort("price", ascending=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting Based on Multiple Columns
    """)
    return


@app.cell
def _(tools):
    tools.sort("brand", "price")
    return


@app.cell
def _(tools):
    tools.sort("brand", "price", descending=[False, True])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting Based on Expressions
    """)
    return


@app.cell
def _(pl, tools):
    tools.sort(pl.col("rpm") / pl.col("price"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting Nested Data Types
    """)
    return


@app.cell
def _(pl):
    lists = pl.DataFrame({"lists": [[2, 2], [2, 1, 3], [1]]})
    lists.sort("lists")
    return


@app.cell
def _(pl):
    structs = pl.DataFrame(
        {
            "structs": [
                {"a": 1, "b": 2, "c": 3},
                {"a": 1, "b": 3, "c": 1},
                {"a": 1, "b": 1, "c": 2},
            ]
        }
    )
    structs.sort("structs")
    return


@app.cell
def _(pl, tools):
    tools_collection = tools.group_by("brand").agg(collection=pl.struct(pl.all()))
    tools_collection
    return (tools_collection,)


@app.cell
def _(pl, tools_collection):
    tools_collection.sort(pl.col("collection").list.len(), descending=True)
    return


@app.cell
def _(pl, tools_collection):
    tools_collection.sort(
        pl.col("collection")
        .list.eval(pl.element().struct.field("price"))
        .list.mean()
    )
    return


@app.cell
def _(pl, tools_collection):
    tools_collection.with_columns(
        mean_price=pl.col("collection")
        .list.eval(pl.element().struct.field("price"))
        .list.mean()
    ).sort("mean_price")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Related Row Operations
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtering Missing Values
    """)
    return


@app.cell
def _(tools):
    tools.drop_nulls("rpm").height
    return


@app.cell
def _(pl, tools):
    tools.filter(pl.all_horizontal(pl.all().is_not_null())).height
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Slicing
    """)
    return


@app.cell
def _(tools):
    tools.with_row_index().gather_every(2).head(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Top and Bottom
    """)
    return


@app.cell
def _(tools):
    tools.top_k(3, by="price")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sampling
    """)
    return


@app.cell
def _(tools):
    tools.sample(fraction=0.2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Semi-Joins
    """)
    return


@app.cell
def _(pl, tools):
    saws = pl.DataFrame(
        {
            "tool": [
                "Table Saw",
                "Plunge Cut Saw",
                "Miter Saw",
                "Jigsaw",
                "Bandsaw",
                "Chainsaw",
                "Seesaw",
            ]
        }
    )
    tools.join(saws, how="semi", on="tool")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Takeaways
    """)
    return


if __name__ == "__main__":
    app.run()

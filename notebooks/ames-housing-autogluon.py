import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import polars as pl
    from sklearn.model_selection import train_test_split
    return pl, train_test_split


@app.cell
def _(pl):
    # Load the Ames housing dataset
    df = pl.read_csv("./data/ames-housing.csv")

    # Display basic information
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns[:5]}... (showing first 5)")

    df.head()
    return (df,)


@app.cell
def _(df, train_test_split):
    # Separate features (X) and target (y)
    # Assuming 'SalePrice' is the target column
    target_col = "SalePrice"

    X = df.drop(target_col)
    y = df.select(target_col)

    # Perform train-test split (80/20 split with random state for reproducibility)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training set size: {len(X_train)} samples")
    print(f"Test set size: {len(X_test)} samples")
    print(f"Split ratio: {len(X_train) / len(df):.1%} train / {len(X_test) / len(df):.1%} test")
    return X_train, y_train


@app.cell
def _(X_train):
    # Display a sample of the training data
    print("Sample of training features:")
    X_train.head(3)
    return


@app.cell
def _(y_train):
    print("Sample of training targets:")
    y_train.head(3)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

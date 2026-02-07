import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc

    return (
        LogisticRegression,
        RandomForestClassifier,
        StandardScaler,
        alt,
        auc,
        classification_report,
        mo,
        pl,
        roc_curve,
        train_test_split,
    )


@app.cell
def _(mo):
    mo.md("""
    # Pima Indians Diabetes Dataset Analysis

    This dataset contains medical diagnostic information for Pima Indian women
    to predict diabetes onset. It includes 768 observations with 8 features.

    **Features:**
    - Pregnancies: Number of times pregnant
    - Glucose: Plasma glucose concentration
    - BloodPressure: Diastolic blood pressure (mm Hg)
    - SkinThickness: Triceps skin fold thickness (mm)
    - Insulin: 2-Hour serum insulin (mu U/ml)
    - BMI: Body mass index
    - DiabetesPedigreeFunction: Diabetes pedigree function
    - Age: Age in years
    - Outcome: Class variable (0 or 1) - 1 indicates diabetes
    """)
    return


@app.cell
def _(pl):
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

    column_names = [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age",
        "Outcome"
    ]

    df = pl.read_csv(url, has_header=False, new_columns=column_names)
    return (df,)


@app.cell
def _(df, mo, pl):
    mo.md(f"""
    ## Dataset Overview

    Total observations: **{len(df)}**

    Diabetes cases: **{df.filter(pl.col("Outcome") == 1).height}** ({df.filter(pl.col("Outcome") == 1).height / len(df) * 100:.1f}%)
    """)
    return


@app.cell
def _(df, mo):
    mo.ui.data_explorer(df)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Feature Distributions by Outcome
    """)
    return


@app.cell
def _(mo):
    feature_selector = mo.ui.dropdown(
        options=[
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age"
        ],
        value="Glucose",
        label="Select Feature"
    )
    feature_selector
    return (feature_selector,)


@app.cell
def _(alt, df, feature_selector, pl):
    df_long = df.select([
        pl.col(feature_selector.value),
        pl.col("Outcome").cast(pl.String)
    ])

    chart = alt.Chart(df_long).mark_boxplot(extent='min-max').encode(
        x=alt.X('Outcome:N', title='Diabetes Outcome'),
        y=alt.Y(f'{feature_selector.value}:Q', title=feature_selector.value),
        color=alt.Color('Outcome:N', legend=None)
    ).properties(
        title=f'{feature_selector.value} Distribution by Diabetes Outcome',
        width=400,
        height=300
    )

    chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Correlation Analysis
    """)
    return


@app.cell
def _(alt, df, pl):
    numeric_cols = [col for col in df.columns if col != "Outcome"]

    corr_with_outcome = (
        df
        .select([
            pl.corr(pl.col(col), pl.col("Outcome")).alias(col)
            for col in numeric_cols
        ])
        .unpivot(variable_name="Feature", value_name="Correlation")
        .sort("Correlation", descending=True)
    )

    corr_chart = alt.Chart(corr_with_outcome).mark_bar().encode(
        x=alt.X('Correlation:Q', title='Correlation with Diabetes'),
        y=alt.Y('Feature:N', sort='-x', title='Feature'),
        color=alt.condition(
            alt.datum.Correlation > 0,
            alt.value("steelblue"),
            alt.value("orange")
        ),
        tooltip=['Feature:N', alt.Tooltip('Correlation:Q', format='.3f')]
    ).properties(
        title='Feature Correlation with Diabetes Outcome',
        width=500,
        height=300
    )

    corr_chart
    return (numeric_cols,)


@app.cell
def _(mo):
    mo.md("""
    ## Pairwise Feature Comparison
    """)
    return


@app.cell
def _(mo, numeric_cols):
    x_axis = mo.ui.dropdown(
        options=numeric_cols,
        value="Glucose",
        label="X-axis"
    )
    y_axis = mo.ui.dropdown(
        options=numeric_cols,
        value="BMI",
        label="Y-axis"
    )
    mo.hstack([x_axis, y_axis])
    return x_axis, y_axis


@app.cell
def _(alt, df, pl, x_axis, y_axis):
    scatter_df = df.select([
        pl.col(x_axis.value),
        pl.col(y_axis.value),
        pl.col("Outcome").cast(pl.String)
    ]).filter(
        (pl.col(x_axis.value) > 0) & (pl.col(y_axis.value) > 0)
    )

    scatter_chart = alt.Chart(scatter_df).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X(f'{x_axis.value}:Q', title=x_axis.value),
        y=alt.Y(f'{y_axis.value}:Q', title=y_axis.value),
        color=alt.Color('Outcome:N', 
                       scale=alt.Scale(domain=['0', '1'], range=['steelblue', 'orange']),
                       legend=alt.Legend(title='Diabetes')),
        tooltip=[
            alt.Tooltip(f'{x_axis.value}:Q', format='.1f'),
            alt.Tooltip(f'{y_axis.value}:Q', format='.1f'),
            'Outcome:N'
        ]
    ).properties(
        title=f'{y_axis.value} vs {x_axis.value}',
        width=500,
        height=400
    )

    scatter_chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## Model Training

    Train classification models to predict diabetes outcome.
    """)
    return


@app.cell
def _(df, train_test_split):
    feature_cols = [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age"
    ]

    X = df.select(feature_cols).to_numpy()
    y = df.select("Outcome").to_numpy().ravel()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_test, X_train, feature_cols, y_test, y_train


@app.cell
def _(StandardScaler, X_test, X_train):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_test_scaled, X_train_scaled


@app.cell
def _(LogisticRegression, RandomForestClassifier, X_train_scaled, y_train):
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train_scaled, y_train)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    return lr_model, rf_model


@app.cell
def _(X_test_scaled, lr_model, rf_model):
    lr_predictions = lr_model.predict(X_test_scaled)
    lr_probas = lr_model.predict_proba(X_test_scaled)[:, 1]

    rf_predictions = rf_model.predict(X_test_scaled)
    rf_probas = rf_model.predict_proba(X_test_scaled)[:, 1]
    return lr_predictions, lr_probas, rf_predictions, rf_probas


@app.cell
def _(mo):
    model_selector = mo.ui.dropdown(
        options=["Logistic Regression", "Random Forest"],
        value="Logistic Regression",
        label="Select Model"
    )
    model_selector
    return (model_selector,)


@app.cell
def _(
    classification_report,
    lr_predictions,
    mo,
    model_selector,
    rf_predictions,
    y_test,
):
    predictions = lr_predictions if model_selector.value == "Logistic Regression" else rf_predictions

    report = classification_report(y_test, predictions, output_dict=True)

    mo.md(f"""
    ### {model_selector.value} Performance

    **Accuracy:** {report['accuracy']:.3f}

    **Class 0 (No Diabetes):**
    - Precision: {report['0']['precision']:.3f}
    - Recall: {report['0']['recall']:.3f}
    - F1-score: {report['0']['f1-score']:.3f}

    **Class 1 (Diabetes):**
    - Precision: {report['1']['precision']:.3f}
    - Recall: {report['1']['recall']:.3f}
    - F1-score: {report['1']['f1-score']:.3f}
    """)
    return


@app.cell
def _(alt, auc, lr_probas, model_selector, pl, rf_probas, roc_curve, y_test):
    probas = lr_probas if model_selector.value == "Logistic Regression" else rf_probas

    fpr, tpr, thresholds = roc_curve(y_test, probas)
    roc_auc = auc(fpr, tpr)

    roc_df = pl.DataFrame({
        "False Positive Rate": fpr,
        "True Positive Rate": tpr
    })

    roc_chart = alt.Chart(roc_df).mark_line(color='steelblue', size=2).encode(
        x=alt.X('False Positive Rate:Q', scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('True Positive Rate:Q', scale=alt.Scale(domain=[0, 1])),
        tooltip=[
            alt.Tooltip('False Positive Rate:Q', format='.3f'),
            alt.Tooltip('True Positive Rate:Q', format='.3f')
        ]
    )

    diagonal = alt.Chart(pl.DataFrame({"x": [0, 1], "y": [0, 1]})).mark_line(
        color='gray',
        strokeDash=[5, 5]
    ).encode(x='x:Q', y='y:Q')

    final_roc = (roc_chart + diagonal).properties(
        title=f'ROC Curve (AUC = {roc_auc:.3f})',
        width=400,
        height=400
    )

    final_roc
    return


@app.cell
def _(alt, feature_cols, pl, rf_model):
    feature_importance = pl.DataFrame({
        "Feature": feature_cols,
        "Importance": rf_model.feature_importances_
    }).sort("Importance", descending=True)

    importance_chart = alt.Chart(feature_importance).mark_bar().encode(
        x=alt.X('Importance:Q', title='Feature Importance'),
        y=alt.Y('Feature:N', sort='-x', title='Feature'),
        color=alt.value('steelblue'),
        tooltip=['Feature:N', alt.Tooltip('Importance:Q', format='.4f')]
    ).properties(
        title='Random Forest Feature Importance',
        width=500,
        height=300
    )

    importance_chart
    return


if __name__ == "__main__":
    app.run()

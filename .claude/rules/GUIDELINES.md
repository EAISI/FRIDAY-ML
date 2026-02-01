# AI Agent Guidelines for FRIDAY-ML

This document provides comprehensive guidance for AI agents working in the FRIDAY-ML educational workspace.

## Project Philosophy

**"Write less, read more, evaluate everything"**

FRIDAY-ML is an educational workspace that bridges ML theory and practice using AI-assisted development. AI agents write boilerplate code while learners focus on understanding principles, auditing generated code, and evaluating models.

The workspace is designed to accompany a standard introduction to machine learning curriculum, with learners using AI coding agents (Claude Code or Codestral) to implement concepts while focusing on understanding the "why" behind the code.

## Key Development Principles

### Educational Context First

**Code is meant to be read and understood by ML learners. Prioritize clarity over cleverness.**

1. **Explain the "why" behind code, not just the "how"**
   - Focus on helping learners understand principles
   - Make design decisions explicit and visible
   - Show the reasoning behind algorithmic choices

2. **Encourage learners to audit and evaluate AI-generated code**
   - Make data transformations explicit (no "magic")
   - Include inline comments for complex logic
   - Show intermediate results where helpful

3. **Progressive disclosure of complexity**
   - Use `hide_code=True` in marimo cells for implementation details
   - Start simple, add complexity gradually
   - Break complex operations into understandable steps

4. **"Write less, read more, evaluate everything" philosophy**
   - Minimize boilerplate by leveraging AutoGluon
   - Focus learner attention on key decisions
   - Always include evaluation and visualization

### Marimo Notebook Patterns

**Use Marimo's reactive `.py` format for all notebooks (not `.ipynb`)**

1. **Structure notebooks with clear conceptual progression**
   ```python
   import marimo as mo

   app = marimo.App()

   @app.cell
   def load_data():
       # Clear, explicit data loading
       df = pl.read_csv("data/dataset.csv")
       return df,

   @app.cell
   def explore_data(df):
       # Show data exploration steps
       summary = df.describe()
       return summary,

   @app.cell(hide_code=True)
   def complex_preprocessing(df):
       # Hide complex implementation details
       # that learners can explore if interested
       processed = (
           df
           .with_columns([...])
           .filter(...)
       )
       return processed,
   ```

2. **Reactive Cells**
   - Structure cells to be self-contained with clear dependencies
   - Return variables as tuples for use in other cells
   - Avoid circular dependencies
   - Use private variables (prefix with `_`) for cell-local data

3. **UI Elements**
   - Use marimo UI elements for interactive exploration
   - Create sliders, dropdowns for hyperparameter tuning
   - Make visualizations interactive where appropriate

### scikit-learn Patterns

**Use scikit-learn for classical machine learning with explicit pipelines and clear workflows**

1. **Standard Supervised Learning Workflow**
   ```python
   from sklearn.model_selection import train_test_split
   from sklearn.linear_model import LogisticRegression
   from sklearn.metrics import classification_report, confusion_matrix

   # Split data
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42, stratify=y
   )

   # Train model
   model = LogisticRegression(max_iter=1000)
   model.fit(X_train, y_train)

   # Evaluate
   y_pred = model.predict(X_test)
   print(classification_report(y_test, y_pred))
   ```

2. **Use Pipelines for reproducible workflows**
   ```python
   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler
   from sklearn.ensemble import RandomForestClassifier

   # Build pipeline
   pipeline = Pipeline([
       ('scaler', StandardScaler()),
       ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
   ])

   # Train and predict in one step
   pipeline.fit(X_train, y_train)
   y_pred = pipeline.predict(X_test)
   ```

3. **Cross-validation for robust evaluation**
   ```python
   from sklearn.model_selection import cross_val_score

   scores = cross_val_score(
       pipeline, X_train, y_train,
       cv=5,
       scoring='accuracy'
   )
   print(f"CV Accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")
   ```

4. **Hyperparameter tuning with GridSearchCV**
   ```python
   from sklearn.model_selection import GridSearchCV

   param_grid = {
       'classifier__n_estimators': [50, 100, 200],
       'classifier__max_depth': [5, 10, None]
   }

   grid_search = GridSearchCV(
       pipeline, param_grid,
       cv=5,
       scoring='accuracy',
       n_jobs=-1
   )
   grid_search.fit(X_train, y_train)

   print(f"Best params: {grid_search.best_params_}")
   print(f"Best score: {grid_search.best_score_:.3f}")
   ```

### AutoGluon Patterns

**Leverage AutoGluon to reduce boilerplate and focus on high-level concepts**

1. **Use TabularPredictor for automated model selection**
   ```python
   from autogluon.tabular import TabularPredictor

   # Simple, clear predictor setup
   predictor = TabularPredictor(
       label=target_column,
       eval_metric="accuracy",
       path="models/experiment_name/"
   ).fit(
       train_data,
       time_limit=300,  # 5 minutes - adjust for demos
       presets='medium_quality'
   )
   ```

2. **Focus on evaluating AutoGluon's model selection decisions**
   - Always show the leaderboard: `predictor.leaderboard()`
   - Explain feature importance: `predictor.feature_importance()`
   - Compare ensemble vs individual models
   - Discuss why AutoGluon selected certain models

3. **Explain feature engineering choices made by AutoGluon**
   - Show original vs transformed features
   - Discuss automatic feature types
   - Explain why certain transformations help

### TensorFlow/Keras Patterns

**Use TFDS for datasets and build explicit input pipelines**

1. **Standard Deep Learning Workflow**
   ```python
   import tensorflow as tf
   import tensorflow_datasets as tfds
   from datetime import datetime

   # 1. Load data with TFDS
   (train_data, test_data), info = tfds.load(
       name='mnist',
       split=['train', 'test'],
       with_info=True,
       as_supervised=True
   )

   # 2. Build explicit input pipeline
   def normalize_img(image, label):
       """Normalize images to [0, 1] range."""
       return tf.cast(image, tf.float32) / 255., label

   train_data = (
       train_data
       .map(normalize_img)
       .cache()
       .shuffle(1000)
       .batch(32)
       .prefetch(tf.data.AUTOTUNE)
   )

   # 3. Define model architecture
   model = tf.keras.Sequential([
       tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
       tf.keras.layers.Dense(128, activation='relu'),
       tf.keras.layers.Dense(10)
   ])

   model.compile(
       optimizer='adam',
       loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
       metrics=['accuracy']
   )

   # 4. Configure TensorBoard for visualization
   log_dir = f"logs/fit/{datetime.now():%Y%m%d-%H%M%S}"
   tensorboard_callback = tf.keras.callbacks.TensorBoard(
       log_dir=log_dir,
       histogram_freq=1
   )

   # 5. Train with callbacks
   history = model.fit(
       train_data,
       epochs=10,
       validation_data=test_data,
       callbacks=[tensorboard_callback]
   )
   ```

2. **Always include visualization**
   - Use TensorBoard callbacks
   - Plot training history (loss, metrics)
   - Show example predictions
   - Visualize learned features where applicable

3. **Use timestamped log directories**
   - Format: `logs/fit/{datetime.now():%Y%m%d-%H%M%S}`
   - Enables comparing multiple training runs
   - Keeps experiments organized

## Common Patterns by Task

### Data Loading

**Use Polars for tabular data, TFDS for standard ML datasets, convert to numpy/pandas for scikit-learn**

```python
# Polars for tabular data
import polars as pl

df = pl.read_csv("data/dataset.csv")

# TFDS for ML benchmarks
import tensorflow_datasets as tfds

dataset, info = tfds.load('mnist', with_info=True)

# Convert Polars to numpy for scikit-learn
X = df.select(feature_columns).to_numpy()
y = df.select('target').to_numpy().ravel()
```

### Data Preprocessing

**Make transformations explicit so learners can audit them**

```python
# Good - explicit transformations
processed = (
    df
    .with_columns([
        pl.col("age").cast(pl.Float64),
        (pl.col("height") / 100).alias("height_m"),
        pl.col("date").str.strptime(pl.Date, format="%Y-%m-%d")
    ])
    .filter(pl.col("age") > 0)
)

# Bad - hidden transformations
processed = preprocess_data(df)  # What does this do?
```

### Model Evaluation

**Always include training history visualization and metrics**

```python
import altair as alt

# Visualize training history
history_df = pl.DataFrame({
    'epoch': range(1, len(history.history['loss']) + 1),
    'train_loss': history.history['loss'],
    'val_loss': history.history['val_loss'],
    'train_accuracy': history.history['accuracy'],
    'val_accuracy': history.history['val_accuracy']
})

chart = alt.Chart(history_df).mark_line().encode(
    x='epoch:Q',
    y='val_loss:Q',
    color=alt.value('blue')
).properties(
    title='Validation Loss Over Epochs',
    width=600,
    height=400
)
```

### Visualization

**Use Altair for declarative, interactive visualizations**

```python
import altair as alt

chart = alt.Chart(df).mark_circle().encode(
    x=alt.X('feature1:Q', title='Feature 1'),
    y=alt.Y('feature2:Q', title='Feature 2'),
    color='label:N',
    tooltip=['feature1', 'feature2', 'label']
).properties(
    title='Feature Space Visualization',
    width=600,
    height=400
).interactive()
```

## Workflow Templates

### scikit-learn Supervised Learning Workflow

1. **Load and prepare data** (1-2 cells)
   ```python
   import polars as pl
   from sklearn.model_selection import train_test_split

   # Load with Polars
   df = pl.read_csv("data/dataset.csv")

   # Prepare features and target
   X = df.select(feature_columns).to_numpy()
   y = df.select('target').to_numpy().ravel()

   # Split data
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42
   )
   ```

2. **Build and train pipeline** (1 cell)
   ```python
   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler
   from sklearn.ensemble import RandomForestClassifier

   pipeline = Pipeline([
       ('scaler', StandardScaler()),
       ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
   ])

   pipeline.fit(X_train, y_train)
   ```

3. **Evaluate with cross-validation** (1 cell)
   ```python
   from sklearn.model_selection import cross_val_score

   cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
   print(f"CV Accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
   ```

4. **Final evaluation and visualization** (2 cells)
   ```python
   from sklearn.metrics import classification_report, confusion_matrix
   import altair as alt

   # Predictions
   y_pred = pipeline.predict(X_test)

   # Metrics
   print(classification_report(y_test, y_pred))

   # Visualize confusion matrix
   cm = confusion_matrix(y_test, y_pred)
   cm_df = pl.DataFrame({
       'true': [0, 0, 1, 1],
       'pred': [0, 1, 0, 1],
       'count': cm.ravel()
   })

   chart = alt.Chart(cm_df).mark_rect().encode(
       x='pred:O',
       y='true:O',
       color='count:Q'
   )
   ```

### AutoGluon Supervised Learning Workflow

1. **Load and explore data** (1-2 cells)
   - Load dataset
   - Show basic statistics
   - Visualize distributions

2. **Prepare data** (1-2 cells)
   - Handle missing values
   - Feature engineering
   - Train/test split

3. **Train model** (1 cell)
   - Configure AutoGluon or build neural network
   - Fit on training data

4. **Evaluate model** (2-3 cells)
   - Show metrics
   - Visualize predictions vs actuals
   - Feature importance / model interpretation

5. **Interactive exploration** (optional)
   - UI elements for hyperparameter tuning
   - Compare multiple models
   - Error analysis

## Educational Approach Checklist

Before completing a notebook, verify:

- [ ] Code is readable and well-structured
- [ ] Complex logic has explanatory comments
- [ ] Data transformations are explicit and visible
- [ ] Visualizations are included for key insights
- [ ] Model evaluation is comprehensive
- [ ] Learners can audit the entire workflow
- [ ] Progressive complexity (simple → advanced)
- [ ] Cells are reactive and self-contained
- [ ] No "magic" - everything is explainable

## Anti-Patterns to Avoid

1. **Don't hide complexity without reason**
   - Only use `hide_code=True` for truly boilerplate code
   - Learners should see the main algorithm logic

2. **Don't skip evaluation**
   - Always show model performance
   - Always include visualizations
   - Explain what metrics mean

3. **Don't use unexplained magic numbers**
   ```python
   # Bad
   model.fit(train_data, epochs=42)

   # Good
   epochs = 10  # Start with 10 epochs for quick iteration
   model.fit(train_data, epochs=epochs)
   ```

4. **Don't assume prior knowledge**
   - Explain domain-specific concepts
   - Define technical terms
   - Link to relevant learning resources

## For More Details

- See [code-style.md](code-style.md) for Python coding standards
- See [marimo.md](marimo.md) for detailed Marimo patterns
- See [security.md](security.md) for security best practices
- See [references/polars/](../../references/polars/) for comprehensive Polars examples

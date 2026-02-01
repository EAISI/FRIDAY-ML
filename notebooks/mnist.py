import marimo

__generated_with = "0.19.7"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Training a neural network on MNIST with Keras

    This notebook demonstrates how to plug TensorFlow Datasets (TFDS) into a Keras model. It is a remix of the following open access resources:

    - [Keras example starter notebook](https://github.com/tensorflow/datasets/blob/master/docs/keras_example.ipynb)

    - [Getting started guide tensorboard](https://github.com/tensorflow/tensorboard/blob/master/docs/get_started.ipynb)
    - [Introduction to Statistical Learning with Python, notebook on deep learning](https://islp.readthedocs.io/en/latest/labs/Ch10-deeplearning-lab.html#)
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from datetime import datetime

    import altair as alt
    from keras_visualizer import visualizer
    import polars as pl
    import tensorflow as tf
    import tensorflow_datasets as tfds
    return alt, datetime, pl, tf, tfds, visualizer


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Create your input pipeline

    Start by building an efficient input pipeline using advices from:
    * The [Performance tips](https://www.tensorflow.org/datasets/performances) guide
    * The [Better performance with the `tf.data` API](https://www.tensorflow.org/guide/data_performance#optimize_performance) guide
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Load a dataset

    Load the MNIST dataset with the following arguments:

    * `shuffle_files=True`: The MNIST data is only stored in a single file, but for larger datasets with multiple files on disk, it's good practice to shuffle them when training.
    * `as_supervised=True`: Returns a tuple `(img, label)` instead of a dictionary `{'image': img, 'label': label}`.
    """)
    return


@app.cell
def _(tfds):
    (ds_train, ds_test), ds_info = tfds.load(
        "mnist",
        split=["train", "test"],
        shuffle_files=True,
        as_supervised=True,
        with_info=True,
    )
    # tfds.show_examples(ds_train, ds_info)
    return ds_info, ds_test, ds_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Build a training pipeline

    Apply the following transformations:

    * `tf.data.Dataset.map`: TFDS provide images of type `tf.uint8`, while the model expects `tf.float32`. Therefore, you need to normalize images.
    * `tf.data.Dataset.cache` As you fit the dataset in memory, cache it before shuffling for a better performance.<br/>
    __Note:__ Random transformations should be applied after caching.
    * `tf.data.Dataset.shuffle`: For true randomness, set the shuffle buffer to the full dataset size.<br/>
    __Note:__ For large datasets that can't fit in memory, use `buffer_size=1000` if your system allows it.
    * `tf.data.Dataset.batch`: Batch elements of the dataset after shuffling to get unique batches at each epoch.
    * `tf.data.Dataset.prefetch`: It is good practice to end the pipeline by prefetching [for performance](https://www.tensorflow.org/guide/data_performance#prefetching).
    """)
    return


@app.cell
def _(ds_info, ds_train, tf):
    def normalize_img(image, label):
        """Normalizes images: `uint8` -> `float32`."""
        return (tf.cast(image, tf.float32) / 255.0, label)


    ds_train_1 = ds_train.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    ds_train_1 = ds_train_1.cache()
    ds_train_1 = ds_train_1.shuffle(ds_info.splits["train"].num_examples)
    ds_train_1 = ds_train_1.batch(128)
    ds_train_1 = ds_train_1.prefetch(tf.data.AUTOTUNE)
    return ds_train_1, normalize_img


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Build an evaluation pipeline

    Your testing pipeline is similar to the training pipeline with small differences:

     * You don't need to call `tf.data.Dataset.shuffle`.
     * Caching is done after batching because batches can be the same between epochs.
    """)
    return


@app.cell
def _(ds_info, ds_test, ds_train, normalize_img, tf, tfds):
    ds_test_1 = ds_test.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    ds_test_1 = ds_test_1.batch(128)
    ds_test_1 = ds_test_1.cache()
    ds_test_1 = ds_test_1.prefetch(tf.data.AUTOTUNE)
    tfds.show_examples(ds_train, ds_info)
    return (ds_test_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Create and train the model

    Plug the TFDS input pipeline into a simple Keras model, compile the model, and train it.
    """)
    return


@app.cell
def _(mo, tf, visualizer):
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10),
        ]
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )

    visualizer(model, file_name="mnist", file_format="png")
    mo.image("./mnist.png")
    return (model,)


@app.cell
def _(datetime, ds_test_1, ds_train_1, model, tf):
    log_dir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    model.fit(ds_train_1, epochs=6, validation_data=ds_test_1, callbacks=[tensorboard_callback])
    return


@app.cell
def _(alt, model, pl):
    base = alt.Chart(pl.DataFrame(model.history.history).with_row_index("epoch")).encode(
        x=alt.X("epoch:Q", axis=alt.Axis(tickMinStep=1))
    )
    alt.layer(
        base.mark_line(color="blue", point=True).encode(y="val_sparse_categorical_accuracy:Q"),
        base.mark_line(color="orange", point=True).encode(y="sparse_categorical_accuracy:Q"),
        base.mark_line(color="green", point=True).encode(y="loss:Q"),
        base.mark_line(color="red", point=True).encode(y="val_loss:Q"),
    )
    return


@app.cell
def _(model, pl):
    pl.DataFrame(model.history.history).with_row_index("epoch")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

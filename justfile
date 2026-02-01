tensorboard:
    uv run tensorboard --logdir logs/

mnist:
    uv run marimo edit notebooks/mnist.py

ames-housing-sklearn:
    uv run marimo edit notebooks/ames-housing-sklearn.py

ames-housing-autogluon:
    uv run marimo edit notebooks/ames-housing-autogluon.py

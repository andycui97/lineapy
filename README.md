# lineapy

This repository contains a few different components:

-   A **transformer** which maps Python code to Python code, makign it lazy by turning control flow and function calls into tracer calls.
-   A **tracer** that adds nodes to the graph (and then executes them with the executor)
-   A **dataflow graph** which is stored in SQLite and represents a Python execution
-   An **executor** which takes the graph and can run it as Python code
-   A **server** which exposes a REST API of the graph that `linea-server` accesses

## Using Linea

There are two ways to use `linea`:

-   The CLI tool: `python lineapy/cli/cli.py --mode dev your_file.py`
    -   The dev mode is local, and the remote one is under development).
-   A new IPython kernel: select the lineapy Kernel when you open your
    jupyter notebook.
    -   Note that this is still under development.

## First-time Setup

```bash
conda create --name lineapy-env python=3.9
conda activate lineapy-env
pip install -r requirements.txt
pip install -r dev-requirements.txt
pip install -e . --user
```

## Tests

Note: these should be run in root (`graph_with_csv_import` does a
relative file access)

```bash
mypy -p lineapy
black --line-length 79 --check .
pytest
```

If you want to inspect the AST of some Python code for debugging, you can run:

```bash
./tests/tools/print_ast.py 'hi(a=10)'
```

### Github Actions

The tests are run on Github Actions. If you are trying to debug a failure that happens on Github Actions, you can try using [`act`](https://github.com/nektos/act), which will run it locally through docker:

```bash
brew install act
act
# When it prompts, the "medium" image seems to work out alright.
```

### Static end to end test/demo

For a static end to end test along with [linea-server](https://github.com/LineaLabs/linea-server)

```bash
python tests/setup_integrated_tests.py
python lineapy/app/application.py
```

`setup_integrated_tests.py` creates the stub data that the flask application then serves.

Then head over to [linea-server](https://github.com/LineaLabs/linea-server) and
run the usual commands there (`python application.py` and `yarn start` in
the `/server` and `/frontend` folders respectively)

Note that if you are running these on EC2, you need to do tunneling on **three**
ports:

-   One for the lineapy flask app, which is currently on 4000
-   One for the linea-server flask app, which is on 5000
-   And one for the linea-server dev server (for the React app), which is on 3000

For Yifan's machine, the tunneling looks like the following:

```bash
ssh -N -f -L localhost:3000:0.0.0.0:3000 ubuntu@3.18.79.230
ssh -N -f -L localhost:5000:0.0.0.0:5000 ubuntu@3.18.79.230
ssh -N -f -L localhost:4000:0.0.0.0:4000 ubuntu@3.18.79.230
```

## Running the servers live

Coming soon!

## Jupyter

To make use of our virtual env, you need to do these steps (reference: https://medium.com/@nrk25693/how-to-add-your-conda-environment-to-your-jupyter-notebook-in-just-4-steps-abeab8b8d084)

```bash
conda install -c anaconda ipykernel
python -m ipykernel install --user --name=lineapy-env
```

## Best practices

For any Jupyter Notebooks that you think your reviewer might directly comment on,
please run `jupyter nbconvert --to script` and commit the corresponding .py script to make comments easier.

## Dev notes

Something weird about the `tests/test_flask_app.py`; please double check even if pytest is passing.

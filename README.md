# Maya-Sammlung.ch 

## Installation instructions:
The current page is driven by TurboGears2 using kajiki templates and sqlalchemy orm.

You have to add the database files to the app directory

use <code>pip install TurboGears2</code>, <code>pip install kajiki</code> and <code>pip install sqlalchemy</code> to install dependencies, set <code>app</code> as your working directory and start <code>python main.py</code>.

or run it in a docker container:
- build: <code>docker build -t katalog_py .</code>
- run:
  - interactive: <code>docker run -it --rm -p 8080:8080  --mount type=bind,source="$(pwd)"/app,target=/app katalog_py</code>
  - deferred: <code>docker run -dt -p 8080:8080  --mount type=bind,source="$(pwd)"/app,target=/app --name katalog_py_instance katalog_py</code>

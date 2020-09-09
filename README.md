# NosenStory API

> **NosenStory** (a.k.a. "Nonsensical Story") is an improvised party game where players answer given short questions, and as result their answers are composed in a brief nonsensical story which is fun to read!

**NS API** is a client-agnostic interface for maintaining NosenStory's game process across multiple chat platforms.

## Prerequisites

- [Python 3.x and pip](https://docs.python-guide.org/starting/installation/)
  * needed to run Pipenv (not related to Python binaries required for bot)
- [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html)
  * needed to reserve dependencies on per-project basis
- [PostgreSQL](https://www.postgresql.org/)
  * needed to store data and get reliable read/write access to it

## Getting Started

Make sure you've fetched submodules as well.
```
$ git submodule init && git submodule update
```

Create `.env` file from `.env.example` and revise variables (`PSQL_*` for PostgreSQL connection):
```
$ cp .env.example .env && nano .env
```

### PyCharm

Project contains meta files specifc to PyCharm IDE (in the author's humble opinion, it's more than feasible for working with Python). These include some sort of inspection guideline to prevent code smell.

1. Set Pipenv as project interpreter (SDK). It also must install dependencies listed in `Pipfile`.
2. Fetch latest gRPC stubs by running configuration "**setup_stubs**".
3. Run configuration "**api**" to activate NS API.

### Shell

Use virtual environment for project and install/update dependencies:
```
$ pipenv shell
$ pipenv install
```

After that, generate fresh gRPC stubs:
```
$ python setup.py stubs
```

Run NS API within virtual environment using one simple command:
```
$ python -m api
```

## License

© 2020 [Rodion Borisov](https://github.com/vintprox), [Sun Maung Oo](https://github.com/SunMaungOo) and [NonStory contributors](https://github.com/nonstory/nonstory/graphs/contributors)

Licensed under the [Apache License, Version 2.0](./LICENSE) (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

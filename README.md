# NonStory Discord Bot (original in Python)

> **NonStory** (a.k.a. "Nonsensical Story") is an improvised party game where players answer given short questions, and as result their answers are composed in a brief nonsensical story which is fun to read!

Here we have Discord bot that automates chat gameplay for NonStory.

## Prerequisites

- [Python 3.x and pip](https://docs.python-guide.org/starting/installation/)
  * needed to run Pipenv (not related to Python binaries required for bot)
- [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html)
  * needed to reserve dependencies on per-project basis
- [PostgreSQL](https://www.postgresql.org/)
  * needed to store data and get reliable read/write access to it

## Getting Started

Use virtual environment for project and install/update dependencies:
```
$ pipenv shell
$ pipenv install
```

Don't forget to revise variables in `.env` file, that include `BOT_TOKEN`, `POLYGON_CHANNEL_ID`, `PSQL_*` (PostgreSQL connection), etc.:
```
$ cp .env.example .env && nano .env
```
You'll need to have proper connection with database set up to make bot really work.

Run bot within virtual environment with one simple command:
```
$ python .
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

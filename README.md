# django-cs50s

Django projects built while following **[CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/)** (CS50W), Harvard's course on web application design. The code here follows the lectures on **Django** (Lecture 3) and **SQL, Models, and Migrations** (Lecture 4).

| Project | Lecture | What it covers |
| --- | --- | --- |
| [`mywebsite/`](mywebsite) | 3 – Django | Projects and apps, URL routing, views, templates, static files, forms, sessions |
| [`airline/`](airline) | 4 – SQL, Models, and Migrations | Models, migrations, relationships (one-to-many, many-to-many), the Django admin, POST forms with CSRF |

---

## Repository layout

```
django-cs50s/
├── airline/                 # Lecture 4 project
│   ├── airline/             # project settings & root URLconf
│   ├── flights/             # app: airports, flights, passengers
│   │   ├── migrations/
│   │   ├── templates/flights/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── db.sqlite3
│   └── manage.py
└── mywebsite/               # Lecture 3 project
    ├── mywebsite/           # project settings & root URLconf
    ├── hello/               # app: hello world & dynamic greetings
    ├── newyear/             # app: "Is it New Year's?"
    ├── tasks/               # app: session-based to-do list
    ├── db.sqlite3
    └── manage.py
```

---

## `mywebsite` — Django fundamentals

A single Django project containing three small apps, each introducing a new core concept.

### `hello` — routing, views and templates

| URL | View | Response |
| --- | --- | --- |
| `/hello/` | `index` | Renders `hello/index.html` — *"Hello, world!"* |
| `/hello/<name>` | `greet` | Renders `greet/index.html` with the name capitalized, e.g. `/hello/alice` → *"Hello, Alice!"* |
| `/hello/brian/` | `brian` | Plain `HttpResponse`: *"Hello, Brian!"* |
| `/hello/david` | `david` | Plain `HttpResponse`: *"Hello, David!"* |

**Concepts:** `HttpResponse` vs. `render()`, path converters (`<str:name>`), passing a context dictionary to a template.

### `newyear` — template logic and static files

| URL | Response |
| --- | --- |
| `/newyear/` | A big **YES** or **NO** answering *"Is it New Year's?"* |

The view checks today's date with `datetime` and passes a boolean to the template, which uses `{% if %}` / `{% else %}` to pick the answer. Styling comes from `newyear/static/styles.css`, loaded via `{% load static %}` and `{% static 'styles.css' %}`.

### `tasks` — forms and sessions

| URL | View | Behaviour |
| --- | --- | --- |
| `/tasks` | `index` | Lists the tasks stored in the current user's session |
| `/tasks/add` | `add` | Shows a `NewTaskForm`; on a valid POST, appends the task and redirects back to the list |

**Concepts:**

- **Django forms** — `NewTaskForm` (`forms.Form`) with a `CharField` for the task and an `IntegerField` for priority (1–10), giving server-side validation for free.
- **Sessions** — each visitor gets their own task list in `request.session`, so tasks persist across requests without a database model.
- **Template inheritance** — `index.html` and `add.html` extend `layout.html` using `{% block body %}`.
- **Named / namespaced URLs** — `app_name = "tasks"` plus `{% url 'tasks:add' %}` and `reverse("tasks:index")`.
- **CSRF protection** — `{% csrf_token %}` in the POST form.

---

## `airline` — models, migrations and the admin

A small flight-management app backed by SQLite, built around the Django ORM.

### Data model

```
┌──────────────┐ 1      * ┌───────────────────┐ *      * ┌──────────────┐
│   Airport    │──────────│      Flight       │──────────│  Passenger   │
├──────────────┤          ├───────────────────┤          ├──────────────┤
│ code (3)     │ origin ─▶│ origin       (FK) │◀─flights │ first        │
│ city         │ dest.  ─▶│ destination  (FK) │          │ last         │
└──────────────┘          │ duration (min)    │          │ flights (M2M)│
                          └───────────────────┘          └──────────────┘
```

| Model | Fields | Notes |
| --- | --- | --- |
| `Airport` | `code`, `city` | Displays as `City (CODE)`, e.g. `New York (JFK)` |
| `Flight` | `origin`, `destination`, `duration` | Two `ForeignKey`s to `Airport` with `related_name="departures"` / `"arrivals"` |
| `Passenger` | `first`, `last`, `flights` | `ManyToManyField` to `Flight` with `related_name="passengers"` |

The schema evolved over three migrations, mirroring the lecture:

1. `0001_initial` — `Flight` with plain-text origin/destination
2. `0002_airport_…` — introduces `Airport` and turns origin/destination into foreign keys
3. `0003_passenger` — adds `Passenger` and the many-to-many relationship

### Pages

| URL | View | Behaviour |
| --- | --- | --- |
| `/flights/` | `index` | Lists every flight with a link to its detail page |
| `/flights/<flight_id>` | `flight` | Shows origin, destination, duration, the booked passengers, and a dropdown of passengers not yet on the flight |
| `/flights/<flight_id>/book` | `book` | POST-only action: adds the selected passenger to the flight, then redirects back to the flight page |
| `/admin/` | Django admin | Full CRUD for airports, flights (custom `list_display`) and passengers |

**Concepts:** `models.Model`, `makemigrations` / `migrate`, `ForeignKey` and `ManyToManyField` with `related_name`, querysets (`.all()`, `.exclude()`), `get_object_or_404`, `HttpResponseRedirect` + `reverse()`, and customizing the admin with `ModelAdmin`.

---

## Getting started

### Prerequisites

- Python 3.12+
- Django 5.2+ (the projects were generated with Django 5.2 and 6.1)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django
```

### Run `mywebsite`

```bash
cd mywebsite
python manage.py migrate        # creates the session tables
python manage.py runserver
```

Then visit <http://127.0.0.1:8000/hello/>, <http://127.0.0.1:8000/newyear/> or <http://127.0.0.1:8000/tasks>.

### Run `airline`

```bash
cd airline
python manage.py migrate
python manage.py createsuperuser   # to log in to the admin
python manage.py runserver
```

Open <http://127.0.0.1:8000/admin/> to add airports, flights and passengers, then browse them at <http://127.0.0.1:8000/flights/>.

You can also explore the ORM interactively:

```bash
python manage.py shell
```

```python
>>> from flights.models import Airport, Flight, Passenger
>>> jfk = Airport.objects.create(code="JFK", city="New York")
>>> lhr = Airport.objects.create(code="LHR", city="London")
>>> f = Flight.objects.create(origin=jfk, destination=lhr, duration=415)
>>> jfk.departures.all()
<QuerySet [<Flight: 1: New York (JFK) to London (LHR)>]>
>>> p = Passenger.objects.create(first="Harry", last="Potter")
>>> p.flights.add(f)
>>> f.passengers.all()
<QuerySet [<Passenger: Harry Potter>]>
```

---

## Notes

These are learning exercises, kept close to the lecture code. A few things you may notice:

- `/hello/<str:name>` is declared before `/hello/david`, so `/hello/david` is handled by `greet` (it still prints *"Hello, David!"*, just via the template).
- `newyear` compares `now.date == 1` (a method, not the day number), so the page always answers **NO**; the intended check is `now.day == 1`.
- The `tasks` form collects a priority but only the task text is stored in the session.
- `DEBUG = True` and the default `SECRET_KEY` are left in `settings.py` — fine locally, not for deployment.

---

## Acknowledgements

Based on the lectures of [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/) by Brian Yu and David J. Malan, Harvard University.

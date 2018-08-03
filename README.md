# PubMan

### PubMan Publication Management Tool

This is a simple Django app that makes use of [Crossref Rest API](https://github.com/CrossRef/rest-api-doc) to let you easily build a collection of publications by a group of people (say, the staff members of an organization).

#### A Little More

The relationships are built from imformation fetched from the crossref.org API with the publications' DOIs (Digital Object Identifiers). This app saves some basic data about each publication, including the  authors and citations.

Additionally, a basic API is in place to retrieve information about the stored publications.

### Installation

Clone this repository into the root of your project. This is the directory containing the `manage.py` file.

This app makes use of a couple modules, namely [http://docs.python-requests.org/en/master/](`requests`) and [crossrefapi](`crossrefapi`), so before getting started, run `pip install requests` and `pip install crossrefapi`.

Now to configure the app itself, you'll need to add `pubman` to your project's installed apps in `settings.py`

```python
  INSTALLED_APPS = [
    ...
    'pubman',
  ]
```

and point Pubman-related urls to the DjOI app's urls file by adding 

```python
urlpatterns = [
    ...
    path('pubman/', include('pubman.urls')),
]
```

to your project's `urls.py` file. Be sure the top of your project's `urls.py` has a line that looks like the following.

```python
from django.urls import path, include`
```

In particular, we've used `include` here, so that should be there. Otherwise you will receive the error  `name 'include' is not defined` because then you have called, but not imported, `include` from the `django.urls` module.

Now, let's add the necessary tables by executing the following commands.

```bash
$ python3 manage.py makemigrations
```

and

```bash
$ python3 manage.py migrate
```

Be sure your development server is up and running. If not, execute

```bash
$ python3 manage.py runserver`
```

Point your browser at `localhost:8000` to see a fairly plain "Welcome to PubMan!" page.

### How to Use

#### Templates

Some basic templates have been included in the PubMan app, and inspection of them will make it clear how to use the various information PubMan makes accessible.

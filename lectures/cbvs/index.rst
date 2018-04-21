===========================
Class-Based Views in Django
===========================

Views
=====

Views
-----

- code for turning a request into a response

- in Flask, they are functions

- in Django, they are functions OR classes

From the Django tutorial, part 3
--------------------------------

A Function-Based view

.. code-block:: python

    from django.http import HttpResponse

    from .models import Question


    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        output = ', '.join([q.question_text for q in latest_question_list])
        return HttpResponse(output)


`Source <https://docs.djangoproject.com/en/1.11/intro/tutorial03/>`_

From the Django tutorial, part 4
--------------------------------

.. code-block:: python

    from django.views import generic
    #...

    from .models import Question


    class IndexView(generic.ListView):
        template_name = 'polls/index.html'
        context_object_name = 'latest_question_list'

        def get_queryset(self):
            """Return the last five published questions."""
            return Question.objects.order_by('-pub_date')[:5]

.. code-block:: python

    from django.conf.urls import url

    from . import views

    app_name = 'polls'
    urlpatterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        #...
    ]

`Source <https://docs.djangoproject.com/en/1.11/intro/tutorial04/>`_

Why CBVs
--------

In Django 1.4... (End of support Feb. 2013)

.. code-block:: python

    def show_list(request, slug=None, 
                  template_name='podcast/show_list.html', 
                  page=0, paginate_by=25, mimetype=None):
        """
        Episode list
        ...
        """

        if slug:
            shows = Show.objects.filter(slug__exact=slug)
        else:
            shows = Show.objects.all()

        return object_list(
            request=request,
            queryset=shows,
            template_name=template_name,
            paginate_by=paginate_by,
            page=page)

`Source <http://www.programcreek.com/python/example/60520/django.views.generic.list_detail.object_list>`_

.. newslide::

Also from Django 1.4... (End of support Feb. 2013)

.. code-block:: python

    def recipe_list(request, queryset, *args, **kwargs):
        recipes = queryset
        filter = None
        if request.GET:
            data = request.GET.copy()
            if data.has_key('categoria'):
                filter = Category.objects.get(slug=data.get('categoria'))
                recipes = recipes.filter(categories=filter)
            elif data.has_key('tipo'):
                filter = Meal.objects.get(slug=data.get('tipo'))
                recipes = recipes.filter(meals=filter)
        else:
            recipes = recipes.order_by('-id')[:12]

        return object_list(request,queryset=recipes,extra_context={'filter':filter})

`Source <http://www.programcreek.com/python/example/60520/django.views.generic.list_detail.object_list>`_

Problems with Function-Based Views
----------------------------------

- repetitive -- not DRY

- monolithic (a.k.a. not modular, can't be broken out and reused)

- lots of conditional view logic

- so many keyword arguments


CBVs and generic.ListView
=========================

CBVs
----

- your view logic can be modular, object-oriented

- Django generic views are modular, object-oriented

Lectures List
-------------

.. code-block:: python

    class LectureSessionListView(DynamicCohortMixin, CurriculumBreadcrumbsMixin,
                                 FrodoHeadlineMixin, generic.ListView):
        """List of all lecture sessions for a particular cohort."""

        template_name = "curriculum/lecturesession_list.html"
        headline = "Lectures"

        def get_queryset(self):
            """Get list of published lecture sessions for this semester."""
            cohort = self.get_cohort()

            return (LectureSession
                    .published.filter(cohort=cohort)
                    .select_related('lecture', 'cohort')
                    .prefetch_related('staff').order_by('start_at')
                    )

.. code-block:: python

    from django.conf.urls import url
    from views import lectures

    urlpatterns = [  #...
            url(r'^lectures/$', lectures.LectureSessionListView.as_view(),
                name='cohort_lectures'),   #...
    ]

from Django: **generic.ListView**
---------------------------------

Inherits from:

- MultipleObjectTemplateResponseMixin
- TemplateResponseMixin
- BaseListView
- MultipleObjectMixin
- ContextMixin
- View

.. newslide:: 

Allows you to:

.. container:: item-incremental

    - Associate a template with the view

      - class attribute **template_name** or method **get_template_names**

    - Specify a set of DB objects to render and make available in the template

      - class attribute **queryset** or method **get_queryset**

    - Specify other things to make available in the template

      - method **get_context_data**

    - Other boring things like handling an HTTP request, making sure the request
      method is allowed, etc.

from Frodo source: **BreadcrumbsMixin**
---------------------------------------

.. code-block:: python

    class BreadcrumbsMixin(object):
    """Provide breadcrumbs to curriculum views.

    Things that use this must also the the SetHeadlineMixin.
    """

    #...

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)

        context['breadcrumbs'] = (
            self.get_breadcrumbs_root()
            + self.get_breadcrumbs_parents()
            + [{'title': self.get_breadcrumb_headline()}]
        )

        return context

.. too sourcecodey
    from Django: **generic.View**
    -----------------------------

    - gets the HTTP request and does some sanity checks

    - **as_view** method checks to make sure no unexpected kwargs got passed

    - **dispatch** method checks to make sure the method is allowed for the
      request's URL

      - if request's method is GET, called self.get()

      - if request's method is POST, called self.post()

Other Generic Views to Know
===========================

generic.TemplateView
--------------------

- parents are **TemplateResponseMixin**, **ContextMixin**, and **View**

- best match to a flask route function

- can process a request (from **View**)

- can pass data to the template via **get_context_data** (from **ContextMixin**)

- can be associated with a particular template (from **TemplateResponseMixin**)

  - so, you can define class attribute **template_name** or method 
    **get_template_names**

generic.DetailView
------------------

- ListView's more specific sister

- inherits from 

  - SingleObjectTemplateResponseMixin

  - TemplateResponseMixin

  - BaseDetailView

  - SingleObjectMixin

  - ContextMixin

  - View

- still has a queryset (attribute or method), but looks for a primary key
  query parameter from the request

generic.CreateView
------------------

- with a Django form class, you can very easily allow users to create
  DB objects 

- a great example of polymorphism

- relatedly, there is **generic.UpdateView**

.. newslide::

.. code-block:: python

    class NotebookCreateForm(forms.ModelForm):
        """A form to create a notebook and all the drawings in it."""

        class Meta:
            model = Notebook
            fields = ['title', 'description', 'id', 'drawn_at']
            widgets = {
                'drawn_at': widgets.MonthYearWidget(years=xrange(1980,2050)),
            }

.. code-block:: python

    class NotebookCreateView(generic.CreateView):
        """Add a notebook and all of its drawings in one go."""

        model = Notebook
        form_class = NotebookCreateForm
        template_name = 'drawings/notebook_create.html'
        headline = "Upload a Notebook"

        form_invalid_message = "Please correct the error(s)."
        form_valid_message = "Information saved."

        # "if everything worked out that should have"
        def form_valid(self, form):
            # can add addl logic here
            return super(NotebookCreateView, self).form_valid(form)

Conclusion
==========

Conclusion
----------

Class-based views are classy as hell.

Resources
---------

`CCBV <https://ccbv.co.uk/>`_

`The Official Django Tutorial, Part 3 <https://docs.djangoproject.com/en/1.11/intro/tutorial03/>`_



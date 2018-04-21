=================================
The Unbearable Heaviness of Being
=================================

About This Talk
===============

Me at PyCon This Year
---------------------

.. image:: hansel.jpg

Dictionaries
============

Dictionaries
------------
Fast, But Heavy

.. newslide::

.. parsed-literal::
    :class: big

    cat_facts = {"fur_color": "black",
                 "age": 9,
                 "napping": True}

    # ... other stuff

    cat_facts['chases_lasers'] = True
    cat_facts['hunting_for_mice'] = True

.. container:: nest-incremental

  - Hash keys/values, store hash and what it points to

  - Providing direct access via hashing takes up space

  - Python makes more space for your dictionary as it grows in size


Objects
=======

They Store Their Attributes in Dictionaries
-------------------------------------------

- You can see instance attributes with ``some_instance.__dict__``
- Also class attributes with ``SomeClassName.__dict__``

Objects Store Their Attributes in Dictionaries
----------------------------------------------

.. code-block:: python

    class Cat(object):
        """A cat."""

        species = "Cat"

        def __init__(self, fur_color):
            self.fur_color = fur_color

        def hunt_for_mice(self):
            self.hunting = True  # a new attribute!

.. container:: one-incremental

    .. parsed-literal::
    
      >>> princess = Cat("black")
      >>> princess.__dict__
      {'fur_color': 'black'}

.. container:: one-incremental 

      >>> Cat.__dict__
      dict_proxy({'__module__': '__main__', 'hunt_for_mice': 
      <function hunt_for_mice at 0x1101dbe60>, 'species': 'Cat',
      '__dict__': <attribute '__dict__' of 'Cat' objects>,
      '__weakref__': <attribute '__weakref__' of 'Cat' objects>,
      '__doc__': 'A cat.', '__init__': <function __init__ at 0x1101dbde8>})

When is this not cool?
----------------------

It's like living in a mansion when you only |reveal-br|
have enough furniture for a one bedroom apartment.



``__slots__``
=============

Using ``__slots__`` with our Cat
--------------------------------

.. code-block:: python

    class FurCat(object):
        """A lighter cat."""

        __slots__ = ('fur_color',)

        species = "Cat"

        def __init__(self, fur_color):
            self.fur_color = fur_color

        def hunt_for_mice(self):
            self.hunting = True  # AttributeError!

Why use ``__slots__``?
----------------------

.. container:: one-incremental

    When you don't want to internally store instance |reveal-br|
    attributes as a dictionary.

.. container:: one-incremental

    *\... okay ... so when do you want to do that?*

.. container:: one-incremental

    When you know your object will need only a |reveal-br|
    particular set of instance attributes,  |reveal-br|
    and no more than that in its lifetime. |reveal-br|




Warning: Premature Optimization
-------------------------------

    "Don’t prematurely optimize and use this everywhere!
    [...]it really only saves you when you have **thousands** 
    of instances."

- Ben Hoyt (http://tech.oyster.com/save-ram-with-python-slots/)

Warning: Inheritance
--------------------

Children of parent classes that have ``__slots__`` |reveal-br|
also can't add instance attributes. 

Thanks
======

Me
--

I teach at Hackbright Academy, a software engineering bootcamp for women.

.. image:: teaching.jpg
  :width: 50%

.. container:: one-incremental

  - Twitter: @megthedeveloper

  - Email: mmm25eg@gmail.com

  - https://hackbrightacademy.com








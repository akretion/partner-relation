================
Partner Relation
================

This module adds relations between partners. The type of relation is
configurable ; it supports symetric and asymetric relations.

For example, you will be able to define on the form view of partner A that :

* Partner A is a competitor of Partner B
  (symetric relation : B is a competitor of A),

* Partner A has been recommended by Partner C
  (asymetric relation : C recommands A),

* Partner A is the editor of Partner D
  (asymetric relation : D is the integrator of A).

The relations that you define on Partner A towards Partner B will
automatically be visible on the form view of Partner B.

This module is an alternative to the module *partner_relations* (with an *s*) in the `partner-contact OCA project <https://github.com/OCA/partner-contact>`_. The two modules were developped at the same time (in 2014). This module is used in production at the `Barroux Abbey <http://www.barroux.org>`_ and there is no plan to migrate to the OCA module for the moment, because the OCA module has features that are not needed for the Abbey and this module fits perfectly the needs.

Configuration
=============

You will have to create the type of relations in the menu
*Sales > Configuration > Address Book > Relations > Partner Relation Types*.

Usage
=====

On the form view of a partner, in the *Relations* tab, you can view and
create the relations of this partner.

Credits
=======

Contributors
------------

* Alexis de Lattre <alexis.delattre@akretion.com>

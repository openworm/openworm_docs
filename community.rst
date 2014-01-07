.. _community:

*******************
OpenWorm Community
*******************

This page contains information intended to help individuals understand what steps to take 
to make contributions to OpenWorm, how to join OpenWorm meetings, how to 
interact with the community online, and how to become
an OpenWorm core member.

.. contents::

Contribution Best Practices
===========================

Once you have identified an issue you want to work on from :ref:`a particular project <projects>`, 
please announce your intention to helping out on the 
`mailing list <https://groups.google.com/forum/?fromgroups#!forum/openworm-discuss>`_ and 
by :ref:`commenting on the 
specific GitHub issue <github-issues>`.  

Using OpenWorm repos on GitHub
------------------------------

Making
a contribution of code to the project will first involve 
:ref:`forking one of our repositories <github-fork>`,
making changes, committing them, creating a pull request back to the original repo, and
then updating the appropriate part of documentation.  

An alternate way to contribute is to 
create a new GitHub repo yourself and begin tackling some issue directly there.  We can
then fork your repo back into the OpenWorm organization at a later point in order to 
bring other contributors along to help you.

More details on best practices using OpenWorm repos on GitHub are available :ref:`on a separate page <github>`.

.. _google-drive:

Creating organizing documents
-----------------------------

Another
great way to contribute is by 
:ref:`organizing ideas or documentation or proposals via a Google
doc <google-drive>`, and then sharing the link on our 
`mailing list <https://groups.google.com/forum/?fromgroups#!forum/openworm-discuss>`_.

To contribute documentation and materials to the OpenWorm Google Drive, log into your Gmail account and click on 
`this link <https://drive.google.com/folderview?id=0B_t3mQaA-HaMaXpxVW5BY2JLa1E&usp=sharing>`_.

All documents located in the OpenWorm folder is viewable to the public.  Comments can be added to both text 
documents and spreadsheets.  In order to edit existing documents or to add a new document, you will need to be 
added to the folder.  You can request access by email your Google ID to info@openworm.org. 

.. Spreadsheets, slide presentation, dynamic documents - should be on google drive (policy of what goes in)
.. Folder structure w/ descriptors

`OpenWorm Docs <https://drive.google.com/a/openworm.org/?tab=oo#folders/0B_t3mQaA-HaMaXpxVW5BY2JLa1E>`_

Taking notes as Google docs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is very useful to create notes and progress reports as the result of meetings as Google docs. Docs should
be shared publicly with view and comment access.

An effective progress report should contain the following information:

* Meeting title
* Attendees
* Date
* Goal being worked on (link back to doc page describing project)
* Previous accomplishments
* Recent progress towards goal
* Next Steps 
* Future Steps

An example of an effective progress report is 
`available online <https://docs.google.com/document/d/1sBgMAD-7RUjHwBgrC204LMqSC81byIaZNRm32lEGWMM/edit>`_.

Once the document is shared, it should be announced on `the mailing list <https://groups.google.com/forum/?fromgroups#!forum/openworm-discuss>`_.

Creating proposals as Google docs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To gather public comment on a direction for the project, it is often effective to create a 
proposal as a world-editable Google Doc.  Once your document is created and shared, 
it should be announced on `the mailing list <https://groups.google.com/forum/?fromgroups#!forum/openworm-discuss>`_.

An example of an effective proposal is 
`available online <https://docs.google.com/a/openworm.org/document/d/1R5yeossrj_Ks1GvTtoE__8HtsrPCNVN46crwiJdSieU/edit#heading=h.8sny9ql7x375>`_

Contributing to the OpenWorm documentation
------------------------------------------

The `OpenWorm documentation <http://openworm.rtfd.org>`_ is a searchable repository
of knowledge we have assembled to help new users get oriented to the different areas 
of the project.  When new contributions are made, it is important that they are incorporated
into the appropriate part of the documentation.

When they are ready to consume by the general public, simulation engines, 
visualization environments, and data sets should be added to the :ref:`resources page <resources>`.

Information about the goals, progress, and roadmap of current or proposed projects should 
be added to the :ref:`projects page <projects>`. 

The docs use `rst format <http://sphinx-doc.org/rest.html>`_.  This kind of 
`markup <https://en.wikipedia.org/wiki/Markup_language>`_ is a bit verbose and unforgiving
in its syntax compared to other languages, but it is convenient for publishing documentation
to the `ReadTheDocs service <https://readthedocs.org/>`_ directly from the GitHub repo, so we use it.

The 'master outline' for the top level is in 
`index.rst <https://raw.github.com/openworm/openworm_docs/master/index.rst>`_.  The 
`'toctree' directive <http://sphinx-doc.org/markup/toctree.html>`_ in this 
file sets up what is on the sidebar.  This assumes that files with the names under the 
toctree are present in the same directory as index.rst.  Under this, the next level of 
hierarchy is determined by `section headers <http://sphinx-doc.org/rest.html#sections>`_.  
In the `projects page <https://raw.github.com/openworm/openworm_docs/master/projects.rst>`_
we've used a hidden toctree in the file, which is creating the 
next level of hierarchy in the sidebar.  In that toctree, you can see an example of referencing 
the underlying directory structure (e.g. 'Projects/worm-movement').

.. _journalclub:

Journal Clubs
-------------
Every few months an academic journal article comes along we can't resist talking about. 
We host a journal club where we invite scientists to present on the paper and to host a 
discussion about it, hopefully with some of the article authors.

You can see 
`past journal clubs we have conducted online 
<https://www.youtube.com/watch?v=JHSqkZ2sFDA&list=PL8ACJC0fGE7D-EkkR7EFgQESpHONC_kcI>`_.

If you have an idea for a good journal club, please post the suggestion 
`on our mailing list <https://groups.google.com/forum/?fromgroups#!forum/openworm-discuss>`_.


Meetings
========

.. _team-meetings:

Team meetings
--------------

We have `a regular meeting <https://www.youtube.com/watch?v=-IyHokN8FkA&list=PL8ACJC0fGE7C7zlCBqkx1LMN1DHGKVp22>`_ 
of the team that is building applications every two weeks.  
We also currently
schedule an ad-hoc `data team meeting <https://www.youtube.com/watch?v=seKjRnw7CB8&list=PL8ACJC0fGE7CGtyJWV2dPOfNxAruk2VcM>`_ 
about every 3-4 weeks.  The events
are on `our community calendar <https://www.google.com/calendar/embed?src=bqvlrm642m3irjehbethokkcdg%40group.calendar.google.com>`_.  
The events are streamed live when they occur and an archive of the meeting videos
and `the minutes <https://drive.google.com/#folders/0B8QUskXehbJtNWM2MjUyM2EtOTMxMC00MWY3LWEyNWMtNDUwMjRiNjM0Mjcx>`_
are kept online.

Working meetings
----------------

Contributors are encouraged to meet with each other on a regular basis to advance areas of 
the project they need interaction on.  

IRC meetings
-----------

We had been running meetings on IRC for some time but have currently discontinued the 
practice.  If there is interest in reviving this, please post on 
`the mailing list <https://groups.google.com/forum/?fromgroups#!forum/openworm-discuss>`_.

Scheduling meetings
-------------------

We like using the `Doodle service <http://doodle.com>`_ for scheduling meetings.  This makes it easy to find
times to meet across various time zones.  Once a meeting is scheduled, we will often create
a Google+ event to track it and remind everyone it is occurring.


Interactions
============

Mailing Lists
---------------
There are two Google Groups in connection with OpenWorm. We suggest joining both lists to stay current, 
introduce yourself to the project, and participate in ongoing discussions.  Simply login with you Gmail 
username and click on "Join Group" for each list.

`This list <https://groups.google.com/forum/?hl=en#!forum/openworm>`_ is for general updates and announcements 
related to the project.

`This list <https://groups.google.com/forum/?hl=en#!forum/openworm-discuss>`_ is for high-volume type technical 
discussions, day-to-day communications, and questions related to the OpenWorm project.


Google Plus
------------
`Follow us on OpenWorm Google+ <https://plus.google.com/+OpenwormOrg/posts>`_

Click on the "Follow" button to be a part of the OpenWorm community on Google+. 

If you need more help with Google+, check out the handy `guide <https://support.google.com/plus/?hl=en#topic=3049662>`_
put out by Google.


YouTube
-------
`View our YouTube channel <http://www.youtube.com/user/OpenWorm>`_

Want to get notified when new content goes live? `Subscribe to the channel <http://www.youtube.com/user/OpenWorm>`_ by clicking on the "subscribe" button while logged in to your Google account.

Playlists
^^^^^^^^^

* Status Updates - Biweekly updates from the OpenWorm team. 
* Journal Clubs - Like journal clubs that meet in person, the OpenWorm journal clubs use discuss new discoveries, tools and resources related to neuroscience, *C. elegans*, computational biology and open source science.  
  Journal clubs are posted to social media in advance for any to watch and recordings then become available on YouTube.  :ref:`Learn more about our journal clubs. <journalclub>`
* Data Team meetings - :ref:`Learn more about our team meetings. <team-meetings>`
* Real *C. elegans*
* Building Blocks


Twitter
-------
`Follow our Twitter feed <http://twitter.com/openworm>`_

Want to tag OpenWorm on a tweet? Use @openworm and share the love.

Blog
----

`Our blog <http://blog.openworm.org>`_ is hosted in Tumblr.

Interesting in being a guest on our blog? We love hearing about what members are of the OpenWorm community are doing.  If you have something to share, contact us at info@openworm.org to discuss.


Membership
==========

More information about the membership policy is 
:ref:`available on a separate page <membership>`.

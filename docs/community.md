OpenWorm Community
==================

This page contains information intended to help individuals understand what steps to take to make contributions to OpenWorm, how to join OpenWorm meetings, how to interact with the community online, and how to become an OpenWorm core member.

An Opening Note
---------------

Feeling lost? Not uncommon in open source projects. In fact, there are [whole papers](http://www.igor.pro.br/publica/papers/OSS2014.pdf) describing the kinds of problems you may be having and some proposed solutions. Help us make helping you easier by [reaching out to us to ask for help](http://openworm.org/contacts.html).

Contribution Best Practices
---------------------------

What do I work on? We outline the work we are doing in the project using [GitHub issues](https://guides.github.com/features/issues/). Therefore, in order to figure out what to help out on, you need to be able to check them out for yourself. One way is to use this documentation to find [a project](../projects/) you want to contribute to.

### Find tasks to work on

Another way is you can [browse the Project level view of issues](https://github.com/orgs/openworm/projects) directly.

Other key boards:

- [Geppetto](https://github.com/orgs/openworm/projects/13)
- [Movement Validation](https://github.com/orgs/openworm/projects/6)
- [Muscle-Neuron-Channel integration](https://github.com/orgs/openworm/projects/5)

### Come chat with us!

You can initiate a conversation with us on [Slack](https://slack.com) channels to get more specific about issues.  We ask that you just sign up as a contributor before receiving an invite to join our Slack channel first by [filling out the form here](https://goo.gl/3ncZWn).  Once you are logged in, you will find channels such as:

- [General](https://app.slack.com/client/T02EPNETZ/C02EPNEUT)
- [Geppetto](https://app.slack.com/client/T02EPNETZ/C89GCLE49)
- [Movement Validation](https://app.slack.com/client/T02EPNETZ/C49LLAMJQ)
- [Muscle model](https://app.slack.com/client/T02EPNETZ/C40BEV91S)
- [ChannelWorm](https://app.slack.com/client/T02EPNETZ/C40MMRWDQ)

Once you have identified an issue you want to work on from a [particular project](../projects/), please announce your intention to help out by commenting on the specific [GitHub issue](../Community/github/#contributing-and-resolving-issues).

### Using OpenWorm repos on GitHub

Making a contribution of code to the project will first involve [forking one of our repositories](../Community/github/#forking-github-repositories), making changes, committing them, creating a pull request back to the original repo, and then updating the appropriate part of documentation.

An alternate way to contribute is to create a new GitHub repo yourself and begin tackling some issue directly there. We can then fork your repo back into the OpenWorm organization at a later point in order to bring other contributors along to help you.

More details on best practices using OpenWorm repos on GitHub are available on [a separate page](../Community/github/).

### Creating organizing documents

Another great way to contribute is by organizing ideas or documentation or proposals via a Google
doc, and then sharing the link on our [Slack](http://openworm.org/contacts.html).

To contribute documentation and materials to the OpenWorm Google Drive, log into your Gmail account and click on [this link](https://drive.google.com/folderview?id=0B_t3mQaA-HaMaXpxVW5BY2JLa1E&usp=sharing).

All documents located in the OpenWorm folder is viewable to the public. Comments can be added to both text documents and spreadsheets. In order to edit existing documents or to add a new document, you will need to be added to the folder. You can request access by email your Google ID to <info@openworm.org>.

### Taking notes as Google docs

It is very useful to create notes and progress reports as the result of meetings as Google docs. Docs should be shared publicly with view and comment access.

An effective progress report should contain the following information:

-   Meeting title
-   Attendees
-   Date
-   Goal being worked on (link back to doc page describing project)
-   Previous accomplishments
-   Recent progress towards goal
-   Next Steps
-   Future Steps

An example of an effective progress report is [available online](https://docs.google.com/document/d/1sBgMAD-7RUjHwBgrC204LMqSC81byIaZNRm32lEGWMM/edit).

Once the document is shared, it should be announced on [Slack](http://openworm.org/contacts.html).

### Creating proposals as Google docs

To gather public comment on a direction for the project, it is often effective to create a proposal as a world-editable Google Doc. Once your document is created and shared, it should be announced on [Slack](http://openworm.org/contacts.html).

An example of an effective proposal is [available online](https://docs.google.com/a/openworm.org/document/d/1R5yeossrj_Ks1GvTtoE__8HtsrPCNVN46crwiJdSieU/edit#heading=h.8sny9ql7x375).

### Contributing to the OpenWorm documentation

The [OpenWorm documentation](http://docs.openworm.org) is a searchable repository of knowledge we have assembled to help new users get oriented to the different areas of the project. When new contributions are made, it is important that they are incorporated into the appropriate part of the documentation.  The GitHub repo for the OpenWorm documentation [is here](http://github.com/openworm/openworm_docs).  An issues list for changes that we are working on to improve the documentation [is here](https://github.com/openworm/openworm_docs/issues).

When they are ready to consume by the general public, simulation engines, visualization environments, and data sets should be added to [the resources page](../Resources/resources/).

Information about the goals, progress, and roadmap of current or proposed projects should be added to [the projects page](../projects/).

The docs use ["GitHub-flavored" markdown format](https://help.github.com/articles/github-flavored-markdown/). This makes writing for GitHub (where most of our code is stored) and writing the documentation seamless. Markdown is also more forgiving in its syntax than, say, ReSTructured text, which was used previously.

The documentation is published using [GitHub Pages](https://pages.github.com/), which helps it remain searchable and beautiful.

The markdown documentation is rendered using the Python module [MkDocs](https://www.mkdocs.org), making theming and structuring much easier. The outline of the Table of Contents tree is structured in `mkdocs.yml`.

After issuing a pull request and merging to master, changes that appear in GitHub will automatically trigger a hook that will cause the documentation on GitHub Pages (and available at http://docs.openworm.org) to become rebuilt and pushed onto the site (using a [GitHub Action](https://github.com/openworm/openworm_docs/actions)).

### Guest Blog Post

We love hearing about what members are of the OpenWorm community are doing. If you have something to share, contact us at <info@openworm.org> to discuss.

### Journal Clubs

Every few months an academic journal article comes along we can't resist talking about. We host a journal club where we invite scientists to present on the paper and to host a discussion about it, hopefully with some of the article authors.

You can see [past journal clubs we have conducted online](https://www.youtube.com/watch?v=JHSqkZ2sFDA&list=PL8ACJC0fGE7D-EkkR7EFgQESpHONC_kcI).

If you have an idea for a good journal club, please contact us at <info@openworm.org>.

Coding Standards
----------------

It is recommended to follow the [PEP8 Guidelines](http://legacy.python.org/dev/peps/pep-0008/). For contributions of Python code to OpenWorm repositories. Compliance can be checked with the [pep8 tool](https://pypi.python.org/pypi/pep8) and [autopep8](http://pypi.python.org/pypi/autopep8).

Meetings
--------

### Working meetings

Contributors are encouraged to meet with each other on Slack on a regular basis to advance areas of the project they need interaction on.

### Scheduling meetings

We like using the [Doodle service](http://doodle.com) for scheduling meetings. This makes it easy to find times to meet across various time zones. Once a meeting is scheduled, we will often create a Google Calendar event to track it and remind everyone it is occurring.

Interactions
------------

### Mailing Lists

There are two Google Groups in connection with OpenWorm.

[This list](https://groups.google.com/forum/?hl=en#!forum/openworm) was for general updates and announcements related to the project.

[This list](https://groups.google.com/forum/?hl=en#!forum/openworm-discuss) was for high-volume type technical discussions, day-to-day communications, and questions related to the OpenWorm project.

>> **⚠ NOTE: Discussions have moved to Slack.**  
>> The mailing lists above have become quiet of late... Most of the in depth discussions in the project have moved to [Slack](http://openworm.org/contacts.html).

### Twitter

[Follow our Twitter feed](http://twitter.com/openworm)

Want to tag OpenWorm on a tweet? Use @openworm and share the love.

### Blog

[Our blog](https://openworm.tumblr.com/) is hosted in Tumblr.

Interesting in being a guest on our blog? We love hearing about what members of the OpenWorm community are doing. If you have something to share, contact us at <info@openworm.org> to discuss.

### YouTube

Our YouTube channel is currently quite out of date, but for historical purposes, you can [view our YouTube channel here.](http://www.youtube.com/user/OpenWorm)

Want to get notified when new content goes live? [Subscribe to the channel](http://www.youtube.com/user/OpenWorm) by clicking on the "subscribe" button while logged in to your Google account.

#### Playlists

-   Status Updates - Frequent updates from the OpenWorm team.
-   Journal Clubs - Like journal clubs that meet in person, the OpenWorm journal clubs use discuss new discoveries, tools and resources related to neuroscience, _C. elegans_, computational biology and open source science. Journal clubs are posted to social media in advance for any to watch and recordings then become available on YouTube. Learn more about our [journal clubs](#journal-clubs).
-   Data Team meetings - Learn more about our [team meetings](#team-meetings).
-   Real _C. elegans_
-   Building Blocks

Membership
----------

More information about the membership policy is available on [a separate page](Community/membership.md).

Use of OpenWorm logo
--------------------

The OpenWorm logo font is Kefa.

This is the OpenWorm logo:

![](Community/openworm_logo.png)

[Click here for a vector version of the logo](https://drive.google.com/folderview?id=0B-GW0T4RUrQ6ZDRFWGQwVmpOSm8&usp=sharing).  All three layers are vector.

It may be adapted for subteams.  Please follow these style rules when doing so:

- Don't apply effects (e.g. shadows) to the text; use flat style
- If any icon is added it should be flat looking and its colour should be #92bd1e
- Do not use detailed/real looking graphics
- Keep it simple
- Do not alter the OpenWorm logo itself
- Logo needs to be readable when rendered in grayscale

Such logos are subject to review by the core team to retain consistency across the project.

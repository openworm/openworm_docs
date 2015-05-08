#Converting your RST docs to MD

1. [Install MkDocs](http://www.mkdocs.org/#installation)
2. Following [their instructions](http://www.mkdocs.org/#getting-started), do `mkdocs projectname` to initialize the project.
3. [Install pandoc](http://pandoc.org/installing.html)
4. Run `./convert.sh your/docs/directory`
5. If all went well you should have a new directory `docs` now, which contains markdown versions of all your old rst docs.
Go through those markdown versions and make corrections on the converter's output.
    * In particular, I had to change local links manually

So now all your new docs go in the docs folder.

**Important**
Your docs will fail to build on ReadTheDocs until you change the "Documentation type" setting to "MkDocs (Markdown)". This is on ReadTheDocs in the "Admin" page for your build.

Modify `mkdocs.yml` to configure your project.

Check out the [mkdocs docs](http://www.mkdocs.org/#mkdocs) to learn more about configuration.

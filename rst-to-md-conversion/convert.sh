#! /bin/bash
#One-off script to convert rst files to markdown with pandoc

#You end up with a copy of your old docs directory tree, with all the rst
# files converted to markdown files using pandoc

#Usage:   ./convert.sh path/to/old/docs

DIR=$(dirname $1);

if ! which "pandoc" > /dev/null; then
  echo "Install pandoc first.";
  exit 1;
fi

if [ -e $DIR/docs ]; then
  echo "We'll make the 'docs' directory in this script.";
  echo "Delete $DIR/docs, or copy it somewhere then rerun the script.";
  exit 1;
fi

mkdir $DIR/docs;
cp -R $1 $DIR/docs;

for file in $(find $DIR/docs -name '*.rst' -print); do
  NEWNAME="${file%rst}md";
  pandoc -r rst -w markdown_github $file > $NEWNAME 2> /dev/null;
  echo "Converted $file to $NEWNAME";
  rm $file;
done

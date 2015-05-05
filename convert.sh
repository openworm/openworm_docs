#! /bin/bash
#One-off script to convert rst files to markdown with pandoc

for file in $(find ~/programming/worm/openworm_docs/old -name '*.rst' -print); do
  OLDNAME=$file;
  NEWNAME=${OLDNAME/old/docs};
  NEWNAME=${NEWNAME/rst/md};
  pandoc -r rst -w markdown_github $OLDNAME > $NEWNAME;
  echo "Converted $OLDNAME to $NEWNAME";
done

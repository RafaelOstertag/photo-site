#!/bin/sh

rsync -aPc --no-times --no-perms --no-owner --no-group --delete _site/ web-1:/data/www/www.rafaelostertag.photo/

#!/bin/sh

lastname="$1"
curl -sL "https://www.familysearch.org/en/surname?surname=$lastname" |
grep -E '<h3 class="countryTitleText">\w+' | cut -d'>' -f2 | cut -d'<' -f1 | tr '\n' ','
echo ''

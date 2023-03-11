#!/usr/bin/perl -p
if (/'(.+)',?/) {
  $_ = $1."\n";
} else {
  $_ = '';
}

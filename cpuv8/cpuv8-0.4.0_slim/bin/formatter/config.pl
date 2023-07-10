#
# config.pl
#
# Copyright 1999-2019 Standard Performance Evaluation Corporation
#
package Spec::Config;

use strict;
use IO::File;
use Safe;
use File::Basename;
$::tools_versions{'formatter/config.pl'} = 0;

require 'util_common.pl';
require 'config_common.pl';

sub copies {
    my $me = shift;
    return 1 unless $me->runmode =~ /rate$/;
    return $me->accessor('copies');
}

sub threads {
    my $me = shift;
    return 1 unless $me->runmode eq 'speed';
    return $me->accessor('threads');
}

sub ranks {
    my $me = shift;
    my $tmp = $me->accessor_nowarn('ranks');
    return $tmp if defined($tmp);
    return $::global_config->accessor_nowarn('ranks') > 1 ? $::global_config->accessor_nowarn('ranks') : 1;
}

1;

# Editor settings: (please leave this at the end of the file)
# vim: set filetype=perl syntax=perl shiftwidth=4 tabstop=8 expandtab nosmarttab:

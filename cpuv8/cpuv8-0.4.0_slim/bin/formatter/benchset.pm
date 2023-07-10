#
# benchset.pm
#
# Copyright 1999-2019 Standard Performance Evaluation Corporation
#

package Spec::Benchset;

use strict;
use vars '@ISA';
$::tools_versions{'formatter/benchset.pm'} = 0;

@ISA = (qw(Spec::Config));

require 'util_common.pl';
require 'benchset_common.pl';

sub results_list {
    my ($me) = @_;
    my $benchhash = $me->{'results'};
    return () if ref($benchhash) ne 'HASH';
    my @result;
    for my $tune ('base', 'peak') {
        for my $bench (sort keys %$benchhash) {
            next if ref($benchhash->{$bench}) ne 'HASH';
            next if !exists $benchhash->{$bench}{$tune};
            if (!exists($benchhash->{$bench}{$tune}{'data'})) {
                Log(0, "WARNING: No data for $bench:$tune\n");
                next;
            }
            push (@result, @{$benchhash->{$bench}{$tune}{'data'}});
        }
    }
    return @result;
}

sub benchmark_results_list {
    my ($me, $bench, $tune) = @_;
    my $benchhash = $me->{'results'};
    return () unless (::ref_type($benchhash) eq 'HASH');
    return () unless (::ref_type($benchhash->{$bench}) eq 'HASH');
    return () unless (::ref_type($benchhash->{$bench}{$tune}) eq 'HASH');

    if (!exists($benchhash->{$bench}{$tune}{'data'})) {
        Log(0, "WARNING: No data for $bench:$tune\n");
        return ();
    }
    return @{$benchhash->{$bench}{$tune}{'data'}};
}

1;

# Editor settings: (please leave this at the end of the file)
# vim: set filetype=perl syntax=perl shiftwidth=4 tabstop=8 expandtab nosmarttab:

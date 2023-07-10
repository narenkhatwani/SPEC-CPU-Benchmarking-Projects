#
#  screen.pl - produces ASCII table on stdout
#  Copyright 2004-2019 Standard Performance Evaluation Corporation
#
#  Authors:  Cloyce D. Spradling
#

use strict;
$::tools_versions{'formats/screen.pl'} = 0;

our ($name, $extension, $synonyms, $part_of_all, $non_default);

$name      = 'Screen';
$extension = undef;
$synonyms  = { map { lc($_) => 1 } ($name, qw(scr display disp terminal term)) };

$non_default = 1;       # You must ask for it by name

sub format {
    my($me, $r, $fn) = @_;

    my @nc = ::allof($r->{'nc'});
    my $invalid = ($r->{'invalid'}
                   || ((ref($r->{'errors'}) eq 'ARRAY') && @{$r->{'errors'}}));

    ::Log(0, "\n\n".join("\n", Spec::Format::Text::screen_format($me, $r, $fn, 0, $invalid, \@nc))."\n\n");

    return ([], []);
}

1;
# Editor settings: (please leave this at the end of the file)
# vim: set filetype=perl syntax=perl shiftwidth=4 tabstop=8 expandtab nosmarttab:

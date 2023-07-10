#
#  pdf.pl - produces PDF output
#  Copyright 1999-2019 Standard Performance Evaluation Corporation
#
#  Author:  Christopher Chan-Nui
#

use strict;
use PSPDF;
$::tools_versions{'formats/pdf.pl'} = 0;

our ($name, $extension, $synonyms, $binary, $part_of_all, $non_default);

$name      = 'PDF';
$extension = 'pdf';
$synonyms  = { map { lc($_) => 1 } ($name, qw(adobe)) };
$binary    = 1;

$non_default = 1;  # You must ask for it by name
$part_of_all = 1;  # Part of '-o all'

sub format () {
    my($me, $r, $path) = @_;
    return undef unless exists $::tools_versions{'formats/ps.pl'};

    eval 'use PDF::API2;
          use PDF::API2::Page;
          use PDF::API2::Content;
          use PDF::API2::Annotation;
          use PDF::API2::NamedDestination;';
    if ($@) {
        main::Log(0, "ERROR: Cannot load PDF::API2 modules for PDF:\n  $@\n");
        $::PDF_ok = 0;
        return undef;
    }

    my @output = split ("\n", Spec::Format::PostScript::SPEC_report($r, 'PDF', $path));
    return (\@output, []);
}

1;
# Editor settings: (please leave this at the end of the file)
# vim: set filetype=perl syntax=perl shiftwidth=4 tabstop=8 expandtab nosmarttab:

#
# locate.pm
#
# Copyright 1999-2019 Standard Performance Evaluation Corporation
#

use strict;
use IO::Dir;
use Time::HiRes qw(time);
use Carp qw(longmess);
use List::Util qw(all);
use List::MoreUtils qw(distinct);
$::tools_versions{'harness/locate.pl'} = 0;

require 'flagutils.pl';
require 'setup_common.pl';

sub locate_benchmarks {
    my ($config) = @_;

    $config->{'formats'} = {} if !exists $config->{'formats'};

    my $benchdir = jp($config->top, $config->benchdir);
    my %seen;
    my $dh = new IO::Dir $benchdir;
    if (!defined $dh) {
        Log(0, "\nCan't open benchmark directory '$benchdir': $!\n");
        do_exit(1);
    }
    while (defined(my $suitename = $dh->read)) {
        next if $suitename =~ /^\./;
        Log(90, "Reading suite directory for '$suitename', '$benchdir'\n");
        my $suitestarttime = Time::HiRes::time;
        my $dir     = jp($benchdir, $suitename);
        my $basedir = $suitename;
        next if !-d $dir;
        my $dh2 = new IO::Dir $dir;
        while (defined(my $bmname = $dh2->read)) {
            next if $bmname =~ /^\./;
            Log(90, "  Reading benchmark directory for '$dir', '$benchdir', '$bmname'\n");
            my $bmstarttime = Time::HiRes::time;
            my $topdir = jp ($dir, $bmname);
            if ($bmname =~ m/^(\d{3})\.(\S+)$/) {
                my ($num, $name) = ($1, $2);
                if ($seen{$name} && $num < 990) {
                    # 990 and up are for "system" benchmarks like specrand
                    # which must be run but aren't reported.
                    Log(0, "\n'$name' appeared as a benchmark name more than once, ignoring\n");
                    next;
                }
                my $specdir = jp($topdir, 'Spec');
                my $pm = jp($specdir, 'object.pm');
                my $flags_file = jp($specdir, 'flags.xml');
                if ($name =~ m/\./) {
                    Log(0, "\nBenchmark name '$name' may not contain a '.'; ignoring\n");
                } elsif (! -d $specdir) {
                    Log(99, "ERROR: No 'Spec' directory for $bmname under $topdir\n");
                } elsif (! -r $pm) {
                    Log(99, "ERROR: No 'object.pm' file for $bmname under $specdir\n");
                } elsif (! -r $flags_file) {
                    Log(99, "ERROR: No 'flags.xml' file for $bmname under $specdir\n");
                } else {
                    my $objectstarttime = Time::HiRes::time;
                    # Get the version
                    my $tmpver = (::read_file(jp($topdir, 'version.txt')))[0];
                    # Get rid of whitespace
                    $tmpver =~ tr/\012\015 \011//d;
                    if (!defined($tmpver) or $tmpver eq '') {
                        Log(0, "\nError instantiating $num.$name: version.txt file is missing\n");
                        next;
                    } elsif ($tmpver !~ /^\d+\.\d+\.\d+(?:\s*\(\S{7,10}\))?$/) {
                        Log(0, "\nError instantiating $num.$name: version.txt file contains nonsense; got '$tmpver'\n");
                        next;
                    }
                    $tmpver = normalize_version($tmpver);

                    # This doesn't get the special Safe treatment because if
                    # you can change an object.pm file, you can just as easily
                    # change the tools directly.
                    if ($::check_integrity and !::check_files(\%::file_sums, $pm)) {
                        Log(0, "\nERROR: The benchmark object file (object.pm in $specdir) is corrupt!\n");
                        next;
                    }
                    eval "
                        package Spec::Benchmark::${name}${num};
                        \@Spec::Benchmark::${name}${num}::ISA     = (qw(Spec::Benchmark));
                        \$Spec::Benchmark::${name}${num}::version = q($tmpver);
                        require '$pm';
                    ";
                    Log(90, sprintf("    Evaluated $pm in %8.9fs\n", Time::HiRes::time - $objectstarttime));
                    if ($@) {
                        Log(0, "\nError requiring '$pm': $@\n");
                        next;
                    }
                    $objectstarttime = Time::HiRes::time;
                    my $class="Spec::Benchmark::${name}${num}";
                    if (!validate_benchlang($class, $bmname)) {
                        Log(0, "\nError validating benchmark languages for $bmname\n\n");
                        next;
                    }
                    if (!$class->can('new')) {
                        Log(0, "\n\nNo 'new' for class '$class' in '$pm'\n");
                        next;
                    }
                    my $obj = $class->new($topdir, $config, $num, $name);
                    if (!defined($obj) || !ref($obj)) {
                        Log(0, "\n\nError initializing '$pm'\n");
                        next;
                    }
                    Log(90, sprintf("    Instantiated $class in %8.9fs\n", Time::HiRes::time - $objectstarttime));
                    $objectstarttime = Time::HiRes::time;
                    locate_srcalts($obj);
                    Log(90, sprintf("    Finding src.alts took %8.9fs\n", Time::HiRes::time - $objectstarttime));
                    $seen{$name}++;
                    $config->{'benchmarks'}{$bmname} = $obj;
                    Log(90, sprintf("  Setting up $name took %8.9fs\n\n", Time::HiRes::time - $bmstarttime));
                }
            } elsif ($bmname =~ /^([^\/\\:;]+)\.bset$/o) {
                my $name = $1;
                my $s = new_safe_compartment('bset_setup_'.$name, 1);
                $s->rdo($topdir);
                if ($@) {
                    Log(0, "\nError requiring benchset file '$topdir': $@\n");
                    next;
                }
                # Now make the new object.  This ensures only variables we
                # expect to see end up in the benchset object and that no
                # extra code comes along.
                eval "
                    package Spec::Benchset::${name};
                    \@Spec::Benchset::${name}::ISA              = (qw(Spec::Benchset));
                    \$Spec::Benchset::${name}::metric           = \${\$s->varglob('metric')};
                    \$Spec::Benchset::${name}::name             = \${\$s->varglob('name')};
                    \$Spec::Benchset::${name}::no_output        = \${\$s->varglob('no_output')};
                    \$Spec::Benchset::${name}::output           = \${\$s->varglob('output')};
                    \$Spec::Benchset::${name}::rate_multiplier  = \${\$s->varglob('rate_multiplier')};
                    \$Spec::Benchset::${name}::ref              = \${\$s->varglob('ref')};
                    \$Spec::Benchset::${name}::speed_multiplier = \${\$s->varglob('speed_multiplier')};
                    \$Spec::Benchset::${name}::test             = \${\$s->varglob('test')};
                    \$Spec::Benchset::${name}::train            = \${\$s->varglob('train')};
                    \$Spec::Benchset::${name}::unitbase         = \${\$s->varglob('unitbase')};
                    \$Spec::Benchset::${name}::metricbase       = \${\$s->varglob('metricbase')};
                    \@Spec::Benchset::${name}::benchmarks       = \@{\$s->varglob('benchmarks')};

                ";
                if ($@) {
                    Log(0, "\nError creating benchset object from '$topdir': $@\n");
                    next;
                }
                my $class="Spec::Benchset::${name}";
                if (!$class->can('new')) {
                    Log(0, "\nNo 'new' for class '$class' in '$topdir'\n");
                    next;
                }
                my $obj = $class->new($config);
                if (!defined($obj) || !ref($obj)) {
                    Log(0, "\nError initializing '$topdir'\n");
                    next;
                }
                $config->{'benchsets'}{$obj->name} = $obj;
            } elsif ($suitename =~ m/^(\d{3})\.(\S+).tar/i) {
                next;
            }
        }
        Log(90, sprintf("Setting up suite took %8.9fs\n", Time::HiRes::time - $suitestarttime));
    }
    my $error = 0;
    for my $set (keys %{$config->{'benchsets'}}) {
        my $obj = $config->{'benchsets'}{$set};
        my $ref = {};
        $config->{'benchsets'}{$set}{'benchmarks'} = $ref;
        my @benchmarks = @{$obj->{'benchmarklist'}};
        for my $bench (@benchmarks) {
            if (!exists $config->{'benchmarks'}{$bench}) {
                Log(0, "\nBenchmark Set '$set' calls for nonexistent benchmark '$bench'\n");
                $obj->{'valid'} = 'X';
                $error++;
            } else {
                $ref->{$bench} = $config->{'benchmarks'}{$bench};
            }
        }
    }
    ::do_exit(1) if $error;
    $config->{'setobjs'} = [ map {$config->{'benchsets'}{$_}} keys %{$config->{'benchsets'}} ];
}

# Validate that the kinds of source files found match the list of benchmark languages, and vice-versa.
# This is done by looking at file extensions like animals (or make(1)).
sub validate_benchlang {
    my ($class, $bmname) = @_;
    my $rc = 1;

    no strict 'refs';   # We're looking at package variables where the package name is itself variable
    my $benchlang = ${"${class}::benchlang"};
    my %lang_seen = map { $_ => 0 } split(/,/, $benchlang);
    my @sources = @{"${class}::sources"};
    my %sourcesmap = %{"${class}::sources"};
    if (@sources and %sourcesmap == 0) {
        $sourcesmap{${"${class}::exename"}} = \@sources;
    }

    # For cloned benchmarks with no sources list, just return success;
    # benchlang validation will be done for the source benchmark
    return $rc if %sourcesmap == 0;

    foreach my $exe (sort keys %sourcesmap) {
        my @exelangs = sources_to_language(@{$sourcesmap{$exe}});
        # Mark the listed languages as in use
        foreach my $lang (@exelangs) {
            $lang_seen{$lang}++ if exists($lang_seen{$lang});
        }

        if (all { exists($lang_seen{$_}) } @exelangs) {
            # This executable uses only languages listed in $benchlang, so it's okay.
            Log(90, "\nNotice: $bmname: $exe uses only languages (".join(', ', @exelangs).") listed in benchlang ($benchlang)\n");
        } else {
            Log(0, "\n\nError: $exe from $bmname contains sources in languages (".
                join(', ', grep { !exists($lang_seen{$_}) } @exelangs).
                ") NOT listed in benchlang ($benchlang)\n");
            $rc = 0;
        }
    }

    # Now check that all languages in $benchlang were used
    my @unused = grep { $lang_seen{$_} == 0 } sort keys %lang_seen;
    if (@unused) {
        Log(0, "\n\nError: $bmname lists languages (".join(', ', @unused).") with no corresponding source files.\n");
        $rc = 0;
    }

    return $rc;
}

# Given a list of source files, return the list of languages that correspond to them,
# and complain if there are any unknown.
sub sources_to_language {
    my (@sources) = @_;

    # This mapping is extracted manually from the implicit rules in Makefile.defaults
    my %extlang = (
        'c'   => 'C',
        'cc'  => 'CXX',
        'C'   => 'CXX',
        'cpp' => 'CXX',
        'cxx' => 'CXX',
        'f'   => 'F',
        'f90' => 'F',
        'f95' => 'F',
        'F'   => 'F',
        'F90' => 'F',
        'F95' => 'F',
    );

    # Convert the list of files to just extensions, and then convert that list
    # to languages as they're expressed in $benchlang.
    my @srclangs = distinct map { $extlang{$_} } map { /\.([^.]+)$/ && $1 || '' } @sources;
    if (grep { !defined } @srclangs) {
        Log(0, "ERROR: one or more sources in the following list use extensions with unknown language mapping.  ".
            "Please adjust sources list in the benchmark object.pm or sources_to_language() in ".(caller())[1]."\n");
    }

    return sort @srclangs;
}

sub locate_srcalts {
    my ($bmobj) = @_;

    my $srcaltdir = jp($bmobj->{'path'}, 'src', 'src.alt');
    my $dh = new IO::Dir $srcaltdir;
    return unless defined($dh);
    while (defined(my $dir = $dh->read)) {
        #print  "Reading '$dir', '$srcaltdir'\n";
        next if $dir eq '.' || $dir eq '..';
        next if $dir =~ /^\./o;         # src.alt names may not begin with '.'
        my $path     = jp($srcaltdir, $dir);
        my $basedir = $dir;
        my $name     = $bmobj->{'name'}.$bmobj->{'num'}.$dir;
        next if ! -d $path;
        my $pm = jp($path, 'srcalt.pm');
        if (! -r $pm) {
            Log(0, "\nERROR: src.alt '$dir' for $bmobj->{'num'}.$bmobj->{'name'} contains no control file! Skipping...\n");
            next;
        }
        my $s = new_safe_compartment('srcalt_'.$name, 1);
        my $infoptr = $s->rdo($pm);
        if ($@) {
            Log(0, "\nERROR: src.alt '$dir' for $bmobj->{'num'}.$bmobj->{'name'} has a bad control file: $@\n");
            next;
        }
        foreach my $member (qw(name forbench usewith filehashes diffhashes diffs)) {
            if (!exists $infoptr->{$member}) {
                Log(0, "\nERROR: src.alt '$dir' for $bmobj->{'num'}.$bmobj->{'name'} has an incomplete control file; ignoring\n");
                next;
            }
        }
        if (ref($infoptr->{'filehashes'}) ne 'HASH') {
            Log(0, "\nERROR: src.alt '$dir' for $bmobj->{'num'}.$bmobj->{'name'} has corrupt file sums; ignoring\n");
            next;
        }
        if ($infoptr->{'forbench'} ne $bmobj->{'num'}.'.'.$bmobj->{'name'}) {
            Log(0, "\nERROR: src.alt '$dir' for $infoptr->{'forbench'} is in $bmobj->{'num'}.$bmobj->{'name'}\'s directory; ignoring\n");
            next;
        }
        my ($min, $max);
        if (ref($infoptr->{'usewith'}) eq 'ARRAY') {
            # It's a range
            ($min, $max) = @{$infoptr->{'usewith'}};
        } else {
            ($min, $max) = ($infoptr->{'usewith'}, $infoptr->{'usewith'});
        }

        if (normalize_version($::suite_version, 1) >= normalize_version($min, 1)
                and normalize_version($::suite_version, 1) <= normalize_version($max, 1)) {
            $infoptr->{'path'} = $path;
            # Fix up the paths in the filehashes struct
            foreach my $filepath (keys %{$infoptr->{'filehashes'}}) {
                next unless ($filepath =~ /^benchspec/);
                $infoptr->{'filehashes'}->{jp($ENV{'SPEC'}, $filepath)} =
                $infoptr->{'filehashes'}->{$filepath};
                # Neaten up
                delete $infoptr->{'filehashes'}->{$filepath};
            }
            $bmobj->{'srcalts'}->{$infoptr->{'name'}} = $infoptr;
            Log(10, "\nFound src.alt '$infoptr->{'name'}' for $bmobj->{'num'}.$bmobj->{'name'}\n");
        } else {
            Log(0, "\nERROR: src.alt '$infoptr->{'name'}' for $bmobj->{'num'}.$bmobj->{'name'} is not useable with this version of ${main::suite}!\n");
        }
    }
}

1;

# Editor settings: (please leave this at the end of the file)
# vim: set filetype=perl syntax=perl shiftwidth=4 tabstop=8 expandtab nosmarttab:

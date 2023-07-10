$benchnum  = '788';
$benchname = 'prime_r';
$exename   = 'prime_r';
$benchlang = 'CXX';
@base_exe  = ($exename);

$calctol = 0;           # No tolerance will ever be set, so don't waste time
$nansupport = 0;        # No NaNs in output, so stringwise-equal is a good
                        # initial check for equality

%workloads = (
    'refspeed' => [ 'refrate' ],
);

@sources = (qw(prime.cpp));

sub invoke {
    my ($me) = @_;
    my (@rc);

    my @temp = main::read_file('control');
    my $exe = $me->exe_file;

    for (@temp) {
        my ($limit) = split;
        next if m/^\s*#/ || m/^\s*$/;
        push @rc, {
            'command' => $exe,
            'args'    => [ $limit ],
            'output'  => "prime_numbers.out",
            'error'   => "prime_numbers.err",
        };
    }
    return @rc;
}

1;

# Editor settings: (please leave this at the end of the file)
# vim: set filetype=perl syntax=perl shiftwidth=4 tabstop=8 expandtab nosmarttab:

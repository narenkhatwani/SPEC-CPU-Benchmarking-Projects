#
# os_common.pl
#
# Copyright 1999-2019 Standard Performance Evaluation Corporation
#

use strict;
$::tools_versions{'os_common.pl'} = 0;

sub initialize_os {
    my ($config) = @_;
    if ($::from_runcpu == 0 and istrue($config->setprocgroup)) {
        eval 'setpgrp';
        ::Log(0, "NOTICE: setpgrp failed: $@\n") if $@ ne '' and $@ !~ /unimplemented/i;
    }
}

1;

# Editor settings: (please leave this at the end of the file)
# vim: set filetype=perl syntax=perl shiftwidth=4 tabstop=8 expandtab nosmarttab:

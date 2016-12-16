#!/usr/bin/perl

use SNMP;
use Config::IniFiles;
use v5.10;
use Data::Dumper;

my $config_file = Config::IniFiles->new( -file => '../machines_to_test.ini' );

my @ips_to_test = $config_file->Sections;

for my $current_ip ( @ips_to_test ) {
    say( 'i am about to try IP: ' . $current_ip );
    my $session = new SNMP::Session( DestHost => $current_ip, Community => 'ntwLABro1' );
    say( 'and my error on the seeesion is: ' . $session->{ErrorNum} );

    my $value;
    my $variable_bind = new SNMP::Varbind();
    do {
        $value = $session->getnext( $variable_bind );
        say( "got me a value of: '$value'" );
        say( '      varbind value is: ' . $variable_bind->val ) ;
        say( '       varbind name is: ' . $variable_bind->val ) ;
        say( '        varbind fmt is: ' . $variable_bind->fmt ) ;
        for my $current_value ( @$variable_bind ) {
            say( "a bind var is: '$current_value'" ) ;
        }
    } until ( $session->{ErrorNum} );

}

no strict 'refs';
for ( keys %SNMP::Varbind:: ) {
    say( $_ ) if exists &{"SNMP::Varbind::$_"};
}

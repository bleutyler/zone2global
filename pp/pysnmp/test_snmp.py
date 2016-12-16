"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.snmplabs.com:161
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,

Functionally similar to:

| $ snmpget -v1 -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0

[10.236.10.24]
oids=
[10.236.10.30] 
oids=
[10.236.10.67] 
oids=
"""
from pysnmp.hlapi import *
import configparser

import re
import sys

ini_file = '../machines_to_test.ini'
ini_configuration = configparser.ConfigParser()
ini_configuration.read( ini_file )

#test_machine_ips = ( '10.236.10.24', '10.236.10.30', '10.236.10.67' )
test_machine_ips = ini_configuration.sections()

def main():
    for ip in test_machine_ips:
        print( '\n*** Testing the IP: ' + ip + ' ***' )

        next_oid = get_sysDescr_oid( ip )
        print ( ' Will do an SNMP walk starting at OID: ' + str( next_oid ) )

        while next_oid != None:
            print( '\n**** LOOP START at OID: ' + str( next_oid  ) + ' ****' )
            errorIndication, errorStatus, errorIndex, varBinds = next(
                nextCmd(SnmpEngine(),
                CommunityData('ntwLABro1', mpModel=0),
                UdpTransportTarget(( ip, 161 )),
                ContextData(),
                ObjectType(ObjectIdentity( str( next_oid ) )))
            )

            if errorIndication:
                print( 'main error 1')
                print(errorIndication)
            elif errorStatus:
                print( 'main error 2')
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                for varBind in varBinds:
                    last_oid = next_oid
                    this_oid = varBind[0]
                    next_oid = varBind[1]
                    print( 'pretty print::' )
                    print(' = '.join([x.prettyPrint() for x in varBind]))
                    print( 'regular print:::' )
                    count_variable = 0
                    for x in varBind:
                        count_variable = count_variable + 1 
                        print( str( count_variable ) + ' ::: ' + str( x ) )

                    oid_regular_expression_pattern = re.compile( '\d\.\d' )
                    if not oid_regular_expression_pattern.search( str(next_oid) ):
                        if oid_regular_expression_pattern.search( str(this_oid) ):
                            if this_oid != last_oid:
                                print( 'yeah using a different return value' )
                                next_oid = this_oid
                            else:
                                print( 'will not reuse OIDs' )
                                sys.exit(1)
                        else:
                            print( 'no OID of any sort was retunred!' )
                            sys.exit(1)

                    print( 'okay so the next oid is: ' + str( next_oid ))


def get_sysDescr_oid( ip : int ):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
        #nextCmd(SnmpEngine(),
               CommunityData('ntwLABro1', mpModel=0),
               UdpTransportTarget(( ip, 161 )),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        # okay so what is varBind[0] ?
        #print( 'hey the varBind is: ' + str(varBinds) )
        for varBind in varBinds:
            oid         = varBind[0]
            oid_values  = varBind[1]
            return oid

if ( __name__ == '__main__' ):
    main()

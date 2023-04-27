import json
import os
from influxdb import InfluxDBClient
import influxdb

#os.chdi("C:\\users\\u26928\\Desktop\\SNMP-FLUS-PY_GRA")
os.chdir("/AUTOMATION/CPU-MEM")

with open('devices4collector.json') as dev_file:
    devices = json.load(dev_file)

for device in devices:

    def snmpget(oid):
        from pysnmp.entity.rfc3413.oneliner import cmdgen
    
        global SNMP_HOST
        global SNMP_PORT
        global SNMP_COMMUNITY

        SNMP_HOST = device['ip']
        SNMP_PORT = 161
        SNMP_COMMUNITY = 'allyours'
    
        cmdGen = cmdgen.CommandGenerator()

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(SNMP_COMMUNITY),
            cmdgen.UdpTransportTarget((SNMP_HOST, SNMP_PORT)),
            oid
        )
    
        # Check for errors and print out results
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                for name, val in varBinds:
                    #print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                    return val

    cpu1 = snmpget(device['cpu1'])
    cpu2 = snmpget(device['cpu2'])
    mem1 = snmpget(device['mem1'])
    mem2 = snmpget(device['mem2'])
    temp1 = snmpget(device['temp1'])
    temp2 = snmpget(device['temp2'])
    hostname = snmpget(device['oidhostname'])

    print(SNMP_HOST)
    print(hostname)
    print(cpu1)
    print(mem1)
    print(device['oidc'])
    #v = 2000
    #vv = 6000
    #hostname = "TRV-TATA"
    #print(v)

    try:
        client = InfluxDBClient(host='localhost',
                                port=8086)
                                #username='admin',
                                #password='password')
        line = "cpumem,hostname=" + str(hostname) + " cpu1=" + str(cpu1) + "," + "cpu2=" + str(cpu2) + "," + "mem1=" + str(mem1) + "," + "mem2=" + str(mem2) + "," + "temp1=" + str(temp1) + "," + "temp2=" + str(temp2)
        #line = "cpumem,hostname=" + str(hostname) + "," + " cpu=" + str(cpu) +"," + "mem=" + str(mem)
        #line = "Bandwidth,hostname=" + str(hostname) + "," + "interface=" + str(ifname) + " download=" + str(download) + "," + "upload=" + str(upload)
        #line = line1 + line2

        #print(vv)
        client.write([line], {'db': 'CPUMEM'}, 204, 'line')
        client.close()
    except influxdb.exceptions.InfluxDBClientError:
        print("No Data fetched")

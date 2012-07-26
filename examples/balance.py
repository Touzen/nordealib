#!/usr/bin/python
import nordea
from sys import argv

conn = nordea.Connection(argv[1], argv[2])

print 'ACCOUNT BALANCE\n%s'%'='*10
for acc, balance in conn.balance.items():
    if acc != 'total':
        print "%s:\t%s"%(acc, balance)
print 'TOTAL:\t%s'%acc['total']

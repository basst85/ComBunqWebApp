import csv
import json
import os
import sys
import requests
from django.core.exceptions import ObjectDoesNotExist
curdir = os.path.abspath(os.curdir)
print curdir
sys.path.insert(0, curdir)
from Manager.models import catagories
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    """docstring for Command."""
    def handle(self, *args,**options):
        print 'This scrpit will add new catagories and filters to the database\n'
        validator()
    

def getJSON():
    
    catFiltersCSV = open('Manager/management/DatabaseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = next(reader)
    catFiltersJSON = [{key:val for key,val in zip(keys,prop)} for prop in reader]
    # print json.dumps(catFiltersJSON,sort_keys=True,indent=2)
    # getHeaders()
    return catFiltersJSON
    

def getHeaders():
    catFiltersCSV = open('Manager/management/DatabaseInput/ComBunqWeb-category-filter.csv')
    reader = csv.reader(catFiltersCSV, delimiter=',', quotechar='"')
    keys = reader.next()
    # print keys
    return keys

# getJSON()

def validator():
    obj = getJSON()
    url = 'https://openiban.com/validate/'
    
    # print json.dumps(obj,sort_keys=True,indent = 2 )
    for x in range(len(getJSON())):
        for y in getHeaders():
            try:
                obj[x][y]
                # print y,':',obj[x][y]
                check = json.loads(requests.get("".join([url,obj[x][y]])).content)
                if check['valid']:
                    print '\nvalid IBAN:',obj[x][y],'-->',y
                    obj[x][y] = newCatInfo(y,obj[x][y])
                    isInDatabase(obj[x][y])
                    
                else:
                    print '\n\nunvalid IBAN:', obj[x][y],'\n\n'
                # print type(list(valid))
            except KeyError:
                continue


class newCatInfo(object):
    """docstring for newCatInfo."""
    def __init__(self, catName,Iban):
        super(newCatInfo, self).__init__()
        self.catName = catName
        self.Iban = Iban
    
    def getIban(self):
        return self.Iban
    
    def __str__(self):
        return self.catName


def isInDatabase(catInfo):
    cat = catagories.objects
    catName = str(catInfo)
    iban = catInfo.getIban()
    try:
        cat.get(Naam = catName)
    
    except ObjectDoesNotExist:
        print catName, 'is not in database'
        # NOTE: create catagory
        p = cat.create(Naam = catName, Rekening = [iban])
        print catName, 'Has been stored in the database with', iban
    else:
        editCat = cat.get(Naam = catName)
        ibanList = editCat.Rekening
        print catName,'is in db, the following ibans are stored:\n\n', ibanList,'\n\n'
        if iban in ibanList:
            print iban,'is already in the list\n'
        else:
            ibanList.append(iban)
            editCat.save()
            print 'Updated list for',catName,'with -->',iban,'\nlist is now -->', ibanList,'\n'
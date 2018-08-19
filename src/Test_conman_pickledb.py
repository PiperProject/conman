#!/usr/bin/env python
  
'''
Test_conman_pickldb.py
'''

#############
#  IMPORTS  #
#############
# standard python packages
import logging
import os
import pickledb 
import sys 
import time 
import unittest

# custom libs
import ConMan


##########################
#  TEST CONMAN PICKLEDB  #
##########################
class Test_conman_pickledb( unittest.TestCase ) :

  logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.DEBUG )
  #logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.INFO )

  ###############
  #  EXAMPLE 1  #
  ###############
  #@unittest.skip( "example 1." )
  def test_example_1( self ) :

    test_id    = "test_example_1"
    NOSQL_TYPE = "pickledb"
    DBNAME     = "../data/" + test_id + ".db"

    # --------------------------------------------------------------- #
    # create db instance

    logging.info( "  " + test_id + ": initializing pickledb instance." )

    if os.path.isfile( DBNAME ) :
      os.remove( DBNAME )

    dbInst = pickledb.load( DBNAME, False )

    # --------------------------------------------------------------- #
    # define cons

    c = ConMan.ConMan( "pickledb", dbInst, "base_case" )
    #c.set_cons( "['pk','author'] WHEN ['title','pubYear']" )
    #c.set_cons( "['fk','author','authorid'] DELETE ON CASCADE" )

    c.set_cons( "['pk','isbn']" )
    c.set_cons( "['fk','aid'] REF ['authorid_list']" )

    c.set_cons( "['dm','author','str']" )
    c.set_cons( "['dm','title','str']" )
    c.set_cons( "['dm','isbn','int']" )
    c.set_cons( "['dm','pubYear','int']" )
    c.set_cons( "['dm','numCopies','int']" )
    c.set_cons( "['dm','categories','list']" )
    c.set_cons( "['dm','cost(Dollars)','float']" )
    c.set_cons( "['dm','authorid_list','list']" )
    c.set_cons( "['dm','aid','int']" )

    # --------------------------------------------------------------- #
    # insert data

    book1 = { "author"        : "Elsa Menzel",
              "aid"           : 10, \
              "title"         : "A Martial Arts Primer", \
              "isbn"          : 0, \
              "pubYear"       : 2018, \
              "numCopies"     : 0, \
              "categories"    : ["fantasy","action","lgbt"], \
              "cost(Dollars)" : 10.00 }
    book2 = { "author"        : "Anna Summers", \
              "aid"           : 11, \
              "title"         : "The Rising", \
              "isbn"          : 1, \
              "pubYear"       : 2017, \
              "numCopies"     : 0, \
              "categories"    : ["fantasy"], \
              "cost(Dollars)" : 9.99 }
    authorid_list = [ 10,11 ]
#    book3 = { "author" : "Kat Green", \
#              "title" : "Frozen Space", \
#              "pubYear" : 2016, \
#              "numCopies" : 0, \
#              "categories" : ["fantasy", "scifi"], \
#              "cost(Dollars)" : 0 }

    c.insert( "authorid_list", authorid_list )
    c.insert( "bid1", book1 )
    c.insert( "bid2", book2 )
#    c.insert( "bid3", book3 )

    logging.debug( "  TEST EXAMPLE 1 : data dump :" )
    for k in dbInst.getall() :
      logging.debug( "key = " + k + ", val = " + str( dbInst.get( k ) ) )

    self.assertEqual( 0, 0 )

    # ---------------------------------------------------- #
    # close pickle db instance

    dbInst.deldb()


#########################
#  THREAD OF EXECUTION  #
#########################
if __name__ == "__main__" :

  unittest.main()

#########
#  EOF  #
#########

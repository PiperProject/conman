#!/usr/bin/env python
  
'''
Test_conman_pickldb.py
'''

#############
#  IMPORTS  #
#############
# standard python packages
import logging, os, pickledb, sys, time, unittest

import ConMan


##########################
#  TEST CONMAN PICKLEDB  #
##########################
class Test_conman_pickledb( unittest.TestCase ) :

  logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.DEBUG )
  #logging.basicConfig( format='%(levelname)s:%(message)s', level=logging.INFO )

  ##################
  #  #
  ##################
  @unittest.skip( "stuff" )
  def test_( self ) :

    test_id    = "test_avg_pickledb"
    NOSQL_TYPE = "pickledb"


#########
#  EOF  #
#########

#! /usr/bin/env python

##########################################################################
# ConMan usage notes:
#
#
##########################################################################

# -------------------------------------- #
import logging, os, pprint, pydot, rdflib, string, sys, time

# import sibling packages HERE!!!

# adapters path
adaptersPath  = os.path.abspath( __file__ + "/../../../../adapters" )
if not adaptersPath in sys.path :
  sys.path.append( adaptersPath )
import Adapter

# settings dir
settingsPath  = os.path.abspath( __file__ + "/../../core" )
if not settingsPath in sys.path :
  sys.path.append( settingsPath )
import settings

# -------------------------------------- #


class ConMan( object ) :
  """ConMan : A General constraint management tool for NoSQL systems.

  Issue queries to an underlying database using the Query class.
  When invoked, ConMan captures queries issued to the Query class
  to analyze inputs and deletion results for data integrity violations.
  Queries violating data integrity return an error.
  Users educate ConMan on data integrity definitions 
  for three different types of constraints:
    Primary Key
    Foreign Key
    Data Type
  Given NoSQL systems often manifest in the absense of a well-defined
  schema, key constraints operate over the looser notion of identifying 
  attributes of stored data.
  """

  ################
  #  ATTRIBUTES  #
  ################
  nosql_type    = None   # the type of nosql database under consideration

  ##########
  #  INIT  #
  ##########
  def __init__( self, nosql_type ) :
    """Constructor"""

    # save nosql db type
    self.nosql_type = nosql_type

    logging.debug( "  ...instantiated ConMan instance." )


  #  


#########################
#  THREAD OF EXECUTION  #
#########################
if __name__ == "__main__" :
  c = ConMan( "pickledb" )


#########
#  EOF  #
#########

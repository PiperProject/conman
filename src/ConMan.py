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


  ################
  #  ATTRIBUTES  #
  ################
  nosql_type    = None   # the type of nosql database under consideration
  ontology      = None   # an rdflib Graph object instance
  MONGOSAVEPATH = None


  ##########
  #  INIT  #
  ##########
  def __init__( self, nosql_type ) :

    # save nosql db type
    self.nosql_type = nosql_type

    # instantiate the ontology graph
    self.ontology  = rdflib.Graph()

    logging.debug( "  ...instantiated ConMan instance." )




#########
#  EOF  #
#########

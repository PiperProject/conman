#! /usr/bin/env python

##########################################################################
# ConMan usage notes:
#
#
##########################################################################

# -------------------------------------- #
import ast
import logging
import os
import string
import sys 
import time 

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
    Domain
  Given NoSQL systems often manifest in the absence of a well-defined
  schema, key constraints operate over the looser notion of identifying 
  attributes of stored data.
  """

  ################
  #  ATTRIBUTES  #
  ################
  nosql_type           = None # the type of nosql database under consideration
  cursor               = None
  OPTIMIZATION_PATTERN = None
  pk_cons = []
  fk_cons = []
  dm_cons = {}

  ##########
  #  INIT  #
  ##########
  def __init__( self, nosql_type, cursor, OPTIMIZATION_PATTERN ) :
    """Constructor"""

    self.nosql_type = nosql_type
    self.cursor     = cursor
    self.OPTIMIZATION_PATTERN = OPTIMIZATION_PATTERN

    logging.debug( "  ...instantiated ConMan instance." )

  ############
  #  INSERT  #
  ############
  def insert( self, key, val ) :
    '''input the insert query and check constraints before pushing
    to the database'''

    if type( val ) == list :
      self.cursor.set( key, val )

    elif self.check_pk_cons( key, val ) and \
         self.check_fk_cons( key, val ) and \
         self.check_dm_cons( key, val ) :

      print "pk = " + str( self.check_pk_cons( key, val ) )
      print "fk = " + str( self.check_fk_cons( key, val ) )
      print "dm = " + str( self.check_dm_cons( key, val ) )

      logging.debug( "  INSERT : inserting " + str(key) + ", " + str(val) )
      self.cursor.set( key, val ) # use adapters to generalize

  ##############
  #  SET CONS  #
  ##############
  def set_cons( self, input_constraint ) :
    '''input a constranint spec'''

    if "pk" in input_constraint :
      self.set_pk_cons( input_constraint )
    elif "fk" in input_constraint :
      self.set_fk_cons( input_constraint )
    elif "dm" in input_constraint :
      self.set_dm_cons( input_constraint )
    else :
      raise ValueError( "wtf???" )

  #################
  #  SET PK CONS  #
  #################
  def set_pk_cons( self, input_constraint ) :
    self.pk_cons.append( self.parse_con( input_constraint ) )

  #################
  #  SET FK CONS  #
  #################
  def set_fk_cons( self, input_constraint ) :
    self.fk_cons.append( self.parse_con( input_constraint ) )

  #################
  #  SET DM CONS  #
  #################
  def set_dm_cons( self, input_constraint ) :
    parsed_con = self.parse_con( input_constraint )

    att = parsed_con[1]
    typ = parsed_con[2]

    # TODO : error checking
    self.dm_cons[ att ] = typ 


  ###################
  #  CHECK PK CONS  #
  ###################
  def check_pk_cons( self, key, val ) :
    '''check for primary key constraint violations'''

    logging.debug( "  CHECK PK CONS : key = " + str( key ) )
    logging.debug( "  CHECK PK CONS : val = " + str( val ) + ", type = " + str( type( val ) ) )
    logging.debug( "  CHECK PK CONS : pk_cons :")
    for k in self.pk_cons :
      logging.debug( str( k ) )

    # need to make sure pk cons in key/val hold relative to 
    # existing db data
    # => need to query database in base_case or query
    #    support structures in optimized cases.

    if self.OPTIMIZATION_PATTERN.lower() == "base_case" :

      if len( self.cursor.getall() ) < 1 :
        print "here2"
        return True

      elif type( val ) == dict :

        for k1 in val :
          if self.is_pk( k1 ) :
            logging.debug( "  CHECK PK CONS : k1 = " + str( k1 ) )
            # TODO : generalize backend
            for k2 in self.cursor.getall() :
              k2_val = self.cursor.get( k2 )
              if type( k2_val ) == dict :
                logging.debug( "  CHECK PK CONS : k2 = " + str( k2_val ) )
                existing_val = self.convert_to_list( str( k2_val ) )
                logging.debug( "  CHECK PK CONS : existing_val = " + str( existing_val ) )
                for i in existing_val :
                  i = i.replace( "'", "" ).split( ":" )
                  print "i0 = " + str( i[0] )
                  print "i1 = " + str( i[1] )
                  if k1 == i[0] and str( val[ k1 ] ) == i[1] :
                    logging.debug( "  CHECK PK CONS : failed because '" + k1 + \
                                   "' == '" + str( i[0] ) + \
                                   "' and '" + str( val[ k1 ] ) + \
                                   " == '" + str( i[1] ) + "'" )
                    print "here2"
                    return False

    print "here1"
    return True

  ###########
  #  IS PK  #
  ###########
  def is_pk( self, a_str ) :
    '''check if the input string is a primary key'''

    # TODO : generalize to primary keys with multiple atts
    logging.debug( "  IS PK : a_str = " + str( a_str ) )

    for i in self.pk_cons :
      if a_str == i[1] :
        return True
    return False

  #####################
  #  CONVERT TO LIST  #
  #####################
  def convert_to_list( self, some_thing ) :
    '''convert input string into a list'''

    if some_thing.startswith( "{" ) :
      some_thing = some_thing[ 1:-1 ]

    some_thing = some_thing.translate( None, string.whitespace )
    some_thing = some_thing.split( "," )
    tmp = []

    i = 0
    while i < len( some_thing ) :
      curr = some_thing[ i ]

      if "[" in curr and not "]" in curr :
        j = i + 1
        while "[" in curr and not "]" in curr :
          curr += "," + some_thing[ j ]
          j += 1
        i = j

      tmp.append( curr )
      i += 1

    return tmp

  ###################
  #  CHECK FK CONS  #
  ###################
  def check_fk_cons( self, key, val ) :
    '''check for foreign key constraint violations'''

    logging.debug( "  CHECK FK CONS : key = " + str( key ) )
    logging.debug( "  CHECK FK CONS : val = " + str( val ) + ", type = " + str( type( val ) ) )
    logging.debug( "  CHECK FK CONS : fk_cons :")
    for k in self.fk_cons :
      logging.debug( k )

    for k in val :
      if self.is_fk( k ) :
        fk_ref = self.is_fk( k )
        if not val[k] in self.cursor.get( fk_ref[0] ) :
          logging.debug( "  CHECK FK CONS : failed on foreign key '" + str( val[k] ) + "'" )
          return False

    return True

  ###########
  #  IS FK  #
  ###########
  def is_fk( self, a_str ) :
    '''check if the input string is a foreign key'''

    # TODO : generalize to primary keys with multiple atts
    logging.debug( "  IS FK : a_str = " + str( a_str ) )

    for i in self.fk_cons :
      if a_str == i[0][1] :
        return i[2]
    return None

  ###################
  #  CHECK DM CONS  #
  ###################
  def check_dm_cons( self, key, val ) :
    '''check for domain constraint violations'''

    logging.debug( "  CHECK DM CONS : key = " + str( key ) )
    logging.debug( "  CHECK DM CONS : val = " + str( val ) + ", type = " + str( type( val ) ) )
    logging.debug( "  CHECK DM CONS : dm_cons :")
    for k in self.dm_cons :
      logging.debug( str( k ) + "," + str( self.dm_cons[k] ) )

    # first check key
    try :
      if not "<type '" + self.dm_cons[ key ] + "'>" == str( type( val ) ) :
        logging.debug( "  CHECK DM CONS : failed0" )
        return False

    # case key isn't set
    except KeyError :
      pass

    # case key type violates a dm constraint
    except ValueError :
      logging.debug( "  CHECK DM CONS : failed1" )
      return False

    # then check val
    if type( val ) == dict :
      for k in val :
        if not self.check_dm_cons( k, val[k] ) :
          logging.debug( "  CHECK DM CONS : failed2" )
          return False
      return True

    elif type( val ) == int :
      if not self.dm_cons[ key ] == "int" :
        logging.debug( "  CHECK DM CONS : failed3" )
        return False

    elif type( val ) == float :
      if not self.dm_cons[ key ] == "float" :
        logging.debug( "  CHECK DM CONS : failed4" )
        return False

    elif type( val ) == str :
      if not self.dm_cons[ key ] == "str" :
        logging.debug( "  CHECK DM CONS : failed5" )
        return False

    elif type( val ) == list :
      if not self.dm_cons[ key ] == "list" :
        logging.debug( "  CHECK DM CONS : failed6" )
        return False

    else :
      raise ValueError( "unrecognized value type for '" + str( val ) + "'" )

    return True

  ###############
  #  PARSE CON  #
  ###############
  def parse_con( self, con ) :
    '''parse the constraint'''

    con = con.translate( None, string.whitespace )

    if "REF" in con :
      con = con.split( "REF" )
      return [ ast.literal_eval( con[0] ),
               "REF",
               ast.literal_eval( con[1] ) ]

    else :
      return ast.literal_eval( con )


#########################
#  THREAD OF EXECUTION  #
#########################
if __name__ == "__main__" :
  c = ConMan( "pickledb" )


#########
#  EOF  #
#########

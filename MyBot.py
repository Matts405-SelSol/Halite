#!/usr/bin/env python3

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants

import random
import logging
#The bot uses the console to communicate with the server.
#Do not print anything or it will crash. Use logging('message') to save to log file
logging.basicConfig(filename='bot.log', level=logging.DEBUG)
log = logging


#Team created function
def compass_check(x, y):
    game_map = game.game_map
    map_cells = game_map._cells
    north = map_cells[y+1][x]
    north = north.halite_amount
    south = map_cells[y-1][x]
    south = south.halite_amount
    east = map_cells[y][x+1]
    east = east.halite_amount
    west = map_cells[y][x-1]
    west = west.halite_amount
    if north > south:
        direction = ['n', north]
    else:
        direction = ['s', south]
    if east > west:
        direction1 = ['e', east]
    else:
        direction1 = ['w', west]
    if direction[1] > direction1[1]:
        log.info(direction)
        return direction[0]
    else:
        log.info(direction1)
        return direction1[0]

def deposit_cargo(shipyard,ship):
    ship_x = ship.position.x
    ship_y = ship.position.y
    shipyard_x = shipyard.position.x
    shipyard_y = shipyard.position.y

    if shipyard_x > ship_x:
        return 'e'
    elif shipyard_x < ship_x:
        return 'w'
    elif shipyard_y > ship_y:
        return 'n'
    elif shipyard_y < ship_y:
        return 's'
    else:
        return "home sweet gnome"


# This game object contains the initial game state.
game = hlt.Game()
# Respond with your name.
game.ready("Legion")

while True:
    # Get the latest game state.
    game.update_frame()
    compass_check(7,8)
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    # A command queue holds all the commands you will run this turn.
    command_queue = []
    logging.debug('queue')
    logging.debug(command_queue)

    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.

        log.debug(ship.halite_amount)
        if ship.halite_amount > 900:
            command_queue.append(ship.move(deposit_cargo(me.shipyard,ship)))

        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(compass_check(ship.position.x, ship.position.y)))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if game.turn_number <= 1 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

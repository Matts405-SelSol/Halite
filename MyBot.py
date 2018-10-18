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
    map_cell_north = map_cells[y+1][x]
    map_cell_south = map_cells[y-1][x]
    map_cell_east = map_cells[y][x+1]
    map_cell_west = map_cells[y][x-1]
    log.debug(map_cell_south.halite)


#Team created functions
def deposit_cargo(ship,shipyard):
    ship_x = ship.position.x
    ship_y = ship.position.y
    shipyard_x = shipyard.position.x
    shipyard_y = shipyard.position.y

    if shipyard_x > ship_x:
        return 'east'
    elif shipyard_x < ship_x:
        return 'west'
    elif shipyard_y > ship_y:
        return 'north'
    elif shipyard_y < ship_y:
        return 'south'
    else:
        return "home sweet home"



# This game object contains the initial game state.
game = hlt.Game()
# Respond with your name.
game.ready("Legion")

while True:
    # Get the latest game state.
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    # A command queue holds all the commands you will run this turn.
    command_queue = []

    for ship in me.get_ships():
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        deposit_cargo(me.shipyard,ship)
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            command_queue.append(
                ship.move(random.choice(["n", "s", "e", "w"])))
        else:
            command_queue.append(ship.stay_still())

    # If you're on the first turn and have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though.
    if game.turn_number <= 1 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)

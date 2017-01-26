from Pirates import *

class count_camper:
	camper_turns = 0
def do_turn(game):
    """
    :type game: PirateGame
    """
    handle_drones(game)

    behaviors = pirate_behaviors()

    my_pirates = game.get_my_living_pirates()

    # camper
    # terrorist
    # dog
    # dog
    # dog

    if len(my_pirates) > 0 and len(game.get_enemy_living_drones()) > 0:
        closest = get_closest_pirate(my_pirates, game.get_enemy_cities()[0])
        behaviors.camper(game, closest, game.get_enemy_cities()[0], 10)
        my_pirates.remove(closest)

    if len(my_pirates) > 0:
        closest = get_closest_pirate(my_pirates, game.get_my_cities()[0])
        behaviors.terrorist(game, closest)
        my_pirates.remove(closest)

    for pirate in my_pirates:
        behaviors.dog(game, pirate)

def get_closest_to_object(locations_list, map_object):

    ret = locations_list[0]

    for location in locations_list:
        if map_object.distance(location) < map_object.distance(ret):
            ret = location

    return ret

def get_closest_pirate(pirates, map_object):

    ret = pirates[0]

    for pirate in pirates:
        if pirate.distance(map_object) < ret.distance(map_object):
            ret = pirate

    return ret

def get_all_locations(game, map_objects_list):

    locations = []

    for object in map_objects_list:
        locations.append(object.location)

    return locations

def get_enemies_in_range(game, location, range):

    enemy_aircrafts = game.get_enemy_living_aircrafts()

    if len(enemy_aircrafts) == 0:
        return []

    else:

        enemies_in_range = []

        for aircraft in enemy_aircrafts:

            if location.distance(aircraft) < range:
                enemies_in_range.append(aircraft)

    return enemies_in_range
    
def get_enemy_drones_in_range(game, location, range):

    enemy_aircrafts = game.get_enemy_living_drones()

    if len(enemy_aircrafts) == 0:
        return []

    else:

        enemies_in_range = []

        for aircraft in enemy_aircrafts:

            if location.distance(aircraft) < range:
                enemies_in_range.append(aircraft)

    return enemies_in_range

def try_attack(game, pirate):
    for i in game.get_enemy_living_aircrafts():
        if pirate.in_attack_range(i):
            game.attack(pirate, i)
            return True
    return False

def try_attack_drones(game, pirate):
    for drone in game.get_enemy_living_drones():
        if pirate.in_attack_range(drone):
            game.attack(pirate, drone)
            return True
    return False

def try_attack_pirates(game, pirate):
    for enemy_pirate in game.get_enemy_living_pirates():
        if pirate.in_attack_range(enemy_pirate):
            game.attack(pirate, enemy_pirate)
            return True
    return False
	
def handle_drones(game):
    for drone in game.get_my_living_drones():
        location = drone.get_location()

        loc_row, loc_col = location.row, location.col

        city_location = game.get_my_cities()[0].location

        city_row, city_col = city_location.row, city_location.col
        if (loc_row == 15 and (city_col > 25 and loc_col > 30 and loc_col < city_col) or (
                            city_col < 25 and loc_col < 15 and loc_col > city_col)):
            sail_to = Location(loc_row, city_col)
        else:
            if loc_row > city_row:

                if loc_row < game.get_row_count() - 1 and loc_col is not city_col:
                    sail_to = Location(game.get_row_count() - 1, loc_col)

                elif loc_row == game.get_row_count() - 1 and loc_col is not city_col:
                    sail_to = Location(loc_row, city_col)

                else:
                    sail_to = Location(city_row, city_col)


            elif loc_row < city_row:

                if loc_row > 0 and loc_col is not city_col:
                    sail_to = Location(0, loc_col)

                elif loc_row == 0 and loc_col is not city_col:
                    sail_to = Location(loc_row, city_col)

                else:
                    sail_to = Location(city_row, city_col)

            else:

                sail_to = Location(city_row, city_col)

        do_sail(game, drone, sail_to)

'''
def handle_drones(game):
    for drone in game.get_my_living_drones():
        location = drone.get_location()
        loc_row, loc_col = location.row,location.col
        city_location = game.get_my_cities()[0].location
        city_row, city_col = city_location.row, city_location.col

        game_rows = game.get_row_count()
        game_cols = game.get_col_count()

        # option 1: island --> right wall --> city
        # option 2: island --> left wall --> city
        # option 3: island --> ceiling --> city
        # option 4: island --> floor --> city

        do_sail(game, drone, sail_to)
'''
def kill_enemy_camper(game, city_range, pirate):

    if not try_attack(game, pirate):
        city = game.get_my_cities()[0]
        enemy_campers = []
        for i in game.get_enemy_living_pirates():
            if city.in_range(i, city_range):
                enemy_campers.append(i)
        if len(enemy_campers) > 0:
			count_camper.camper_turns = count_camper.camper_turns+1
			if count_camper.camper_turns > 3:
				do_sail(game, pirate, enemy_campers[0])
				return True
        else:
			count_camper.camper_turns = 0
        return False
    return True

def connect_lists(list1, list2):

    ret = []

    for i in list1:
        ret.append(i)

    for i in list2:
        ret.append(i)

    return ret

def do_sail(game, pirate, location):
    sail_options = game.get_sail_options(pirate, location)
    game.set_sail(pirate, sail_options[0])

class pirate_behaviors:

    def __init__(self):
        pass

    def camper(self, game, pirate, location, move_range):

        if not try_attack_drones(game, pirate) and not try_attack(game, pirate):
            if pirate.distance(location) > move_range:
                do_sail(game, pirate, location)

            else:

                enemies_in_range = get_enemy_drones_in_range(game, location, move_range)

                if len(enemies_in_range) != 0:
                    enemy_closest_to_location = get_closest_to_object(enemies_in_range, location)

                    if (location.distance(enemy_closest_to_location)) <= move_range:
                        do_sail(game, pirate, enemy_closest_to_location)

                    return

                else:
                    if len(game.get_enemy_living_drones()) > 0:
                        closest_obj = get_closest_to_object(game.get_enemy_living_drones(), pirate)
                        do_sail(game, pirate, closest_obj)


    def terrorist(self, game, pirate):
        if not kill_enemy_camper(game, 5, pirate):
            self.dog(game, pirate)

    def dog(self, game, pirate):
        if not try_attack_pirates(game, pirate) and not try_attack_drones(game, pirate):

            objectives = connect_lists(game.get_not_my_islands(), game.get_enemy_living_pirates())

            if len(objectives) != 0:

                closest_obj = get_closest_to_object(objectives, pirate)

                do_sail(game, pirate, closest_obj)

            else:
                #need to put something
                do_sail(game, pirate, game.get_my_cities()[0])

    def escort(self, game, pirate):
        pass
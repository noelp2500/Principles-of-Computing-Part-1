# Cookie Clicker
# Author - Noel Pereira
# Submission - http://www.codeskulptor.org/#user47_IY4NaKIKOpT1Tdr.py 

####################################################################

"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self, cookies = 0.0, total_cookies = 0.0, time = 0.0, cps = 1.0):
        self._cookies = cookies								# The current number of cookies 
        self._total_cookies = total_cookies					# The total number of cookies produced throughout the entire game
        self._time = time									# The current time (in seconds) of the game
        self._cps = cps										# The current CPS 
        self._history = [(0.0, None, 0.0, 0.0)]				# History list (time, item, cost of item, total cookies)
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Cookies: " + str(self.get_cookies()) \
                + " total cookes: " + str(self._total_cookies)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS
        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time
        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list
        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)
        For example: [(0.0, None, 0.0, 0.0)]
        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)
        Should return a float with no fractional part
        """
        time_until = (cookies-self._cookies)/self.get_cps()
      
        if time_until < 0:
            return 0.0
        if time_until- int(time_until) == 0:
            return float(int(time_until))
        return float(int(time_until)+1)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._time += time
            self._cookies += self._cps*time
            self._total_cookies += self._cps*time      
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Should do nothing if you cannot afford the item
        """
        
        if self._cookies >= cost:
            self._cookies -= cost 
           
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookies))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    game_info = build_info.clone()
    game_state = ClickerState()
    # Replace with your code
    while game_state.get_time() <= duration:
        item_name = strategy(game_state.get_cookies(), game_state.get_cps(), 
                             game_state.get_history(), duration-game_state.get_time(), game_info)
        if item_name == None:
            break
        
        time_elapse = game_state.time_until(game_info.get_cost(item_name))                
        if time_elapse > duration-game_state.get_time():
            break
            
        game_state.wait(time_elapse)
        game_state.buy_item(item_name, game_info.get_cost(item_name), game_info.get_cps(item_name))
        game_info.update_item(item_name)
        
    if game_state.get_time() < duration:
        game_state.wait(duration-game_state.get_time())
    

    return game_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!
    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None
    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cost = float("inf")
    choose = None
    for items in build_info.build_items():
        if build_info.get_cost(items) < cost:
            if cookies >= build_info.get_cost(items) - time_left*cps:
                cost = build_info.get_cost(items)
                choose = items
    return choose

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cost = float("-inf")
    choose = None
    for items in build_info.build_items():
        if build_info.get_cost(items) > cost:
            if cookies >= build_info.get_cost(items) - time_left*cps:
                cost = build_info.get_cost(items)
                choose = items
    return choose

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    efficiency = float("-inf")
    choose = None
    for items in build_info.build_items():
        power = build_info.get_cps(items)/build_info.get_cost(items)
        wait_time = (build_info.get_cost(items)-cookies)/cps
        if time_left >= wait_time:
            if power/wait_time > efficiency:
                efficiency = power/wait_time
                choose = items
    return choose
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

   

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    print simulate_clicker(provided.BuildInfo(), SIM_TIME, strategy_best)
    
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    



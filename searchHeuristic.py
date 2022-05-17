import numpy
import numpy as np
import flask
import copy

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


class Mission:
    def __init__(self, key, value, shortcut=None):
        if shortcut:
            self.task_num = shortcut[0]
            self.course_num = shortcut[1]
            self.difficulty = shortcut[2]
            self.time = shortcut[3]
        else:
            self.task_num = int(key[11])
            self.course_num = int(key[-1])
            self.difficulty = int(value[0])
            self.time = int(value[1])

    def __eq__(self, other):
        return (self.task_num == other.task_num) and\
               (self.course_num == other.course_num) and\
               (self.difficulty == other.difficulty) and\
               (self.time == other.time)



class State:
    def __init__(self, starting_matrix, missions_to_schedule):
        self.schedule = starting_matrix
        self.missions = [Mission(key, missions_to_schedule[key]) for key in missions_to_schedule.keys()]

    def compute_successor(self, action):
        self_course = copy.deepcopy(self)
        mission_to_remove = action[1]
        coordinates = action[0]

        for mission in self_course.missions:
            if mission == mission_to_remove:
                self_course.missions.remove(mission)
                break

        if numpy.all(coordinates == numpy.array([-1,-1])):
            half = int(mission_to_remove.time / 2)
            rest = mission_to_remove.time - half
            self_course.missions.append(Mission(None, None, shortcut=(mission_to_remove.task_num,
                                                   mission_to_remove.course_num,
                                                   mission_to_remove.difficulty,
                                                   half)))
            self_course.missions.append(Mission(None, None, shortcut=(mission_to_remove.task_num,
                                                   mission_to_remove.course_num,
                                                   mission_to_remove.difficulty,
                                                   rest)))
        else:
            x = coordinates[0]
            y = coordinates[1]
            if mission_to_remove.time > 1:
                min_x = coordinates[0] - mission_to_remove.time + 1
                self_course.schedule[min_x:x,y] = float(mission_to_remove.task_num) + (0.1 * float(mission_to_remove.course_num))
            else:
                self_course.schedule[x,y] = float(mission_to_remove.task_num) + (0.1 * float(mission_to_remove.course_num))
        return self_course



class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def __init__(self, starting_matrix, missions_to_schedule):
        """
        Returns the start state for the search problem
        """
        self.schedule = starting_matrix
        self.missions_to_schedule = list(missions_to_schedule.keys())
        self.missions_info = missions_to_schedule


    def get_start_state(self):
        return State(self.schedule, self.missions_info)


    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        return (not state.missions) or numpy.all(state.schedule != 0)

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of pairs,
        (successor, action), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there.
        """
        states = []
        for mission in state.missions:
            time = mission.time
            free_times = np.zeros(state.schedule.shape)
            for i in range(state.schedule.shape[1]):
                consecutive_hours = 0
                for j in range(state.schedule.shape[0]):
                    if state.schedule[j][i] == 0:
                        consecutive_hours += 1
                    else:
                        consecutive_hours = 0
                    free_times[j][i] = consecutive_hours
            if numpy.any(free_times >= time):
                for j in range(free_times.shape[1]):
                    for i in range(free_times.shape[0]):
                        if free_times[i][j] == time:
                            first = (i ,j)
                            break
                action = (first, mission)
                states.append((state.compute_successor(action), action))
            else:
                action = (numpy.array([-1, -1]), mission)
                states.append((state.compute_successor(action), action))
        return states


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    nodePath = dict()
    root = problem.get_start_state()
    fringe = Stack()
    fringe.push((root, None, root))
    while not fringe.isEmpty():
        currNode, currAction, prevNode = fringe.pop()
        if currNode not in nodePath:
            nodePath[currNode] = list(nodePath.get(prevNode, []))
            nodePath[currNode].append(currAction)
            if problem.is_goal_state(currNode):
                return currNode
            currNeighbors = problem.get_successors(currNode)
            for (neighbor, action) in currNeighbors:
                if neighbor not in nodePath:
                    fringe.push((neighbor, action, currNode))
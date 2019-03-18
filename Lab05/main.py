import matplotlib.pyplot as plt
import numpy as np
import random
from enum import IntEnum


class Task:
    def __init__(self, task_type, birth_time, exec_time, left_time, deadline):
        self.task_type = task_type
        self.birth_time = birth_time
        self.exec_time = exec_time
        self.left_time = left_time
        self.deadline = deadline

    def less_important(self, another, cmp_deadlines):
        if cmp_deadlines:
            return self.deadline > another.deadline
        else: return self.task_type > another.task_type


class Arrival:
    def __init__(self, time, task_type):
        self.time = time
        self.task_type = task_type

    def task_by_type(self, lmbd):
        exec_time, period = {
                'SMALL': (5.0, 5.0 / lmbd),
                'MEDIUM': (10.0, 10.0 / lmbd),
                'LARGE': (20.0, 20.0 / lmbd)
                }[self.task_type.name]
        return erlang_by_mean(exec_time), erlang_by_mean(period)


class TaskType(IntEnum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Strategy(IntEnum):
    RATE_MONOTONIC = 1
    EARLIEST_DEADLINE_FIRST = 2


def erlang(k, lmbd):
    acc = 0.0
    for _ in range(k):
        r = random.random()
        acc += -1.0 / lmbd * np.log(r)
    return acc / k


def erlang_by_mean(mean):
    K = 16
    return erlang(K, 1.0 / mean)


class System:
    def __init__(self, lmbd, strategy):
        self.tasks = []
        self.arrivals = [Arrival(0.1, TaskType.LARGE),\
                Arrival(0.2, TaskType.MEDIUM),\
                Arrival(0.3, TaskType.SMALL)]
        self.lmbd = lmbd
        self.strategy = strategy
    
    def add_arrival(self, new_arrival):
        # index for insertion
        index = len(self.arrivals)
        while ((index > 0) and (self.arrivals[index-1].time < new_arrival.time)):
            index -= 1
        self.arrivals.insert(index, new_arrival)

    def add_task(self, new_task):
        # index for insertion
        index = len(self.tasks)
        cmp_deadlines = True if (self.strategy == Strategy.EARLIEST_DEADLINE_FIRST)\
                else False
        while ((index > 0) and \
                (new_task.less_important(self.tasks[index-1], cmp_deadlines))):
            index -= 1
        self.tasks.insert(index, new_task)

    def simulate(self, ticks):
        DEADLINE_COEFF = 5.0
        current_time = 0.0
        deadline_missed = 0
        idle_time = 0.0
        waiting_times = []
        while (current_time < ticks):
            earliest_arrival_time = self.arrivals[-1].time
            earliest_finish_time = self.tasks[-1].left_time + current_time \
                    if (not len(self.tasks) == 0) else float('inf')
            # decides which event happended first
            if (earliest_arrival_time < earliest_finish_time):
                # time jump to tne new event
                delta = earliest_arrival_time - current_time
                current_time = earliest_arrival_time
                # if there are no tasks in system => system was idle during time jump
                if (len(self.tasks) == 0): idle_time += delta
                arrival = self.arrivals.pop()
                arrival_type = arrival.task_type
                exec_time, period = arrival.task_by_type(self.lmbd)
                # adds new arrival with the same type
                self.add_arrival(Arrival(time=current_time+period, task_type=arrival_type))
                if (not len(self.tasks) == 0): self.tasks[-1].left_time -= delta
                # adds new task to the system
                self.add_task(Task(task_type = arrival_type, birth_time = current_time,\
                        exec_time = exec_time, left_time = exec_time,\
                        deadline = current_time + DEADLINE_COEFF * exec_time))
            else:
                current_time = earliest_finish_time
                finished_task = self.tasks.pop()
                waiting_times.append(\
                        current_time - finished_task.birth_time - finished_task.exec_time)
                if (current_time > finished_task.deadline): deadline_missed += 1

        # Statistics
        system_load = 1 - (idle_time / current_time)

        for task in self.tasks:
            if (task.deadline < current_time): deadline_missed += 1
            waiting_times.append(\
                    current_time - task.birth_time - task.exec_time)

        waiting_time_mean = sum(waiting_times) / len(waiting_times)

        return deadline_missed, system_load, waiting_time_mean


if __name__ == "__main__":
    TICKS = 10000.0
    STRATEGY_RM = Strategy.RATE_MONOTONIC
    STRATEGY_EDF = Strategy.EARLIEST_DEADLINE_FIRST
    stats_deadlines = []
    stats_sys_load = []
    stats_waiting_time = []
    for l in np.arange(0.5, 0.9, 0.05):
        system = System(lmbd = l, strategy = STRATEGY_EDF)
        deadline_missed, system_load, waiting_time_mean = system.simulate(TICKS)
        stats_deadlines.append(deadline_missed)
        stats_sys_load.append(system_load)
        stats_waiting_time.append(waiting_time_mean)

    lambdas = np.arange(0.5, 0.9, 0.05)

    plt.subplot(3, 1, 1)
    plt.plot(lambdas, stats_deadlines, 'k')
    plt.ylabel('deadline_missed')
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(lambdas, stats_sys_load, 'b')
    plt.ylabel('system_load')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(lambdas, stats_waiting_time, 'c')
    plt.xlabel('lambda')
    plt.ylabel('waiting_time_mean')
    plt.grid(True)

    # plt.savefig('fig.png')
    plt.show()

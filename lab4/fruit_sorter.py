"""
Fruit sorter game using the Stack ADT

Author: Luc Bibeau
When: February 27, 2026
"""

import random
from stack import Stack

FILES = ["config1.txt", "config2.txt", "config3.txt"]


def get_random_state(states):
    """
    Chooses a random state and returns a list of Stacks as well
    as how many of those stacks must be filled to win.
    :param states: list[str], config files
    :return: tuple(list[Stack], int), populated stacks and win condition
    """
    index = random.randrange(0, len(states))
    with open(states[index], "r", encoding="UTF-8") as file:  # my computer couldn't figure out the codec, force UTF-8
        lines = file.read().splitlines()

    cap_string = lines.pop(0)
    cap = int(cap_string.split(" ")[1])

    stacks_string = lines.pop(0)
    number_of_stacks = int(stacks_string.split(" ")[1])

    stacks = []
    fruits = {}

    for i in range(number_of_stacks):
        stack = Stack(cap)

        if len(lines) > 0:
            for fruit in lines.pop(0):
                if fruit not in fruits:
                    fruits[fruit] = 0
                fruits[fruit] += 1
                stack.push(fruit)

        stacks.append(stack)

    win_condition = 0  # how many stacks must be full to win
    for fruit in fruits:
        if fruits[fruit] >= cap:
            win_condition += 1

    return stacks, win_condition


def get_integer(prompt, min, max):
    """
    Gets an integer from the user between (inclusive) min and max.
    :param prompt: str, prompt to display to user
    :param min: int, min integer
    :param max: int, max integer
    :return: int
    """

    num = min - 1
    while not (min <= num <= max):
        try:
            num = int(input(prompt))
        except ValueError:
            pass

    return num


def get_stack(stacks, to):
    """
    Gets a stack from the user.
    :param stacks: list of stacks
    :param to: bool, true if item being moved TO stack, false if being moved FROM
    :return: stack
    """
    to_str = "to" if to else "from"

    num_of_stacks = len(stacks)

    index = get_integer(f"Select a stack to move {to_str} (1-{num_of_stacks}): ", 1, num_of_stacks)
    stack = stacks[index - 1]

    return stack


def display_stacks(stacks):
    """
    Displays a list of stacks
    :param stacks: list[Stack], stacks to display
    :return: None
    """
    print("\nCurrent Stacks:")
    for k, v in enumerate(stacks):
        print(f"Stack {k + 1}: {v}")


def main():
    print("Welcome to Fruit Sorter!")

    stacks, win_condition = get_random_state(FILES)
    playing = True

    while playing:
        display_stacks(stacks)

        move_from = get_stack(stacks, False)
        move_to = get_stack(stacks, True)

        item = None
        try:
            item = move_from.pop()
            move_to.push(item)
        except Exception as e:
            print(e)

            if not item is None:  # if pop was successful but push failed, push back into original stack.
                move_from.push(item)

        complete_stacks = 0
        for stack in stacks:
            if stack.is_completed():
                complete_stacks += 1

        playing = complete_stacks != win_condition

    display_stacks(stacks)
    print("Congratulations! You've won the game!")


if __name__ == "__main__":
    main()
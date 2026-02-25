import random
from stack import Stack

FILES = ["config1.txt", "config2.txt", "config3.txt"]

# TODO: Implement the fruit sorter game logic here


def get_random_state(states):
    """
    Chooses a random state and returns a list of Stacks.
    :param states: list[str], config files
    :return: list[Stack], populated stacks
    """
    index = random.randrange(0, len(states))
    index = 0
    with open(states[index], "r", encoding="UTF-8") as file:  # my computer couldn't figure out the codec, force UTF-8
        lines = file.read().splitlines()

    cap_string = lines.pop(0)
    cap = int(cap_string.split(" ")[1])

    stacks_string = lines.pop(0)
    number_of_stacks = int(stacks_string.split(" ")[1])

    stacks = []
    for i in range(number_of_stacks):
        stack = Stack(cap)

        if len(lines) > 0:
            for fruit in lines.pop(0):
                stack.push(fruit)

        stacks.append(stack)

    return stacks


def display_stacks(stacks):
    print("Current Stacks:")
    for k, v in enumerate(stacks):
        print(f"Stack {k + 1}: {v}")


def main():
    stacks = get_random_state(FILES)
    playing = True

    while playing:
        display_stacks(stacks)
        playing = False

if __name__ == "__main__":
    main()
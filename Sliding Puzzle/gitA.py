import timeit
from gitB import State
import glob
import cv2
import matplotlib.pyplot as plt
from matplotlib import animation


fig, ax = plt.subplots(3, 3)#, figsize=(13,13))
fig.subplots_adjust(left=0.125, bottom=0.1, right=0.7, top=0.85, wspace=0.01, hspace=0.01)

goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_node = State
initial_state = list()
pomocni = initial_state
board_len = 0
board_side = 0

moves = list()
costs = set()

#slike
images = []
for img in glob.glob("./Slike1/*.jpg"):
    n = cv2.imread(img)
    images.append(n)

def ida(start_state):

    pomocni = initial_state
    global costs

    threshold = get_heuristika(start_state)

    while 1:
        response = pretraga(start_state, threshold)

        if type(response) is list:
            return response
            break


        threshold = response
        costs = set()


def pretraga(start_state, threshold):

    global goal_node, costs

    explored, stack = set(), list([State(start_state, None, None, 0, 0, threshold)])

    while stack:
        node = stack.pop()

        #pretraženi čvorovi
        explored.add(node.map)

        #postignuto ciljno stanje
        if node.state == goal_state:
            goal_node = node
            return stack

        #zbir ciljne i heurističke procijenjene cijene prelazi vrijednost tresholda
        if node.key > threshold:
            costs.add(node.key)

        if node.depth < threshold:

            #susjedni trenutnog čvora u obrnutom poretku kako bi se mogao rekonstruirati put i vraiti u korijen
            neighbors = reversed(expand(node))

            for neighbor in neighbors:
                #ako njegov put nije ispitivan
                if neighbor.map not in explored:

                    #f =  g + h
                    neighbor.key = neighbor.cost + get_heuristika(neighbor.state)
                    stack.append(neighbor)
                    explored.add(neighbor.map)

    return min(costs)


def expand(node):


    neighbors = list()

    #susjedi ca 4 strane
    neighbors.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    #susjedi koji imaju stanje, tj imaju vrijesnost
    #npr ako je čvor u donjem desnom cosku, onda on nema desnog i donjeg susjeda pa se oni izbacuju
    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes

#izmjena vrijednosti prilikom kretanja plocica
def move(state, position):

    new_state = state[:]

    index = new_state.index(0)

    if position == 1:  # Up

        if index not in range(0, board_side):

            temp = new_state[index - board_side]
            new_state[index - board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 2:  # Down

        if index not in range(board_len - board_side, board_len):

            temp = new_state[index + board_side]
            new_state[index + board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # Left

        if index not in range(0, board_len, board_side):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # Right

        if index not in range(board_side - 1, board_len, board_side):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


def get_heuristika(state):
    return sum(abs(b % board_side - g % board_side) + abs(b//board_side - g//board_side)
               for b, g in ((state.index(i), goal_state.index(i)) for i in range(1, board_len)))


def backtrace():

    current_node = goal_node
    #print(initial_state)
    while initial_state != current_node.state:

        if current_node.move == 1:
            movement = 'Up'
        elif current_node.move == 2:
            movement = 'Down'
        elif current_node.move == 3:
            movement = 'Left'
        else:
            movement = 'Right'

        moves.insert(0, movement)
        current_node = current_node.parent

    return moves


def export(time):

    global moves
    print(moves)
    moves = backtrace()

    file = open('output.txt', 'w')
    file.write("path_to_goal: " + str(moves))
    file.write("\ncost_of_path: " + str(len(moves)))
    file.write("\nsearch_depth: " + str(goal_node.depth))
    file.write("\nrunning_time: " + format(time, '.8f'))
    #file.write("\nmax_ram_usage: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.8f'))
    file.close()

    ani = animation.FuncAnimation(fig, moving, interval=1000)
    plt.show()


def plot():

    k = 0
    for i in range(3):
        for j in range(3):
            img = images[pomocni[i*3+j]]
            ax[i][j].axis('off')
            ax[i][j].imshow(img, interpolation='none')


def moving(i):
    if i == len(moves) +3:
        img = images[9]
        ax[2][2].axis('off')
        ax[2][2].imshow(img, interpolation='none')
    if i == 0 or i > len(moves):
        return 1

    zeroPosition = pomocni.index(0)
    move = moves[i-1]
    if move == 'Left':
        pomocni[zeroPosition] = pomocni[zeroPosition-1]
        pomocni[zeroPosition - 1] = 0
        zeroPosition = zeroPosition -1
    elif move == 'Right':
        pomocni[zeroPosition] = pomocni[zeroPosition + 1]
        pomocni[zeroPosition + 1] = 0
        zeroPosition = zeroPosition + 1
    elif move == 'Up':
        pomocni[zeroPosition] = pomocni[zeroPosition - 3]
        pomocni[zeroPosition - 3] = 0
        zeroPosition = zeroPosition - 3
    elif move == 'Down':
        pomocni[zeroPosition] = pomocni[zeroPosition + 3]
        pomocni[zeroPosition + 3] = 0
        zeroPosition = zeroPosition + 3
    plot()
    return i+1



def read(configuration):

    global board_len, board_side

    data = configuration.split(",")

    for element in data:
        initial_state.append(int(element))

    board_len = len(initial_state)

    board_side = int(board_len ** 0.5)

    print("bl bs" + str(board_len) + " " + str(board_side))


def main():

    read('8,3,5,7,1,2,4,6,0')
    #read('1,2,3,4,6,8,7,5,0')

    start = timeit.default_timer()

    ida(initial_state)

    stop = timeit.default_timer()

    export(stop-start)


if __name__ == '__main__':
    main()
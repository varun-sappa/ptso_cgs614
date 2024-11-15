# import matplotlib features
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.lines as lines
import matplotlib.patches as patches
import numpy as np

# import python libraries
import builtins
import math
import sys
import time

##################
# task specifications
##################
TASK_TEXT_1 = "Imagine you are standing at the"
TASK_TEXT_2 = "and facing the"
TASK_TEXT_3 = "Point to the"

TASK_ITEMS = [("flower", "tree", "cat", 301),  # example
              ("car", "traffic light", "stop sign", 123),
              ("cat", "tree", "car", 237),
              ("stop sign", "cat", "house", 83),
              ("cat", "flower", "car", 156),
              ("stop sign", "tree", "traffic light", 319),
              ("stop sign", "flower", "car", 235),
              ("traffic light", "house", "flower", 333),
              ("house", "flower", "stop sign", 260),
              ("car", "stop sign", "tree", 280),
              ("traffic light", "cat", "car", 48),
              ("tree", "flower", "house", 26),
              ("cat", "house", "traffic light", 150)
              ]

# Parameters for customization
NUM_QUESTIONS = 10
TIME_PER_QUESTION = 20  # seconds per question
ERROR_THRESHOLD = 30  # degrees

TOTAL_TEST_TIME = NUM_QUESTIONS * TIME_PER_QUESTION
TIME_IN_SECONDS = TOTAL_TEST_TIME

INSTRUCTION_TEXT = "This is a test of your ability to imagine different perspectives\n" + \
                   "or orientations in space. On each of the following screens you will\n" + \
                   "see a picture of an array of objects and an \"arrow circle\" with a question\n" + \
                   "about the direction between some of the objects. For the question on\n" + \
                   "each screen, you should imagine that you are standing at one object in\n" + \
                   "the array (which will be named in the center of the circle) and facing\n" + \
                   "another object, named at the top of the circle. Your task is to draw an\n" + \
                   "arrow from the center object showing the direction to a third object\n" + \
                   "from this facing orientation.\n\n" + \
                   "Look at the sample item in the other window. In this item you are asked to\n" + \
                   "imagine that you are standing at the flower, which is named in the center\n" + \
                   "of the circle, and facing the tree, which is named at the top of the\n" + \
                   "circle. Your task is to draw an arrow pointing to the cat. In the sample\n" + \
                   "item this arrow has been drawn for you. In the test items, your task is to\n" + \
                   "draw this arrow. Can you see that if you were at the flower facing the tree,\n" + \
                   "the cat would be in this direction? Please ask the experimenter now if you\n" + \
                   "have any questions about what you are required to do.\n\n" + \
                   f"There are {NUM_QUESTIONS} items in this test, one on each screen. For each item, the array\n" + \
                   "of objects is shown at the top of the window and the arrow circle is shown at\n" + \
                   "the bottom. Please do not pick up or turn the monitor, and do not make\n" + \
                   "any marks on the maps. Try to mark the correct directions but do not spend\n" + \
                   "too much time on any one question.\n\n" + \
                   f"You will have {TOTAL_TEST_TIME} seconds for this test. Each question will automatically\n" + \
                   f"advance after {TIME_PER_QUESTION} seconds. You can use SPACE in the other window to\n" + \
                   "confirm your selection early."

##################
# main function
##################
def main():
    matplotlib.rcParams['toolbar'] = 'None'
    subject_id = input("Please insert your participant ID: ")
    
    # Open result and log files
    result_filename = f'results-{subject_id}.txt'
    log_filename = f'logs-{subject_id}.txt'
    result_file = open(result_filename, 'w+')
    log_file = open(log_filename, 'w+')
    
    # Write headers to log file
    log_file.write("task_id,correct_angle,logged_angle,error\n")
    
    create_test_window(subject_id)
    create_instruction_window()

    builtins.result_file = result_file
    builtins.log_file = log_file
    builtins.subject_id = subject_id
    builtins.errors = []
    builtins.task_id = 0
    builtins.score = 0
    builtins.total_start_time = None  # To record the start time of the test
    load_task(builtins.task_id)

    plt.show()

##################
# plot creator functions
##################
def create_instruction_window():
    ins_fig = plt.figure("Instructions", figsize=(8, 7))
    ins_ax = ins_fig.add_subplot(1, 1, 1)
    ins_ax.text(0.01, 0, INSTRUCTION_TEXT, verticalalignment='center', fontsize=12.5)
    plt.xticks([])
    plt.yticks([])
    plt.ylim([-1.0, 1.0])
    ins_fig.tight_layout()


def create_test_window(SUBJECT_ID):
    test_fig = plt.figure("Perspective Taking Test - Participant " + str(SUBJECT_ID), figsize=(7.5, 7.5))

    # object array subplot
    pic_ax = test_fig.add_subplot(2, 1, 1)
    picture = mpimg.imread('object_array.png')
    plt.xticks([])
    plt.yticks([])
    pic_ax.set_title("Remaining Time: " + str(TIME_PER_QUESTION))
    pic_ax.imshow(picture)

    # user input subplot
    input_ax = test_fig.add_subplot(2, 1, 2)
    input_ax.axis('equal')

    circle = patches.Circle((0, 0), 1.015, facecolor='none', edgecolor='black', linewidth=3)
    input_ax.add_patch(circle)

    upright_line = lines.Line2D((0, 0), (0, 1), linewidth=3, color='black')
    input_ax.add_line(upright_line)
    input_ax.add_line(lines.Line2D((0, -0.03), (1, 0.95), linewidth=3, color='black'))  # left arrow wedge
    input_ax.add_line(lines.Line2D((0, 0.03), (1, 0.95), linewidth=3, color='black'))  # right arrow wedge

    answer_line = lines.Line2D((0, 0), (0, 1), linewidth=3, color='orange')
    input_ax.add_line(answer_line)

    text_bottom = input_ax.text(0.0, -0.15, 'text_bottom', fontsize=10, horizontalalignment='center')
    text_top = input_ax.text(0.0, 1.15, 'text_top', fontsize=10, horizontalalignment='center')
    text_example = input_ax.text(-1.0, 0.58, 'text_example', fontsize=10, horizontalalignment='center')
    text_instruction = input_ax.text(0.0, -1.2, 'text_instruction', fontsize=10, horizontalalignment='center')

    plt.xlim(-1.5, 1.5)
    plt.xticks([])
    plt.ylim(-1.5, 1.5)
    plt.yticks([])
    test_fig.tight_layout()

    # event handling
    builtins.fig = test_fig
    builtins.answer_line = answer_line
    builtins.picture_ax = pic_ax
    builtins.text_bottom = text_bottom
    builtins.text_top = text_top
    builtins.text_example = text_example
    builtins.text_instruction = text_instruction
    test_fig.canvas.mpl_connect('button_press_event', on_click)
    test_fig.canvas.mpl_connect('key_press_event', on_key_press)


def load_task(INDEX):
    task_id_as_text = str(INDEX) + '.'
    item_tuple = TASK_ITEMS[INDEX]
    located_at = item_tuple[0].replace(' ', '\; ')
    facing_to = item_tuple[1].replace(' ', '\; ')
    pointing_to = item_tuple[2].replace(' ', '\; ')

    instruction_text = task_id_as_text + ' ' + TASK_TEXT_1 + ' $\mathtt{' + located_at + '}$ ' + TASK_TEXT_2 + \
                       ' $\mathtt{' + facing_to + '}$. ' + TASK_TEXT_3 + ' $\mathtt{' + pointing_to + '}$.'
    builtins.text_instruction.set_text(instruction_text)

    if INDEX == 0:  # example case
        builtins.answer_line.set_data([0.0, -0.86], [0.0, 0.52])
        builtins.text_example.set_text('cat')
    else:
        builtins.answer_line.set_data([0.0, 0.0], [0.0, 1.0])
        builtins.text_example.set_text('')

    if INDEX == 1:  # first real task, start total timer
        builtins.total_start_time = time.time()
        builtins.total_timer = builtins.fig.canvas.new_timer(interval=1000)
        builtins.total_timer.add_callback(update_total_time)
        builtins.total_timer.start()

    # Stop previous question timer if exists
    if hasattr(builtins, 'question_timer'):
        builtins.question_timer.stop()

    # Start new question timer (including example)
    builtins.question_start_time = time.time()
    builtins.question_timer = builtins.fig.canvas.new_timer(interval=1000)
    builtins.question_timer.add_callback(update_question_time)
    builtins.question_timer.start()

    # Start per-question timeout timer (except for example)
    if INDEX > 0:
        if hasattr(builtins, 'question_timeout_timer'):
            builtins.question_timeout_timer.stop()
        builtins.question_timeout_timer = builtins.fig.canvas.new_timer(interval=TIME_PER_QUESTION * 1000)
        builtins.question_timeout_timer.add_callback(per_question_timeout)
        builtins.question_timeout_timer.start()

    # Update the displayed remaining time to start from TIME_PER_QUESTION
    builtins.picture_ax.set_title("Remaining Time: " + str(TIME_PER_QUESTION))

    builtins.text_bottom.set_text(item_tuple[0])
    builtins.text_top.set_text(item_tuple[1])
    builtins.fig.canvas.draw()


##################
# callbacks
##################
def on_click(EVENT):
    if EVENT.inaxes is None:
        return
    length = euclidean_distance([0, 0], [EVENT.xdata, EVENT.ydata])
    if length == 0:
        return  # Prevent division by zero
    builtins.answer_line.set_data([0.0, EVENT.xdata / length], [0.0, EVENT.ydata / length])
    builtins.fig.canvas.draw()


def on_key_press(EVENT):
    if EVENT.key == ' ':
        if hasattr(builtins, 'question_timer'):
            builtins.question_timer.stop()
        if hasattr(builtins, 'question_timeout_timer'):
            builtins.question_timeout_timer.stop()
        process_current_question()
        advance_to_next_question()


def per_question_timeout():
    process_current_question()
    advance_to_next_question()


def process_current_question():
    if builtins.task_id > 0:  # exclude example
        correct_angle = round(TASK_ITEMS[builtins.task_id][3], 4)
        logged_angle = round(compute_response_line_angle(), 4)
        error = round(angle_difference(correct_angle, logged_angle), 4)
        # Log per-question data to log_file
        builtins.log_file.write(f"{builtins.task_id},{correct_angle},{logged_angle},{error}\n")
        builtins.errors.append(error)
        if error < ERROR_THRESHOLD:
            builtins.score += 1


def advance_to_next_question():
    builtins.task_id += 1

    if builtins.task_id <= NUM_QUESTIONS:  # move on to the next task
        load_task(builtins.task_id)
    else:  # no more tasks, terminate the test
        # Stop all timers
        if hasattr(builtins, 'total_timer'):
            builtins.total_timer.stop()
        if hasattr(builtins, 'question_timer'):
            builtins.question_timer.stop()
        if hasattr(builtins, 'question_timeout_timer'):
            builtins.question_timeout_timer.stop()
        
        # Calculate total time taken
        if builtins.total_start_time:
            total_time_taken = round(time.time() - builtins.total_start_time, 2)
        else:
            total_time_taken = 0
        
        # Write summary to result_file
        builtins.result_file.write(f"participant_id: {builtins.subject_id}\n")
        builtins.result_file.write(f"total_score: {builtins.score}\n")
        builtins.result_file.write(f"total_time_taken_seconds: {total_time_taken}\n")
        
        # Close both files
        builtins.log_file.close()
        builtins.result_file.close()
        
        print(f'The test has terminated successfully.')
        print(f'Results saved to file {builtins.result_file.name}.')
        print(f'Your total score is: {builtins.score}')
        print(f'Total time taken: {total_time_taken} seconds')
        sys.exit(0)


def update_question_time():
    elapsed = max(TIME_PER_QUESTION - round(time.time() - builtins.question_start_time), 0)
    builtins.picture_ax.set_title("Remaining Time: " + str(elapsed))
    builtins.fig.canvas.draw()
    if elapsed <= 0:
        per_question_timeout()


def update_total_time():
    elapsed = max(TOTAL_TEST_TIME - round(time.time() - builtins.total_start_time), 0)
    # builtins.picture_ax.set_title("Remaining Time: " + str(elapsed))111
    builtins.fig.canvas.draw()
    if elapsed <= 0:
        # Time's up for the whole test
        if hasattr(builtins, 'total_timer'):
            builtins.total_timer.stop()
        if hasattr(builtins, 'question_timer'):
            builtins.question_timer.stop()
        if hasattr(builtins, 'question_timeout_timer'):
            builtins.question_timeout_timer.stop()
        process_current_question()
        advance_to_next_question()

##################
# math helpers
##################
def compute_response_line_angle():
    answer_line_data = builtins.answer_line.get_data()
    answer_line_endpoint = (answer_line_data[0][1], answer_line_data[1][1])
    upright_endpoint = (0.0, 1.0)
    cosine_value = answer_line_endpoint[0] * upright_endpoint[0] + \
                   answer_line_endpoint[1] * upright_endpoint[1]

    angle = angle_between_normalized_2d_vectors(upright_endpoint, answer_line_endpoint) * 180.0 / math.pi

    # convert angle to range (0; 360]
    if angle < 0:
        angle *= -1
    else:
        angle = 360.0 - angle

    return angle


def euclidean_distance(POINT_1, POINT_2):
    return math.sqrt(pow(POINT_1[0] - POINT_2[0], 2) + pow(POINT_1[1] - POINT_2[1], 2))


def angle_between_normalized_2d_vectors(VEC1, VEC2):
    return math.atan2(VEC1[0] * VEC2[1] - VEC1[1] * VEC2[0], VEC1[0] * VEC2[0] + VEC1[1] * VEC2[1])


def angle_difference(ANGLE_1, ANGLE_2):
    phi = math.fmod(abs(ANGLE_2 - ANGLE_1), 360)
    distance = 360 - phi if phi > 180 else phi
    return distance


if __name__ == '__main__':
    main()

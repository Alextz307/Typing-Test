import curses
from curses import wrapper
import time 
import random 


def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr('Welcome to the speed typing test!\n')
	stdscr.addstr('Press any key to start the game!')
	stdscr.refresh()
	stdscr.getkey()


def load_text():
	with open('text.txt', 'r') as file:
		lines = file.readlines()
		return random.choice(lines).strip()


def display_text(stdscr, target, current, wpm):
	stdscr.clear()

	stdscr.addstr(target)
	stdscr.addstr(1, 0, f'WPM: {wpm}')

	for i, ch in enumerate(current):
		if ch == target[i]:
			ch_color = curses.color_pair(1) 
		else:
			ch_color = curses.color_pair(2)

		stdscr.addstr(0, i, ch, ch_color)

	stdscr.refresh()


def wpm_test(stdscr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		display_text(stdscr, target_text, current_text, wpm)

		if ''.join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ('KEY_BACKSPACE', '\b', '\x7f'):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

	start_screen(stdscr)

	while True:
		wpm_test(stdscr)

		stdscr.addstr(2, 0, 'You completed the text! Press any key to continue...')
		key = stdscr.getkey()

		if ord(key) == 27:
			break


wrapper(main)

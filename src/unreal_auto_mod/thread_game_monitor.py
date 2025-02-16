import time
import threading

from unreal_auto_mod.data_structures import HookStateType
from unreal_auto_mod import hook_states, utilities, window_management, log, processes

found_process = False
found_window = False
window_closed = False
run_monitoring_thread = False
game_monitor_thread = ''


def game_monitor_thread_runner(tick_rate: float = 0.01):
    while run_monitoring_thread:
        time.sleep(tick_rate)
        game_monitor_thread_logic()


def get_game_window():
    return window_management.get_window_by_title(utilities.get_game_window_title())


@hook_states.hook_state_decorator(HookStateType.POST_GAME_LAUNCH)
def found_game_window():
    global found_window
    log.log_message('Window: Game Window Found')
    found_window = True


def game_monitor_thread_logic():
    global found_process
    global found_window
    global window_closed

    if not found_process:
        if processes.is_process_running(utilities.get_game_process_name()):
            log.log_message('Process: Found Game Process')
            found_process = True
    elif not found_window:
        time.sleep(4)
        if get_game_window():
            found_game_window()
    elif not window_closed:
        if not get_game_window():
            log.log_message('Window: Game Window Closed')
            stop_game_monitor_thread()
            window_closed = True


def start_game_monitor_thread():
    global game_monitor_thread
    global run_monitoring_thread
    run_monitoring_thread = True
    game_monitor_thread = threading.Thread(target=game_monitor_thread_runner, daemon=True)
    game_monitor_thread.start()


@hook_states.hook_state_decorator(HookStateType.POST_GAME_CLOSE)
def stop_game_monitor_thread():
    global run_monitoring_thread
    run_monitoring_thread = False


def game_monitor_thread():
    start_game_monitor_thread()
    log.log_message('Thread: Game Monitoring Thread Started')
    game_monitor_thread.join()
    log.log_message('Thread: Game Monitoring Thread Ended')
    log.log_message(f'Timer: Time since script execution: {utilities.get_running_time()}')

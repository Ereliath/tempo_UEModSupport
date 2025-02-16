import time
import threading

from unreal_auto_mod import hook_states, log
from unreal_auto_mod.data_structures import HookStateType


def constant_thread_runner(tick_rate: float = 0.01):
    while run_constant_thread:
        time.sleep(tick_rate)
        constant_thread_logic()


def constant_thread_logic():
    hook_states.hook_state_checks(HookStateType.CONSTANT)


def start_constant_thread():
    global constant_thread
    global run_constant_thread
    run_constant_thread = True
    constant_thread = threading.Thread(target=constant_thread_runner, daemon=True)
    constant_thread.start()


@hook_states.hook_state_decorator(HookStateType.POST_INIT)
def post_constant_thread_created_message():
    log.log_message('Thread: Constant Thread Started')


def constant_thread():
    start_constant_thread()
    post_constant_thread_created_message()


def stop_constant_thread():
    global run_constant_thread
    run_constant_thread = False
    log.log_message('Thread: Constant Thread Ended')

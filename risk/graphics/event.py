###############################################################################
## Wrapper module for pygame's event
## linux seems to have issues when two threads pump at the same time but
## windows doesn't properly pump events for some reason =(. However, bad things
## happens when multiple threads pump at once. This module is thread safe.
#
import threading

import pygame

import risk
import risk.logger
import risk.errors.game_master

from risk.errors.input import UserQuitInput

_BLOCK = True
_NO_BLOCK = False
mutex = threading.Semaphore()

def wait_for_event():
    # this is a bit strange, but pygame will invoke pump internally so there's
    # really no reason to call pump when waiting for event
    mutex.acquire(_BLOCK)
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        mutex.release()
        raise UserQuitInput()
    mutex.release()
    return event

def get_events():
    mutex.acquire(_BLOCK)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            mutex.release()
            raise UserQuitInput()
    mutex.release()
    return events

def pump():
    # best effort, don't pump if another thread has already done so
    acquired = mutex.acquire(_NO_BLOCK)
    if acquired:
        pygame.event.pump()
        mutex.release()


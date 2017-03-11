"""Pygame helper module."""

import pygame


# pylint: disable=no-member
pygame.init()


# TODO: maybe there is need to rewrite this, or completely remove.
def create_display(res, fullscreen, depth, caption):
    """Create pygame display."""

    display = pygame.display.set_mode(res, fullscreen, depth)
    pygame.display.set_caption(caption)
    return display


def get_clock():
    """Helper for unification with other backends."""
    return pygame.time.Clock()

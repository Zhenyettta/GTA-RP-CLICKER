#  Copyright (c) Made by Zhenyok!

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class State:
    RECT_ACCELERATION = 582.45
    FREE_FALL_ACCELERATION = 214.35

    time: float
    fish_y: float
    rect_y: float
    fish_speed: float
    rect_speed: float

    @classmethod
    def from_previous_state(
            cls,
            prev_state: State,
            time: float,
            fish_y: float,
            rect_y: float,
            # accelerated: bool
    ) -> State:
        delta_time = time - prev_state.time
        fish_speed = (fish_y - prev_state.fish_y) / delta_time
        # rect_speed = (prev_state.rect_speed
        #               + self.RECT_ACCELERATION * delta_time * accelerated
        #               - self.FREE_FALL_ACCELERATION * delta_time)
        rect_speed = (rect_y - prev_state.rect_y) / delta_time

        return cls(
            time=time,
            fish_y=fish_y,
            rect_y=rect_y,
            fish_speed=fish_speed,
            rect_speed=rect_speed
        )

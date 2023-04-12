"""
`python gpt4.py` to render a video
"""
import copy
import math
import operator as op
import random
from datetime import datetime
from functools import reduce
from manim import *  # type: ignore
from settings import *


class Recto(RoundedRectangle):
    def __init__(self, curvature: float = RECTO_CURVATURE, **kwargs):
        if not RECTO_CURVATURE_RANGE[0] <= curvature <= RECTO_CURVATURE_RANGE[1]:
            curvature = random.uniform(*RECTO_CURVATURE_RANGE)
        super().__init__(
            corner_radius=curvature * 0.5 * RECTO_HEIGHT,
            height=RECTO_HEIGHT,
            width=RECTO_HEIGHT * random.uniform(*RECTO_WIDTH_MULTIPLIER_RANGE),
            color=random.choice(RECTO_COLOR_LIST),
            fill_opacity=1.0,
            stroke_width=0,
            sheen_factor=random.uniform(*SHEEN_FACTOR_RANGE),
            sheen_direction=np.array(
                (random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), 0.0)
            ),
            **kwargs,
        )


class RectoChain(VGroup):
    """Comprised of a group of Recto that are connected end-to-end.

    Parameters
    ----------
    recto_span
        span between any two Recto

    Attributes
    ----------
    effective_width
        actual render width which should be smaller than the frame width
    """

    def __init__(self, recto_span: float = RECTO_SPAN, *vmobjects, **kwargs):
        recto_number = random.randint(*RECTO_NUMBER_RANGE)
        recto_list = [Recto() for _ in range(recto_number)]
        total_recto_width = 0.0
        for recto in recto_list:
            total_recto_width += recto.width
        self.effective_width = total_recto_width + RECTO_SPAN * recto_number
        if self.effective_width < FRAME_WIDTH:
            raise Exception(
                f"Randomly generated RectoChain has the smaller width ({self.effective_width}) than the frame width ({FRAME_WIDTH})"
            )
        super().__init__(
            *recto_list, *copy.deepcopy(recto_list[: RECTO_NUMBER_RANGE[0]]), **kwargs
        )
        self.arrange(buff=recto_span)


class GPT4(Scene):
    def construct(self):
        config.frame_x_radius = FRAME_X_RADIUS
        config.frame_y_radius = FRAME_Y_RADIUS

        self.camera.background_color = BACKGROUNG_COLOR
        self.camera.frame_height = FRAME_HEIGHT
        self.camera.frame_width = FRAME_WIDTH
        # self.add(
        #     NumberPlane(
        #         x_range=(
        #             -config["frame_x_radius"],
        #             config["frame_x_radius"],
        #             1,
        #         ),
        #         y_range=(
        #             -config["frame_y_radius"],
        #             config["frame_y_radius"],
        #             1,
        #         ),
        #     )
        # )

        rc_list = [RectoChain() for _ in range(RECTOCHAIN_NUMBER)]
        rc_list[0].to_corner(buff=0.0)
        # self.add(rc_list[0])
        for i in range(1, RECTOCHAIN_NUMBER):
            rc_list[i].next_to(
                rc_list[i - 1], direction=UP, buff=RECTOCHAIN_SPAN
            ).to_edge(edge=RIGHT if i % 2 == 1 else LEFT, buff=0.0)
            # self.add(rc_list[i])

        animation_list = []
        for i in range(RECTOCHAIN_NUMBER):
            rc = rc_list[i]
            direction_vector = LEFT if i % 2 == 0 else RIGHT
            segment_list = self.get_segment_list(rc)
            velocity_list = [
                random.uniform(
                    BASE_VELOCITY / VELOCITY_FACTOR, BASE_VELOCITY * VELOCITY_FACTOR
                )
                for _ in range(len(segment_list) - 1)
            ]
            animation_list.append(
                Succession(
                    *(
                        SmoothShift(
                            rc
                            if index == 0
                            else rc.shift(direction_vector * segment_list[index - 1]),
                            direction_vector * value,
                            start_velocity=BASE_VELOCITY
                            if index == 0
                            else velocity_list[index - 1],
                            end_velocity=BASE_VELOCITY
                            if index == len(segment_list) - 1
                            else velocity_list[index],
                        )
                        for index, value in enumerate(segment_list)
                    ),
                    run_time=RUN_TIME,
                )
            )

        self.play(AnimationGroup(*animation_list))

        # rc_list = [RectoChain() for _ in range(RECTOCHAIN_NUMBER)]
        # rc_list[0].to_corner(buff=0.0)
        # # self.add(rc_list[0])
        # for i in range(1, RECTOCHAIN_NUMBER):
        #     rc_list[i].next_to(
        #         rc_list[i - 1], direction=UP, buff=RECTOCHAIN_SPAN
        #     ).to_edge(edge=RIGHT if i % 2 == 1 else LEFT, buff=0.0)
        #     # self.add(rc_list[i])
        # animations = []
        # for i in range(RECTOCHAIN_NUMBER):
        #     rc = rc_list[i]
        #     animations.append(
        #         # rc.animate, ApplyMethod, either would be fine
        #         # rc.animate(
        #         #     run_time=RUN_TIME,
        #         #     rate_func=rate_functions.linear,
        #         # ).shift((LEFT if i % 2 == 0 else RIGHT) * rc.effective_width)
        #         ApplyMethod(
        #             rc.shift,
        #             (LEFT if i % 2 == 0 else RIGHT) * rc.effective_width,
        #             run_time=RUN_TIME,
        #             rate_func=rate_functions.linear,
        #         )
        #     )
        # self.play(AnimationGroup(*animations))

    @classmethod
    def get_segment_list(cls, rc: RectoChain) -> list[float]:
        interpolation_list: list[float] = []
        interpolation_number: int = math.floor(
            rc.effective_width / INTERPOLATION_REFERENCE
        )
        generation_times: int = 0

        while len(interpolation_list) < interpolation_number:
            new_interpolation = random.uniform(0, rc.effective_width)
            generation_times += 1
            if generation_times > interpolation_number * 10:
                break

            if not any(
                abs(new_interpolation - existing_interpolation) < MIN_SHIFT_DISTANCE
                for existing_interpolation in interpolation_list
            ):
                if (
                    new_interpolation - 0 < MIN_SHIFT_DISTANCE
                    or rc.effective_width - new_interpolation < MIN_SHIFT_DISTANCE
                ):
                    continue
                interpolation_list.append(new_interpolation)

        interpolation_list.sort()
        segment_list: list[float] = [
            interpolation_list[i]
            if i == 0
            else interpolation_list[i] - interpolation_list[i - 1]
            for i in range(len(interpolation_list))
        ]
        segment_list.append(rc.effective_width - interpolation_list[-1])
        return segment_list


class SmoothShift(Animation):
    def __init__(
        self,
        mobject: Mobject,
        *vectors: np.ndarray,
        start_velocity: float = 1.0,
        end_velocity: float = 1.0,
        suspend_mobject_updating: bool = True,
        **kwargs,
    ) -> None:
        self.mob_coordinates: np.ndarray = mobject.get_center()
        self.total_vector: np.ndarray = reduce(op.add, vectors)
        self.shift_distance: float = float(np.linalg.norm(self.total_vector))
        self.start_velocity: float = start_velocity
        self.end_velocity: float = end_velocity
        super().__init__(
            mobject,
            run_time=self.shift_distance * 2 / (start_velocity + end_velocity),
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs,
        )

    def interpolate_mobject(self, alpha: float) -> None:
        s = (
            (self.start_velocity - self.end_velocity) * self.run_time / (2 * PI)
        ) * math.sin(PI * alpha) + (
            self.start_velocity + self.end_velocity
        ) / 2 * self.run_time * alpha

        self.mobject.move_to(
            self.mob_coordinates + self.total_vector * (s / self.shift_distance)
        )


class Test(Scene):
    def construct(self):
        config.frame_x_radius = FRAME_X_RADIUS
        config.frame_y_radius = FRAME_Y_RADIUS

        self.camera.background_color = BACKGROUNG_COLOR
        self.camera.frame_height = FRAME_HEIGHT
        self.camera.frame_width = FRAME_WIDTH
        # self.add(
        #     NumberPlane(
        #         x_range=(
        #             -config["frame_x_radius"],
        #             config["frame_x_radius"],
        #             1,
        #         ),
        #         y_range=(
        #             -config["frame_y_radius"],
        #             config["frame_y_radius"],
        #             1,
        #         ),
        #     )
        # )

        rectochain_number = 8
        rc_list = [RectoChain() for _ in range(rectochain_number)]
        rc_list[0].to_corner(buff=0.0)
        for i in range(1, rectochain_number):
            rc_list[i].next_to(
                rc_list[i - 1], direction=UP, buff=RECTOCHAIN_SPAN
            ).to_edge(edge=RIGHT if i % 2 == 1 else LEFT, buff=0.0)
        animation_list = []
        for i in range(rectochain_number):
            rc = rc_list[i]
            direction_vector = LEFT if i % 2 == 0 else RIGHT
            segment_list = GPT4.get_segment_list(rc)
            velocity_list = [
                random.uniform(0.25, 4.0) for _ in range(len(segment_list) - 1)
            ]
            animation_list.append(
                Succession(
                    *(
                        SmoothShift(
                            rc
                            if index == 0
                            else rc.shift(direction_vector * segment_list[index - 1]),
                            direction_vector * value,
                            start_velocity=1.0
                            if index == 0
                            else velocity_list[index - 1],
                            end_velocity=1.0
                            if index == len(segment_list) - 1
                            else velocity_list[index],
                        )
                        for index, value in enumerate(segment_list)
                    ),
                    run_time=RUN_TIME,
                )
            )

        self.play(AnimationGroup(*animation_list))


with tempconfig(
    {
        "preview": True,
        "pixel_height": PIXEL_HEIGHT,
        "pixel_width": PIXEL_WIDTH,
        "frame_rate": FRAME_RATE,
        "output_file": f"{GPT4.__name__.lower()}_{PIXEL_WIDTH}x{PIXEL_HEIGHT}_{int(FRAME_RATE)}fps_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        # "output_file": f"{Test.__name__.lower()}_{PIXEL_WIDTH}x{PIXEL_HEIGHT}_{int(FRAME_RATE)}fps",
    }
):
    scene = GPT4()
    scene.render()

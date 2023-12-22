from manim import *
import sympy as sp
from test import Find_x_Star

class Newtons1DOptimization(Scene):

    def construct(self):
        my_plane = NumberPlane(
            x_range=[-5, 5, 1],
            x_length=10,
            y_range=[-5, 5, 1],
            y_length=10,
            axis_config={"color": WHITE},
        )
        my_plane.add_coordinates()

        x = sp.symbols('x')
        func = x ** 4 / 20 + x / 4 + 1
        my_function = my_plane.plot(lambda x: 1 / 20 * x ** 4 + 1 / 4 * x + 1,
                                    x_range=(-3, 3, 0.1)).set_z_index(1)
        label = MathTex("f(x)= \\frac{x^4}{20} + \\frac{x}{4} + 1")
        label.shift(LEFT * 5, UP * 2.5)
        self.play(DrawBorderThenFill(my_plane))
        self.play(Create(my_function), Write(label))
        self.wait(2)

        x_k = -3
        x_star = Find_x_Star(func, x)
        taylor_approximation = func.series(x, x_k, 3).removeO()
        taylor_func = sp.lambdify(x, taylor_approximation, "numpy")
        taylor_plot = my_plane.plot(taylor_func,
                                    x_range=(-3, 3, 0.1),
                                    color=RED).set_z_index(1)

        taylor_label = MathTex("f(x) \\approx f(x_k) + f'(x_k)(x-x_k) + \\frac{f''(x_k)}{2}(x-x_k)^2").set_z_index(1)
        taylor_label.shift(RIGHT * 4, DOWN * 1.5)
        self.play(Create(taylor_plot), Write(taylor_label))

        f_prime = sp.diff(func, x)
        f_double_prime = sp.diff(f_prime, x)
        for i in range(5):
            first_derivative_at_x = f_prime.subs(x, x_k)
            second_derivative_at_x = f_double_prime.subs(x, x_k)

            # Check if the second derivative is non-zero to avoid division by zero
            if second_derivative_at_x != 0:
                taylor_approximation = func.series(x, x_k, 3).removeO()
                taylor_func = sp.lambdify(x, taylor_approximation, "numpy")
                new_line = my_plane.plot(taylor_func,
                                         x_range=(-3, 3, 0.1),
                                         color=RED).set_z_index(1)
                self.play(Transform(taylor_plot, new_line))

                x_k1 = x_k - first_derivative_at_x / second_derivative_at_x
                x_k = x_k1
                dot = Dot(my_plane.c2p(x_k, 0))
                self.add(dot)
                dot2 = Dot(my_plane.c2p(x_k, taylor_func(x_k)))

                self.add(dot2)
                self.wait(1)

            else:
                print("Division by zero. Stopping the iteration.")
                break

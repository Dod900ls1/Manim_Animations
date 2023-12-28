from manim import *
import sympy as sp
from NewtonsOptimization import Find_x_Star


class Newtons1DOptimization(MovingCameraScene):
    # Helper function to fix the sizes of dots based on the camera frame
    def fix_dots_sizes(self):
        dots = [d for d in self.mobjects if isinstance(d, Dot)]
        dot_scale = dots[0].width / self.camera.frame.width

        def updater(dot, dt):
            dot.set_width(dot_scale * self.camera.frame.width)

        for dot in dots:
            dot.add_updater(updater)

    # Helper function to fix the linewidth of the NumberPlane based on the camera frame
    def fix_numberplane_linewidth(self):
        numberplanes = [d for d in self.mobjects if isinstance(d, NumberPlane)]
        line_scale = numberplanes[0].x_axis.stroke_width / self.camera.frame.width

        def updater(np, dt):
            for l in list(np.background_lines) + [np.get_x_axis(), np.get_y_axis()]:
                l.set_stroke(width=line_scale * self.camera.frame.width)

        for np in numberplanes:
            np.add_updater(updater)

    def construct(self):
        # Set up the NumberPlane
        my_plane = NumberPlane(
            x_range=[-5, 5, 1],
            x_length=10,
            y_range=[-5, 5, 1],
            y_length=10,
            axis_config={"color": WHITE},
        )
        my_plane.add_coordinates()

        # Define the function and plot it
        x = sp.symbols('x')
        func = x ** 4 / 20 + x / 4 + 1
        my_function = my_plane.plot(lambda x: 1 / 20 * x ** 4 + 1 / 4 * x + 1,
                                    x_range=(-3, 3, 0.1)).set_z_index(1)
        label = MathTex("f(x)= \\frac{x^4}{20} + \\frac{x}{4} + 1")
        label.shift(LEFT * 5, UP * 2.5)

        # Display the NumberPlane and the function plot
        self.play(DrawBorderThenFill(my_plane))
        self.play(Create(my_function), Write(label))
        self.wait(2)

        # Initial values
        x_k = -3
        x_star = Find_x_Star(func, x_k)

        # Mark the minimum point on the graph
        min_point = Dot(my_plane.c2p(x_star, 0), radius=0.05)
        min_point_label = MathTex("x^*").next_to(min_point, DOWN)
        self.add(min_point, min_point_label)

        # Initial Taylor approximation
        taylor_approximation = func.series(x, x_k, 3).removeO()
        taylor_func = sp.lambdify(x, taylor_approximation, "numpy")
        taylor_plot = my_plane.plot(taylor_func,
                                    x_range=(-3, 3, 0.1),
                                    color=RED).set_z_index(1)

        # First and second derivatives
        f_prime = sp.diff(func, x)
        f_double_prime = sp.diff(f_prime, x)

        while abs(x_k - x_star) > 0.001:
            first_derivative_at_x = f_prime.subs(x, x_k)
            second_derivative_at_x = f_double_prime.subs(x, x_k)

            # Check if the second derivative is non-zero to avoid division by zero
            if second_derivative_at_x != 0:
                # Update Taylor approximation
                taylor_approximation = func.series(x, x_k, 3).removeO()
                taylor_func = sp.lambdify(x, taylor_approximation, "numpy")
                new_line = my_plane.plot(taylor_func,
                                         x_range=(-3, 3, 0.1),
                                         color=RED).set_z_index(1)
                self.play(Transform(taylor_plot, new_line))

                # Update x_k based on Newton's method
                x_k1 = x_k - first_derivative_at_x / second_derivative_at_x
                x_k = x_k1

                # Mark the current point and its corresponding y-value on the graph
                dot = Dot(my_plane.c2p(x_k, 0), radius=0.05)
                self.add(dot)
                dot2 = Dot(my_plane.c2p(x_k, taylor_func(x_k)), radius=0.05)
                self.add(dot2)
                self.wait(1)

                # Check if the iteration is close enough to the minimum point
                if abs(x_k - x_star) < 0.001:
                    # Save camera state and perform some visual adjustments
                    self.camera.frame.save_state()
                    self.fix_dots_sizes()
                    self.fix_numberplane_linewidth()
                    self.play(self.camera.frame.animate.move_to(dot).set(width=dot.width * 2))
                    self.wait(0.3)

                    # Create a line from "dot" to "min_point"
                    distance_line = Line(dot.get_center(), min_point.get_center())

                    distance = np.linalg.norm(np.array(dot.get_center()) - np.array(min_point.get_center()))

                    # Create the label for the distance
                    distance_label = MathTex(
                        f"\\lvert \\text{{dot}} - \\text{{min\_point}} \\rvert = {distance:.7f} < \\epsilon").scale(
                        0.02)
                    distance_label.next_to(distance_line, UP * 0.001)

                    # Display the label
                    self.play(Create(distance_label))

                    self.wait(2)
                    self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=14))
                    self.wait(1)

            else:
                print("Division by zero. Stopping the iteration.")
                break

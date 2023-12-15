from manim import *


class GoldenSectionSearch(Scene):
    def construct(self):
        # Create the number line
        my_plane = NumberPlane(
            x_range=[-5, 5, 1],
            x_length=10,
            y_range=[-5, 5, 1],
            y_length=10,  # y-axis range from -2 to 2 with step 1
            axis_config={"color": WHITE},
        )
        my_plane.add_coordinates()

        # Add the axes to the scene
        def func(x):
            return x ** 4 + x ** 3 + x

        # Plot the function and add label
        my_function = my_plane.plot(lambda x: x ** 4 + x ** 3 + x,
                                    x_range=(-3, 3, 0.1)).set_z_index(1)
        label = MathTex("f(x)=x^4 + x^3 + x")
        label.shift(LEFT * 3.5, UP * 2.5)
        self.play(DrawBorderThenFill(my_plane))
        self.play(Create(my_function), Write(label))

        # Golden Section Search parameters
        a = -2
        b = 2
        u_1 = a + (3 - 5 ** 0.5) * (b - a) / 2
        u_2 = a + (5 ** 0.5 - 1) * (b - a) / 2
        dot_colors = [GREEN, RED, ORANGE, DARK_BLUE]

        dots_on_x_axis = VGroup()
        # Mark points on x-axis only
        start_points = [a, b, u_1, u_2]
        labels = ['a', 'b', 'u_1', 'u_2']
        line = Line(my_plane.c2p(u_2, 0), my_plane.c2p(u_2, func(u_2)), color=BLUE)
        line1 = Line(my_plane.c2p(u_1, 0), my_plane.c2p(u_1, func(u_1)), color=BLUE)

        # Perform the golden section search animation
        for i in range(6):  # Adjust the number of iterations as needed
            print(f"Iteration number: {i}")

            # Start scene
            if i == 0:
                labels_group = VGroup()
                for j, point in enumerate(start_points):
                    dot = Dot(my_plane.c2p(point, 0), color=dot_colors[j])  # Place dots on the x-axis (y = 0)
                    self.add(dot)
                    self.wait(1)
                    dots_on_x_axis.add(dot)
                    label = Text(labels[j], font_size=30, color=dot_colors[j]).next_to(dot, RIGHT,
                                                                                       buff=0.05).set_z_index(1)
                    labels_group.add(label)

                # Adjust the positions to form a column on the right-upper corner
                labels_group.arrange(DOWN, aligned_edge=RIGHT, buff=0.05)
                labels_group.shift(UP * 2.2 + RIGHT * 2.2)  # Adjust as needed

                self.play(Create(labels_group))
                self.wait(2)

                self.play(Create(line), Create(line1))

            # Update values for the next iteration
            if func(u_1) < func(u_2):
                print(f"{func(u_1)} < {func(u_2)}")
                b = u_2
                line.set_color(RED)

                self.wait(1)
                self.remove(*dots_on_x_axis)

                # Swap dots
                dots_on_x_axis[1] = Dot(my_plane.c2p(b, 0), color=RED)
                swap = u_1
                u_2 = swap
                dots_on_x_axis[3] = Dot(my_plane.c2p(u_2, 0), color=DARK_BLUE)
                u_1 = a + (3 - 5 ** 0.5) * (b - a) / 2
                dots_on_x_axis[2] = Dot(my_plane.c2p(u_1, 0), color=ORANGE)
                self.add(*dots_on_x_axis)

                # Simultaneously change the color of the line and transform it
                self.play(Succession(Transform(line, line1), ApplyMethod(line.set_color, BLUE)), run_time=1)
                new_line = Line(my_plane.c2p(u_1, 0), my_plane.c2p(u_1, func(u_1)), color=BLUE)
                self.remove(line1)
                self.play(Transform(line1, new_line))

            else:
                a = u_1
                line1.set_color(RED)

                self.wait(1)

                # Remove only dots and lines associated with u_2
                self.remove(*dots_on_x_axis)

                dots_on_x_axis[0] = Dot(my_plane.c2p(a, 0), color=GREEN)
                swap = u_2
                u_1 = swap
                dots_on_x_axis[3] = Dot(my_plane.c2p(u_1, 0), color=ORANGE)
                u_2 = a + (5 ** 0.5 - 1) * (b - a) / 2
                dots_on_x_axis[2] = Dot(my_plane.c2p(u_2, 0), color=DARK_BLUE)
                self.add(dots_on_x_axis)

                # Simultaneously change the color of the line and transform it
                self.play(Succession(Transform(line1, line), ApplyMethod(line1.set_color, BLUE)), run_time=1)
                new_line = Line(my_plane.c2p(u_2, 0), my_plane.c2p(u_2, func(u_2)), color=BLUE)
                self.remove(line)
                self.play(Transform(line, new_line))

        self.wait(2)  # Wait at the end of the animation

# To run this code write "manim -pql GoldenRationOptimization.py GoldenSectionSearch" in terminal

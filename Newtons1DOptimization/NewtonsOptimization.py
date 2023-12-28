import sympy as sp


def Find_x_Star(f, x_k) -> float:
    x = sp.symbols('x')
    f_prime = sp.diff(f, x)
    f_double_prime = sp.diff(f_prime, x)

    for i in range(100):
        first_derivative_at_x = f_prime.subs(x, x_k).evalf()
        second_derivative_at_x = f_double_prime.subs(x, x_k).evalf()

        # Check if the second derivative is non-zero to avoid division by zero
        if second_derivative_at_x != 0:
            x_k1 = x_k - first_derivative_at_x / second_derivative_at_x
            x_k = x_k1
        else:
            print("Division by zero. Stopping the iteration.")
            break
    return float(x_k)


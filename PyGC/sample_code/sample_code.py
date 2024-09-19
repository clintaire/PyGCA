def calculate():
    a = 5
    b = a + 10
    c = a = 15  # This should raise an issue (using = instead of ==)
    d = b - 5

def compare_values(x, y):
    return x = y  # Incorrect, should be '=='
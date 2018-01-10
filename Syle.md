#Style

If you are contributing to the repository, please conform to styles
guide in the following order:

1. Any styles explicitly stated in this guide
2. The main Autocomm style guide
3. The latest PEP8 guidelines

#Functions

Follow PEP8 guidelines about docstring documentation. Include a 
docstring for every function, as well as its parameters and
return values. Additionally, always include asserts to ensure
that your inputs are expected, and give a reasonable error message.
Finally, include parameter type annotations in the function 
signature and specify the return type.


Specify optional parameters with [optional] and typing with 
\<type\>.

An example is below.

```python
def add(x: int, y: int, factor: int=1) -> int:
    """
    Returns the sum of two numbers.
    
    :param x: <int>, first number to add
    :param y: <int>, second number to add
    :param factor: [optional] <int>, factor to scale sum by
    :return: <int>, sum of two numbers
    """
    return (x + y) * factor

```
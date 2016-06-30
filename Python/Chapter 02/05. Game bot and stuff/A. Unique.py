import sys


def unique(iterable):
    if iterable:
        begining = True
        iterator = iter(iterable)
        previous_element = next(iterator)
        unique_elements = [previous_element]
        try:
            for element in iterator:
                if element == previous_element:
                    continue
                else:
                    unique_elements.append(element)
                    previous_element = element
        except (ValueError, StopIteration):
            return unique_elements
    else:
        return []
    return unique_elements


exec(sys.stdin.read())

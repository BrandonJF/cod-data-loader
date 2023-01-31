from requirementtuple import Requirement
TestData = {
    'A': [],
    'B': [Requirement('A', 0)],
    'C': [Requirement('B', 0), Requirement('D', 0)],
    'D': [Requirement('E', 0)],
}

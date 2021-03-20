letters = {
    "A": -1,
    "B": -1,
    "C": -1,
    "D": -1,
    "E": -1,
    "F": -1,
    "G": -1,
    "H": -1,
    "I": -1,
    "J": -1,
    "K": -1,
    "L": -1,
    "M": -1,
    "N": -1,
    "O": -1,
    "P": -1,
    "Q": -1,
    "R": -1,
    "S": -1,
    "T": -1,
    "U": -1,
    "V": -1,
    "X": -1,
    "Y": -1,
    "W": -1,
    "Z": -1,
}
data = {}
domains = {}
variables = []
constraints = {}


def readInputFile(path):
    data = {}
    with open(path, "r") as inputFile:
        firstLine = inputFile.readline()
        data["LHS"] = firstLine.split("=")[0].split("+")
        data["RHS"] = firstLine.split("=")[-1]
    return data


def getVariables(data):
    variables = []
    for operand in data["LHS"]:
        variables += list(operand)
    variables += list(data["RHS"])
    return list(set(variables))


def consistent(variable, assignment):
    for constraint in constraints[variable]:
        if not constraint.satisfied(assignment):
            return False
    return True


# def backtracking_search(assignment):
#     if len(assignment) == len(variables):
#         return assignment

#     # get all variables in the CSP but not in the assignment
#     unassigned = [v for v in variables if v not in assignment]

#     # get the every possible domain value of the first unassigned variable
#     first = unassigned[0]
#     for value in domains[first]:
#         local_assignment = assignment.copy()
#         local_assignment[first] = value
#         # if we're still consistent, we recurse (continue)
#         if consistent(first, local_assignment):
#             result = backtracking_search(local_assignment)
#             # if we didn't find the result, we will end up backtracking
#             if result is not None:
#                 return result
#     return None


def getDomains(letters):
    possibleDigits = {}
    for letter in letters:
        possibleDigits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # no leading 0s
    maxOperandLength = len(data["LHS"][0])
    possibleDigits[data["LHS"][0][0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for operand in data["LHS"][1:]:
        possibleDigits[operand[0]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if maxOperandLength < len(operand):
            maxOperandLength = len(operand)
    if len(data["RHS"]) > maxOperandLength:
        possibleDigits[str(list(data["RHS"])[0])] = [1]
    else:
        possibleDigits[str(list(data["RHS"])[0])] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    return possibleDigits


data = readInputFile("input.txt")
variables = getVariables(data)
domains = getDomains(variables)

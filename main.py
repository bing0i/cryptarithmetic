data = {}
domains = {}
variables = []


def readInputFile(path):
    data = {}
    with open(path, "r") as inputFile:
        firstLine = inputFile.readline()
        data["LHS"] = firstLine.split("=")[0].split("+")
        data["RHS"] = firstLine.split("=")[-1]
    return data


def writeOutputFile(path, result):
    with open(path, "w") as outputFile:
        if isinstance(result, str):
            outputFile.write(result)
        else:
            outputFile.write("".join([str(v) for v in result.values()]))
    return True


def getVariables(data):
    variables = []
    for operand in data["LHS"]:
        variables += list(operand)
    variables += list(data["RHS"])
    return list(set(variables))


def getDomains(letters):
    possibleDigits = {}
    for letter in letters:
        possibleDigits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

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


def isSatisfied(assignedVariables):
    if len(set(assignedVariables.values())) < len(assignedVariables):
        return False

    if len(assignedVariables) == len(variables):
        unit = 1
        result = []
        tmpSum = 0
        for index in range(len(data["LHS"])):
            for letter in reversed(data["LHS"][index]):
                tmpSum += assignedVariables[letter] * unit
                unit = unit * 10
            result.append(tmpSum)
            tmpSum = 0
            unit = 1

        rhsSum = 0
        unit = 1
        for letter in reversed(data["RHS"]):
            rhsSum += assignedVariables[letter] * unit
            unit = unit * 10

        lhsSum = 0
        for index in range(len(result)):
            lhsSum += result[index]

        return lhsSum == rhsSum

    return True


def backtrack(assignedVariables):
    if len(assignedVariables) == len(variables):
        return assignedVariables

    unassignedVariables = [v for v in variables if v not in assignedVariables]

    firstUnassignedVariable = unassignedVariables[0]
    for value in domains[firstUnassignedVariable]:
        localAssignedVariables = assignedVariables.copy()
        localAssignedVariables[firstUnassignedVariable] = value
        if isSatisfied(localAssignedVariables):
            result = backtrack(localAssignedVariables)
            if result is not None:
                return result
    return None


def sortResult(result):
    if result == None:
        return "No solution"
    sortedKeys = sorted(result.keys())
    newResult = {}
    for key in sortedKeys:
        newResult[key] = result[key]
    return newResult


data = readInputFile("input.txt")
variables = getVariables(data)
domains = getDomains(variables)

result = sortResult(backtrack({}))
writeOutputFile("output.txt", result)
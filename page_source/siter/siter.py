#!/usr/bin/env python3

import re

def assertIsObject(object, objectName):
    if not isinstance(object, dict):
        raise Exception(objectName, "is not an object")

def assertHas(object, field, scopeName="global"):
    assertIsObject(object, scopeName)
    if field not in object:
        raise Exception(field, "is not a recognized identifier in", scopeName)

def parseExpression(text, globalObject):
    object = globalObject
    objectName = "global"
    if len(text) == 0:
        return globalObject
    firstChar = text[0]
    if firstChar is '"':
        text = text[1:]
        literal = ""
        while True:
            if len(text) == 0:
                raise Exception("Expected an end to the string literal", literal)
            letter = text[0]
            text = text[1:]
            if letter is '"':
                break
            literal += letter
        object = literal
        objectName = '"{}"'.format(literal)

    parts = text.split('.')

    for step in parts:
        assertHas(object, step, scopeName=objectName)
        object = object[step]
        objectName+="."+step
    return object

def handleLet(text, globalObject, override=False):
    parts = [text.strip() for text in text.split('=')]
    if len(parts) < 2:
        raise Exception("expected an equals sign in let/override statement")

    var, expr = parts[0], "=".join(parts[1:])
    var = var.split('.')[-1]
    if not re.match('^[a-zA-Z][a-zA-Z0-9]*$', var) or var in handlers:
        raise Exception("Illegal variable name:", var)
    object = parseExpression(parts[0][:-len(var)-1], globalObject)
    exists = var in object
    if exists is not override:
        raise Exception("use override iff variable already exists! Name:", var)
    object[var] = parseExpression(expr, globalObject)

def doAppend(text, globalObject):
    pass

def printExpr(text, globalObject):
    print(parseExpression(text, globalObject))

handlers = {
    "#": lambda text, globalObject: None,
    "let": handleLet,
    "override": lambda text, globalObject: handleLet(text, globalObject, override=True),
    "append": doAppend,
    "debug": printExpr
}

def parseLine(text, globalObject):
    for key, value in handlers.items():
        if text.startswith(key):
            value(text[len(key):].strip(), globalObject)

lineGotTo = 0
fileGotTo = None
def parseSiter(text, fileName):
    global fileGotTo, lineGotTo
    old = (fileGotTo, lineGotTo)
    fileGotTo, lineGotTo = (fileName, 0)

    globalObject = {}

    for line in text:
        lineGotTo += 1
        parseLine(line, globalObject)

    fileGotTo, lineGotTo = old
    return globalObject

def main():
    confObj = {}
    with open("conf.siter") as conf:
        confObj = parseSiter(conf, "conf.siter")

def tryMain():
    try:
        main()
    except Exception as e:
        print("got to line", lineGotTo, "in file", fileGotTo, "before encountering:")
        print("siter: error:", *e.args)

if __name__ == "__main__":
    tryMain()

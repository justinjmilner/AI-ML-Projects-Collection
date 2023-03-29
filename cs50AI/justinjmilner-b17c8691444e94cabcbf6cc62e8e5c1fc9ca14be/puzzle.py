from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledge = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
)


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    knowledge,

    # If A is Knight
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is Knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    knowledge,

    # If A is Knight
    Implication(AKnight, And(AKnave, BKnave)),

    # If A is Knave
    Implication(AKnave, Not(And(AKnave, BKnave)))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    knowledge,

    # If A is Knight
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # If A is Knave
    Implication(AKnave, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # If B is Knight
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # If B is Knave
    Implication(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    knowledge,

    # If A is Knight
    Implication(AKnight, Or(AKnight, AKnave)),

    # If A is Knave
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # If B is Knight
    Implication(BKnight, And(Implication(Or(AKnight, AKnave), AKnave), CKnave)),

    # If B is Knave
    Implication(BKnave, And(Implication(Or(AKnight, AKnave), Not(AKnave)), Not(CKnave))),

    # If C is Knight
    Implication(CKnight, AKnight),

    # If C is Knave
    Implication(CKnave, Not(AKnight))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

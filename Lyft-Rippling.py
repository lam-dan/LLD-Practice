# Are You Referring to the "Simple Database" Problem?
# Based on your description, it sounds like you are referring to a well-known type of question sometimes called the "Simple Database" or "In-Memory Transactional Key-Value Store" problem, which has been reported by candidates as appearing in Lyft's laptop interview round.
# Typical Structure of the Question
# Part 1: Read from stdin and write to stdout
# You are asked to implement a simple key-value store that reads commands from standard input (stdin) and writes results to standard output (stdout).
# Commands might include: SET key value, GET key, UNSET key, and END (to terminate the program).
# You need to parse each line from stdin, execute the command, and print the result to stdout.
# Part 2: BEGIN, ROLLBACK, and COMMIT
# The second part introduces transaction support.
# You add commands like BEGIN (start a transaction), ROLLBACK (undo changes since the last BEGIN), and COMMIT (make all changes permanent).
# This requires you to manage a stack or history of changes so you can undo or commit as needed.

# Example Input/Output
# javascript
# SET a 10
# GET a
# BEGIN
# SET a 20
# GET a
# ROLLBACK
# GET a
# END

# Expected Output:
# javascript
# 10
# 20
# 10
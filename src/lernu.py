# -*- coding: utf-8 -*-

import sys
from string import strip
from random import shuffle, sample, choice
from optparse import OptionParser

class Dictionary:
    def __init__(self):
        self.answers = []
        self.questions = []
        self.comments = []
        self.confirmation = "!lernu"

    def __len__(self):
        return len(self.answers)

    def add(self, answer, question, comment):
        self.answers.append(answer)
        self.questions.append(question)
        self.comments.append(comment)

    def show(self):
        for i in xrange(len(self)):
            print """%d:
        Question: %s
        Answer: %s
        Comment: %s""" %(i, self.questions[i], self.answers[i], self.comments[i])

    def update(self, filename):
        try:
            f = open(filename)
        except IOError:
            sys.exit("Could not open file")
        if f.readline().strip() != self.confirmation:
            sys.exit("Invalid format of the file")
        for line in f:
            s = line.strip()
            if not s or s[0] == "#":
                continue
            try:
                cm = s.index("#")
            except:
                cm =len(s)
            try:
                df = s.index("==")
            except:
                continue
            answer = s[:df].strip()
            question = s[df+2:cm].strip()
            comment = s[cm+1:].strip()
            self.add(answer, question, comment)

def ask(n):
    print
    print "Question: %s" % src.questions[n]
    attempts = settings["attempts"]
    while attempts:
        attempt = raw_input("Your answer: ")
        if attempt == src.answers[n]:
            print "Right!"
            break
        else:
            attempts -= 1
            print "Wrong."
    if not attempts:
        print "Right answer: %s" % src.answers[n]
        if settings["showComments"] and src.comments[n]: print "Comment: %s" % src.comments[n]
    return int(attempts > 0)

def test(n):
    variants = sample(xrange(len(src)), settings["varNum"])
    if n in variants:
        correct = variants.index(n)
    else:
        correct = choice(xrange(settings["varNum"]))
        variants[correct] = n
    print
    print "Question: %s" % src.questions[n]
    for i in xrange(settings["varNum"]):
        print "%d) %s" %(i, src.answers[variants[i]])
    attempts = settings["attempts"]
    while attempts:
        attempt = raw_input("Number of answer: ")
        try:
            attempt = int(attempt)
        except:
            print "Enter only the number, please"
            continue
        if attempt == correct:
            print "Right!"
            break
        else:
            attempts -= 1
            print "Wrong."
    if not attempts:
        print "Right answer: %d (%s)" %(correct,  src.answers[n])
        if settings["showComments"] and src.comments[n]:
            print "Comment: %s" % src.comments[n]
    return int(attempts > 0)

def pack(sequence):
    if settings["random"]:
        shuffle(sequence)
    scores = 0
    mistakes = []
    for i in sequence:
        if settings["test"]:
            correct = test(i)
        else:
            correct = ask(i)
        if correct:
            scores +=1
        else:
            mistakes.append(i)
    print "All: %d; Correct: %d" % (len(sequence), scores)
    if mistakes:
        repeat = raw_input("Do you want to check questions you make mistakes in again? (y/N) ")
        if repeat in settings["positiveResponses"]:
            pack(mistakes)

def update_settings():
    usage = "usage: %prog [options] FILE [FILE]..."
    parser = OptionParser(usage=usage)
    parser.add_option("-a", "--attempts", dest="attempts",
            help="NUMBER of attempts to guess", metavar="NUM")
    parser.add_option("-r", "--random", dest="random",
            action="store_true", help="shuffle questions")
    parser.add_option("-c", "--comments", dest="showComments",
            action="store_true", help="print comments after mistakes")
    parser.add_option("-t", "--test", dest="test", action="store_true",
            help="use tests insted of questions")
    parser.add_option("-v", "--variables", dest="varNum",
            help="NUMBER of variables in test mode", metavar="NUM")
    parser.add_option("-s", "--start", dest="start",
            help="start with NUM quetion", metavar="NUM")
    parser.add_option("-e", "--end", dest="end",
            help="end with NUM question", metavar="NUM")
    (opts, args) = parser.parse_args()
    if args:
        for filename in args:
            src.update(filename)
        if opts.attempts:
            settings["attempts"] = opts.attempts
        if opts.random:
            settings["random"] = opts.random
        if opts.showComments:
            settings["showComments"] = opts.showComments
        if opts.test:
            settings["test"] = opts.test
        if opts.varNum:
            settings["varNum"] = opts.varNum
        if opts.start:
            settings["start"] = opts.start
        if opts.end:
            settings["end"] = opts.end
        else:
            settings["end"] = len(src)
    else:
        parser.error("incorrect number of arguments")

if __name__ == "__main__":
    src = dictionary()
    settings = {
                "random" : False,
                "attempts" : 1,
                "test" : False,
                "varNum" : 3, 
                "showComments" : False, 
                "positiveResponses" : ["yes", "y", "ok"] , 
                "start" : 0, 
                "end" : 0
    }
    update_settings()
    #src.show()
    pack(xrange(settings["start"], settings["end"]))

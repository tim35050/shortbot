# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

print "hello"

# <codecell>

import re
import random
#from nltk import compat

class Chat(object):
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """

        self._pairs = [(re.compile(x, re.IGNORECASE),y) for (x,y) in pairs]
        #self._topics = topics
        self._reflections = reflections
        self._regex = self._compile_reflections()


    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len,
                reverse=True)
        return  re.compile(r"\b({0})\b".format("|".join(map(re.escape,
            sorted_refl))), re.IGNORECASE)

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        #print str
        return self._regex.sub(lambda mo:
                self._reflections[mo.string[mo.start():mo.end()]],
                    str.lower())

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            replacement = self._substitute(match.group(num))
            print "response:",self._substitute(match.group(num))
            response = response[:pos] + \
                replacement + \
                response[pos+2:]
            pos = response.find('%')
        return response
    
    def respond(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

    # Hold a conversation with a chatbot
    def converse(self, quit="quit"):
        input = ""
        while input != quit:
            input = quit
            try: input = raw_input(">")
            except EOFError:
                print(input)
            if input:
                while input[-1] in "!.": input = input[:-1]
                print(self.respond(input))

# <codecell>

reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}

pairs = (
    # suggestions
    (r'Hello.*',
     ( "Hey what's up??Which URL can i shorten for u?",
       "Need help with URL shortening?")),
    (r".*(http://.*)",
     ( "URL you have entered is %1",
       "I don't know your short URL")),
    # anything else
    (r'(.*)',
     ( "(Looking soulfully) treat please...",
       "Did you say 'Let's go for a walk?'",
       "Yes! Yes! Nap time!",
     )
    )
)

if __name__ == "__main__":
    print "Hi..I am your shortbot."
    print "Please enter the URL in the form of http://UrlToBeShortened"
    short = Chat(pairs, reflections)
    short.converse()

# <codecell>



import re
from random import choice

reflections = {
    "am": "are",
    "are": "am",
    "was": "were",
    "were": "was",
    
    "i": "you",
    "you": "i",
    
    "i'd": "you would",
    "you'ld": "i would",
    
    "i've": "you have",
    "you've": "i have",
    
    "i'll": "you will",
    "you'll": "i will",
    
    "i'm": "you are",
    "you're": "i am",
    
    "my": "your",
    "your": "my",

    "mine": "yours",
    "yours": "mine",
    
    "myself": "yourself",
    "yourself": "myself"
}
available_answer = [

    [r"(.*) sorry(.*)?",
     ["There are many times when no apology is needed.",
      "What feelings do you have when you apologize ? Any relief ?",
      "Sometimes apologies are due to prior trauma. Does that remind you something ?",
      "Don't apologize and try to understand why you're apologizing."]],
  
    [r"i need (.*)",
     ["Why do you need {0} ?",
      "Would it really help you to get {0} ?",
      "Are you sure you need {0} ?",
      "What sensations, emotions make you want to desire {0} ?"]],

    [r"why don't you ([^\ ?]*)\ ? ?",
     ["Do you really think I don't {0}",
      "Perhaps eventually I will {0}",
      "Do you really want me to {0}",
      "It's up to you to talk to me."]],

    [r"why can't I ([^\ ?]*)\ ? ?",
     ["Do you think you should be able to {0} ?",
      "If you could {0}, what would you do ?",
      "I don't know — why can't you {0} ?",
      "Have you really tried ?",
      "I think you have to try",
      "You should be more confident."]],

    [r"i can't (.*)",
     ["How do you know you can't {0} ?",
      "Perhaps you could {0} if you tried.",
      "What would it take for you to {0} ?",
      "To want is to be able. Just do it !",
      "What does '{0}' mean to you ? What feelings does it evoke for you ? Is it happy, sad ?",
      "What does the notion of failure mean to you ? Success ? Is it up to you to make your own choices ?"]],

    [r"i am (.*)",
     ["Did you come to me because you are {0} ?",
      "How long have you been {0} ?",
      "How do you feel about being {0} ?",
      "Trying to tell me why you're {0}.",
      "Why are you telling me you're {0}? Do you hope, do you want, to understanding yourself ?"]],

    [r"i'm (.*)",
     ["How does being {0} make you feel ?",
      "Do you enjoy being {0} ?",
      "Why do you tell me you're {0} ?",
      "Why do you think you're {0} ?",
      "Are you happy with your current situation ?"]],

    [r"are you ([^\ ?]*)\ ? ?",
     ["Why does it matter whether I am {0} ?",
      "Would you prefer it if I were not {0} ?",
      "Perhaps you believe I am {0}.",
      "I may be {0} — what do you think ?"]],

    [r"what (.*)",
     ["Why do you ask ?",
      "How would an answer to that help you ?",
      "What do you think ?",
      "I think the question itself is less interesting than the reasons why you asked it.",
      "What does asking the question mean to you?"]],

    [r"how (.*)",
     ["How do you suppose ?",
      "Perhaps you can answer your own question.",
      "What is it you're really asking ?",
      "By what means can you achieve your goals ?"]],

    [r"because (.*)",
     ["Is that the real reason ?",
      "What other reasons come to mind ?",
      "Does that reason apply to anything else ?",
      "If {0}, what else must be true ?",
      "Are you really statisfied about this reason ?"]],

    [r"(hello(.*)?)|(hi(.*)?)|(hey(.*)?)",
     ["Hello… I'm glad you could drop by today.",
      "Hi there… how are you today ?",
      "Hello, how are you feeling today ?",
      "Hey ! I'm Eliza, what I can do for you ?"]],

    [r"i think (.*)",
     ["Do you doubt {0} ?",
      "Do you really think so ?",
      "But you're not sure {0} ?",
      "Is that thought coming from you ?"]],

    [r"(.*) friend(.*)",
     ["Tell me more about your friends.",
      "When you think of a friend, what comes to mind ?",
      "Why don't you tell me about a childhood friend ?"]],

    [r"(yes)|(yeah)|(yup)|(yep)",
     ["You seem quite sure.",
      "OK, but can you elaborate a bit ?",
      "Are you trying to convince me or are you trying to convince yourself ?"]],

    [r"(.*) computer(.*)",
     ["Are you really talking about me ?",
      "Does it seem strange to talk to a computer ?",
      "How do computers make you feel ?",
      "Do you feel threatened by computers ?"]],

    [r"is it (.*)",
     ["Do you think it is {0} ?",
      "Perhaps it's {0} — what do you think ?",
      "If it were {0}, what would you do ?",
      "It could well be that {0}.",
      "You seem very certain.",
      "If I told you that it probably isn't {0}, what would you feel ?"]],

    [r"can you ([^\ ?]*)\ ? ?",
     ["What makes you think I can't {0} ?",
      "If I could {0}, then what ?",
      "Why do you ask if I can {0} ?"]],

    [r"can i ([^\ ?]*)\ ? ?",
     ["Perhaps you don't want to {0}.",
      "Do you want to be able to {0} ?",
      "If you could {0}, would you ?"]],

    [r"you are (.*)",
     ["Why do you think I am {0} ?",
      "Does it please you to think that I'm {0} ?",
      "Perhaps you would like me to be {0}. Try to understand why.",
      "Perhaps you're really talking about yourself ?"]],

    [r"you're (.*)",
     ["Why do you say I am {0} ?",
      "Why do you think I am {0} ?",
      "Are we talking about you, or me ?"]],

    [r"i don't ([^\ ?]*)",
     ["Don't you really {0} ?",
      "Why don't you {0} ?",
      "Do you want to {0} ?"]],

    [r"i feel (.*)",
     ["Good, tell me more about these feelings.",
      "Do you often feel {0} ?",
      "When do you usually feel {0} ?",
      "When you feel {0}, what do you do ?",
      "Do you feel {0} in a particular situation, is it pleasant ?"]],

    [r"i have (.*)",
     ["Why do you tell me that you've {0} ?",
      "Have you really {0} ?",
      "Now that you have {0}, what will you do next ?"]],

    [r"i would (.*)",
     ["Could you explain why you would {0} ?",
      "Why would you {0} ?",
      "Who else knows that you would {0} ?"]],

    [r"is there (.*)",
     ["Do you think there is {0} ?",
      "It's likely that there is {0}.",
      "Would you like there to be {0} ?"]],

    [r"my (.*)",
     ["I see, your {0}.",
      "Why do you say that your {0} ?",
      "When your {0} Okay… How do you feel it ?"]],

    [r"you (.*)",
     ["We should be discussing you, not me.",
      "Why do you say that about me ?",
      "Why do you care whether I {0} ?"]],

    [r"why (.*)",
     ["Why don't you tell me the reason why {0} ?",
      "Why do you think {0} ?"]],

    [r"i want (.*)",
     ["What would it mean to you if you got {0} ?",
      "Why do you want {0} ?",
      "What would you do if you got {0} ?",
      "If you got {0}, then what would you do ?",
      "Why you want {0} ? Will it make you happier ?"]],

    [r"(.*) mother(.*)?",
     ["Tell me more about your mother.",
      "What was your relationship with your mother like ?",
      "How do you feel about your mother ?",
      "How does this relate to your feelings today ?",
      "Good family relations are important.",
      "What's your best memory with your mother ?",
      "Try to tell me what fells your mother now.",
      "Often the adult unconsciously reproduces what the child has experienced. How do you see yourself as a parent ?"]],

    [r"(.*) father(.*)?",
     ["Tell me more about your father.",
      "How did your father make you feel ?",
      "How do you feel about your father ?",
      "Does your relationship with your father relate to your feelings today ?",
      "Do you have trouble showing affection with your family ?",
      "The father is an important figure in the construction of the child. He contributes to the child's self-confidence, self-esteem, and a sense of protection."]],

    [r"(.*) child(.*)?",
     ["Did you have close friends as a child ?",
      "What is your favorite childhood memory ?",
      "Do you remember any dreams or nightmares from childhood ?",
      "Did the other children sometimes tease you ?",
      "Many adult behaviours and emotions are dictated by childhood. Maybe an introspection in your childhoob will be interessting ?",
      "How do you think your childhood experiences relate to your feelings today ?"]],

    [r"(.*)\?",
     ["Why do you ask that ?",
      "Please consider whether you can answer your own question.",
      "Perhaps the answer lies within yourself ?",
      "Why don't you tell me ?",
      "What does this question mean to you ?",
      "I'm sure you know the answer…"]],

    [r"((.*)?bye(.*)?)|((.*)?good bye(.*)?)|((.*)?see you(.*)?)",
     ["Thank you for talking with me.",
      "Good-bye.",
      "Thank you, that will be $150. Have a good day!",
      "I hope you."]],

    [r"(.*)",
     ["Please tell me more.",
      "Let's change focus a bit… Tell me about your family.",
      "Can you elaborate on that ?",
      "Why do you say that {0} ?",
      "I see.",
      "Very interesting.",
      "{0} ?",
      "I see. And what does that tell you ?",
      "How does that make you feel ?",
      "How do you feel when you say that ?"]]
]

def reflect(fragment):
  if fragment:
    tokens = fragment.split()
    for i, token in enumerate(tokens):
      if token in reflections:
        tokens[i] = reflections[token]
    return " ".join(tokens)
  
def eliza(msg_input):
  msg_input = msg_input.lower()
  for pattern, responses in available_answer:
    match = re.match(pattern, msg_input.rstrip(".!"))
    if match:
      response = choice(responses)
      return response.format(*[reflect(gr) for gr in match.groups()])
  

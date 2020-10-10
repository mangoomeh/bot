import random

def greet(name):
    x = [
        f"Hi {name}, I'm mangoBot!",
        f"Hello {name}, I love mango~",
        f"{name} at your service.",
        f"Good day {name}~",
        f"{name} Nice to meet you!",
        f"{name} How are you doing?",
        f"{name} What's up?",
        f"{name} Do you know that you can access my list of commands using !help ?",
        f"Zzz...(what?) oh sorry {name} I was just snoozing a lil.",
        f"{name} why are you talking to a bot? Haha, just kidding.",
        f"{name} Sorry what did you say again?",
        f"{name} Hi there!",
        f"{name} Heeeeeeyyyyyy~",
        f"{name} Whatcha doin'?",
        f"Hi {name}",
        f"{name} is talking to mangoBot~",
        f"mangoBot wants to talk to {name}",
        f"{name} wanna test how knowledgeable you are? Try using !quiz !",
        f"{name}, get a quote from me by using !quote :)",
        f"{name}, do you you can check time using !time ?"
        ]
    return random.choice(x)

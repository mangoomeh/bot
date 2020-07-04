# quiz.py
quizset = [
    "The tallest building in the world is located in which city?",  # 1
    "Which year was the original Toy Story film released in the US?",  # 2
    "Name the current UK Home Secretary",  # 3
    "What does BBC stand for?",  # 4
    "What nut is used to make marzipan?",  # 5
    "What element does 'O' represent in the periodic table?",  # 6
    "What is the name of the river that runs through Egypt?",  # 7
    "Who played Jack Sparrow in Pirates Of The Caribbean?",  # 8
    "What year was the very first model of the iPhone released?",  # 9
    "What is meteorology the study of?",  # 10
    "Which planet is the hottest in the solar system?",  # 11
    "What part of the atom has no electric charge?",  # 12
    "What is the chemical symbol for potassium?",  # 13
    "Which planet has the most gravity?",  # 14
    "Which animal can be seen on the Porsche logo?",  # 15
    "How many parts (screws and bolts included) does the average car have?",  # 16
    "Which country produces the most coffee in the world?",  # 17
    "Which country invented tea?",  # 18
    "Which brand of alcohol is Russia notoriously known for?",  # 19
    "Which European nation was said to invent hot dogs?",  # 20
    "Which country is responsible for giving us pizza and pasta?",  # 21
    "What percentage of our bodies is made up of water?",  # 22
    "What is the largest organ?",  # 23
    "What kind of cells are found in the brain?",  # 24
    "Which continent is the largest?",  # 25
    "Which desert is the largest in the world?",  # 26
    "Which two countries share the longest (or largest) international border?",  # 27
    "What is the smallest country in the world?",  # 28
    "What genre of music did Taylor Swift start in?",  # 29
    "How many Lord of the Rings films are there?",  # 30
    "Who played Jack Dawson (main male lead) in Titanic? (full name)",  # 31
    "In what year was the first episode of South Park aired?",  # 32
    "How many hearts does an octopus have?",  # 33
    "How many eyes does a bee have?",  # 34
    "What is the fastest land animal?",  # 35
    "24 x (3 + 4) + 88 = ?",  # 36
    "37 x (2 + 3) + 59 = ?",  # 37
    "17 x (5 + 4) + 44 = ?",  # 38
    "67 x (2 + 1) + 93 = ?",  # 39
    "87 x 7 + 95 = ?",  # 40
    "5! = ?",  # 41
    "1 + 2 + 3.. + 10 = ?",  # 42
    "What is my name?",  # 43
    "T or F? Pi can be written correctly as a fraction.",  # 44
    "Which is bigger? Googol or billion?",  # 45
    "T or F? All sides are equal in an Isoceles triangle.",  # 46
    "Which mathematical symbol was determined by Whiz Ferdinand Von Lindemann 1882?",  # 47
    "An angle more than 90 degrees but less than 180 degrees is called?",  # 48
    "Number system with the base of 2 is called?",  # 49
    "Polygon with eight sides called?",  # 50
    "An improper fraction is always greater than what number?",  # 51
    "The ancient Babylonians had their number system based on?",  # 52
    "Which is the most ancient? Fibonacci, Kaprekar, Mersenne or Figurate?",  # 53
    "How many prime numbers are there between 1 to 10?",  # 54
    "What comes next in the Fibonacci sequence: 0,1,1,2,3,5,8,13 __?",  # 55
    "Number system with the base of 12 is called?",  # 56
    "Which year was Minecraft released?",  # 57
    "What does Mario jump on after completing a level?",  # 58
    "What does NES stand for?",  # 59
    "Which planet size is approximately the same as Minecraft?",  # 60
    "Name the character abused by Mario",  # 61
    "In the game Overcooked, which kingdom is in danger?",  # 62
    "T or F? Epic is better than Rare.",  # 63
    "Name the arena where elite barbarians card is unlocked.",  # 64
    "How many trophies to reach PEKKA Playhouse?",  # 65
    "T or F? Each player has 3 princess towers.",  # 66
    "Highest damage spell in clash royale?",  # 67
    "What is the name of the first arena in clash royale?",  # 68
    "When was Clash Royale originally released?",  # 69
    "How many hours does Giant Chest take to open?",  # 70
    "How many hours does Magical Chest take to open?"  # 71
]

answers = [
    "Dubai",  # 1
    "1995",  # 2
    "Priti Patel",  # 3
    "British Broadcasting Corporation",  # 4
    "Almonds",  # 5
    "Oxygen",  # 6
    "Nile River",  # 7
    "Johnny Depp",  # 8
    "2007",  # 9
    "The Weather",  # 10
    "Venus",  # 11
    "Neutron",  # 12
    "K",  # 13
    "Jupiter",  # 14
    "Horse",  # 15
    "30000",  # 16
    "Brazil",  # 17
    "China",  # 18
    "Vodka",  # 19
    "Germany",  # 20
    "Italy",  # 21
    "60-65%",  # 22
    "Skin",  # 23
    "Neurons",  # 24
    "Asia",  # 25
    "Sahara",  # 26
    "Canada and USA",  # 27
    "Vatican City",  # 28
    "Country",  # 29
    "3",  # 30
    "Leonardo DiCaprio",  # 31
    "1997",  # 32
    "3",  # 33
    "5",  # 34
    "Cheetah",  # 35
    "256",  # 36
    "244",  # 37
    "197",  # 38
    "294",  # 39
    "704",  # 40
    "120",  # 41
    "55",  # 42
    "mangoBot",  # 43
    "F",  # 44
    "Googol",
    "F",  # 45
    "Pi",  # 46
    "Obtuse",  # 47
    "Binary",  # 48
    "Octagon",  # 49
    "1",  # 50
    "60",  # 51
    "Figurate",  # 52
    "4",  # 53
    "21",  # 54
    "Duodecimal",  # 55
    "2009",  # 56
    "Flag pole",  # 57
    "Nintendo Entertainment System",  # 58
    "Neptune",  # 59
    "Donkey Kong",  # 60
    "Onion Kingdom",  # 61
    "F",  # 62
    "Hog Mountain",  # 63
    "1000",  # 64
    "F",  # 65
    "Rocket",  # 66
    "Goblin Stadium",  # 67
    "4 January 2016",  # 68
    "12",  # 69
    "12"  # 70
]

import random

def get_random_word(difficulty='medium'):

    word_list = [
        ('spain', 'Country'), ('australia', 'Country'), ('thailand', 'Country'), ('canada', 'Country'), ('brazil', 'Country'),
        ('nigeria', 'Country'), ('italy', 'Country'), ('russia', 'Country'), ('japan', 'Country'), ('india', 'Country'),
        ('hamburger', 'Food'), ('pasta', 'Food'), ('sushi', 'Food'), ('taco', 'Food'), ('icecream', 'Food'),
        ('laptop', 'Technology'), ('camera', 'Technology'), ('robot', 'Technology'), ('drone', 'Technology'), ('satellite', 'Technology'),
        ('guitar', 'Thing'), ('bookshelf', 'Thing'), ('lampshade', 'Thing'), ('telescope', 'Thing'), ('shoes', 'Thing'),
        ('programming', 'Field of Study'), ('chemistry', 'Field of Study'), ('history', 'Field of Study'), ('psychology', 'Field of Study'), ('mathematics', 'Field of Study'),
        ('nintendo', 'Game'), ('minecraft', 'Game'), ('fortnite', 'Game'), ('overwatch', 'Game'), ('pokemon', 'Game'),
        ('carrot', 'Vegetable'), ('cucumber', 'Vegetable'), ('tomato', 'Vegetable'), ('broccoli', 'Vegetable'), ('spinach', 'Vegetable'),
        ('pomegranate', 'Fruit'), ('watermelon', 'Fruit'), ('strawberry', 'Fruit'), ('blueberry', 'Fruit'), ('pineapple', 'Fruit'),
        ('parrot', 'Animal'), ('elephant', 'Animal'), ('giraffe', 'Animal'), ('kangaroo', 'Animal'), ('penguin', 'Animal'),
        ('museum', 'Place'), ('library', 'Place'), ('park', 'Place'), ('beach', 'Place'), ('castle', 'Place'),
        ('computer', 'Thing'), ('glasses', 'Thing'), ('backpack', 'Thing'), ('umbrella', 'Thing'), ('bracelet', 'Thing'),
        ('blockchain', 'Technology'), ('artificialintelligence', 'Technology'), ('augmentedreality', 'Technology'), ('biotechnology', 'Technology'), ('nanotechnology', 'Technology'),
        ('football', 'Sport'), ('basketball', 'Sport'), ('tennis', 'Sport'), ('golf', 'Sport'), ('cycling', 'Sport'),
        ('lobster', 'Food'), ('steak', 'Food'), ('pizza', 'Food'), ('sushi', 'Food'), ('chocolate', 'Food'),
        ('australia', 'Country'), ('thailand', 'Country'), ('canada', 'Country'), ('brazil', 'Country'), ('nigeria', 'Country'),
        ('pyramid', 'Place'), ('eiffeltower', 'Place'), ('colosseum', 'Place'), ('machupicchu', 'Place'), ('greatwall', 'Place'),
        ('astronaut', 'Occupation'), ('doctor', 'Occupation'), ('chef', 'Occupation'), ('engineer', 'Occupation'), ('artist', 'Occupation'),
        ('penguin', 'Animal'), ('koala', 'Animal'), ('zebra', 'Animal'), ('panda', 'Animal'), ('dolphin', 'Animal')
    ]
    
    # Filter words based on difficulty level
    if difficulty == 'easy':    
        filtered_word_list = [(word, category) for word, category in word_list if len(word) <= 6]
    elif difficulty == 'medium':
        filtered_word_list = [(word, category) for word, category in word_list if 6 < len(word) <= 8]
    elif difficulty == 'hard':
        filtered_word_list = [(word, category) for word, category in word_list if 8 < len(word) <= 12]
    elif difficulty == 'veryhard':
        filtered_word_list = [(word, category) for word, category in word_list if len(word) > 12]

    if not filtered_word_list:
        raise ValueError(f'No words available for the selected difficulty level: {difficulty}')

    return random.choice(filtered_word_list)
    

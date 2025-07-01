import json
import random

def load_scraped_data(filename="scraped_data.json"):
    """Load scraped data from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found. Please run scraper.py first.")
        return []

def generate_episode_questions(episodes_data):
    """Generate questions about episode titles and summaries"""
    questions = []
    
    for episode in episodes_data:
        # Question 1: What happened in this episode?
        if episode.get('summary') and len(episode['summary']) > 20:
            question = {
                "id": len(questions) + 1,
                "question": f"What happens in the Rick and Morty episode '{episode['title']}'?",
                "correct_answer": episode['summary'],
                "type": "episode_summary"
            }
            
            # Generate distractors from other episodes
            other_summaries = [ep['summary'] for ep in episodes_data if ep != episode and ep.get('summary')]
            distractors = random.sample(other_summaries, min(3, len(other_summaries)))
            
            all_options = [episode['summary']] + distractors
            random.shuffle(all_options)
            
            question["options"] = all_options
            question["correct_index"] = all_options.index(episode['summary'])
            questions.append(question)
        
        # Question 2: Which episode is this?
        if episode.get('summary') and len(episode['summary']) > 20:
            question = {
                "id": len(questions) + 1,
                "question": f"Which Rick and Morty episode features this plot: '{episode['summary'][:100]}...'?",
                "correct_answer": episode['title'],
                "type": "episode_identification"
            }
            
            # Generate distractors from other episode titles
            other_titles = [ep['title'] for ep in episodes_data if ep != episode and ep.get('title')]
            distractors = random.sample(other_titles, min(3, len(other_titles)))
            
            all_options = [episode['title']] + distractors
            random.shuffle(all_options)
            
            question["options"] = all_options
            question["correct_index"] = all_options.index(episode['title'])
            questions.append(question)
    
    return questions

def generate_character_questions(episodes_data):
    """Generate questions about characters"""
    questions = []
    all_characters = set()
    
    # Collect all characters
    for episode in episodes_data:
        if episode.get('characters'):
            all_characters.update(episode['characters'])
    
    all_characters = list(all_characters)
    
    for episode in episodes_data:
        if episode.get('characters') and len(episode['characters']) > 1:
            # Pick a character from this episode
            character = random.choice(episode['characters'])
            
            question = {
                "id": len(questions) + 1000,  # Different ID range
                "question": f"Which character appears in the Rick and Morty episode '{episode['title']}'?",
                "correct_answer": character,
                "type": "character_episode"
            }
            
            # Generate distractors from other characters
            other_characters = [char for char in all_characters if char != character]
            distractors = random.sample(other_characters, min(3, len(other_characters)))
            
            all_options = [character] + distractors
            random.shuffle(all_options)
            
            question["options"] = all_options
            question["correct_index"] = all_options.index(character)
            questions.append(question)
    
    # Generate general character questions
    main_characters = ["Rick Sanchez", "Morty Smith", "Summer Smith", "Jerry Smith", "Beth Smith"]
    for char in main_characters:
        if char in all_characters:
            question = {
                "id": len(questions) + 1000,
                "question": f"What is {char.split()[0]}'s relationship to the main family in Rick and Morty?",
                "correct_answer": get_character_relationship(char),
                "type": "character_relationship"
            }
            
            # Generate relationship distractors
            relationships = [
                "Grandfather", "Grandson", "Daughter", "Father", "Mother",
                "Sister", "Brother", "Uncle", "Aunt", "Cousin", "Friend", "Neighbor"
            ]
            other_relationships = [rel for rel in relationships if rel != get_character_relationship(char)]
            distractors = random.sample(other_relationships, min(3, len(other_relationships)))
            
            all_options = [get_character_relationship(char)] + distractors
            random.shuffle(all_options)
            
            question["options"] = all_options
            question["correct_index"] = all_options.index(get_character_relationship(char))
            questions.append(question)
    
    return questions

def get_character_relationship(character):
    """Get the relationship of a character to the Smith family"""
    relationships = {
        "Rick Sanchez": "Grandfather",
        "Morty Smith": "Grandson", 
        "Summer Smith": "Granddaughter",
        "Jerry Smith": "Father",
        "Beth Smith": "Mother"
    }
    return relationships.get(character, "Friend")

def generate_quote_questions(episodes_data):
    """Generate questions about quotes"""
    questions = []
    
    for episode in episodes_data:
        if episode.get('quotes') and len(episode['quotes']) > 0:
            quote = random.choice(episode['quotes'])
            
            # Question: Which episode featured this quote?
            question = {
                "id": len(questions) + 2000,  # Different ID range
                "question": f"Which Rick and Morty episode features the quote: '{quote}'?",
                "correct_answer": episode['title'],
                "type": "quote_episode"
            }
            
            # Generate distractors from other episode titles
            other_titles = [ep['title'] for ep in episodes_data if ep != episode and ep.get('title')]
            distractors = random.sample(other_titles, min(3, len(other_titles)))
            
            all_options = [episode['title']] + distractors
            random.shuffle(all_options)
            
            question["options"] = all_options
            question["correct_index"] = all_options.index(episode['title'])
            questions.append(question)
    
    # Add some famous Rick and Morty quote questions
    famous_quotes = [
        {
            "quote": "Wubba lubba dub dub!",
            "character": "Rick Sanchez",
            "meaning": "I am in great pain, please help me"
        },
        {
            "quote": "I'm Pickle Rick!",
            "character": "Rick Sanchez", 
            "episode": "Pickle Rick"
        },
        {
            "quote": "Nobody exists on purpose, nobody belongs anywhere, everybody's gonna die.",
            "character": "Morty Smith",
            "context": "Existential advice"
        },
        {
            "quote": "That's slavery with extra steps!",
            "character": "Rick Sanchez",
            "context": "Microverse commentary"
        }
    ]
    
    for quote_data in famous_quotes:
        question = {
            "id": len(questions) + 2000,
            "question": f"Who says the famous line: '{quote_data['quote']}'?",
            "correct_answer": quote_data['character'],
            "type": "quote_character"
        }
        
        characters = ["Rick Sanchez", "Morty Smith", "Summer Smith", "Jerry Smith", "Beth Smith", "Mr. Meeseeks"]
        other_characters = [char for char in characters if char != quote_data['character']]
        distractors = random.sample(other_characters, min(3, len(other_characters)))
        
        all_options = [quote_data['character']] + distractors
        random.shuffle(all_options)
        
        question["options"] = all_options
        question["correct_index"] = all_options.index(quote_data['character'])
        questions.append(question)
    
    return questions

def generate_trivia_questions(episodes_data):
    """Generate general Rick and Morty trivia questions"""
    questions = []
    
    trivia_questions = [
        {
            "question": "What does 'Wubba lubba dub dub' mean in Bird Person language?",
            "correct_answer": "I am in great pain, please help me",
            "distractors": ["Hello, how are you?", "Let's go on an adventure", "I love you too"]
        },
        {
            "question": "What is the name of Rick's spaceship AI?",
            "correct_answer": "Ship",
            "distractors": ["JARVIS", "HAL", "Computer"]
        },
        {
            "question": "What dimension do Rick and Morty originally come from?",
            "correct_answer": "C-137",
            "distractors": ["C-132", "J19-Zeta-7", "35-C"]
        },
        {
            "question": "What is Jerry's job in the early seasons?",
            "correct_answer": "Unemployed",
            "distractors": ["Teacher", "Salesman", "Doctor"]
        },
        {
            "question": "What does Rick turn himself into to avoid family therapy?",
            "correct_answer": "A pickle",
            "distractors": ["A rat", "A bird", "A robot"]
        },
        {
            "question": "What is the name of the alien parasite that says 'Ooh wee!'?",
            "correct_answer": "Mr. Poopybutthole",
            "distractors": ["Mr. Meeseeks", "Squanch", "Birdperson"]
        }
    ]
    
    for i, trivia in enumerate(trivia_questions):
        question = {
            "id": len(questions) + 3000 + i,
            "question": trivia["question"],
            "correct_answer": trivia["correct_answer"],
            "type": "trivia"
        }
        
        all_options = [trivia["correct_answer"]] + trivia["distractors"]
        random.shuffle(all_options)
        
        question["options"] = all_options
        question["correct_index"] = all_options.index(trivia["correct_answer"])
        questions.append(question)
    
    return questions

def generate_all_questions():
    """Generate all types of questions"""
    episodes_data = load_scraped_data()
    
    if not episodes_data:
        return []
    
    all_questions = []
    
    # Generate different types of questions
    episode_questions = generate_episode_questions(episodes_data)
    character_questions = generate_character_questions(episodes_data)
    quote_questions = generate_quote_questions(episodes_data)
    trivia_questions = generate_trivia_questions(episodes_data)
    
    all_questions.extend(episode_questions)
    all_questions.extend(character_questions)
    all_questions.extend(quote_questions)
    all_questions.extend(trivia_questions)
    
    # Shuffle all questions
    random.shuffle(all_questions)
    
    return all_questions

def save_questions(questions, filename="quiz_questions.json"):
    """Save generated questions to JSON file"""
    with open(filename, 'w') as f:
        json.dump(questions, f, indent=2)
    print(f"Generated {len(questions)} questions and saved to {filename}")

if __name__ == "__main__":
    # Generate questions
    questions = generate_all_questions()
    
    if questions:
        # Save questions
        save_questions(questions)
        
        # Display sample questions
        print("\nSample Rick and Morty Questions:")
        for i, q in enumerate(questions[:5]):
            print(f"\nQ{i+1}: {q['question']}")
            for j, option in enumerate(q['options']):
                marker = "✅" if j == q['correct_index'] else "  "
                print(f"{chr(65+j)}. {option} {marker}")
    else:
        print("No questions generated. Please check your data.")

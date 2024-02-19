'''
Modify to load actual samples
'''


samples = [
    {
        "id": "sample1",
        "question": "What is the capital of France?",
        "baseline_answer": "The capital of France is Paris.",
        "method_answer": "Paris is the capital city of France."
    },
    {
        "id": "sample2",
        "question": "What causes rain?",
        "baseline_answer": "Rain is caused by moisture condensing in the air.",
        "method_answer": "When water vapor in the atmosphere cools and condenses, it falls as rain."
    },
    {
        "id": "sample3",
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "baseline_answer": "'To Kill a Mockingbird' was written by Harper Lee.",
        "method_answer": "The author of 'To Kill a Mockingbird' is Harper Lee."
    }
]

def get_samples():
    return samples
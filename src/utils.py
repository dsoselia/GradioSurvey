import os
import gradio as gr
import random
import json
from typing import List, Dict

from config import STATIC, OUTPUT, COLLECT_NAMES, MAKE_PUBLIC, QUESTIONS



def update_interface(
    samples: List,
    user_id: str,
    text_counter: int,
    selected_prompt_index: int,
    evaluation: str,
):
    consent_visible = True
    if text_counter >= QUESTIONS:
        consent_visible = False
    interface_visible = not consent_visible
    selected_prompt = samples[selected_prompt_index]
    baseline_text = selected_prompt["baseline_answer"]
    method_text = selected_prompt["method_answer"]
    question = selected_prompt["question"]
    question_id = selected_prompt["id"]
    file_path = os.path.join(OUTPUT, user_id + ".jsonl")
    current_data = {
        "user_id": user_id,
        "text_counter": text_counter,
        "baseline_text": baseline_text,
        "method_text": method_text,
        "evaluation": evaluation,
        "selected_prompt_index": selected_prompt_index,
        "question_id": question_id,
        "question": question,
    }
    with open(file_path, "a") as f:
        f.write(json.dumps(current_data) + "\n")

    with open(file_path, "r") as f:
        data = []
        for line in f:
            data.append(json.loads(line))
    used_question_indicies = [d["selected_prompt_index"] for d in data]
    unused_question_indicies = [
        i for i in range(len(samples)) if i not in used_question_indicies
    ]
    new_selected_prompt_index = random.choice(unused_question_indicies)
    new_text_counter = text_counter + 1

    question = samples[new_selected_prompt_index]["question"]
    baseline_text = samples[new_selected_prompt_index]["baseline_answer"]
    method_text = samples[new_selected_prompt_index]["method_answer"]

    return (
        question,
        baseline_text,
        method_text,
        new_text_counter,
        new_selected_prompt_index,
        [],
        gr.update(visible=consent_visible),
        gr.update(visible=interface_visible),
        "Prompt: " + str(new_text_counter) + " / {}".format(QUESTIONS),
    )


def validate_consent(name: str, consent_box: bool):
    random_id = str(random.randint(0, 1000000))
    if COLLECT_NAMES:
        # "all_ids.txt"
        with open(os.path.join(OUTPUT, "all_ids.txt"), "a") as f:
            f.write("User name: " + name + " ID: " + random_id + "\n")
    if consent_box:
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            random_id,
            "Session ID: {}".format(random_id),
        )
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        random_id,
        "Session ID: {}".format(random_id),
    )


def get_file(name: str) -> str:
    try:
        with open(os.path.join(STATIC, name), "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {name} was not found in the {STATIC} directory.")
    except Exception as e:
        print(f"An error occurred while reading the file {name}: {e}")

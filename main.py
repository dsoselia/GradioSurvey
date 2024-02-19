# %%

import gradio as gr
import random
import os
import json
from src.utils import update_interface, validate_consent, get_file
from src.load_samples import get_samples
from config import STATIC, OUTPUT, COLLECT_NAMES, MAKE_PUBLIC, QUESTIONS




    

# %%

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)


# %%
    
consent_text = get_file("consent.md")
question_prompt = get_file("question_prompt.md")
end_message_text = get_file("end_message.md")
# %%




with gr.Blocks() as demo:
    samples = get_samples()
    user_id = gr.State("0")
    end_message = gr.Markdown(end_message_text, visible=False)

    with gr.Column(visible=False) as interface:

        texts_counter = gr.State(0)
        selected_prompt_index = gr.State(0)

        id_label = gr.Label("Session ID: " + user_id.value)

        progress_counter = gr.Markdown("Prompt: " + str(texts_counter.value))

        text_prompt = gr.Markdown(question_prompt)
        
        text0 = gr.Textbox(value=samples[selected_prompt_index.value]["question"], label="Question", lines=7)
        text1 = gr.Textbox(value=samples[selected_prompt_index.value]["baseline_answer"], label="Model A", lines=10)
        text2 = gr.Textbox(value=samples[selected_prompt_index.value]["method_answer"], label="Model B" , lines=10)

        radio = gr.Radio(["Answer 1 is better", "Answer 2 is better", "They are about the same"], label="Evaluation")

        next_prompt = gr.Button("Next")
        samples = gr.State(samples)
        next_prompt.click(fn=update_interface, inputs=[samples, user_id, texts_counter, selected_prompt_index, radio], 
                     outputs=[text0, text1, text2, texts_counter, selected_prompt_index, radio, interface, end_message, progress_counter])
    
    with gr.Column(visible=True) as consent:
        consent_text = gr.Markdown(consent_text)
        if COLLECT_NAMES:
            name_textbox = gr.Textbox(placeholder="Your name")
        else:
            name_textbox = None
        consent_checkbox = gr.Checkbox(label="I agree to participate in this study")
        button_confirm  = gr.Button("Confirm")
        button_confirm.click(fn=validate_consent, inputs= [name_textbox, consent_checkbox ], outputs=[interface, consent, user_id, id_label] )



demo.launch(share=MAKE_PUBLIC)
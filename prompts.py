import pandas as pd
import re
from collections import Counter
import ast

system_prompt_highlight = """You are a helpful assistant and an expert in emotion analysis. When processing input text:
1. **Immutable Input**  
   - You may only insert `**` markers.  
   - Never delete, normalize, split, merge, or alter any original character (letters, apostrophes, punctuation, whitespace).

2. **Subjective Emotion Only**  
   - Only highlight spans that reveal the speaker's internal emotional state or attitude.  
   - This includes:
     - Explicit emotion words 
     - Implicit cues/phrases of feeling or reaction 
   - Do not mark:
     - Purely factual or descriptive statements 
     - Neutral descriptions of events without any sentiment

3. **Self-Check**  
   - After inserting your markers, remove all `**` and verify that the remaining text is identical to the input. Retry until it passes.
   - If the input is completely neutral, return it unchanged, with no markers.
   - Any pair of `**` must surround the entire span.

4. **Output**  
   - Return only the marked text. No headers, no metadata, no removed, added, or modified words.
"""

system_prompt_retrieve = """You are a helpful assistant. When processing input text:
1. **Immutable Input**  
   - Never delete, normalize, split, merge, or alter any original character (letters, apostrophes, punctuation, whitespace).

2. **Subjective Emotion Only**  
   - Only retrieve spans that reveal the speaker's internal emotional state or attitude.  
   - This includes:
     - Explicit emotion words 
     - Implicit cues/phrases of feeling or reaction 
   - Do not retrieve:
     - Purely factual or descriptive statements 
     - Neutral descriptions of events without any sentiment

3. **Self-Check**  
   - Verify that the remaining text is identical to the input. Retry until it passes.

4. **Output**
    - Return all spans on a single line, with each span separated by " | ". If there is only one span, do not include the " | ". No headers, no metadata, no removed, added, or modified words.
"""

def retrieve_emotion_prompt(text, cot=False):
    base_prompt = f'''*Begin Instructions*
You are given text. Some spans are emotionally expressive.
Return only the full unmodified emotionally expressive spans, and nothing else.
*End Instructions*

{text}
    '''
    cot_prompt = f'''*Begin Instructions*
You are given text. Some spans are emotionally expressive.
Return the full unmodified emotionally expressive spans.

Reason step-by-step and explore the emotion content. Output "Reasoning:" and then your reasoning steps.
After reasoning, output "Response:" followed by the spans, and nothing else.

*End Instructions*

{text}
    '''
    if not cot:
        return base_prompt
    else:
        return cot_prompt

def highlight_emotion_prompt(text, cot=False):
    base_prompt = f'''*Begin Instructions*
You are given text. Some spans are emotionally expressive. Surround the emotionally expressive spans with `**`.
Return only the full unmodified text with those markers, and nothing else.
*End Instructions*

{text}
    '''

    cot_prompt = f'''*Begin Instructions*
You are given text. Some spans are emotionally expressive. Surround the emotionally expressive spans with `**`.
Return the full unmodified text with those markers.

Reason step-by-step and explore the emotion content. Output "Reasoning:" and then your reasoning steps.
After reasoning, output "Response:" followed by the full unmodified text with those markers, and nothing else.

*End Instructions*

{text}
    '''
    if not cot:
        return base_prompt
    else:
        return cot_prompt
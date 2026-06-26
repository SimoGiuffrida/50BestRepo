from prompts import SUMMARY_SYSTEM_PROMPT, MAP_SYSTEM_PROMPT, REDUCE_SYSTEM_PROMPT

def test_all_prompts_are_non_empty_strings():
    for prompt in [SUMMARY_SYSTEM_PROMPT, MAP_SYSTEM_PROMPT, REDUCE_SYSTEM_PROMPT]:
        assert isinstance(prompt, str)
        assert len(prompt) > 50

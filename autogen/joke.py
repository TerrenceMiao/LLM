"""
"Tell a joke" by using AutoGen with local LLM - TheBloke/Llama-2-7B-Chat-GGUF, llama-2-7b-chat.Q4_K_M.gguf. Run:

$ rm -rf .cache
$ python joke.py
"""

import autogen

llm_config = {"config_list": [{
    "model": "gpt-3.5-turbo",
}]}

llm_config_local = {"config_list": [{
    "model": "llama2",
    "base_url": "http://localhost:1234/v1",
}]}

bob = autogen.AssistantAgent(
    name = "Bob",
    system_message = "You love telling jokes",
    llm_config = llm_config_local,
)

alice = autogen.AssistantAgent (
    name = "Alice",
    system_message = "Criticise the joke. After criticising is done, don't ask more jokes, just reply 'TERMINATE'",
    llm_config = llm_config_local,
)

def termination_message(msg) :
    return "TERMINATE" in str(msg.get("content", ""))

user_proxy = autogen.UserProxyAgent(
    name = "user_proxy",
    code_execution_config = {"use_docker": False},
    is_termination_msg = termination_message,
    human_input_mode = "NEVER",
)

groupchat = autogen.GroupChat(
    agents = [bob, alice, user_proxy],
    messages = [],
    speaker_selection_method = "round_robin",
)

manager = autogen.GroupChatManager(
    groupchat = groupchat,
    code_execution_config = {"use_docker": False},
    llm_config = llm_config_local,
    is_termination_msg = termination_message,
)

user_proxy.initiate_chat(
    manager,
    message = "Tell a joke",
)

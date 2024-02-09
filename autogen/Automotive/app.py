import autogen
import base64
from autogen.agentchat.contrib.multimodal_conversable_agent import (
    MultimodalConversableAgent,
)
from inventory import get_inventory, get_inventory_declaration
from mail_sender import send_mail, send_email_declaration
from flask import Flask, request, render_template

## Test Images
# https://teslamotorsclub.com/tmc/attachments/camphoto_1144747756-jpg.650059/
# https://cdn.motor1.com/images/mgl/o6rkL/s1/tesla-model-3-broken-screen.webp

app = Flask(__name__)

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")

config_list_4v = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-vision-preview"],
    },
)

llm_config = {"config_list": config_list}

use_docker = False


def is_termination_msg(data):
    has_content = "content" in data and data["content"] is not None
    return has_content and "TERMINATE" in data["content"]


user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    code_execution_config={"use_docker": use_docker},
    is_termination_msg=is_termination_msg,
    system_message="You are the boss",
    human_input_mode="NEVER",
    function_map={"get_inventory": get_inventory, "send_mail": send_mail},
)

damage_analyst = MultimodalConversableAgent(
    name="damage_analyst",
    code_execution_config={"use_docker": use_docker},
    system_message="As the Damage Analyst, your role is to accurately describe the contents of the image provided. Respond only with what is visually evident in the image, without adding any additional information or assumptions.",
    llm_config={"config_list": config_list_4v, "max_tokens": 300},
)

inventory_manager = autogen.AssistantAgent(
    name="inventory_manager",
    system_message="An inventory management specialist, this agent accesses the inventory database to provide information on the availability and pricing of spare parts.",
    llm_config={"config_list": config_list, "functions": [get_inventory_declaration]},
)

customer_support_agent = autogen.AssistantAgent(
    name="customer_support_agent",
    system_message="A Customer Suppport Agent, responsible for drafting and sending client emails following confirmation of inventory and pricing details specific to the brand (and damage if visible) of the car. It signals task completion by responding with 'TERMINATE' after the email has been sent.",
    llm_config={"config_list": config_list, "functions": [send_email_declaration]},
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, damage_analyst, inventory_manager, customer_support_agent],
    messages=[],
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    code_execution_config={"use_docker": use_docker},
    llm_config=llm_config,
)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image_url = request.form["image"]
        customer_email = request.form["email"]
        customer_message = request.form["message"]

        initiate_chat(image_url, customer_message, customer_email)

        return render_template("result.html")
    else:
        return render_template("index.html")


def initiate_chat(image_url, message, customer_email):
    print(f"Mail: {customer_email}")
    user_proxy.initiate_chat(
        manager,
        message=f"""
                Process Overview:
                Step 1: Damage Analyst identifies the car brand and the requested part (is something central, or something broken or missing) from the customer's message and image.
                Step 2: Inventory Manager verifies part availability in the database.
                Step 3: Customer Support Agent composes and sends a response email to the customer.

                Customer's Message: '{message}'
                Image Reference: '{image_url}'
                Customers Email: '{customer_email}'
            """,
    )


if __name__ == "__main__":
    app.run(debug=True)

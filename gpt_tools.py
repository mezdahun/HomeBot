import os
import openai

import html_tools
from html_tools import scrape_is_html
openai.api_key = "api_key"

self_description = """
I am David, a Wissenschaftlicher Mitarbeiter (TVL-13) in the Humboldt Universität zu Berlin, studying the field between biology, 
robotics and mathematics. I live in Berlin for 6 years and looking for a long-term apartment that I can call a home. 
As a scientist, I would like a quiet place to work and relax. A nice kitchen and a Balcony would be a plus. """

with open("test.html", "r") as f:
    html_source = f.read()

def get_GPT_application_email_prompt(html_source):
    """Scraping the HTML data, summarizing to a short text and sending to GPT as a prompt to return application email"""

    html_data_dict = scrape_is_html(html_source)

    html_details_text = ""
    for key, value in html_data_dict.items():
        if value is not None:
            html_details_text += f"---{key}: {value}\n"

    prompt = f"{self_description}\n\n Write an application email in german for the Expose with following details:\n{html_details_text}"

    prompt += "\n\n Here are the rules for writing the email:\n" \
              "1.) The email should be consise (max. 8 sentences)).\n" \
              "1.b) The email should be polite.\n" \
              "2.) It should contain a short introduction about me.\n" \
              "3.) The email should mention that I like the apartment.\n" \
              "4.a) The email should NOT have a list of the details of the apartment, except the following:\n" \
              "4.b) If the apartment details say that the flat is on a high floor, mention that this details makes " \
              "the apartment even more ideal for me.\n"\
              "4.c) Do the same as if the the flat has a renovated kitchen.\n"\
              "4.d) Do the same if it has a balcony.\n"\
              "5.) The email should mention that I like the apartment and should end with a memorable/unique closing statement " \
              "asking for a viewing appointment.\n" \
              "6.) Reason sentence by sentence and put the number of rule you used to write that sentence in parentheses" \
              " after the sentence."
    print(prompt)

    return prompt, html_data_dict

def get_GPT_application_email(id):
    html_source = html_tools.download_html_as_text(id)
    prompt, html_data_dict = get_GPT_application_email_prompt(html_source)
    # response = openai.Completion.create(
    #               model="text-davinci-003",
    #               prompt=prompt,
    #               temperature=0,
    #               max_tokens=1012,
    #             )
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1518)

    from pprint import pprint
    pprint(response)
    return response, html_data_dict

# from pprint import pprint
# pprint(get_GPT_application_email(html_source))
import streamlit as st
import pandas as pd
import openai

# Title of the web application
st.title('Excel File Upload and Analysis')

# File uploader allows user to add their own Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

def chat_with_gpt4(prompt, model="gpt-4", max_tokens=200):
    try:
        openai.api_key = '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'
        
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def generate_description(product_name, colour_code, colour_name, dp_1, dp_2, dp_3, dp_4, dp_5, dp_6, dp_7, dp_8):
    desc_prompt = f"""
    You are generating product descriptions based on individuals details of garments, these descriptions are roughly 400 characters.
    3 examples are provided below:

    ```
    Details:
    Celest Button Through Dress	Lapis	Lapis
    •  Length: 93cm (size small)	•  Relaxed Fit    	•  Printed woven viscose	• 100% viscose	•  Round Neckline  	•  Button up front is nursing friendly	•  Elbow Length Sleeve 	•  Nursing

    Description:
    "One of our best-selling styles has been recreated in this beautiful, earthy-toned and warm pattern. This shirt dress with all-over  print, cuffed elbow length sleeves, an empire seam, and gathered skirt can be buttoned down, or worn open as a duster over your swimsuit or shorts. It’s the easiest throw-on-and-go dress for expecting mothers, and those nursing thanks to the buttons! 
    
    This effortless summer dress is our go-to with sneakers or slides. "
    ```

    ```
    Details:
    Capri Shirred Dress 	WhLapis	White / Lapis
    •  Length: 99cm (size small without straps)	•  Fitted bodice with gathered skirt	•  Printed woven cotton	• 100% cotton	•  Removable straps 	•  Wear as a dress with or without the straps or wear as a skirt	•  Sleeveless 	•  Non nursing

    Description:
    "The Capri Shirred Dress is your go-to dress this season with endless styling possibilities. Framed with a square smocked bodice, removable straps, and gathered skirt with frill, this dress is a core wardrobe piece.

    Style this dress on its own – or create an alternate look by styling it as a skirt with the Clara Relaxed Shirt tied under the bust. You can also remove the shoulder for a strapless look. "
    ```

    ```
    Details:
    Logan Cargo Pant 	Choco	Chocolate 
    •  Length: 75cm inleg	• Relaxed fit	• Soft woven Tencel	• 100% lyocell	• Elastic waistband 	• Straight leg	•  Front rise 32cm (size small)	•  Leg opening 52cm (size small)

    Description:
    "We know you love our Tencel Off Duty Pant, so we reimagined the style and fit into your new favourite cargo pant! Made with an elastic waistband for built-in comfort, the Logan Cargo Pant features a straight leg, side pockets, and adjustable hems so you can create your own look. More lightweight than you'd expect, these cargos are easy to dress up or down. 

    Style yours with our Luxe Knit Tank Top and sneakers for easy off duty style.
    "
    ```

    To emulate the writing style of the product descriptions provided, you should aim for a blend of descriptive elegance, practical detailing, and lifestyle integration. Here are detailed instructions to achieve this style:

    Start with an Engaging Hook: Begin each description with a compelling feature that captures the essence of the product. Use adjectives that convey luxury or ease.

    Focus on Fabric and Feel: Describe the materials used with sensory language that evokes a tactile response. Give the reader an idea of how the fabric feels against the skin, which is especially important for maternity wear.

    Detail the Design: Highlight key design features such as "button-up front," "smocked bodice," or "removable belted waist." Be specific about the elements that add to the functionality and style, like sleeve length, type of closure, and type of neckline.

    Incorporate Functionality: Since these are maternity clothes, emphasize features that add practical value, like "nursing friendly" or "adjustable waist tie." Use phrases that speak directly to the needs of the target demographic.

    Set the Scene: Suggest occasions or settings where the garment could be worn. Phrases like "for casual Fridays," "perfect for your maternity shoot," or "essential for any occasion" help the reader visualize when and where they could wear the item.

    Styling Suggestions: Offer fashion tips on how to complete the look. Advise on pairing the item with accessories or other pieces of clothing, for example, "pair with sneakers or sandals" or "wear with your favorite denim jacket."

    Use Emotive and Sensory Language: Infuse the description with words that appeal to emotions and senses. Descriptions like "beautiful tone shines in the light" create a vivid image and an emotional connection.

    Versatility and Transition: Point out the versatility of the garment, and how it can transition through various stages of maternity and different times of the day. Use phrases like "from AM to PM" or "at any stage of pregnancy and beyond."

    Close with a Call-to-Action: End with a simple and effective directive that invites the reader to imagine themselves wearing the piece, such as "Step into a ready-to-go fit" or "This effortless summer dress is our go-to."

    Edit for Clarity and Flow: Ensure that sentences are clear and flow smoothly. Avoid jargon that might confuse the reader, and ensure that the description is easy to follow.

    Character Length: The descriptions are all 350-450 characters in length

    --------

    Please generate a description for the following details. DO NOT REFERENCE THE NUMERICAL LENGTHS OF THE GARMENT. IMPORTANT: KEEP YOUR DESCRIPTIONS TO 400 CHARACTERS:
    {product_name} 	{colour_code}	{colour_name}
    {dp_1}	{dp_2}	{dp_3}	{dp_4} 	{dp_5}	{dp_6} 	{dp_7}  {dp_8}
    """

    return chat_with_gpt4(desc_prompt)

def format_description(description):
    return '<br><br>'.join(filter(None, description.split('\n')))

def strip_bullet_points(text):
    characters_to_strip = '•*- '
    return text.lstrip(characters_to_strip)

def generate_html(row_data):
    description = format_description(row_data['Description'])
    html_template = f"""
    {description}
    <br><br>
    <ul>
        <li>{strip_bullet_points(row_data['Dot Point 2'])}</li>
        <li>{strip_bullet_points(row_data['Dot Point 3'])}</li>
        <li>{strip_bullet_points(row_data['Dot Point 5'])}</li>
        <li>{strip_bullet_points(row_data['Dot Point 6'])}</li>
        <li>{strip_bullet_points(row_data['Dot Point 7'])}</li>
        <li>{strip_bullet_points(row_data['Dot Point 8'])}</li>
        <li>{strip_bullet_points(row_data['Dot Point 4'])}</li>
        <li>{strip_bullet_points(row_data['Dot Point 1'])}</li>
    </ul>
    """
    return html_template.strip()

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    descriptions = []
    htmls = []

    for index, row in df.iterrows():
        product_name = row['Product Name']
        colour_code = row['Clr Code']
        colour_name = row['Clr Name']
        dp_1 = row['Dot Point 1']
        dp_2 = row['Dot Point 2']
        dp_3 = row['Dot Point 3']
        dp_4 = row['Dot Point 4']
        dp_5 = row['Dot Point 5']
        dp_6 = row['Dot Point 6']
        dp_7 = row['Dot Point 7']
        dp_8 = row['Dot Point 8']

        description = generate_description(product_name, colour_code, colour_name, dp_1, dp_2, dp_3, dp_4, dp_5, dp_6, dp_7, dp_8)
        descriptions.append(description)

        html = generate_html(row)
        htmls.append(html)

    df['Generated Descriptions'] = descriptions
    df['Generated HTMLs'] = htmls

    st.write(df.to_html(escape=False), unsafe_allow_html=True)
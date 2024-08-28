import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
from utils import handle_null
import webbrowser
def display_use_case_card(use_case):
    reference_implementation_link = use_case['Repo Link']
    reference_implementation_text = use_case['Reference Implementation']

    performance_metrics = "<br> <br> Results: <br>".join(filter(None, [
        handle_null(use_case['Model Performance Metrics']),
        handle_null(use_case['Model Performance Results'])
    ]))

    st.markdown(f"""
    <div class="use-case-card" style="border: 2px solid #ec008c;">
        <h3 style="color: #ec008c;">{use_case['Use Case Title']}</h3>
        <table class="use-case-table">
            <tr>
                <th>Category</th>
                <th>Details</th>
            </tr>
            <tr>
                <td>Applicable Industry</td>
                <td>{handle_null(use_case['All Applicable Industries'])}</td>
            </tr>
            <tr>
                <td>Use Case Description</td>
                <td>{handle_null(use_case['Use Case Description'])}</td>
            </tr>
            <tr>
                <td>Business Value</td>
                <td>{handle_null(use_case['Business Value Description'])}</td>
            </tr>
            <tr>
                <td>AI Capabilities</td>
                <td>{handle_null(use_case['AI Capabilities'])}</td>
            </tr>
            <tr>
                <td>Dataset Description</td>
                <td>{handle_null(use_case['Dataset Summary'])}</td>
            </tr>
            <tr>
                <td>Model Specifics</td>
                <td>
                    {handle_null(use_case['Model Specifics'])}
                     <br>
                     <br>
                     Reference Implementation:
                     <br>
                     <a href="{reference_implementation_link}" target="_blank">{reference_implementation_text}</a>
                 </td>
            </tr>
            <tr>
                <td>Performance Metrics</td>
                <td>{performance_metrics}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)



def display_use_cases(filtered_use_cases, show_all):
    if not show_all:
        items_per_page = 4
        total_pages = (
                                  len(filtered_use_cases) + items_per_page - 1) // items_per_page if not filtered_use_cases.empty else 1

        if not filtered_use_cases.empty:
            st.sidebar.markdown(f"Total items: {len(filtered_use_cases)}")
            st.sidebar.markdown(f"Page {st.session_state.page_number} of {total_pages}")

            # Pagination controls
            prev_page, next_page = st.sidebar.columns(2)
            if st.session_state.page_number > 1:
                if prev_page.button("Previous"):
                    st.session_state.page_number -= 1
            if st.session_state.page_number < total_pages:
                if next_page.button("Next"):
                    st.session_state.page_number += 1

            start_idx = (st.session_state.page_number - 1) * items_per_page
            end_idx = start_idx + items_per_page
            current_items = filtered_use_cases.iloc[start_idx:end_idx]

            col1, col2 = st.columns(2)
            cols = [col1, col2]

            for idx, (_, use_case) in enumerate(current_items.iterrows()):
                with cols[idx % 2]:
                    display_use_case_card(use_case)
                    if st.button("Generate Card", key=f"generate_card_{idx}"):
                        image = generate_card_image(use_case)
                        image.save(f"generated_cards/card{_+1}.png")
                        st.success("Card successfully generated!")
                        webbrowser.open('file://' + os.path.realpath(f"generated_cards/card{_+1}.png"))
        else:
            st.write("Please enter a search query to display use cases.")
    else:
        st.sidebar.markdown(f"Total items: {len(filtered_use_cases)}")
        for _, use_case in filtered_use_cases.iterrows():
            display_use_case_card(use_case)




def generate_card_image(use_case):
    width, height = 1000, 700
    background_color = (255, 255, 255)  # White background
    border_color = (236, 0, 140)  # Pink border
    font_color = (0, 0, 0)  # Black text for all content
    link_color = (0, 0, 255)  # Blue color for links
    box_color = (255, 255, 255)  # White boxes

    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Load fonts
    font_path = os.path.dirname(os.path.abspath(__file__))
    header_font = ImageFont.truetype(os.path.join(font_path, "arialbd.ttf"), 28)
    title_font = ImageFont.truetype(os.path.join(font_path, "arialbd.ttf"), 14)
    content_font = ImageFont.truetype(os.path.join(font_path, "arial.ttf"), 14)

    # Function to draw a rounded rectangle
    def draw_rounded_rectangle(x, y, w, h, radius, outline=None, width=1):
        draw.arc([x, y, x + radius * 2, y + radius * 2], 180, 270, fill=outline, width=width)
        draw.arc([x + w - radius * 2, y, x + w, y + radius * 2], 270, 0, fill=outline, width=width)
        draw.arc([x, y + h - radius * 2, x + radius * 2, y + h], 90, 180, fill=outline, width=width)
        draw.arc([x + w - radius * 2, y + h - radius * 2, x + w, y + h], 0, 90, fill=outline, width=width)
        draw.line([x + radius, y, x + w - radius, y], fill=outline, width=width)
        draw.line([x + radius, y + h, x + w - radius, y + h], fill=outline, width=width)
        draw.line([x, y + radius, x, y + h - radius], fill=outline, width=width)
        draw.line([x + w, y + radius, x + w, y + h - radius], fill=outline, width=width)

    # Function to draw a box with text
    def draw_box(x, y, w, h, title, content, is_link=False):
        draw_rounded_rectangle(x, y, w, h, 10, outline=border_color, width=2)
        draw.text((x + 10, y + 10), title, font=title_font, fill=font_color)

        # Wrap and draw content
        content_width = w - 20
        content_height = h - 45
        lines = []
        words = str(content).split()
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + " " + word
            bbox = draw.textbbox((0, 0), test_line, font=content_font)
            test_width = bbox[2] - bbox[0]
            if test_width <= content_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

        y_text = y + 40
        for line in lines:
            if y_text + 18 > y + h - 10:  # Leave some padding at the bottom
                break
            if is_link:
                draw.text((x + 10, y_text), line, font=content_font, fill=link_color)
                text_width = draw.textbbox((x + 10, y_text), line, font=content_font)[2] - (x + 10)
                draw.line((x + 10, y_text + 15, x + 10 + text_width, y_text + 15), fill=link_color)
            else:
                draw.text((x + 10, y_text), line, font=content_font, fill=font_color)
            y_text += 18

    # Calculate dynamic box sizes based on content
    def calculate_box_height(content, width):
        lines = []
        words = str(content).split()
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            bbox = draw.textbbox((0, 0), test_line, font=content_font)
            test_width = bbox[2] - bbox[0]
            if test_width <= width - 20:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return len(lines) * 18 + 70  # 70 for padding and title

    # Calculate card dimensions dynamically
    box_width = 290
    column_spacing = 15
    row_spacing = 15
    card_padding = 20

    # Calculate heights for each column
    column_heights = [0, 0, 0]
    fields = [
        ['All Applicable Industries', 'Use Case Description'],
        ['Business Value Description', 'Dataset Summary'],
        ['AI Capabilities', 'Model Specifics', 'Performance Metrics']
    ]

    for col, field_list in enumerate(fields):
        for field in field_list:
            if field == 'Model Specifics':
                content = f"{use_case['Model Specifics']} \n Reference Implementation: \n {use_case['Reference Implementation']}"
            elif field == 'Performance Metrics':
                content = f"{use_case['Performance Metrics']}"
            else:
                content = use_case[field]

            column_heights[col] += calculate_box_height(content, box_width) + row_spacing

    card_height = max(column_heights) + 80  # Add space for header and padding
    card_width = 3 * box_width + 2 * column_spacing + 2 * card_padding

    card_x = (width - card_width) // 2
    card_y = (height - card_height) // 2

    # Draw rounded rectangle for the card border
    draw_rounded_rectangle(card_x, card_y, card_width, card_height, 20, outline=border_color, width=1)

    # Draw header
    header_text = f"#{use_case['Unique Code']} {use_case['Use Case Title']}"
    draw.text((card_x + 20, card_y + 15), header_text, font=header_font, fill=font_color)

    # Draw boxes in 3 columns
    y_offset = card_y + 60

    for col, field_list in enumerate(fields):
        column_y_offset = y_offset
        for field in field_list:
                #     content = f"{model_specifics} \n Reference Implementation: \n <a href='{use_case['Repo Link']}' target='_blank'>{use_case['Reference Implementation']}</a>"
            if field == 'Model Specifics':
                content = (f"{use_case['Model Specifics']}"
                           f" "
                           f" Ref Implementation: \n {use_case['Reference Implementation']}")

            elif field == 'Performance Metrics':
                content = (f"{use_case['Model Performance Metrics']} "
                           f" "
                           f" Results:"
                           f" "
                           f" {use_case['Model Performance Results']}")
            else:
                content = use_case[field]

            box_height = calculate_box_height(content, box_width)
            is_link = (field == 'REFERENCE IMPLEMENTATION')
            draw_box(card_x + card_padding + col * (box_width + column_spacing),
                     column_y_offset, box_width, box_height,
                     field.replace('_', ' ').title() + ':', content, is_link=is_link)
            column_y_offset += box_height + row_spacing

    return image


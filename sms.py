# import os
# import xml.etree.ElementTree as ET

# # Path to the SMS backup file
# file_path = r"D:\oldpc\lib\sms-20240128133724.xml"

# # Directory to save the conversations
# output_dir = r"D:\output_conversations"
# os.makedirs(output_dir, exist_ok=True)

# def parse_sms_backup(file_path, output_dir):
#     try:
#         # Open and parse the XML file iteratively
#         context = ET.iterparse(file_path, events=("start", "end"))
#         context = iter(context)

#         conversations = {}
#         current_sms = {}

#         for event, elem in context:
#             if event == "start" and elem.tag == "sms":
#                 # Extract SMS attributes
#                 current_sms = {
#                     "address": elem.get("address"),
#                     "date": elem.get("date"),
#                     "body": elem.get("body"),
#                     "contact_name": elem.get("contact_name") or "Unknown",
#                 }
#             elif event == "end" and elem.tag == "sms":
#                 # Add to conversation dictionary
#                 address = current_sms["address"]
#                 if address not in conversations:
#                     conversations[address] = []
#                 conversations[address].append(
#                     f"[{current_sms['date']}] {current_sms['contact_name']}: {current_sms['body']}"
#                 )
#                 elem.clear()  # Clear the element to save memory

#         # Save conversations to files
#         for address, messages in conversations.items():
#             sanitized_address = address.replace("+", "").replace(" ", "_").replace("/", "_")
#             output_file = os.path.join(output_dir, f"conversation_{sanitized_address}.txt")
#             with open(output_file, "w", encoding="utf-8") as out_file:
#                 out_file.write("\n".join(messages))
        
#         print(f"Conversations saved in {output_dir}")

#     except ET.ParseError as e:
#         print(f"Parse error: {e}")
#     except Exception as e:
#         print(f"Error: {e}")

# # Run the function
# parse_sms_backup(file_path, output_dir)






# import os
# import xml.etree.ElementTree as ET

# # Path to the SMS backup file
# file_path = r"D:\oldpc\lib\sms-20240128133724.xml"

# # Directory to save the conversations
# output_dir = r"D:\output_conversations"
# os.makedirs(output_dir, exist_ok=True)

# def parse_sms_backup(file_path, output_dir):
#     try:
#         # Open and parse the XML file iteratively
#         context = ET.iterparse(file_path, events=("start", "end"))
#         context = iter(context)

#         conversations = {}
#         current_sms = {}

#         for event, elem in context:
#             if event == "start" and elem.tag == "sms":
#                 # Extract SMS attributes
#                 current_sms = {
#                     "address": elem.get("address"),
#                     "date": elem.get("date"),
#                     "body": elem.get("body"),
#                     "type": elem.get("type"),  # Extract type (sent or received)
#                     "contact_name": elem.get("contact_name") or "Unknown",
#                 }
#             elif event == "end" and elem.tag == "sms":
#                 # Determine direction (sent or received)
#                 direction = "Received" if current_sms["type"] == "1" else "Sent"

#                 # Add to conversation dictionary
#                 address = current_sms["address"]
#                 if address not in conversations:
#                     conversations[address] = []
#                 conversations[address].append(
#                     f"[{current_sms['date']}] {current_sms['contact_name']} ({direction}): {current_sms['body']}"
#                 )
#                 elem.clear()  # Clear the element to save memory

#         # Save conversations to files
#         for address, messages in conversations.items():
#             sanitized_address = address.replace("+", "").replace(" ", "_").replace("/", "_")
#             output_file = os.path.join(output_dir, f"conversation_{sanitized_address}.txt")
#             with open(output_file, "w", encoding="utf-8") as out_file:
#                 out_file.write("\n".join(messages))
        
#         print(f"Conversations saved in {output_dir}")

#     except ET.ParseError as e:
#         print(f"Parse error: {e}")
#     except Exception as e:
#         print(f"Error: {e}")

# # Run the function
# parse_sms_backup(file_path, output_dir)



#extracts media and sms from backup xml file
# import os
# import xml.etree.ElementTree as ET
# import base64

# # Path to the SMS backup file
# file_path = r"D:\oldpc\lib\sms-20240128133724.xml"

# # Directory to save conversations and media
# output_dir = r"D:\output_conversations"
# media_dir = os.path.join(output_dir, "media")
# os.makedirs(media_dir, exist_ok=True)

# def save_media(part, media_dir, msg_id):
#     """Save media content from an MMS part."""
#     content_type = part.get("ct")
#     data = part.get("data")
#     file_name = part.get("name") or f"media_{msg_id}"
#     src = part.get("src")  # Path to media on the original device

#     # Determine file extension from content type
#     extension = content_type.split("/")[-1] if content_type else "bin"
#     file_path = os.path.join(media_dir, f"{file_name}.{extension}")

#     # Try to save Base64-encoded data
#     if data:
#         try:
#             with open(file_path, "wb") as media_file:
#                 media_file.write(base64.b64decode(data))
#             return file_path
#         except Exception as e:
#             print(f"Error saving Base64 media: {e}")
#             return None
#     elif src:
#         # Log missing external file
#         missing_message = f"Missing file: {src}"
#         print(missing_message)
#         return missing_message
#     return None

# def parse_sms_backup(file_path, output_dir, media_dir):
#     try:
#         # Open and parse the XML file iteratively
#         context = ET.iterparse(file_path, events=("start", "end"))
#         context = iter(context)

#         conversations = {}
#         current_sms = {}
#         msg_id = 0  # Counter for unique message IDs

#         for event, elem in context:
#             if event == "start" and elem.tag == "sms":
#                 # Extract SMS attributes
#                 current_sms = {
#                     "id": msg_id,
#                     "address": elem.get("address"),
#                     "date": elem.get("date"),
#                     "body": elem.get("body"),
#                     "type": elem.get("type"),  # Sent or received
#                     "contact_name": elem.get("contact_name") or "Unknown",
#                 }
#                 msg_id += 1

#             elif event == "start" and elem.tag == "mms":
#                 # Process MMS message
#                 current_sms = {
#                     "id": msg_id,
#                     "address": elem.get("address"),
#                     "date": elem.get("date"),
#                     "type": elem.get("type"),
#                     "contact_name": elem.get("contact_name") or "Unknown",
#                     "media": [],  # Store paths to media
#                 }
#                 msg_id += 1

#             elif event == "start" and elem.tag == "part":
#                 # Extract media information from MMS
#                 if "media" in current_sms:
#                     media_path = save_media(elem, media_dir, current_sms["id"])
#                     if media_path:
#                         current_sms["media"].append(media_path)

#             elif event == "end" and elem.tag in ("sms", "mms"):
#                 # Add to conversation dictionary
#                 address = current_sms["address"]
#                 if address not in conversations:
#                     conversations[address] = []

#                 # Format message with media if applicable
#                 direction = "Received" if current_sms["type"] == "1" else "Sent"
#                 message = f"[{current_sms['date']}] {current_sms['contact_name']} ({direction}): {current_sms.get('body', '')}"
#                 if "media" in current_sms and current_sms["media"]:
#                     message += "\n  Media: " + ", ".join(current_sms["media"])

#                 conversations[address].append(message)
#                 elem.clear()  # Clear the element to save memory

#         # Save conversations to files
#         for address, messages in conversations.items():
#             sanitized_address = address.replace("+", "").replace(" ", "_").replace("/", "_")
#             output_file = os.path.join(output_dir, f"conversation_{sanitized_address}.txt")
#             with open(output_file, "w", encoding="utf-8") as out_file:
#                 out_file.write("\n".join(messages))

#         print(f"Conversations and media saved in {output_dir}")

#     except ET.ParseError as e:
#         print(f"Parse error: {e}")
#     except Exception as e:
#         print(f"Error: {e}")

# # Run the function
# parse_sms_backup(file_path, output_dir, media_dir)





import os
import xml.etree.ElementTree as ET
import base64
from datetime import datetime

# Path to the SMS backup file
file_path = r"D:\oldpc\lib\sms-20240128133724.xml"

# Directory to save conversations and media
output_dir = r"D:\output_conversations"
media_dir = os.path.join(output_dir, "media")
os.makedirs(media_dir, exist_ok=True)

def save_media(part, media_dir, msg_id):
    """Save media content from an MMS part."""
    content_type = part.get("ct")
    data = part.get("data")
    file_name = part.get("name") or f"media_{msg_id}"
    src = part.get("src")  # Path to media on the original device

    # Determine file extension from content type
    extension = content_type.split("/")[-1] if content_type else "bin"
    file_path = os.path.join(media_dir, f"{file_name}.{extension}")

    # Try to save Base64-encoded data
    if data:
        try:
            with open(file_path, "wb") as media_file:
                media_file.write(base64.b64decode(data))
            return file_path
        except Exception as e:
            print(f"Error saving Base64 media: {e}")
            return None
    elif src:
        # Log missing external file
        missing_message = f"Missing file: {src}"
        print(missing_message)
        return missing_message
    return None

def format_timestamp(timestamp):
    """Convert Unix timestamp to human-readable date and time."""
    try:
        return datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error formatting timestamp: {e}")
        return "Unknown Date/Time"

def parse_sms_backup(file_path, output_dir, media_dir):
    try:
        # Open and parse the XML file iteratively
        context = ET.iterparse(file_path, events=("start", "end"))
        context = iter(context)

        conversations = {}
        current_sms = {}
        msg_id = 0  # Counter for unique message IDs

        for event, elem in context:
            if event == "start" and elem.tag == "sms":
                # Extract SMS attributes
                current_sms = {
                    "id": msg_id,
                    "address": elem.get("address"),
                    "date": format_timestamp(elem.get("date")),
                    "body": elem.get("body"),
                    "type": elem.get("type"),  # Sent or received
                    "contact_name": elem.get("contact_name") or "Unknown",
                }
                msg_id += 1

            elif event == "start" and elem.tag == "mms":
                # Process MMS message
                current_sms = {
                    "id": msg_id,
                    "address": elem.get("address"),
                    "date": format_timestamp(elem.get("date")),
                    "type": elem.get("type"),
                    "contact_name": elem.get("contact_name") or "Unknown",
                    "media": [],  # Store paths to media
                }
                msg_id += 1

            elif event == "start" and elem.tag == "part":
                # Extract media information from MMS
                if "media" in current_sms:
                    media_path = save_media(elem, media_dir, current_sms["id"])
                    if media_path:
                        current_sms["media"].append(media_path)

            elif event == "end" and elem.tag in ("sms", "mms"):
                # Add to conversation dictionary
                address = current_sms["address"]
                if address not in conversations:
                    conversations[address] = []

                # Format message with media if applicable
                direction = "Received" if current_sms["type"] == "1" else "Sent"
                message = f"[{current_sms['date']}] {current_sms['contact_name']} ({direction}): {current_sms.get('body', '')}"
                if "media" in current_sms and current_sms["media"]:
                    message += "\n  Media: " + ", ".join(current_sms["media"])

                conversations[address].append(message)
                elem.clear()  # Clear the element to save memory

        # Save conversations to files
        for address, messages in conversations.items():
            sanitized_address = address.replace("+", "").replace(" ", "_").replace("/", "_")
            output_file = os.path.join(output_dir, f"conversation_{sanitized_address}.txt")
            with open(output_file, "w", encoding="utf-8") as out_file:
                out_file.write("\n".join(messages))

        print(f"Conversations and media saved in {output_dir}")

    except ET.ParseError as e:
        print(f"Parse error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Run the function
parse_sms_backup(file_path, output_dir, media_dir)

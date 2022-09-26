import frappe
import requests
import random

@frappe.whitelist(allow_guest=True)
def handle():
    if frappe.request.method == "GET":
        return verify_token_and_fulfill_challenge()

def verify_token_and_fulfill_challenge():
    note = frappe.new_doc("Note")
    ran = random.randint(0, 1000)
    note.title = "Webhook Testing - " + str(ran)
    note.content = frappe.form_dict.get("hub")
    mode = frappe.form_dict.get("hub.mode")
    token = frappe.form_dict.get("hub.verify_token")
    challenge = frappe.form_dict.get("hub.challenge")

    expected_token = frappe.db.get_single_value("WhatsApp Cloud API Settings", "webhook_verify_token")

    if (mode and token):
        if (mode == "subscribe" and token == expected_token):
            note.public = 0
            return Response(meta_challenge, status=200)
        else:
            note.public = 1
            return Response(status=403)
    note.content = note.content + "<br><br>" + "in if else"
    note.save()
    frappe.db.commit()

    return Response(meta_challenge, status=400)

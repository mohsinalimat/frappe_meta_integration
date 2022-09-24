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
    meta_challenge = frappe.form_dict.get("hub.challenge")
    expected_token = frappe.db.get_single_value("WhatsApp Cloud API Settings", "webhook_verify_token")
    note.content = meta_challenge
    if frappe.form_dict.get("hub.verify_token") != expected_token:
        note.public = 0
        note.save()
        frappe.db.commit()
        frappe.throw("Verify token does not match")
    else:
        note.public = 1
        note.save()
        frappe.db.commit()

    return Response(meta_challenge, status=200)

from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
import threading
from django.utils import timezone
from .models import *


@receiver(post_save, sender=Report)
def send_email_on_save(sender, instance, created, **kwargs):
    if created:
        subject = 'Action Required'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = ['k.krishnamadhav@imop.co.in']  # Replace with the actual recipient email address
        formatted_date = instance.created_at.strftime("%b %d, %Y")
        # Customize HTML content directly in the signal
        html_content = f'''
                           <h3
                            style="border:3px solid #005b96;padding:15px;border-radius:10px;font:poppins;">
                            <div
                                    style="border: 0px solid black; background: #9990; border-radius: 50%; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
                                    <img src="https://www.imop.co.in/assets/img/Main/logo.png" alt
                                            height="60" width="60"
                                            style="margin-right: 10px;">
                                    <span style="margin-left:auto;margin-top:23px;">{formatted_date}</span>
                            </div>
                            <div
                                    style="background:#005b9611;padding:20px;border-radius:10px;font:poppins;">
                                    <br>
                                    Greetings of the day...
                                    <br>
                                    <br>
                                    A new object with Part Number
                                    <strong style="color:#005b96;">{instance.file_name}</strong>
                                    has been created by
                                    <strong style="color:#5b0096;">{instance.created_by}</strong>

                                    <hr>
                                    <span>
                                            Please find the following attached file for your
                                            reference.
                                    </span>
                            </div>
                    </h3>
                        '''

        # Create plain text content by stripping HTML tags
        plain_text_content = strip_tags(html_content)

        # Use threading to send the email in a separate thread
        thread = threading.Thread(
            target=send_email_in_thread,
            args=(subject, plain_text_content, html_content, from_email, to_email,instance),
        )
        thread.start()
        

@receiver(post_save, sender=Report)
def send_email_after_object_save(sender, instance, created, **kwargs):
    if not created and instance.is_approved in [1,0]:  # Only proceed if the instance was updated, not created
        try:
            # Retrieve the latest values from the database
            updated_instance = sender.objects.get(pk=instance.pk)

            subject = 'Action Required - Object Updated After Save'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['m.karthikarun@imop.co.in', 'k.krishnamadhav@imop.co.in']
            formatted_date = timezone.now().strftime("%b %d, %Y")
            status = None
            if instance.is_approved == 1:
                status = f'''<span style="color:green">Approved</span>'''
            elif instance.is_approved == 0:
                status = f'''<span style="color:red">Rejected</span>'''
            else:
                status = f'''<span style="color:blue">Pending</span>'''
            print(instance.is_approved,status,'status >>>>>>>>>>>>>>>>>>>>>>>>')
            html_content = f'''
               <h3 style="border:3px solid #005b96;padding:15px;border-radius:10px;font:poppins;">
                    <div style="border: 0px solid black; background: #9990; border-radius: 50%; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
                        <img src="https://www.imop.co.in/assets/img/Main/logo.png" alt height="60" width="60" style="margin-right: 10px;">
                        <span style="margin-left:auto;margin-top:23px;">{formatted_date}</span>
                    </div>
                    <div style="background:#005b9611;padding:20px;border-radius:10px;font:poppins;">
                        <br>
                        Greetings of the day...
                        <br>
                        <br>
                        The object with Part Number
                        <strong style="color:#005b96;">{updated_instance.file_name}</strong>
                        has been updated. Updated Status: {status}

                        <hr>
                        <span>
                            Please find the following attached file for your reference.
                        </span>
                    </div>
                </h3>
            '''

            plain_text_content = strip_tags(html_content)

            thread = threading.Thread(
                target=send_email_in_thread,
                args=(subject, plain_text_content, html_content, from_email, to_email, updated_instance),
            )
            thread.start()

        except sender.DoesNotExist:
            pass


def send_email_in_thread(subject, plain_text_content, html_content, from_email, to_email,instance):
    email = EmailMultiAlternatives(
        subject,
        plain_text_content,
        from_email,
        to_email,
    )
    email.attach_alternative(html_content, "text/html")
    attached_file_path = instance.file.path  # Assuming 'file' is the FileField in your model
    email.attach_file(attached_file_path)
    email.send()
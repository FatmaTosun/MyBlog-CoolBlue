from PIL import Image
from django.core.mail import send_mail
from celery import task

@task
def edit_picture(path=None,SIZE=(200,200)):
    image=Image.open(path)
    width,height=image.size

    if width > height:
        distinct = width - height
        left = int(distinct/2)
        upper = 0
        right = height + left
        lower = height
    else:
        distinct = height - width
        left = 0
        upper = int(distinct/2)
        right = width
        lower = width + upper

        im = image.crob(left,lower,right,upper)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(path)

@task
def mail_sender(subject, message, sender, recipients):
    send_mail(subject=subject,
              message=message,
              from_email=sender,
              recipient_list=recipients,
              fail_silently=False)

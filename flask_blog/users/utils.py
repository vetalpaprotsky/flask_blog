import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, image_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + image_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_pics', image_filename)

    # Resize image and save it
    output_size = (128, 128)
    image = Image.open(form_image)
    image.thumbnail(output_size)
    image.save(image_path)

    # Save image as it is
    # form_image.save(image_path)

    return image_filename


def send_password_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

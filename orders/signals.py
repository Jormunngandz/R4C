import os
from typing import List

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from robots.models import Robot
from dotenv import load_dotenv
load_dotenv()


@receiver(post_save, sender=Robot)
def send_mail_to_customer(sender, instance: Robot, created: bool, **kwargs):

    if created:
        orders: List[Order] = Order.objects.filter(robot_serial=instance.serial).select_related("customer")
        for order in orders:
            if order.robot_serial == instance.serial:
                send_mail(
                    "Фабрика Роботов. Ваш робот готов!",
                    f"Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model},"
                    f" версии {instance.version}.\n"
                    "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами",
                    f"{os.getenv('SMTP_LOGIN')}",
                    [f"{order.customer.email}"],
                    fail_silently=False,
                )


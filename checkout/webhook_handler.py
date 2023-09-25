from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handle webhook for Stripe
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle webhook event of generic, unknown, unexpected
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the webhook from Stripe for payment_intent.succeeded
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created\
                 order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the webhook from Stripe for payment_intent.payment_failed
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
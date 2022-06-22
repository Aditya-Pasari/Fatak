from django.shortcuts import redirect, render

import razorpay
from Fatak.settings import YOUR_API_KEY, YOUR_API_SECRET
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import *


razorpay_client = razorpay.Client(auth=(YOUR_API_KEY, YOUR_API_SECRET))

# Create your views here.

def razorpay_page(request):
    print("ENTERING VIEW")
    
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = YOUR_API_KEY
    context['razorpay_amount'] = amount
    context['currency'] = currency  
    context['callback_url'] = callback_url


    #x = client.payment.all()
    #for item in x['items']:
    #    print(item)
    #    print('\n')

    return render(request, 'razorpay.html', context=context)
    #return render(request, 'index.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    print("Entering Payment Handler")
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print(params_dict)
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print("Result = " + str(result))
            #if result is None:
            if result:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    print("if there is an error while capturing payment")
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                print("if signature verification fails")
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            print("Please send required parameters in POST request")
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        print("Please send POST request")
        return HttpResponseBadRequest()



def create_customer(request):
        
    if request.method == 'POST':
        name = request.POST.get('name', '')
        phoneno = request.POST.get('phoneno', '')
        email = request.POST.get('email', '')
        amount = request.POST.get('amount', '')
        note1 = request.POST.get('note1', '')
        note2 = request.POST.get('note2', '')
        
        try:
            if(RazorpayCustomer.objects.get(email = email).exists()):
                print("Customer already present")
                return redirect('home')
        except:
            x = razorpay_client.customer.all()
            customer_present = False
            customer = ""

            for cust in x['items']:
                if(cust['email'] == email):
                    customer_present = True
                    customer = cust
                    break
            
            if(not customer_present):
                customer = razorpay_client.customer.create({
                    "name": name,
                    "contact": phoneno,
                    "email": email,
                    "notes": {
                        "notes_key_1": note1,
                        "notes_key_2": note2
                    }
                })

                c = RazorpayCustomer(createdby = request.user, 
                            id = customer['id'],
                            name = name,
                            email = email,
                            contact = phoneno,
                            gstin = '',
                            notes1 = note1,
                            notes2 = note2,
                        )
			
                c.save()	

            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": "INR",
                "method": "upi",
                "customer_id": customer['id'],
                "receipt": "Receipt No. 1",
                "notes": {
                    "notes_key_1": note1,
                    "notes_key_2": note2
                },
                
            })

            o = RazorpayOrderID(
                        payer       =   'cust_JjIxpRhIF51R53',
                        receiver    =   customer['id'],
                        order_id    =   razorpay_order['id'],
                        amount      =   razorpay_order['amount'],
                        amount_paid =   razorpay_order['amount_paid'],
                        amount_due  =   razorpay_order['amount_due'],
                        currency    =   razorpay_order['currency'],
                        status      =   razorpay_order['status'],
                        notes1      =   razorpay_order['notes']['notes_key_1'],
                        notes2      =   razorpay_order['notes']['notes_key_2'],
    
            )

            o.save()

            print(customer)
            print(razorpay_order)
            context = {}
            context['key'] = YOUR_API_KEY
            context['order_id'] = razorpay_order['id']
            context['customer_id'] = customer['id']
            
            return render(request, 'razorpay_checkout.html', context = context)
            
        
            
            

    return render(request, 'create_customer.html')


from fastapi import APIRouter, Request

from config.config import LAVA_API_KEY, OFFER_ID

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/create")
async def create_payment(request: Request):
    payment = await request.app.state.http.post(
        "https://gate.lava.top/api/v3/invoice",
        headers={"Content-Type": "application/json", "X-Api-Key": LAVA_API_KEY},
        json={"email": "example@example.com", "offerId": OFFER_ID, "currency": "RUB"},
    )

    payment.raise_for_status()
    invoice = payment.json()
    print(invoice)

    payment_url = invoice.get("paymentUrl")
    if payment_url:
        return payment_url
    
    return 

# {'id': 'ec50877b-aa44-4834-9388-476936fcb007', 'status': 'new', 'amountTotal': {'currency': 'RUB', 'amount': 50.0}, 'paymentUrl': 'https://app.lava.top/products/7a6cb856-978f-4e49-a1cb-abc99206e0af/d5863884-7647-4582-8afc-db2eb2f99eeb?paymentParams=CiAgICAgICAgewogICAgICAgICAgImludm9pY2VJZCI6ICJlYzUwODc3Yi1hYTQ0LTQ4MzQtOTM4OC00NzY5MzZmY2IwMDciLAogICAgICAgICAgInBheW1lbnRTZXR0aW5ncyI6IHsiaWQiOiJlYzUwODc3Yi1hYTQ0LTQ4MzQtOTM4OC00NzY5MzZmY2IwMDciLCJ0eXBlIjoiaW52b2ljZSIsInN0YXR1cyI6Im5ldyIsImFtb3VudF90b3RhbCI6eyJjdXJyZW5jeSI6IlJVQiIsImFtb3VudCI6NTAuMDB9LCJwcm92aWRlciI6eyJuYW1lIjoic21hcnRfZ2xvY2FsIiwibWV0aG9kIjoiY2FyZCIsInBhcmFtZXRlcnMiOnsic3R5bGVzaGVldCI6Imh0dHBzOi8vd2lkZ2V0LnNtYXJ0LWdsb2NhbC5jb20vcGF5bWVudC1mb3JtLmNzcyIsInNjcmlwdCI6Imh0dHBzOi8vd2lkZ2V0LnNtYXJ0LWdsb2NhbC5jb20vcGF5bWVudC1mb3JtLmpzIiwicHVibGljX3Rva2VuIjoiNDllMWRmYTdkY2ViNWJkMWE4Y2FhZmY5YmMwM2NhMThjZmE3ZDU0NmI2MjIyMWQwMjNkMjIxY2E4OWFiODg1MyIsImlmcmFtZUFsbG93ZWQiOiJ0cnVlIn19fQogICAgICAgIH0KICAgICAg&signature=b60f9252f7dbbe671e381f0095d8efc0e3dff5d5ea88c7c26cbcbbd19a9ae64c'}

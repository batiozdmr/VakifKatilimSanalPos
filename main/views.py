import requests, hashlib, base64, urllib.parse
import urllib3
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SANAL_POS = {
    'customer_id': '201282',  # Müsteri Numarasi
    'merchant_id': '3282',  # Magaza Kodu
    'username': 'nilegit',  # Web Yönetim ekranalrindan olusturulan api rollü kullanici
    'password': '856760',  # Web Yönetim ekranalrindan olusturulan api rollü kullanici sifresi
    'ok_url': 'http://127.0.0.1:8000/ok-url/',
    'fail_url': 'http://127.0.0.1:8000/fail-url/',
    'kart_onay_url': 'https://boa.vakifkatilim.com.tr/VirtualPOS.Gateway/Home/ThreeDModelPayGate',
    'odeme_onay_url': 'https://boa.vakifkatilim.com.tr/VirtualPOS.Gateway/Home/ThreeDModelProvisionGate',
}

SANAL_KART = {
    'kart_name': 'Batıhan Özdemir',  # Kart Sahibi
    'kart_no': '5353550000958906',  # Kart Numarasi
    'son_kullanma_tarihi_yil': '23',  # Son Kullanım Tarihi Yıl
    'son_kullanma_tarihi_ay': '01',  # Son Kullanım Tarihi Ay
    'cvv': '741',  # cvv
}

MERCHANT = {
    'name': 'Batıhan Özdemir',
    'phone': '05442655693',
    'mail': 'ozdemirbatihan@gmail.com',
    'adres_id': '61',
}


def main(request):
    return render(request, "index.html", {})


@csrf_exempt
def payment(request):
    amount = 1 * 100
    merchant_order_id = 1461
    hashed_password = base64.b64encode(hashlib.sha1(f"{SANAL_POS['password']}".encode('ISO-8859-9')))
    hashed_data = base64.b64encode(hashlib.sha1(
        f"{SANAL_POS['merchant_id']}{merchant_order_id}{amount}{SANAL_POS['ok_url']}{SANAL_POS['fail_url']}{SANAL_POS['username']}{hashed_password}".encode(
            'ISO-8859-9')))

    data = f"""<?xml version="1.0" encoding="UTF-8"?>
    <VPosMessageContract xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <OkUrl>{str(SANAL_POS["ok_url"])}</OkUrl>
    <FailUrl>{str(SANAL_POS["fail_url"])}</FailUrl>
    <HashData>{hashed_data}</HashData>
    <MerchantId>{int('3282')}</MerchantId>
    <SubMerchantId>0</SubMerchantId>
    <CustomerId>{int('201282')}</CustomerId>
    <UserName>{str(SANAL_POS['username'])}</UserName>
    <HashPassword>{hashed_password}</HashPassword>
    <MerchantOrderId>{int('1461')}</MerchantOrderId>
    <InstallmentCount>0</InstallmentCount>
    <Amount>{amount}</Amount>
    <DisplayAmount>{amount}</DisplayAmount>
    <FECAmount>0</FECAmount>
    <FECCurrencyCode>0949</FECCurrencyCode> <AdditionalData>
    <AdditionalDataList>
         <VPosAdditionalData>
             <Key>MD</Key>
             <Data>test_data</Data>
            <Description>test_description</Description>
         </VPosAdditionalData>
    </AdditionalDataList>
    </AdditionalData>
    <Addresses>
     <VPosAddressContract>
    <Type>1</Type>
    <Name>{str('Refik Söylemez')}</Name>
    <PhoneNumber>{int('5347933295')}</PhoneNumber>
    <OrderId>{int(1461)}</OrderId>
    <AddressId>{int(35)}</AddressId>
    <Email>{str('refiksoylemez@msn.com')}</Email>
    </VPosAddressContract>
    </Addresses>
    <APIVersion>1.0.0</APIVersion>
    <CardNumber>{str('4183421230670449')}</CardNumber>
    <CardExpireDateYear>{str('27')}</CardExpireDateYear>
    <CardExpireDateMonth>{str('07')}</CardExpireDateMonth>
    <CardCVV2>{str('154')}</CardCVV2>
    <CardHolderName>{str(SANAL_KART['kart_name'])}</CardHolderName>
    <PaymentType>1</PaymentType>
    <DebtId>0</DebtId>
    <SurchargeAmount>0</SurchargeAmount>
    <SGKDebtAmount>0</SGKDebtAmount>
    <InstallmentMaturityCommisionFlag>0</InstallmentMaturityCommisionFlag>
    <TransactionSecurity>3</TransactionSecurity>
    </VPosMessageContract>"""
    print(data)
    headers = {'Content-Type': 'application/xml'}
    r = requests.post(SANAL_POS['kart_onay_url'], data=data.encode('ISO-8859-9'), headers=headers)
    template = 'donate/payment_return.html'
    return render(request, template, {'Sonuc': r.text})


@csrf_exempt
def payment_ok(request):
    merchant_order_id = 1461
    amount = 1 * 100
    md = request.POST.get('MD')
    hashed_password = base64.b64encode(hashlib.sha1(f"{SANAL_POS['password']}".encode('ISO-8859-9')))
    hashed_data = base64.b64encode(hashlib.sha1(
        f"{SANAL_POS['merchant_id']}{merchant_order_id}{amount}{SANAL_POS['ok_url']}{SANAL_POS['fail_url']}{SANAL_POS['username']}{hashed_password}".encode(
            'ISO-8859-9')))

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
     <VPosMessageContract xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
     <OkUrl>{str(SANAL_POS["ok_url"])}</OkUrl>
     <FailUrl>{str(SANAL_POS["fail_url"])}</FailUrl>
     <HashData>{hashed_data}</HashData>
     <MerchantId>{int(SANAL_POS["merchant_id"])}</MerchantId>
     <SubMerchantId>0</SubMerchantId>
     <CustomerId>{int('201282')}</CustomerId>
     <MerchantOrderId>{int(request.POST.get('MerchantOrderId'))}</MerchantOrderId>
     <InstallmentCount>0</InstallmentCount>
     <Amount>{amount}</Amount>
     <FECAmount>0</FECAmount>
     <AdditionalData>
         <AdditionalDataList>
             <VPosAdditionalData>
                 <Key>MD</Key>
                 <Data>{md}</Data>
             </VPosAdditionalData>
         </AdditionalDataList>
    </AdditionalData>
    <PaymentType>1</PaymentType>
    <SurchargeAmount>0</SurchargeAmount>
    <SGKDebtAmount>0</SGKDebtAmount>
    <InstallmentMaturityCommisionFlag>0</InstallmentMaturityCommisionFlag>
    <TransactionSecurity>3</TransactionSecurity> 
    </VPosMessageContract>"""
    print(xml)
    gelen = requests.post(SANAL_POS['odeme_onay_url'], data=xml.encode('ISO-8859-9'))
    gelen_error_cod = gelen.text
    data = urllib.parse.unquote(gelen_error_cod)
    return render(request, 'donate/payment_ok.html', {'sonuc': data})


@require_http_methods(['POST'])
@csrf_exempt
def fail_url(request):
    global Sonuc
    template = 'payment_fail.html'
    error_cod = request.POST.get('ResponseCode')

    if error_cod == "00":
        Sonuc = "Ödeme Başarıyla Alındı"
    if error_cod == "01":
        Sonuc = "BANKANIZI ARAYINIZ"
    if error_cod == "03":
        Sonuc = "GEÇERSİZ ÜYE İŞYERİ"
    if error_cod == "04":
        Sonuc = "İŞLEM ONAYLANMADI " + "HATA KODU: " + error_cod
    if error_cod == "05":
        Sonuc = "İŞLEM ONAYLANMADI " + "HATA KODU: " + error_cod
    if error_cod == "06":
        Sonuc = "İŞLEM ONAYLANMADI " + "HATA KODU: " + error_cod
    if error_cod == "12":
        Sonuc = "Bakiyesi-Kredi limiti Yetersiz"
    if error_cod == "13":
        Sonuc = "İŞLEM ONAYLANMADI " + "HATA KODU: " + error_cod
    if error_cod == "54":
        Sonuc = "VADE SONU GEÇMİŞ KART"
    if error_cod == "51":
        Sonuc = "Bakiyesi-Kredi limiti Yetersiz"
    else:
        Sonuc = " Beklenmeyen Bir Hata Oluştu " + "HATA KODU: " + error_cod

    return render(request, template, {'Sonuc': Sonuc})

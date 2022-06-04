import base64
import hashlib

import urllib3
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SANAL_POS = {
    'customer_id': '201282',  # Müsteri Numarasi
    'merchant_id': '3282',  # Magaza Kodu
    'username': 'nilegit',  # Web Yönetim ekranalrindan olusturulan api rollü kullanici
    'password': '856760',  # Web Yönetim ekranalrindan olusturulan api rollü kullanici sifresi
    'ok_url': 'http://127.0.0.1:8000/payment_return/',
    'fail_url': 'http://127.0.0.1:8000/payment_return/',
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

    hashed_password = base64.b64encode(hashlib.sha1(f"{SANAL_POS['password']}".encode('ISO-8859-9')).digest()).decode()
    hashed_data = base64.b64encode(hashlib.sha1(
        f"{SANAL_POS['merchant_id']}{merchant_order_id}{amount}{SANAL_POS['ok_url']}{SANAL_POS['fail_url']}{SANAL_POS['username']}{hashed_password}".encode(
            'ISO-8859-9')).digest()).decode()
    data = f"""
    <?xml version="1.0" encoding="UTF-16"?>
    <VPosMessageContract
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <OkUrl>{str(SANAL_POS["ok_url"])}</OkUrl>
    <FailUrl>{str(SANAL_POS["fail_url"])}</FailUrl>
    <HashData>{hashed_data}</HashData>
    <MerchantId>{int(SANAL_POS['merchant_id'])}</MerchantId>
    <SubMerchantId>0</SubMerchantId>
    <CustomerId>{int(SANAL_POS['customer_id'])}</CustomerId>
    <UserName>{str(SANAL_POS['username'])}</UserName>
    <HashPassword>{hashed_password}</ HashPassword >
    <MerchantOrderId>{merchant_order_id}</MerchantOrderId>
    <InstallmentCount>0</InstallmentCount>
    <Amount>{amount}</Amount>
    <DisplayAmount>{amount}</DisplayAmount>
    <FECAmount>0</FECAmount>
    <FECCurrencyCode>0949</FECCurrencyCode> <AdditionalData>
    <AdditionalDataList>
     <VPosAdditionalData>
     <Key>test_key</Key>
     <Data>test_data</Data>
    <Description>test_description</Description>
     </VPosAdditionalData>
    </AdditionalDataList>
    </AdditionalData>
    <Addresses>
     <VPosAddressContract>
    <Type>1</Type>
    <Name>{str(MERCHANT['name'])}</Name>
    <PhoneNumber>{int(MERCHANT['phone'])}</PhoneNumbe>
    <OrderId>{merchant_order_id}</OrderId>
    <AddressId>{int(MERCHANT['adres_id'])}</AddressId>
    <Email>{str(MERCHANT['mail'])}</Ema>
    </VPosAddressContract>
    </Addresses>
    <APIVersion>1.0.0</APIVersion>
    <CardNumber>{int(SANAL_KART['kart_no'])}</CardNumber>
    <CardExpireDateYear>{int(SANAL_KART['son_kullanma_tarihi_yil'])}</CardExpireDateYear>
    <CardExpireDateMonth>{int(SANAL_KART['son_kullanma_tarihi_ay'])}</CardExpireDateMonth>
    <CardCVV2>{int(SANAL_KART['cvv'])}</CardCVV2>
    <CardHolderName>{str(SANAL_KART['kart_name'])}</CardHolderName>
    <PaymentType>1</PaymentType>
    <DebtId>0</DebtId>
    <SurchargeAmount>0</SurchargeAmount>
    <SGKDebtAmount>0</SGKDebtAmount>
    <InstallmentMaturityCommisionFlag>0</InstallmentMaturityCo mmisionFlag>
    <TransactionSecurity>3</TransactionSecurity>
    </VPosMessageContract>
    """

    headers = {'Content-Type': 'application/xml'}
    r = requests.post(SANAL_POS['kart_onay_url'], data=data.encode('ISO-8859-9'), headers=headers)
    return HttpResponse(r)


@require_http_methods(['POST'])
@csrf_exempt
def payment_return(request):
    Sonuc = "Beklenmedik bir hata oluştu"
    try:
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "0":
            Sonuc = "Onaylanmamış"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "1":
            Sonuc = "Onaylandı Başarılı"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "2":
            Sonuc = "Kart sahibi banka veya Kart 3D-Secure Üyesi Değil"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "3":
            Sonuc = "Kart prefixi 3D-Secure sisteminde tanımlı değil"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "4":
            Sonuc = "Authentication Attempt"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "5":
            Sonuc = "Sistem ulaşılabilir değil"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "6":
            Sonuc = "3D-Secure Hatası"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "7":
            Sonuc = "Sistem Hatası"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "8":
            Sonuc = "Geçersiz Kart"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] == "9":
            Sonuc = "Üye İşyeri 3D-Secure sistemine kayıtlı değil"
        if request.POST['ResponseCode'] and request.POST['ResponseCode'] != "1":
            Sonuc = Sonuc + " " + str(request.POST['ResponseMessage'])

        return render(request, "index.html", {'Sonuc': Sonuc})
    except Exception as e:
        print(e)
        return render(request, "index.html", {'Sonuc': Sonuc})

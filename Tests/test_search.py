import allure
import requests
from Pages.Add_To_Cart_api import AddToCartAPI
from Pages.Wrong_Add_To_Cart_api import WrongRequestAPI
from Tests.constants import API1_url
from Tests.constants import API2_url
from Pages.Update_cart_api import UpdateCartAPI
from Pages.Delete_From_Cart_api import DeleteFromCart
from Pages.Send_Empty_Post_Request_api import EmptyPostRequest

base_url = "https://web-agr.chitai-gorod.ru/web/api/v2"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjQxNzkxNDEsImlhdCI6MTc3NjQ0MDM2MywiZXhwIjoxNzc2NDQzOTYzLCJ0eXBlIjoyMCwianRpIjoiMDE5ZDljMTgtY2I5OS03MzE2LWI2N2QtZjgyY2Q2MTU1OTE4Iiwicm9sZXMiOjEwfQ.Ey3P-bF0xLhjyi_c7vrttrKiZndep82vm4t0LMAaSeVvuUSROjVcrCDkmHnPIbIf-RpHSYoxv0xVfJwLhyk2ujoueoM4vFXukYZlfAgaXe81cTTZcOCXdBHpjMnsX4kO94N7lLA4F46LacnG2UvCs9SFm_f_kxwby-rZHD8WOAP_as2E9AfHSJ0uMQ6-0-8ZCW1kCyvKRMqfIXTi_YOkOp3UZqzO6EduJhz8blXhIrSyj-XNq2-jiKM2qIwLGFYBI24gV3MggZgYoNK7Te2qE2h3E5t9zSPviEkApk9grooYM1-jrRx2_8YTBma18-DTQLOOaMWsIfvroNPaLTAw5g"
def test_search():
    book = "запах смерти"
    param_q = {"phrase": f"{book}"}
    my_headers = {"authorization": f"Bearer {token}"}
    res = requests.get(url = f"{base_url}/search/product", params=param_q, headers=my_headers)
    assert res.status_code == 200

    data = res.json()
    title = data['data']['attributes']['seo']['title']
    assert book in title
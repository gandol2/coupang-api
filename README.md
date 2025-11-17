# Coupang Open API Python Wrapper

**coupang**은 쿠팡 오픈 API의 파이썬 래퍼(Python wrapper)입니다.  
현재 10개의 주제에 대해 구현되어 있으며, Python 표준 라이브러리만으로 작동합니다.

## 🚀 빠른 시작

### 설치

```bash
# pip로 설치 (PyPI 등록 전)
pip install git+https://github.com/gandol2/coupang-api.git

# uv로 설치
uv add git+https://github.com/gandol2/coupang-api.git

# 로컬 경로로 설치 (개발 모드)
uv add --editable ./coupang-api
```

### 설정

프로젝트 루트에 `coupang.ini` 파일을 생성하세요:

```ini
[DEFAULT]
SECRETKEY = 발급받은_SecretKey
ACCESSKEY = 발급받은_AccessKey
VENDOR_ID = 업체코드
```

> API Key는 [쿠팡 오픈 API](https://developers.coupang.com/hc/ko/articles/360033980613)에서 발급받을 수 있습니다.

### 기본 사용법

```python
from coupang.category import get_product_auto_category, get_category_meta
from coupang.product import get_products_by_query, get_product_by_product_id
from coupang.ordersheet import get_ordersheet

# 1. 카테고리 자동 추천 (머신러닝)
result = get_product_auto_category({'productName': '무선 이어폰'})
print(result)
# {'code': 200, 'message': 'OK',
#  'data': {'predictedCategoryId': '12345', 'predictedCategoryName': '이어폰'}}

# 2. 카테고리 메타 정보 조회
category_meta = get_category_meta({'displayCategoryCode': '12345'})
print(category_meta)

# 3. 상품 목록 조회
products = get_products_by_query({
    'sellerProductName': '무선 이어폰',
    'page': 1,
    'size': 20
})

# 4. 특정 상품 상세 조회
product_detail = get_product_by_product_id({'productId': '123456'})

# 5. 발주서 조회 (일단위)
orders = get_ordersheet(
    path={'createdAt': 'days'},
    query={'createdAtFrom': '2025-01-01', 'createdAtTo': '2025-01-31'}
)
```

### 고급 사용 - 커스텀 함수 추가

이 패키지는 데코레이터 기반으로 쉽게 확장할 수 있습니다:

```python
import json
from coupang.common import coupang

@coupang
def custom_api_call(path):
    """커스텀 API 호출 예시"""
    return {
        'method': "GET",
        'path': f"/v2/providers/seller_api/apis/api/v1/custom/{path.get('id')}"
    }

# 사용
result = custom_api_call({'id': '12345'})
```

## 📋 API 함수 목록

현재 10개의 주제에 대해 구현되어 있으며, 그 내용은 아래와 같습니다.

1. 카테고리 API(category)
    - 카테고리 메타정보 조회
        - get_category_meta(path)
    - 카테고리 추천
        - get_product_auto_category(body)
    - 카테고리 목록조회
        - get_categories()
    - 카테고리 조회
        - get_category(path)
    - 카테고리 유효성 검사
        - get_category_validation(path)
2. 물류센터 API(shipping)
    - 출고지 생성
        - register_outbound_shipping_center(body)
    - 출고지 조회
        - outbound_shipping_place(query)
    - 출고지 수정
        - update_outbound_shipping_place(body)
    - 반품지 생성
        - update_shipping_center_by_vendor(path, body)
    - 반품지 목록 조회
        - get_shipping_center_by_vendor(path, query)
    - 반품지 수정
        - update_shipping_center_by_return_center_code(path, body)
    - 반품지 단건 조회
        - get_shipping_by_center_code(query)
3. 상품 API(product)
    - 상품 생성
        - create_product(body)
    - 상품 승인 요청
        - approve_product(path)
    - 상품 조회
        - get_product_by_product_id(path)
    - 상품 조회(승인불필요)
        - get_partial_product_by_product_id(path)
        - 해당 상품의 배송 및 반품지 등의 관련 정보를 조회
    - 상품 수정(승인필요)
        - update_product(body)
    - 상품 수정(승인불필요)
        - update_partial_product(body)
        - 배송 및 반품지 관련 정보를 별도의 승인 절차 없이 빠르게 수정
    - 상품 삭제
        - delete_product(path)
    - 상품 등록 현황 조회
        - get_inflow_status()
    - 상품 목록 페이징 조회
        - get_products_by_query(query)
    - 상품 목록 구간 조회
        - get_products_by_time_frame(query)
    - 상품 상태변경이력 조회
        - get_product_status_history(query)
    - 상품 요약 정보 조회
        - get_product_by_external_sku(path)
    - 상품 아이템별 수량/가격/상태 조회
        - get_product_quantity_price_status(path)
    - 상품 아이템별 수량 변경
        - update_product_quantity_by_item(path)
    - 상품 아이템별 가격 변경
        - update_product_price_by_item(path)
    - 상품 아이템별 판매 재개
        - resume_product_sales_by_item(path)
    - 상품 아이템별 판매 중지
        - stop_product_sales_by_item(path)
4. 배송/환불 API(ordersheet)
    - 발주서 목록 조회(일단위/분단위)
        - get_ordersheet(path, query)
    - 발주서 단건 조회(shipment_box_id)
        - get_ordersheet_by_shipmentboxid(path)
    - 발주서 단건 조회(order_id)
        - get_ordersheet_by_orderid(path)
    - 배송상태 변경 히스토리 조회
        - get_ordersheet_history(path)
    - 상품준비중 처리
        - update_ordersheet_status(body)
    - 송장업로드 처리
        - update_order_shipping_info(body)
    - 송장업데이트 처리
        - update_order_invoice(body)
    - 출고중지완료 처리
        - stop_return_request_shipment(body)
    - 이미출고 처리
        - stop_return_request_by_receipt(body)
    - 주문 상품 취소 처리
        - cancel_order_processing(body)
    - 장기 미배송 완료 처리
        - update_invoice_delivery_by_invoice_no(path, body)
5. 반품 API(returns)
    - 반품/취소 요청 목록 조회
        - get_return_request_by_query(path, query)
    - 반품요청 단건 조회
        - get_return_request_by_receipt(path)
    - 반품상품 입고 확인 처리
        - get_return_request_confirmation(body)
    - 반품요청 승인 처리
        - approve_return_request_by_receipt(body)
    - 반품철회 이력 기간별 조회
        - get_return_withdraw_request(path, query)
    - 반품철회 이력 접수번호로 조회
        - get_return_withdraw_by_cancel_ids(path, body)
    - 회수 송장 등록
        - create_return_exchange_invoice(path, body)
6. 교환 API(exchange)
    - 교환요청 목록조회
        - get_exchange_request(path, query)
    - 교환요청상품 입고 확인처리
        - confirm_exchange_request(body)
    - 교환요청 거부 처리
        - reject_exchange_request(body)
    - 교환상품 송장 업로드 처리
        - update_invoice_exchange_request(body)
7. CS API(cs)
    - 상품별 고객문의 조회
        - get_customer_service_request(query)
    - 상품별 고객문의 답변
        - update_customer_service_request(path, body)
    - 쿠팡 콜센터 문의 조회
        - get_inquiry_by_query(query)
    - 쿠팡 콜센터 문의 답변
        - update_inquiry(body)
    - 쿠팡 콜센터 문의 확인
        - confirm_inquiry(path, body)
8. 정산 API(settlement)
    - 매출내역 조회
        - get_revenue_history(query)
    - 지급내역 조회
        - settlement_histories(query)
9. 검색(search)
    - 상품검색
        - search(keywords)
10. 로켓그로스 API(rocketgrowth)
    - 로켓그로스 주문 목록 조회
        - get_rocketgrowth_orders(query)
    - 로켓그로스 주문 상세 조회
        - get_rocketgrowth_order_detail(path)
    - 로켓창고 재고 조회
        - get_rocketwarehouse_inventory(query)
    - 로켓그로스 상품 목록 페이징 조회
        - get_rocketgrowth_products_by_query(query)
    - 로켓그로스 상품 생성
        - create_rocketgrowth_product(body)
    - 로켓그로스 상품 수정
        - update_rocketgrowth_product(body)
    - 로켓그로스 상품 조회
        - get_rocketgrowth_product_by_id(path)
    - 로켓그로스 카테고리 메타 정보 조회
        - get_rocketgrowth_category_meta(path)
    - 로켓그로스 카테고리 목록 조회
        - get_rocketgrowth_categories()

## 📝 매개변수 안내

-   **path**: Path Segment Parameter (dict 자료형)
-   **body**: Body Parameter (dict 자료형)
-   **query**: Query String Parameter (dict 자료형)
-   **keywords**: 검색 키워드 (str 자료형, search 함수 전용)

## 📚 참고 자료

-   [쿠팡 오픈 API 공식문서](https://developers.coupang.com/hc/ko)
-   [API Key 발급 가이드](https://developers.coupang.com/hc/ko/articles/360033980613)

## 🔧 개발 환경

-   Python >= 3.8
-   외부 의존성 없음 (표준 라이브러리만 사용)
-   빌드 시스템: hatchling

## 📄 라이선스

이 프로젝트는 원본 저장소에서 포크되었으며, uv 호환성을 위해 재구조화되었습니다.

## 🤝 기여

이슈와 Pull Request는 언제나 환영합니다!

import json
import urllib.parse
from common import coupang


##############################################################################
# 로켓그로스 주문 관련 함수                                                  # 
##############################################################################


@coupang
def get_rocketgrowth_orders(query):
    '''로켓그로스 주문 목록 조회
    
    특정 기간 동안의 로켓그로스 주문 목록을 조회합니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    paidDateFrom: 검색 시작일 (필수, 형식: 'YYYYMMDD')
    paidDateTo: 검색 종료일 (필수, 형식: 'YYYYMMDD')
    nextToken: 다음 페이지 토큰 (선택)
    
    [예시]
    query = {
        'vendorId': 'A00012345',
        'paidDateFrom': '20240101',
        'paidDateTo': '20240131'
    }
    
    [반환값]
    {
        'data': {
            'orders': [...],
            'nextToken': '...'
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/41131195825433
    '''
    
    vendor_id = query.get('vendorId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/rg_open_api/apis/api/v1/vendors/{vendor_id}/rg/orders",
        'query': urllib.parse.urlencode({k: v for k, v in query.items() if k != 'vendorId'})
    }


@coupang
def get_rocketgrowth_order_detail(path):
    '''로켓그로스 주문 상세 조회
    
    특정 로켓그로스 주문의 상세 정보를 조회합니다.
    
    [path 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    orderId: 주문 번호 (필수)
    
    [예시]
    path = {
        'vendorId': 'A00012345',
        'orderId': '1234567890'
    }
    
    [반환값]
    {
        'data': {
            'orderId': '...',
            'orderDate': '...',
            'items': [...],
            ...
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/41129805240473
    '''
    
    vendor_id = path.get('vendorId')
    order_id = path.get('orderId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/rg_open_api/apis/api/v1/vendors/{vendor_id}/rg/order/{order_id}"
    }


##############################################################################
# 로켓창고 재고 관련 함수                                                    # 
##############################################################################


@coupang
def get_rocketwarehouse_inventory(query):
    '''로켓창고 재고 조회
    
    로켓창고에 보관된 상품의 재고 정보를 조회합니다.
    국내 로켓 물류센터의 재고 현황을 확인할 수 있습니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    vendorItemId: 판매자 상품 아이템 ID (선택)
    nextToken: 다음 페이지 토큰 (선택)
    
    [예시 1] 전체 재고 조회
    query = {
        'vendorId': 'A00012345'
    }
    
    [예시 2] 특정 상품 재고 조회
    query = {
        'vendorId': 'A00012345',
        'vendorItemId': '1234567890'
    }
    
    [반환값]
    {
        'data': {
            'inventories': [
                {
                    'vendorItemId': '...',
                    'availableQuantity': 100,
                    'reservedQuantity': 10,
                    ...
                },
                ...
            ],
            'nextToken': '...'
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/41090779386521
    '''
    
    vendor_id = query.get('vendorId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/rg_open_api/apis/api/v1/vendors/{vendor_id}/rg/inventory/summaries",
        'query': urllib.parse.urlencode({k: v for k, v in query.items() if k != 'vendorId'})
    }


##############################################################################
# 로켓그로스 상품 관련 함수                                                  # 
##############################################################################


@coupang
def get_rocketgrowth_products_by_query(query):
    '''로켓그로스 상품 목록 페이징 조회
    
    등록된 로켓그로스 및 로켓그로스/마켓플레이스 동시 운영 상품 목록을
    페이징 방식으로 조회합니다.
    
    [query 파라미터]
    nextToken: 다음 페이지 토큰 (선택)
    maxPerPage: 페이지당 최대 결과 수 (선택, 기본값: 50, 최대: 100)
    status: 상품 상태 (선택)
        - APPROVAL_REQUESTED: 승인 요청
        - APPROVED: 승인 완료
        - ON_SALE: 판매 중
        - SUSPENSION: 판매 중지
    sellerProductName: 상품명 검색 (선택)
    
    [예시]
    query = {
        'status': 'ON_SALE',
        'maxPerPage': 50
    }
    
    [반환값]
    {
        'code': 'SUCCESS',
        'data': {
            'content': [...],
            'nextToken': '...'
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/39427498030745
    '''
    
    return {
        'method': "GET",
        'path': "/v2/providers/seller_api/apis/api/v1/marketplace/seller-products",
        'query': urllib.parse.urlencode(query)
    }


@coupang
def create_rocketgrowth_product(body):
    '''로켓그로스 상품 생성
    
    쿠팡에서 판매할 로켓그로스 및 마켓플레이스/로켓그로스 동시 운영 상품을 등록합니다.
    
    [주의]
    - 초당 10건 이하로 호출
    - requested 파라미터를 true로 설정하면 자동으로 판매 승인 요청
    
    [body 파라미터]
    sellerProductName: 상품명 (필수)
    vendorId: 판매자 ID (필수)
    saleStartedAt: 판매 시작일시 (필수)
    saleEndedAt: 판매 종료일시 (필수)
    displayCategoryCode: 노출 카테고리 코드 (필수)
    brand: 브랜드명 (필수)
    deliveryMethod: 배송 방식 (필수)
    deliveryCompanyCode: 배송업체 코드 (필수)
    deliveryChargeType: 배송비 타입 (필수)
    items: 상품 아이템 정보 리스트 (필수)
    images: 상품 이미지 정보 리스트 (필수)
    notices: 상품고시 정보 리스트 (필수)
    requested: 승인 요청 여부 (선택, 기본값: false)
    
    [예시]
    body = {
        "sellerProductName": "테스트 상품",
        "vendorId": "A00012345",
        "saleStartedAt": "2024-01-01T00:00:00",
        "saleEndedAt": "2024-12-31T23:59:59",
        "displayCategoryCode": "194176",
        "brand": "테스트 브랜드",
        "deliveryMethod": "SEQUENCIAL",
        "deliveryCompanyCode": "CJGLS",
        "deliveryChargeType": "FREE",
        "items": [...],
        "images": [...],
        "notices": [...],
        "requested": true
    }
    
    [반환값]
    {
        'code': 'SUCCESS',
        'data': {
            'sellerProductId': 1234567890
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/39406974365849
    '''
    
    return {
        'method': "POST",
        'path': "/v2/providers/seller_api/apis/api/v1/marketplace/seller-products",
        'body': json.dumps(body).encode('utf-8')
    }


@coupang
def update_rocketgrowth_product(body):
    '''로켓그로스 상품 수정
    
    등록된 로켓그로스 또는 마켓플레이스/로켓그로스 동시 운영 상품 정보를 수정합니다.
    상품 조회 API로 조회된 JSON 전문에서 원하는 값만 수정 후 전체 JSON 전문을 전송합니다.
    
    [주의]
    - 수정 후 승인이 필요할 수 있음
    - requested 파라미터를 true로 설정하면 자동으로 판매 승인 요청
    
    [body 파라미터]
    sellerProductId: 판매자 상품 ID (필수)
    sellerProductName: 상품명 (필수)
    vendorId: 판매자 ID (필수)
    ... (상품 생성과 동일한 필드들)
    
    [예시]
    body = {
        "sellerProductId": 1234567890,
        "sellerProductName": "수정된 상품명",
        "vendorId": "A00012345",
        ...
    }
    
    [반환값]
    {
        'code': 'SUCCESS',
        'data': {
            'sellerProductId': 1234567890
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/39407792403609
    '''
    
    return {
        'method': "PUT",
        'path': "/v2/providers/seller_api/apis/api/v1/marketplace/seller-products",
        'body': json.dumps(body).encode('utf-8')
    }


@coupang
def get_rocketgrowth_product_by_id(path):
    '''로켓그로스 상품 조회
    
    등록된 로켓그로스 또는 마켓플레이스/로켓그로스 동시 운영 상품의 정보를 조회합니다.
    
    [path 파라미터]
    sellerProductId: 판매자 상품 ID (필수)
    
    [예시]
    path = {'sellerProductId': '1234567890'}
    
    [반환값]
    {
        'code': 'SUCCESS',
        'data': {
            'sellerProductId': 1234567890,
            'sellerProductName': '...',
            'items': [
                {
                    'vendorItemId': '...',
                    ...
                }
            ],
            ...
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/37338749441689
    '''
    
    return {
        'method': "GET",
        'path': f"/v2/providers/seller_api/apis/api/v1/marketplace/seller-products/{path.get('sellerProductId')}"
    }


##############################################################################
# 로켓그로스 카테고리 관련 함수                                              # 
##############################################################################


@coupang
def get_rocketgrowth_category_meta(path):
    '''로켓그로스 카테고리 메타 정보 조회
    
    노출 카테고리 코드를 이용하여 해당 카테고리에 속한 정보를 조회합니다.
    - 고시정보 (법적 고시사항)
    - 옵션 (색상, 사이즈 등)
    - 구비서류
    - 인증정보 목록
    
    [path 파라미터]
    displayCategoryCode: 노출 카테고리 코드 (필수)
    
    [예시]
    path = {'displayCategoryCode': '194176'}
    
    [반환값]
    {
        'code': 'SUCCESS',
        'data': {
            'displayCategoryCode': '194176',
            'requiredDocuments': [...],
            'certifications': [...],
            'notices': [...],
            'attributes': [...],
            'options': [...]
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/39429124103449
    '''
    
    return {
        'method': "GET",
        'path': f"/v2/providers/seller_api/apis/api/v1/marketplace/meta/display-categories/{path.get('displayCategoryCode')}"
    }


@coupang
def get_rocketgrowth_categories():
    '''로켓그로스 카테고리 목록 조회
    
    로켓그로스 운영 카테고리의 전체 목록을 조회합니다.
    카테고리 코드와 카테고리명을 포함한 계층 구조 정보를 반환합니다.
    
    [반환값]
    {
        'code': 'SUCCESS',
        'data': [
            {
                'displayCategoryCode': '...',
                'displayCategoryName': '...',
                'children': [...]
            },
            ...
        ]
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/39428894927257
    '''
    
    return {
        'method': "GET",
        'path': "/v2/providers/seller_api/apis/api/v1/marketplace/meta/rg/display-category-codes"
    }


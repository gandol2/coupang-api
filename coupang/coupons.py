import json
import urllib.parse
from coupang.common import coupang

##############################################################################
# (공통) 예산 및 계약서 관련 함수                                              # 
##############################################################################


@coupang
def get_budget_status(query):
    '''공통 예산현황 조회
    
    현재 설정된 모든 계약의 쿠폰 예산 현황을 조회합니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    contractId: 계약서 ID (선택, 자유계약의 경우 -1 입력, 기본값: 모든 계약 조회)
    targetMonth: 조회하고자 하는 예산월 (선택, 형식: 'YYYY-MM', 입력하지 않으면 현재 월 조회)
    
    [예시 1] 특정 계약의 특정 월 예산 조회
    query = {
        'vendorId': 'A00012345',
        'contractId': 10,
        'targetMonth': '2024-11'
    }
    
    [예시 2] 자유계약 예산 조회
    query = {
        'vendorId': 'A00012345',
        'contractId': -1,
        'targetMonth': '2024-11'
    }
    
    [예시 3] 모든 계약의 현재 월 예산 조회
    query = {
        'vendorId': 'A00012345'
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': [
                {
                    'contractId': 10,
                    'contractName': '계약명',
                    'targetMonth': '2024-11',
                    'totalBudget': 1000000,
                    'usedBudget': 500000,
                    'remainingBudget': 500000,
                    ...
                },
                ...
            ]
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360033922353
    '''
    
    vendor_id = query.get('vendorId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/budgets",
        'query': urllib.parse.urlencode({k: v for k, v in query.items() if k != 'vendorId'})
    }


@coupang
def get_contract(query):
    '''공통 계약서 단건 조회
    
    특정 계약서 ID에 해당하는 계약서의 상세 정보를 조회합니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    contractId: 계약서 ID (필수, 조회할 계약서 ID)
    
    [예시]
    query = {
        'vendorId': 'A00012345',
        'contractId': 9962
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'contractId': 9962,
                'contractName': '계약명',
                'status': 'ACTIVE',
                'startDate': '2024-01-01',
                'endDate': '2024-12-31',
                'totalBudget': 10000000,
                ...
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034204213
    '''
    
    vendor_id = query.get('vendorId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/contract",
        'query': urllib.parse.urlencode({k: v for k, v in query.items() if k != 'vendorId'})
    }



@coupang
def get_contracts(query):
    '''공통 계약서 목록 조회
    
    현재 설정된 모든 계약서의 목록을 조회합니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    
    [예시]
    query = {
        'vendorId': 'A00012345'
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': [
                {
                    'contractId': 10,
                    'contractName': '계약명',
                    'status': 'ACTIVE',
                    'startDate': '2024-01-01',
                    'endDate': '2024-12-31',
                    ...
                },
                ...
            ]
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034204233
    '''
    
    vendor_id = query.get('vendorId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/contracts"
    }




##############################################################################
# [즉시할인쿠폰] 관련 함수                                                     # 
##############################################################################


@coupang
def create_instant_discount_coupon(body):
    '''즉시할인쿠폰 생성
    
    쿠팡에서 사용할 즉시할인쿠폰을 생성합니다.
    쿠폰 생성 요청은 비동기로 처리되며, requestedId로 요청 상태를 확인할 수 있습니다.
    
    [주의]
    - WING에서 예산을 설정하여 계약서 ID(contractId)를 먼저 발급받아야 합니다.
    - 쿠폰 생성 후 쿠폰 아이템을 생성해야 특정 상품에 적용됩니다.
    - 유효 시작일과 종료일을 정확히 설정해야 합니다.
    
    [body 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    contractId: 계약서 ID (필수, WING에서 발급받은 계약서 ID)
    name: 프로모션명 (필수, 최대 45자)
    maxDiscountPrice: 최대 할인 금액 (필수, 최소 10원 이상)
    discount: 할인율 (필수)
    startAt: 유효 시작일 (필수, 형식: 'YYYY-MM-DD HH:MM:SS')
    endAt: 유효 종료일 (필수, 형식: 'YYYY-MM-DD HH:MM:SS')
    type: 할인 방식 (필수, 'RATE'|'FIXED_WITH_QUANTITY'|'PRICE')
        - RATE: 정률 할인
        - FIXED_WITH_QUANTITY: 수량 고정 할인
        - PRICE: 정액 할인
    wowExclusive: 로켓와우 회원 전용 여부 (선택, 기본값: 'false')
        - false: 전체 고객 대상
        - true: 로켓와우 회원 한정
    
    [예시]
    body = {
        "vendorId": "A00012345",
        "contractId": "10",
        "name": "신규 쿠폰 20240101",
        "maxDiscountPrice": "1000",
        "discount": "10",
        "startAt": "2024-01-01 00:00:00",
        "endAt": "2024-12-31 23:59:59",
        "type": "PRICE",
        "wowExclusive": "false"
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestedId': '12345678'
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034208913
    '''
    
    vendor_id = body.get('vendorId')
    
    # vendorId는 path에 사용되므로 body에서 제외
    request_body = {k: v for k, v in body.items() if k != 'vendorId'}
    
    return {
        'method': "POST",
        'path': f"/v2/providers/fms/apis/api/v2/vendors/{vendor_id}/coupon",
        'body': json.dumps(request_body).encode('utf-8')
    }


@coupang
def expire_instant_discount_coupon(query):
    '''즉시할인쿠폰 파기
    
    생성된 즉시할인쿠폰을 파기합니다.
    쿠폰 파기 요청은 비동기로 처리되며, requestedId로 요청 상태를 확인할 수 있습니다.
    
    [주의]
    - 파기된 쿠폰은 복구할 수 없습니다.
    - 이미 발급된 쿠폰에는 영향을 주지 않습니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    couponId: 쿠폰 ID (필수, 파기할 쿠폰 ID)
    
    [예시]
    query = {
        'vendorId': 'A00012345',
        'couponId': 684245
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestedId': '87654321'
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034208973
    '''
    
    vendor_id = query.get('vendorId')
    coupon_id = query.get('couponId')
    
    return {
        'method': "PUT",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/coupons/{coupon_id}",
        'query': 'action=expire'
    }


@coupang
def get_instant_discount_request_status(path):
    '''즉시할인쿠폰 요청상태 확인
    
    즉시할인쿠폰 관련 API(생성, 파기, 아이템 생성 등)의 요청 상태를 확인합니다.
    비동기로 처리되는 요청의 성공/실패 여부를 requestedId를 통해 조회합니다.
    
    [path 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    requestedId: 요청 ID (필수, 쿠폰 생성/파기/아이템 생성 시 반환된 ID)
    
    [예시]
    path = {
        'vendorId': 'A00012345',
        'requestedId': '12345678'
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestedId': '12345678',
                'status': 'SUCCESS',
                'message': '처리 완료'
            }
        }
    }
    
    [status 값]
    - REQUESTED: 요청됨
    - INPROGRESS: 처리 중
    - SUCCESS: 성공
    - FAIL: 실패
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360033685834
    '''
    
    vendor_id = path.get('vendorId')
    requested_id = path.get('requestedId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/requested/{requested_id}"
    }


@coupang
def create_instant_discount_coupon_items(body):
    '''즉시할인쿠폰 아이템 생성
    
    생성된 쿠폰을 특정 상품(아이템)에 적용합니다.
    쿠폰 아이템 생성 요청은 비동기로 처리되며, requestedId로 요청 상태를 확인할 수 있습니다.
    
    [주의]
    - 한 번의 호출에 최대 10,000개의 vendorItemId를 적용할 수 있습니다.
    - vendorItemId는 옵션 ID를 의미합니다.
    
    [body 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    couponId: 쿠폰 ID (필수)
    vendorItems: 적용할 옵션 ID 리스트 (필수, 배열, 최대 10,000개)
    
    [예시]
    body = {
        'vendorId': 'A00012345',
        'couponId': 68,
        'vendorItems': [3226138951, 3226138847, 3226138900]
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestedId': '87654321'
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034209053
    '''
    
    vendor_id = body.get('vendorId')
    coupon_id = body.get('couponId')
    
    # vendorId와 couponId는 path에 사용되므로 body에서 제외
    request_body = {k: v for k, v in body.items() if k not in ['vendorId', 'couponId']}
    
    return {
        'method': "POST",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/coupons/{coupon_id}/items",
        'body': json.dumps(request_body).encode('utf-8')
    }


@coupang
def get_instant_discount_coupons_by_status(query):
    '''즉시할인쿠폰 목록 조회 (status)
    
    쿠폰 상태를 기준으로 즉시할인쿠폰 목록을 조회합니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    status: 쿠폰 상태 (필수)
        - STANDBY: 대기 중
        - APPLIED: 적용됨
        - PAUSED: 일시 중지
        - EXPIRED: 만료됨
    page: 페이지 번호 (선택, 기본값: 0)
    size: 페이지 당 건수 (선택, 기본값: 10)
    sort: 정렬 순서 (선택, 'asc' 또는 'desc', 기본값: 'asc')
    
    [예시]
    query = {
        'vendorId': 'A00012345',
        'status': 'APPLIED',
        'page': 0,
        'size': 20,
        'sort': 'desc'
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': [
                {
                    'couponId': 684245,
                    'couponName': '쿠폰명',
                    'status': 'APPLIED',
                    ...
                },
                ...
            ],
            'totalElements': 100,
            'totalPages': 5
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034209513
    '''
    
    vendor_id = query.get('vendorId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/coupons",
        'query': urllib.parse.urlencode({k: v for k, v in query.items() if k != 'vendorId'})
    }


@coupang
def get_instant_discount_coupons_by_order_id(query):
    '''즉시할인쿠폰 목록 조회 (orderId)
    
    주문번호를 기준으로 즉시할인쿠폰 목록을 조회합니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    orderId: 주문 번호 (필수)
    page: 페이지 번호 (선택, 기본값: 0)
    size: 페이지 당 건수 (선택, 기본값: 10)
    sort: 정렬 순서 (선택, 'asc' 또는 'desc', 기본값: 'asc')
    
    [예시]
    query = {
        'vendorId': 'A00012345',
        'orderId': '1234567890',
        'page': 0,
        'size': 20
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': [
                {
                    'couponId': 684245,
                    'couponName': '쿠폰명',
                    'orderId': '1234567890',
                    ...
                },
                ...
            ],
            'totalElements': 10,
            'totalPages': 1
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034209573
    '''
    
    vendor_id = query.get('vendorId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/coupons",
        'query': urllib.parse.urlencode({k: v for k, v in query.items() if k != 'vendorId'})
    }


@coupang
def get_instant_discount_coupon_items_by_status(query):
    '''즉시할인쿠폰 아이템 목록 조회 (status)
    
    쿠폰 상태를 기준으로 쿠폰이 적용된 아이템(옵션 ID) 목록을 조회합니다.
    
    [query 파라미터]
    vendorId: 판매자 ID (필수, 예: 'A00012345')
    couponId: 쿠폰 ID (필수)
    status: 쿠폰 상태 (필수)
        - STANDBY: 대기 중
        - APPLIED: 적용됨
        - PAUSED: 일시 중지
        - EXPIRED: 만료됨
    page: 페이지 번호 (선택, 기본값: 0)
    size: 페이지 당 건수 (선택, 기본값: 10)
    sort: 정렬 순서 (선택, 'asc' 또는 'desc', 기본값: 'asc')
    
    [예시]
    query = {
        'vendorId': 'A00012345',
        'couponId': 99,
        'status': 'APPLIED',
        'page': 0,
        'size': 50,
        'sort': 'asc'
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': [
                {
                    'vendorItemId': 3226138951,
                    'status': 'APPLIED',
                    ...
                },
                ...
            ],
            'totalElements': 200,
            'totalPages': 4
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034209633
    '''
    
    vendor_id = query.get('vendorId')
    coupon_id = query.get('couponId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/fms/apis/api/v1/vendors/{vendor_id}/coupons/{coupon_id}/items",
        'query': urllib.parse.urlencode({k: v for k, v in query.items() if k not in ['vendorId', 'couponId']})
    }




##############################################################################
# [다운로드쿠폰] 관련 함수                                                     # 
##############################################################################


@coupang
def create_download_coupon(body):
    '''다운로드쿠폰 생성
    
    고객이 다운로드하여 사용할 수 있는 쿠폰을 생성합니다.
    쿠폰 생성 요청은 비동기로 처리되며, requestedId로 요청 상태를 확인할 수 있습니다.
    
    [주의]
    - WING에서 예산을 설정하여 계약서 ID(contractId)를 먼저 발급받아야 합니다.
    - 쿠폰 생성 후 쿠폰 아이템을 생성해야 특정 상품에 적용됩니다.
    - 정책(policies)은 배열 형태로 여러 개 설정 가능합니다.
    
    [body 파라미터]
    title: 쿠폰 명칭 (필수)
    contractId: 계약서 ID (필수)
    couponType: 쿠폰 유형 (필수, 'DOWNLOAD' 고정)
    startDate: 유효 시작일 (필수, 형식: 'YYYY-MM-DD HH:MM:SS')
    endDate: 유효 종료일 (필수, 형식: 'YYYY-MM-DD HH:MM:SS')
    userId: 사용자 ID (필수, WING 로그인 계정)
    policies: 할인 정책 리스트 (필수, 배열)
        - title: 정책 명칭 (필수)
        - typeOfDiscount: 할인 유형 (필수, 'RATE'|'PRICE')
            * RATE: 정률 할인
            * PRICE: 정액 할인
        - description: 정책 설명 (필수)
        - minimumPrice: 최소 구매 금액 (필수)
        - discount: 할인율 또는 할인 금액 (필수)
        - maximumDiscountPrice: 최대 할인 금액 (필수)
        - maximumPerDaily: 일일 최대 다운로드 수 (필수)
    
    [예시]
    body = {
        "title": "신규 다운로드 쿠폰",
        "contractId": 15,
        "couponType": "DOWNLOAD",
        "startDate": "2024-01-01 00:00:00",
        "endDate": "2024-12-31 23:59:59",
        "userId": "testaccount1",
        "policies": [
            {
                "title": "정액 할인 정책",
                "typeOfDiscount": "PRICE",
                "description": "10,000원 이상 구매 시 1,000원 할인",
                "minimumPrice": 10000,
                "discount": 1000,
                "maximumDiscountPrice": 1000,
                "maximumPerDaily": 1
            }
        ]
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestedId': '12345678'
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034205493
    '''
    
    return {
        'method': "POST",
        'path': "/v2/providers/marketplace_openapi/apis/api/v1/coupons",
        'body': json.dumps(body).encode('utf-8')
    }


@coupang
def expire_download_coupon(body):
    '''다운로드쿠폰 파기
    
    생성된 다운로드쿠폰을 파기합니다.
    쿠폰 파기 요청은 비동기로 처리되며, requestedId로 요청 상태를 확인할 수 있습니다.
    
    [주의]
    - 파기된 쿠폰은 복구할 수 없습니다.
    - 이미 고객이 다운로드한 쿠폰에는 영향을 주지 않습니다.
    
    [body 파라미터]
    couponId: 쿠폰 ID (필수, 파기할 쿠폰 ID)
    userId: 사용자 ID (필수, WING 로그인 계정)
    
    [예시]
    body = {
        "couponId": 15350660,
        "userId": "testaccount1"
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestedId': '87654321'
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360033683034
    '''
    
    return {
        'method': "PUT",
        'path': "/v2/providers/marketplace_openapi/apis/api/v1/coupons/expire",
        'body': json.dumps(body).encode('utf-8')
    }


@coupang
def create_download_coupon_items(body):
    '''다운로드쿠폰 아이템 생성
    
    생성된 다운로드쿠폰을 특정 상품(아이템)에 적용합니다.
    쿠폰 아이템 생성 요청은 비동기로 처리되며, requestedId로 요청 상태를 확인할 수 있습니다.
    
    [주의]
    - 다운로드쿠폰을 먼저 생성한 후 아이템을 생성해야 합니다.
    - vendorItemId는 판매자 상품 아이템 ID(옵션 ID)를 의미합니다.
    - couponItems 배열에 여러 쿠폰의 아이템을 한 번에 생성할 수 있습니다.
    
    [body 파라미터]
    couponItems: 쿠폰 아이템 정보 리스트 (필수, 배열)
        - couponId: 쿠폰 ID (필수)
        - userId: 사용자 ID (필수, WING 로그인 계정)
        - vendorItemIds: 적용할 상품 아이템 ID 목록 (필수, 배열)
    
    [예시]
    body = {
        "couponItems": [
            {
                "couponId": 15350660,
                "userId": "testaccount1",
                "vendorItemIds": [
                    2306264997,
                    4802314648,
                    4230264914
                ]
            }
        ]
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestedId': '99887766'
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034208773
    '''
    
    return {
        'method': "PUT",
        'path': "/v2/providers/marketplace_openapi/apis/api/v1/coupon-items",
        'body': json.dumps(body).encode('utf-8')
    }


@coupang
def get_download_coupon_request_status(query):
    '''다운로드쿠폰 요청상태 확인
    
    다운로드쿠폰 관련 API(생성, 아이템 생성 등)의 요청 상태를 확인합니다.
    비동기로 처리되는 요청의 성공/실패 여부를 requestTransactionId를 통해 조회합니다.
    
    [query 파라미터]
    requestTransactionId: 요청 트랜잭션 ID (필수, 쿠폰 생성/아이템 생성 시 반환된 ID)
    
    [예시]
    query = {
        'requestTransactionId': 'et5_154210571558673553106'
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'requestTransactionId': 'et5_154210571558673553106',
                'status': 'SUCCESS',
                'message': '처리 완료'
            }
        }
    }
    
    [status 값]
    - PENDING: 대기 중
    - PROCESSING: 처리 중
    - SUCCESS: 성공
    - FAIL: 실패
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360034209973
    '''
    
    return {
        'method': "GET",
        'path': "/v2/providers/marketplace_openapi/apis/api/v1/coupons/transactionStatus",
        'query': urllib.parse.urlencode(query)
    }


@coupang
def get_download_coupon(path):
    '''다운로드쿠폰 단건 조회
    
    특정 쿠폰 ID에 해당하는 다운로드쿠폰의 상세 정보를 조회합니다.
    
    [path 파라미터]
    couponId: 쿠폰 ID (필수)
    
    [예시]
    path = {
        'couponId': 11234224
    }
    
    [반환값]
    {
        'rcode': '0',
        'rMessage': 'success',
        'data': {
            'content': {
                'couponId': 11234224,
                'title': '쿠폰 명칭',
                'contractId': 15,
                'couponType': 'DOWNLOAD',
                'startDate': '2024-01-01 00:00:00',
                'endDate': '2024-12-31 23:59:59',
                'status': 'ACTIVE',
                'policies': [
                    {
                        'title': '정액 할인 정책',
                        'typeOfDiscount': 'PRICE',
                        'description': '10,000원 이상 구매 시 1,000원 할인',
                        'minimumPrice': 10000,
                        'discount': 1000,
                        'maximumDiscountPrice': 1000,
                        'maximumPerDaily': 1
                    }
                ],
                ...
            }
        }
    }
    
    [참고 문서]
    https://developers.coupangcorp.com/hc/ko/articles/360033685974
    '''
    
    coupon_id = path.get('couponId')
    
    return {
        'method': "GET",
        'path': f"/v2/providers/marketplace_openapi/apis/api/v1/coupons/{coupon_id}"
    }


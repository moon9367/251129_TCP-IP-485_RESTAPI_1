#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
REST API Server - Modbus TCP/IP → REST API Conversion
================================================================================
REST API Server converting Modbus TCP Controller to RESTful API

Features:
- GET /api/settings/{name}: Read settings (Word Address 0~59)
- PUT /api/settings/{name}: Write settings (Word Address 0~59)
- GET /api/sensors/{name}: Read sensor values (Word Address 70~79)
- GET /api/status/{name}: Read status (Word Address 60~69, 80~84)
- GET /api/controls/list: List all control items

Auto Swagger Documentation: http://localhost:8000/docs

Usage:
    python rest_api_server.py
    
Required Packages:
    pip install fastapi uvicorn pymodbus python-multipart

Examples:
    # Read sensor (English name)
    GET http://localhost:8000/api/sensors/indoor_current_temperature
    
    # Read sensor (Korean name - also supported)
    GET http://localhost:8000/api/sensors/내부현재온도
    
    # Read setting
    GET http://localhost:8000/api/settings/dehumidifier_auto_mode
    
    # Write setting
    PUT http://localhost:8000/api/settings/dehumidifier_auto_mode
    Body: {"value": 1}
    
    # Check status
    GET http://localhost:8000/api/status/circulation_fan_output_indicator
================================================================================
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import logging
from typing import Optional, Any, Dict, List, Union
import uvicorn
import requests
import xmltodict
from datetime import datetime

# 로컬 모듈 임포트
from control_specs import CONTROL_SPECS, get_spec, list_all, get_by_type, get_by_address
from modbus_tcp_controller import ModbusController

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# FastAPI 앱 생성
# ============================================================================

app = FastAPI(
    title="Modbus TCP REST API Server",
    description="""
    ## REST API Server Converting RS485 Modbus TCP/IP
    
    ### Main Features
    - **Settings Management**: Word Address 0~59 (Read/Write)
    - **Sensor Values**: Word Address 70~79 (Read Only)
    - **Status Check**: Word Address 60~69, 80~84 (Read Only)
    
    ### Type Classification
    - **WRITE Available**: REGISTER_WRITE, BIT_WRITE, BIT_RANGE_WRITE
    - **READ Only**: SENSOR_READ, BIT_READ, REGISTER_READ
    
    ### API Documentation
    - Swagger UI: `/docs`
    - ReDoc: `/redoc`
    
    ### Supported Names
    - **English**: `indoor_current_temperature`, `dehumidifier_auto_mode`, etc.
    - **Korean**: `내부현재온도`, `제습오토모드`, etc. (also supported)
    """,
    version="2.0.0",
    contact={
        "name": "TSPOL NAS Project",
        "url": "https://github.com/your-project"
    }
)

# CORS 설정 (필요시)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modbus 컨트롤러 (전역 인스턴스)
controller: Optional[ModbusController] = None


# ============================================================================
# 요청/응답 모델
# ============================================================================

class WriteRequest(BaseModel):
    """Write Setting Request"""
    value: Union[int, float] = Field(
        ...,
        description="Value to write (integer or float)",
        example=1
    )

class ReadResponse(BaseModel):
    """Read Response"""
    success: bool = Field(..., description="Success status")
    name: str = Field(..., description="Control item name (English)")
    value: Optional[Union[int, float, bool]] = Field(None, description="Read value")
    unit: Optional[str] = Field(None, description="Unit")
    type: Optional[str] = Field(None, description="Type")
    address: Optional[int] = Field(None, description="Word address")
    description: Optional[str] = Field(None, description="Description")
    error: Optional[str] = Field(None, description="Error message")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "name": "indoor_current_temperature",
                "value": 23.5,
                "unit": "°C",
                "type": "SENSOR_READ",
                "address": 70,
                "description": "Indoor current temperature (내부현재온도)"
            }
        }

class WriteResponse(BaseModel):
    """Write Response"""
    success: bool = Field(..., description="Success status")
    name: str = Field(..., description="Control item name (English)")
    written_value: Union[int, float] = Field(..., description="Written value")
    verified_value: Optional[Union[int, float]] = Field(None, description="Verified value")
    type: Optional[str] = Field(None, description="Type")
    address: Optional[int] = Field(None, description="Word address")
    error: Optional[str] = Field(None, description="Error message")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "name": "dehumidifier_auto_mode",
                "written_value": 1,
                "verified_value": 1,
                "type": "BIT_WRITE",
                "address": 18
            }
        }

class ControlInfo(BaseModel):
    """Control Item Information"""
    name: str = Field(..., description="Control item name (English)")
    type: str
    address: int
    unit: Optional[str] = None
    description: Optional[str] = None
    writable: bool
    readable: bool

class ControlListResponse(BaseModel):
    """Control Item List Response"""
    total: int
    writable: int
    readable_only: int
    controls: List[ControlInfo]


# ============================================================================
# 시작/종료 이벤트
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 Modbus 연결"""
    global controller
    logger.info("=" * 70)
    logger.info("🚀 REST API 서버 시작")
    logger.info("=" * 70)
    
    # Modbus 컨트롤러 생성 및 연결
    controller = ModbusController(
        host="aiseednaju.iptime.org",
        port=9139,
        unit_id=1
    )
    
    if controller.connect():
        logger.info("✅ Modbus 연결 성공")
        logger.info(f"   호스트: {controller.host}")
        logger.info(f"   포트: {controller.port}")
        logger.info(f"   Unit ID: {controller.unit_id}")
    else:
        logger.error("❌ Modbus 연결 실패 - 일부 기능이 동작하지 않을 수 있습니다")
    
    logger.info("=" * 70)
    logger.info("📝 API 문서: http://localhost:8000/docs")
    logger.info("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 Modbus 연결 해제"""
    global controller
    if controller:
        controller.close()
        logger.info("🔌 Modbus 연결 종료")
    logger.info("👋 REST API 서버 종료")


# ============================================================================
# 유틸리티 함수
# ============================================================================

def check_connection():
    """Check Modbus connection"""
    if controller is None:
        raise HTTPException(
            status_code=503,
            detail="Modbus controller not initialized"
        )
    if not controller.is_connected():
        # Try to reconnect
        if not controller.connect():
            raise HTTPException(
                status_code=503,
                detail="Modbus not connected - reconnection failed"
            )

def is_writable(spec_type: str) -> bool:
    """Check if the type is writable"""
    writable_types = ['REGISTER_WRITE', 'BIT_WRITE', 'BIT_RANGE_WRITE']
    return spec_type in writable_types

def get_category(spec_type: str) -> str:
    """Get category based on type"""
    if spec_type == 'SENSOR_READ':
        return 'sensors'
    elif is_writable(spec_type):
        return 'settings'
    else:
        return 'status'


# ============================================================================
# Endpoints: Basic
# ============================================================================

@app.get("/", tags=["Basic"])
async def root():
    """Root Endpoint - API Information"""
    return {
        "name": "Modbus TCP REST API Server",
        "version": "3.0.0 (English Only)",
        "status": "running",
        "modbus_connected": controller.is_connected() if controller else False,
        "api_docs": "/docs",
        "endpoints": {
            "settings": "/api/settings/{name}",
            "sensors": "/api/sensors/{name}",
            "status": "/api/status/{name}",
            "list": "/api/controls/list"
        },
        "example_names": ["indoor_current_temperature", "dehumidifier_auto_mode", "heating_on_temperature_setting"]
    }


@app.get("/health", tags=["Basic"])
async def health_check():
    """Health Check"""
    modbus_status = "connected" if (controller and controller.is_connected()) else "disconnected"
    
    return {
        "status": "healthy",
        "modbus": modbus_status,
        "timestamp": "2024-12-09"
    }


# ============================================================================
# Endpoints: Control Items List
# ============================================================================

@app.get("/api/controls/list", response_model=ControlListResponse, tags=["Control List"])
async def list_controls(
    category: Optional[str] = None,
    writable_only: bool = False
):
    """
    List all control items
    
    - **category**: Category filter (settings, sensors, status)
    - **writable_only**: Show only writable items
    """
    controls = []
    
    for name, spec in CONTROL_SPECS.items():
        spec_type = spec.get('type', 'UNKNOWN')
        spec_category = get_category(spec_type)
        writable = is_writable(spec_type)
        
        # Filtering
        if category and spec_category != category:
            continue
        if writable_only and not writable:
            continue
        
        controls.append(ControlInfo(
            name=name,
            type=spec_type,
            address=spec.get('address', 0),
            unit=spec.get('unit'),
            description=spec.get('description'),
            writable=writable,
            readable=True
        ))
    
    writable_count = sum(1 for c in controls if c.writable)
    
    return ControlListResponse(
        total=len(controls),
        writable=writable_count,
        readable_only=len(controls) - writable_count,
        controls=controls
    )


# ============================================================================
# Endpoints: Settings (WRITE Available)
# ============================================================================

@app.get("/api/settings/{name}", response_model=ReadResponse, tags=["Settings"])
async def read_setting(name: str):
    """
    Read setting value (Word Address 0~59)
    
    - **name**: Setting item name (English only)
      - Examples: `dehumidifier_auto_mode`, `heating_on_temperature_setting`
    """
    check_connection()
    
    spec = get_spec(name)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"Control item '{name}' not found")
    
    # Check if it's a writable type
    spec_type = spec.get('type', '')
    if not is_writable(spec_type):
        raise HTTPException(
            status_code=400,
            detail=f"'{name}' is not a setting. Use /api/{get_category(spec_type)}/{name} instead"
        )
    
    # Perform read
    try:
        value = controller.read_by_name(name)
        
        if value is None:
            return ReadResponse(
                success=False,
                name=name,
                type=spec_type,
                address=spec.get('address'),
                description=spec.get('description'),
                error="Read failed"
            )
        
        return ReadResponse(
            success=True,
            name=name,
            value=value,
            unit=spec.get('unit'),
            type=spec_type,
            address=spec.get('address'),
            description=spec.get('description')
        )
    
    except Exception as e:
        logger.error(f"Settings read error ({name}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/settings/{name}", response_model=WriteResponse, tags=["Settings"])
async def write_setting(name: str, request: WriteRequest):
    """
    Write setting value (Word Address 0~59)
    
    - **name**: Setting item name (English only)
    - **value**: Value to write (integer or float)
    
    Example:
    ```json
    {
        "value": 1
    }
    ```
    """
    check_connection()
    
    spec = get_spec(name)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"Control item '{name}' not found")
    
    # Check if it's a writable type
    spec_type = spec.get('type', '')
    if not is_writable(spec_type):
        raise HTTPException(
            status_code=400,
            detail=f"'{name}' is not writable (type: {spec_type})"
        )
    
    # Perform write
    try:
        success = controller.write_by_name(name, request.value)
        
        if not success:
            return WriteResponse(
                success=False,
                name=name,
                written_value=request.value,
                type=spec_type,
                address=spec.get('address'),
                error="Write failed"
            )
        
        # Verify by reading back
        verified_value = controller.read_by_name(name)
        
        return WriteResponse(
            success=True,
            name=name,
            written_value=request.value,
            verified_value=verified_value,
            type=spec_type,
            address=spec.get('address')
        )
    
    except Exception as e:
        logger.error(f"Settings write error ({name}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Endpoints: Sensor Values (READ Only)
# ============================================================================

@app.get("/api/sensors/all", tags=["Sensors"])
async def read_all_sensors():
    """Read all sensor values at once"""
    check_connection()
    
    from control_specs import get_by_type
    sensor_names = get_by_type('SENSOR_READ')
    sensors = {}
    
    for name in sensor_names:
        try:
            spec = get_spec(name)
            value = controller.read_by_name(name)
            
            sensors[name] = {
                "value": value,
                "unit": spec.get('unit'),
                "address": spec.get('address'),
                "description": spec.get('description'),
                "success": value is not None
            }
        except Exception as e:
            sensors[name] = {
                "value": None,
                "unit": spec.get('unit') if spec else None,
                "success": False,
                "error": str(e)
            }
    
    return {
        "success": True,
        "count": len(sensors),
        "sensors": sensors
    }


@app.get("/api/sensors/{name}", response_model=ReadResponse, tags=["Sensors"])
async def read_sensor(name: str):
    """
    Read sensor value (Word Address 70~79)
    
    - **name**: Sensor name (English only)
      - Examples: `indoor_current_temperature`, `outdoor_current_humidity`
    """
    check_connection()
    
    spec = get_spec(name)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"Control item '{name}' not found")
    
    # Check if it's a sensor type
    spec_type = spec.get('type', '')
    if spec_type != 'SENSOR_READ':
        raise HTTPException(
            status_code=400,
            detail=f"'{name}' is not a sensor. Use /api/{get_category(spec_type)}/{name} instead"
        )
    
    # Perform read
    try:
        value = controller.read_by_name(name)
        
        if value is None:
            return ReadResponse(
                success=False,
                name=name,
                type=spec_type,
                address=spec.get('address'),
                description=spec.get('description'),
                error="Sensor read failed"
            )
        
        return ReadResponse(
            success=True,
            name=name,
            value=value,
            unit=spec.get('unit'),
            type=spec_type,
            address=spec.get('address'),
            description=spec.get('description')
        )
    
    except Exception as e:
        logger.error(f"Sensor read error ({name}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Endpoints: Status (READ Only)
# ============================================================================

@app.get("/api/status/{name}", response_model=ReadResponse, tags=["Status"])
async def read_status(name: str):
    """
    Read status value (Word Address 60~69, 80~84)
    
    - **name**: Status item name (English only)
      - Examples: `circulation_fan_output_indicator`, `internal_temperature_sensor_error`
    """
    check_connection()
    
    spec = get_spec(name)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"Control item '{name}' not found")
    
    # Check if it's a READ-only type (excluding SENSOR_READ)
    spec_type = spec.get('type', '')
    if is_writable(spec_type):
        raise HTTPException(
            status_code=400,
            detail=f"'{name}' is not a status. Use /api/settings/{name} instead"
        )
    if spec_type == 'SENSOR_READ':
        raise HTTPException(
            status_code=400,
            detail=f"'{name}' is a sensor value. Use /api/sensors/{name} instead"
        )
    
    # Perform read
    try:
        value = controller.read_by_name(name)
        
        if value is None:
            return ReadResponse(
                success=False,
                name=name,
                type=spec_type,
                address=spec.get('address'),
                description=spec.get('description'),
                error="Status read failed"
            )
        
        return ReadResponse(
            success=True,
            name=name,
            value=value,
            unit=spec.get('unit'),
            type=spec_type,
            address=spec.get('address'),
            description=spec.get('description')
        )
    
    except Exception as e:
        logger.error(f"Status read error ({name}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Weather API (기상청 단기예보 API)
# ============================================================================

def get_current_date_string():
    """현재 날짜를 YYYYMMDD 형식으로 반환"""
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

def get_current_hour_string():
    """base_time 계산 (기상청 API 기준시각)"""
    now = datetime.now()
    if now.minute < 45:  # base_time와 base_date 구하는 함수
        if now.hour == 0:
            base_time = "2330"
        else:
            pre_hour = now.hour - 1
            if pre_hour < 10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"
    return base_time

# 기상청 API 설정
WEATHER_API_KEY = "a7de9d6c66498750cf126311c474f3e510759c74af41adcc43da34d6e68b1274"
WEATHER_API_URL = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

# 나주시 기상청 격자 좌표 (nx=52, ny=87)
# 기상청 API는 GPS 좌표가 아닌 격자 좌표(nx, ny)를 사용합니다
NAJU_NX = "52"
NAJU_NY = "87"

# 날씨 정보 캐시 (API 호출 횟수 제한 대응)
weather_cache = {
    "data": None,
    "timestamp": None,
    "cache_minutes": 10  # 10분간 캐시 유지
}

@app.get("/api/weather/naju", tags=["날씨 정보"])
async def get_naju_weather():
    """
    전라남도 나주시 현재 날씨 정보 조회
    
    기상청 초단기예보 API를 사용하여 나주시의 현재 날씨를 조회합니다.
    
    **반환 정보:**
    - temperature: 기온 (°C)
    - humidity: 습도 (%)
    - sky: 하늘상태 (맑음/구름많음/흐림)
    - precipitation: 강수형태 (없음/비/눈 등)
    - weather_text: 날씨 설명 텍스트
    
    **캐싱:**
    - 10분간 캐시 유지 (API 호출 횟수 제한 대응)
    
    **주의사항:**
    - 기상청 API 키 설정 필요: `WEATHER_API_KEY` 변수에 실제 키 입력
    - 기상청 공공데이터포털에서 키 발급: https://www.data.go.kr/
    """
    
    # 캐시 확인 (10분 이내면 캐시된 데이터 반환)
    if weather_cache["data"] is not None and weather_cache["timestamp"] is not None:
        from datetime import datetime, timedelta
        cache_age = datetime.now() - weather_cache["timestamp"]
        if cache_age < timedelta(minutes=weather_cache["cache_minutes"]):
            logger.info(f"💾 캐시된 날씨 정보 반환 (캐시 나이: {int(cache_age.total_seconds())}초)")
            cached_data = weather_cache["data"].copy()
            cached_data["cached"] = True
            cached_data["cache_age_seconds"] = int(cache_age.total_seconds())
            return cached_data
    
    # API 키 확인
    if WEATHER_API_KEY == "발급한 키":
        return {
            "success": False,
            "error": "기상청 API 키가 설정되지 않았습니다",
            "message": "rest_api_server.py의 WEATHER_API_KEY를 실제 키로 변경해주세요",
            "guide": "https://www.data.go.kr/ 에서 기상청 단기예보 API 키 발급 가능"
        }
    
    try:
        # API 요청 파라미터
        params = {
            'serviceKey': WEATHER_API_KEY,
            'pageNo': '1',
            'numOfRows': '1000',
            'dataType': 'XML',
            'base_date': get_current_date_string(),
            'base_time': get_current_hour_string(),
            'nx': NAJU_NX,
            'ny': NAJU_NY
        }
        
        logger.info(f"🌤 날씨 API 요청: base_date={params['base_date']}, base_time={params['base_time']}, nx={NAJU_NX}, ny={NAJU_NY}")
        
        # API 요청
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        
        logger.info(f"📥 날씨 API 응답 상태: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"❌ 기상청 API 오류: {response.status_code}")
            logger.error(f"응답 내용: {response.text[:500]}")
            
            # 429 오류 (Too Many Requests) 특별 처리
            if response.status_code == 429:
                error_msg = "API 호출 횟수 제한 초과. 10분 후 다시 시도하거나 캐시된 데이터를 사용하세요."
                logger.warning(f"⚠️ {error_msg}")
                
                # 캐시된 데이터가 있으면 반환 (만료되었어도)
                if weather_cache["data"] is not None:
                    logger.info("💾 만료된 캐시 데이터 반환 (429 오류 대응)")
                    expired_cache = weather_cache["data"].copy()
                    expired_cache["cached"] = True
                    expired_cache["expired"] = True
                    expired_cache["note"] = "API 호출 제한으로 인한 캐시 데이터"
                    return expired_cache
                
                raise HTTPException(status_code=429, detail=error_msg)
            
            raise HTTPException(
                status_code=response.status_code,
                detail=f"기상청 API 요청 실패: {response.status_code}"
            )
        
        # XML -> 딕셔너리 변환
        xml_data = response.text
        logger.debug(f"XML 응답 (처음 500자): {xml_data[:500]}")
        
        dict_data = xmltodict.parse(xml_data)
        
        # 응답 체크
        if 'response' not in dict_data:
            logger.error(f"❌ 응답 형식 오류: {dict_data}")
            raise HTTPException(status_code=500, detail="기상청 API 응답 형식 오류")
        
        # 기상청 API 오류 코드 확인
        result_code = dict_data['response']['header'].get('resultCode', 'UNKNOWN')
        result_msg = dict_data['response']['header'].get('resultMsg', '')
        
        logger.info(f"기상청 API 결과: {result_code} - {result_msg}")
        
        if result_code != '00':
            logger.error(f"❌ 기상청 API 오류: [{result_code}] {result_msg}")
            raise HTTPException(
                status_code=500,
                detail=f"기상청 API 오류 [{result_code}]: {result_msg}"
            )
        
        # 값 추출
        weather_data = {
            'temperature': None,  # 기온 (T1H)
            'humidity': None,     # 습도 (REH)
            'sky': None,          # 하늘상태 (SKY)
            'precipitation': None # 강수형태 (PTY)
        }
        
        items = dict_data['response']['body']['items']['item']
        for item in items:
            if item['category'] == 'T1H':
                weather_data['temperature'] = item['fcstValue']
            elif item['category'] == 'REH':
                weather_data['humidity'] = item['fcstValue']
            elif item['category'] == 'SKY':
                weather_data['sky'] = item['fcstValue']
            elif item['category'] == 'PTY':
                weather_data['precipitation'] = item['fcstValue']
        
        # 날씨 텍스트 생성
        weather_text = "나주시 "
        
        # 강수형태에 따른 날씨
        if weather_data['precipitation'] == '0':
            if weather_data['sky'] == '1':
                weather_text += "맑음"
                weather_icon = "☀️"
            elif weather_data['sky'] == '3':
                weather_text += "구름많음"
                weather_icon = "🌤"
            elif weather_data['sky'] == '4':
                weather_text += "흐림"
                weather_icon = "☁️"
            else:
                weather_text += "알 수 없음"
                weather_icon = "🌫"
        elif weather_data['precipitation'] == '1':
            weather_text += "비"
            weather_icon = "🌧"
        elif weather_data['precipitation'] == '2':
            weather_text += "비와 눈"
            weather_icon = "🌨"
        elif weather_data['precipitation'] == '3':
            weather_text += "눈"
            weather_icon = "❄️"
        elif weather_data['precipitation'] == '5':
            weather_text += "빗방울"
            weather_icon = "🌦"
        elif weather_data['precipitation'] == '6':
            weather_text += "빗방울과 눈날림"
            weather_icon = "🌨"
        elif weather_data['precipitation'] == '7':
            weather_text += "눈날림"
            weather_icon = "🌨"
        else:
            weather_text += "알 수 없음"
            weather_icon = "🌫"
        
        # 응답 데이터 생성
        response_data = {
            "success": True,
            "location": "전라남도 나주시",
            "temperature": weather_data['temperature'],
            "humidity": weather_data['humidity'],
            "sky_code": weather_data['sky'],
            "precipitation_code": weather_data['precipitation'],
            "weather_text": weather_text,
            "weather_icon": weather_icon,
            "base_date": get_current_date_string(),
            "base_time": get_current_hour_string(),
            "summary": f"{weather_text} · {weather_data['temperature']}°C",
            "cached": False
        }
        
        # 캐시 업데이트
        from datetime import datetime
        weather_cache["data"] = response_data.copy()
        weather_cache["timestamp"] = datetime.now()
        logger.info(f"💾 날씨 정보 캐시 업데이트 완료 (유효시간: {weather_cache['cache_minutes']}분)")
        
        return response_data
        
    except HTTPException:
        # FastAPI HTTPException은 그대로 raise (재처리하지 않음)
        raise
    except requests.Timeout:
        logger.error("❌ 기상청 API 타임아웃")
        raise HTTPException(status_code=504, detail="기상청 API 응답 시간 초과")
    except requests.RequestException as e:
        logger.error(f"❌ 네트워크 오류: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=500, detail=f"네트워크 오류: {str(e)}")
    except KeyError as e:
        logger.error(f"❌ 응답 파싱 오류 (KeyError): {str(e)}")
        logger.error(f"응답 데이터 구조: {dict_data if 'dict_data' in locals() else 'N/A'}")
        raise HTTPException(status_code=500, detail=f"응답 파싱 오류: 필요한 데이터 없음 ({str(e)})")
    except Exception as e:
        logger.error(f"❌ 날씨 조회 오류: {type(e).__name__} - {str(e)}")
        logger.exception("상세 오류:")
        raise HTTPException(status_code=500, detail=f"날씨 조회 실패: {type(e).__name__} - {str(e)}")


# ============================================================================
# Endpoints: Raw Register Access (Advanced Users)
# ============================================================================

@app.get("/api/raw/read/{address}", tags=["Advanced"])
async def raw_read_register(address: int, count: int = 1):
    """
    Raw 레지스터 읽기 (고급 사용자용)
    
    - **address**: 레지스터 주소 (0~84)
    - **count**: 읽을 개수
    """
    check_connection()
    
    if address < 0 or address > 84:
        raise HTTPException(status_code=400, detail="address는 0~84 범위여야 합니다")
    
    registers = controller.read_holding_register(address, count)
    
    if registers is None:
        raise HTTPException(status_code=500, detail="레지스터 읽기 실패")
    
    return {
        "success": True,
        "address": address,
        "count": count,
        "values": registers
    }


@app.post("/api/raw/write/{address}", tags=["고급 기능"])
async def raw_write_register(address: int, value: int):
    """
    Raw 레지스터 쓰기 (고급 사용자용)
    
    - **address**: 레지스터 주소 (0~59만 쓰기 가능)
    - **value**: 쓸 값 (0~65535)
    
    ⚠️ 주의: 직접 레지스터를 쓰면 시스템 오동작이 발생할 수 있습니다!
    """
    check_connection()
    
    if address < 0 or address > 59:
        raise HTTPException(
            status_code=400,
            detail="쓰기는 워드주소 0~59만 가능합니다 (설정값 영역)"
        )
    
    if value < 0 or value > 65535:
        raise HTTPException(status_code=400, detail="value는 0~65535 범위여야 합니다")
    
    result = controller.write_register(address, value)
    
    if not result:
        raise HTTPException(status_code=500, detail="레지스터 쓰기 실패")
    
    # 검증 읽기
    verified = controller.read_holding_register(address, 1)
    
    return {
        "success": True,
        "address": address,
        "written_value": value,
        "verified_value": verified[0] if verified else None
    }


# ============================================================================
# 서버 실행
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Modbus TCP REST API Server 시작")
    print("=" * 70)
    print("📝 API 문서: http://localhost:8000/docs")
    print("📚 ReDoc: http://localhost:8000/redoc")
    print("=" * 70)
    
    uvicorn.run(
        "rest_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Modbus TCP Controller
================================================================================
RS485 Modbus TCP/IP 통신 컨트롤러

기능:
- 센서 데이터 읽기
- 비트 제어 (ON/OFF)
- 레지스터 쓰기
- 제어명세서 기반 자동 함수 생성

사용법:
    controller = ModbusController(host="168.131.153.52", port=9139)
    controller.connect()
    
    # 센서 읽기
    temp = controller.read_sensor(70, scale=10)
    
    # 비트 제어
    controller.write_bit(20, 15, 1)
    
    controller.close()
================================================================================
"""

from pymodbus.client import ModbusTcpClient
import logging
import time

# 제어 명세서 데이터베이스 import
from control_specs import CONTROL_SPECS

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def modbus_int16_to_temp(raw_u16, scale=0.1):
    """
    Modbus unsigned 16비트 값을 signed 16비트로 변환 후 스케일 적용
    
    영하 온도를 올바르게 처리하기 위한 변환 함수
    
    Args:
        raw_u16: MODBUS로 수신한 0~65535 값 (unsigned)
        scale: 스케일 팩터 (기본 0.1, 실제 사용시 나누기 값이면 1/scale로 전달)
                예: scale=10이면 실제로는 1/10 = 0.1로 전달
    
    Returns:
        변환된 실제 값 (float)
    """
    # unsigned 16비트를 signed 16비트로 변환
    if raw_u16 >= 0x8000:          # 32768 이상이면 음수
        raw_s16 = raw_u16 - 0x10000  # 65536을 빼서 음수로 변환
    else:
        raw_s16 = raw_u16
    
    # 스케일 적용 (나누기)
    return raw_s16 / scale


class ModbusController:
    """Modbus TCP 통신 컨트롤러"""
    
    def __init__(self, host="aiseednaju.iptime.org", port=9139, unit_id=1, timeout=5, retries=3):
        """
        초기화
        
        Args:
            host: Modbus TCP 서버 IP 또는 도메인
            port: 포트 번호
            unit_id: Modbus Unit ID (Slave ID)
            timeout: 타임아웃 (초)
            retries: 재시도 횟수
        """
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.timeout = timeout
        self.retries = retries
        self.client = None
        
    def connect(self, max_retries=3, retry_delay=2):
        """
        서버 연결 (재시도 로직 포함)
        
        Args:
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 간 대기 시간 (초)
            
        Returns:
            성공: True
            실패: False
        """
        # 기존 연결이 있으면 먼저 종료
        if self.client:
            try:
                self.client.close()
            except:
                pass
            self.client = None
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"연결 시도 {attempt}/{max_retries}: {self.host}:{self.port}")
                
                self.client = ModbusTcpClient(
                    host=self.host,
                    port=self.port,
                    timeout=self.timeout,
                    retries=1  # pymodbus 내부 재시도는 1회로 제한
                )
                
                result = self.client.connect()
                
                if result:
                    logger.info(f"✅ 연결 성공: {self.host}:{self.port}")
                    return True
                else:
                    logger.warning(f"⚠️  연결 실패 (시도 {attempt}/{max_retries})")
                    if attempt < max_retries:
                        logger.info(f"   {retry_delay}초 후 재시도...")
                        time.sleep(retry_delay)
                    
            except Exception as e:
                logger.warning(f"⚠️  연결 오류 (시도 {attempt}/{max_retries}): {e}")
                if attempt < max_retries:
                    logger.info(f"   {retry_delay}초 후 재시도...")
                    time.sleep(retry_delay)
        
        logger.error(f"❌ 연결 실패: {self.host}:{self.port} (최대 재시도 횟수 초과)")
        return False
    
    def close(self):
        """연결 종료"""
        if self.client:
            self.client.close()
            logger.info("연결 종료")
    
    def is_connected(self):
        """연결 상태 확인"""
        return self.client is not None and self.client.connected
    
    # ========================================================================
    # 센서 읽기 (SENSOR_READ / BIT_READ)
    # ========================================================================
    
    def read_holding_register(self, address, count=1):
        """
        Holding Register 읽기 (Raw 값)
        
        Args:
            address: 레지스터 주소
            count: 읽을 레지스터 개수
            
        Returns:
            성공: [register_values]
            실패: None
        """
        if not self.is_connected():
            logger.error("연결되지 않음")
            return None
        
        try:
            resp = self.client.read_holding_registers(
                address=address,
                count=count,
                slave=self.unit_id
            )
            
            if resp.isError():
                logger.error(f"읽기 실패: 주소 {address}")
                return None
            
            if hasattr(resp, 'registers') and resp.registers:
                return resp.registers
            else:
                logger.error(f"데이터 없음: 주소 {address}")
                return None
                
        except Exception as e:
            logger.error(f"읽기 오류: {e}")
            return None
    
    def read_sensor(self, address, scale=1, signed=False):
        """
        센서값 읽기 (스케일 적용)
        
        Args:
            address: 레지스터 주소
            scale: 스케일 값 (예: 10이면 value/10)
            signed: True면 signed 16비트로 변환 (영하 온도 등)
            
        Returns:
            성공: 실제 센서값 (float)
            실패: None
        """
        registers = self.read_holding_register(address, count=1)
        if registers is None:
            return None
        
        raw_value = registers[0]
        
        # signed 변환이 필요한 경우 (온도 등)
        if signed:
            actual_value = modbus_int16_to_temp(raw_value, scale)
        else:
            actual_value = raw_value / scale
        
        logger.info(f"센서 읽기: 주소 {address}, Raw={raw_value}, 실제값={actual_value} (signed={signed})")
        return actual_value
    
    def read_bit(self, address, bit_num):
        """
        특정 비트 읽기
        
        Args:
            address: 워드 주소
            bit_num: 비트 번호 (0~15)
            
        Returns:
            성공: 0 또는 1
            실패: None
        """
        registers = self.read_holding_register(address, count=1)
        if registers is None:
            return None
        
        word_value = registers[0]
        bit_value = (word_value >> bit_num) & 1
        logger.info(f"비트 읽기: 주소 {address}, 비트 {bit_num}, 값={bit_value}")
        return bit_value
    
    def read_bit_range(self, address, bit_start, bit_end):
        """
        비트 범위 읽기 (여러 비트를 하나의 값으로)
        
        Args:
            address: 워드 주소
            bit_start: 시작 비트 번호
            bit_end: 종료 비트 번호
            
        Returns:
            성공: 비트 범위의 값
            실패: None
        """
        registers = self.read_holding_register(address, count=1)
        if registers is None:
            return None
        
        word_value = registers[0]
        bit_count = bit_end - bit_start + 1
        mask = (1 << bit_count) - 1
        bit_range_value = (word_value >> bit_start) & mask
        logger.info(f"비트 범위 읽기: 주소 {address}, 비트 {bit_start}~{bit_end}, 값={bit_range_value}")
        return bit_range_value
    
    # ========================================================================
    # 레지스터 쓰기 (BIT_WRITE / REGISTER_WRITE)
    # ========================================================================
    
    def write_register(self, address, value):
        """
        레지스터 쓰기 (워드 전체)
        
        Args:
            address: 레지스터 주소
            value: 쓸 값 (0~65535)
            
        Returns:
            성공: True
            실패: False
        """
        if not self.is_connected():
            logger.error("연결되지 않음")
            return False
        
        try:
            resp = self.client.write_register(
                address=address,
                value=value,
                slave=self.unit_id
            )
            
            if resp.isError():
                logger.error(f"쓰기 실패: 주소 {address}, 값={value}")
                return False
            
            logger.info(f"쓰기 성공: 주소 {address}, 값={value}")
            return True
            
        except Exception as e:
            logger.error(f"쓰기 오류: {e}")
            return False
    
    def write_bit(self, address, bit_num, bit_value):
        """
        특정 비트 쓰기 (ON/OFF 제어)
        
        Args:
            address: 워드 주소
            bit_num: 비트 번호 (0~15)
            bit_value: 비트 값 (0 또는 1)
            
        Returns:
            성공: True
            실패: False
        """
        # 1단계: 현재 워드 값 읽기
        registers = self.read_holding_register(address, count=1)
        if registers is None:
            return False
        
        current_value = registers[0]
        
        # 2단계: 비트 값 변경
        if bit_value == 1:
            new_value = current_value | (1 << bit_num)  # 비트를 1로 설정
        else:
            new_value = current_value & ~(1 << bit_num)  # 비트를 0으로 설정
        
        # 3단계: 워드 쓰기
        logger.info(f"비트 쓰기: 주소 {address}, 비트 {bit_num}, {bit_value} (현재={current_value}, 새값={new_value})")
        return self.write_register(address, new_value)
    
    def write_bit_range(self, address, bit_start, bit_end, value):
        """
        비트 범위 쓰기 (여러 비트를 하나의 값으로)
        
        Args:
            address: 워드 주소
            bit_start: 시작 비트 번호
            bit_end: 종료 비트 번호
            value: 쓸 값
            
        Returns:
            성공: True
            실패: False
        """
        # 1단계: 현재 워드 값 읽기
        registers = self.read_holding_register(address, count=1)
        if registers is None:
            return False
        
        current_value = registers[0]
        
        # 2단계: 비트 범위 값 변경
        bit_count = bit_end - bit_start + 1
        mask = (1 << bit_count) - 1
        
        # 값이 범위를 벗어나는지 체크
        max_value = mask
        if value > max_value or value < 0:
            logger.error(f"값 범위 초과: {value} (최대: {max_value})")
            return False
        
        # 해당 비트 범위를 클리어하고 새 값을 설정
        clear_mask = ~(mask << bit_start) & 0xFFFF
        new_value = (current_value & clear_mask) | (value << bit_start)
        
        # 3단계: 워드 쓰기
        logger.info(f"비트 범위 쓰기: 주소 {address}, 비트 {bit_start}~{bit_end}, {value} (현재={current_value}, 새값={new_value})")
        return self.write_register(address, new_value)
    
    def write_sensor_value(self, address, value, scale=1, signed=False):
        """
        센서 설정값 쓰기 (스케일 적용)
        
        Args:
            address: 레지스터 주소
            value: 실제 값 (예: 25.0도, -5.0도)
            scale: 스케일 값 (예: 10이면 value*10)
            signed: True면 signed 16비트로 변환 (영하 온도 등)
            
        Returns:
            성공: True
            실패: False
        """
        register_value = int(value * scale)
        
        # signed 변환이 필요한 경우 (음수 처리)
        if signed and register_value < 0:
            register_value = register_value + 0x10000  # 음수를 unsigned로 변환
        
        # unsigned 16비트 범위로 제한
        register_value = register_value & 0xFFFF
        
        logger.info(f"센서 설정값 쓰기: 주소 {address}, 실제값={value}, 레지스터값={register_value} (signed={signed})")
        return self.write_register(address, register_value)
    
    # ========================================================================
    # 제어명세서 기반 범용 함수들
    # ========================================================================
    
    def read_by_name(self, name):
        """
        제어명세서 이름으로 데이터 읽기
        
        Args:
            name: CONTROL_SPECS에 정의된 제어 이름
            
        Returns:
            성공: 읽은 값
            실패: None
        """
        spec = CONTROL_SPECS.get(name)
        if not spec:
            logger.error(f"알 수 없는 제어 이름: {name}")
            return None
        
        spec_type = spec['type']
        address = spec['address']
        scale = spec.get('scale', 1)
        
        try:
            if spec_type == 'SENSOR_READ' or spec_type == 'REGISTER_READ':
                # 레지스터 전체 읽기
                count = spec.get('count', 1)
                registers = self.read_holding_register(address, count)
                if registers is None:
                    return None
                
                if count == 1:
                    # 온도 관련 항목은 signed 변환 적용
                    is_temperature = '온도' in spec.get('korean_name', '') or 'temperature' in name.lower()
                    if is_temperature:
                        value = modbus_int16_to_temp(registers[0], scale)
                    else:
                        value = registers[0] / scale
                else:
                    # 2워드 이상인 경우 (예: 32비트 값)
                    value = (registers[0] << 16) | registers[1]
                
                logger.info(f"[{name}] 읽기 성공: {value} {spec.get('unit', '')}")
                return value
                
            elif spec_type == 'BIT_READ':
                # 단일 비트 읽기
                bit_num = spec['bit']
                value = self.read_bit(address, bit_num)
                logger.info(f"[{name}] 비트 읽기: {value}")
                return value
                
            elif spec_type == 'BIT_RANGE_READ':
                # 비트 범위 읽기
                bit_start = spec['bit_start']
                bit_end = spec['bit_end']
                value = self.read_bit_range(address, bit_start, bit_end)
                logger.info(f"[{name}] 비트 범위 읽기: {value}")
                return value
                
            else:
                logger.error(f"지원하지 않는 타입: {spec_type}")
                return None
                
        except Exception as e:
            logger.error(f"[{name}] 읽기 오류: {e}")
            return None
    
    def write_by_name(self, name, value):
        """
        제어명세서 이름으로 데이터 쓰기
        
        Args:
            name: CONTROL_SPECS에 정의된 제어 이름
            value: 쓸 값
            
        Returns:
            성공: True
            실패: False
        """
        spec = CONTROL_SPECS.get(name)
        if not spec:
            logger.error(f"알 수 없는 제어 이름: {name}")
            return False
        
        spec_type = spec['type']
        address = spec['address']
        scale = spec.get('scale', 1)
        
        try:
            if spec_type == 'REGISTER_WRITE':
                # 레지스터 전체 쓰기
                # 온도 관련 항목은 signed 변환 적용
                is_temperature = '온도' in spec.get('korean_name', '') or 'temperature' in name.lower()
                register_value = int(value * scale)
                
                # signed 변환이 필요한 경우 (음수 처리)
                if is_temperature and register_value < 0:
                    register_value = register_value + 0x10000  # 음수를 unsigned로 변환
                
                # unsigned 16비트 범위로 제한
                register_value = register_value & 0xFFFF
                
                result = self.write_register(address, register_value)
                logger.info(f"[{name}] 쓰기: {value} → {register_value} (signed={is_temperature})")
                return result
                
            elif spec_type == 'BIT_WRITE':
                # 비트 쓰기
                bit_num = spec['bit']
                result = self.write_bit(address, bit_num, value)
                logger.info(f"[{name}] 비트 쓰기: {value}")
                return result
                
            else:
                logger.error(f"[{name}] 쓰기를 지원하지 않는 타입: {spec_type}")
                return False
                
        except Exception as e:
            logger.error(f"[{name}] 쓰기 오류: {e}")
            return False
    
    def read_multiple(self, names):
        """
        여러 항목을 한번에 읽기
        
        Args:
            names: 제어 이름 리스트
            
        Returns:
            딕셔너리 {name: value}
        """
        results = {}
        for name in names:
            value = self.read_by_name(name)
            results[name] = value
        return results
    
    def get_spec_info(self, name):
        """
        제어 명세 정보 조회
        
        Args:
            name: 제어 이름
            
        Returns:
            명세 정보 딕셔너리
        """
        return CONTROL_SPECS.get(name)
    
    def list_all_controls(self):
        """
        모든 제어 항목 이름 반환
        
        Returns:
            제어 이름 리스트
        """
        return list(CONTROL_SPECS.keys())
    
    # ========================================================================
    # 레거시 함수들 (하위 호환성 유지)
    # ========================================================================
    
    # 센서 읽기 함수들
    def 내부온도_읽기(self):
        """내부 온도 센서 읽기 (°C)"""
        return self.read_sensor(address=70, scale=10)
    
    def 내부습도_읽기(self):
        """내부 습도 센서 읽기 (%)"""
        return self.read_sensor(address=71, scale=10)
    
    def 내부일사량_읽기(self):
        """내부 일사량 센서 읽기 (W/m²)"""
        return self.read_sensor(address=72, scale=1)
    
    def 외부온도_읽기(self):
        """외부 온도 센서 읽기 (°C)"""
        return self.read_sensor(address=75, scale=10)
    
    def 외부습도_읽기(self):
        """외부 습도 센서 읽기 (%)"""
        return self.read_sensor(address=76, scale=10)
    
    def 감우센서_읽기(self):
        """감우센서 읽기 (0=비없음, 1=비감지)"""
        return self.read_bit(address=66, bit_num=14)
    
    # 비트 제어 함수들
    def 천장우측닫기_제어(self, on_off):
        """천장 우측 닫기 모드 제어 (0=OFF, 1=ON)"""
        return self.write_bit(address=20, bit_num=15, bit_value=on_off)
    
    def 천장우측열기_제어(self, on_off):
        """천장 우측 열기 모드 제어 (0=OFF, 1=ON)"""
        return self.write_bit(address=20, bit_num=14, bit_value=on_off)


# ============================================================================
# 섹션별 테스트 함수
# ============================================================================

def ensure_connection(controller):
    """연결 상태 확인 및 자동 연결"""
    if not controller.is_connected():
        print("  ℹ️  연결 시도 중...")
        if controller.connect():
            print("  ✓ 연결 성공")
            return True
        else:
            print("  ✗ 연결 실패")
            return False
    return True


def test_connection(controller):
    """섹션 0: 연결 테스트"""
    print("\n" + "="*70)
    print("[ 섹션 0 ] 연결 테스트")
    print("="*70)
    
    if controller.is_connected():
        print("✓ 이미 연결됨")
        print(f"  서버: {controller.host}:{controller.port}")
        print(f"  Unit ID: {controller.unit_id}")
        return True
    
    if controller.connect():
        print("✓ Modbus TCP 연결 성공")
        print(f"  서버: {controller.host}:{controller.port}")
        print(f"  Unit ID: {controller.unit_id}")
        return True
    else:
        print("✗ 연결 실패")
        return False


def test_sensor_read(controller):
    """섹션 1: 센서 현재값 읽기 (SENSOR_READ)"""
    print("\n" + "="*70)
    print("[ 섹션 1 ] 센서 현재값 읽기 (SENSOR_READ)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    sensors = [
        ("내부현재온도", "°C"),
        ("내부현재습도", "%"),
        ("내부현재일사량", "W/m²"),
        ("외부현재온도", "°C"),
        ("외부현재습도", "%"),
    ]
    
    for name, unit in sensors:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        print(f"  {status} {name}: {value} {unit}")
    
    print("\n섹션 1 완료")


def test_register_read(controller):
    """섹션 2: 설정값 읽기 (REGISTER_READ)"""
    print("\n" + "="*70)
    print("[ 섹션 2 ] 설정값 읽기 (REGISTER_READ)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    registers = [
        ("IO보드국번", "-"),
        ("PCB주위온도설정", "°C"),
        ("센서값저장주기", "분"),
        ("유동팬ON온도", "°C"),
        ("유동팬OFF온도", "°C"),
        ("유동팬ON습도", "%"),
        ("유동팬OFF습도", "%"),
    ]
    
    for name, unit in registers:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        print(f"  {status} {name}: {value} {unit}")
    
    print("\n섹션 2 완료")


def test_bit_read(controller):
    """섹션 3: 비트 상태 읽기 (BIT_READ)"""
    print("\n" + "="*70)
    print("[ 섹션 3 ] 비트 상태 읽기 (BIT_READ)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    bits = [
        "센서기록유닛포함",
        "센서파일타입",
        "비밀번호사용",
        "유동팬시간조절",
        "유동팬습도조절",
        "유동팬온도조절",
        "유동팬강제운전",
        "유동팬오토모드",
        "관수강제운전",
        "관수오토모드",
    ]
    
    for name in bits:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        state = "ON" if value == 1 else "OFF" if value == 0 else "ERROR"
        print(f"  {status} {name}: {state} ({value})")
    
    print("\n섹션 3 완료")


def test_bit_range_read(controller):
    """섹션 4: 비트 범위 읽기 (BIT_RANGE_READ)"""
    print("\n" + "="*70)
    print("[ 섹션 4 ] 비트 범위 읽기 (BIT_RANGE_READ)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    bit_ranges = [
        ("유동팬OFF시간", "-"),
        ("유동팬온시간", "-"),
        ("함수율관수설정", "-"),
        ("관수시작시", "시"),
        ("관수OFF시간", "분"),
        ("관수ON시간", "분"),
        ("관수종료시", "시"),
        ("관수반복회수", "회"),
        ("다음관수일", "일"),
    ]
    
    for name, unit in bit_ranges:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        print(f"  {status} {name}: {value} {unit}")
    
    print("\n섹션 4 완료")


def test_multiple_read(controller):
    """섹션 5: 다중 항목 읽기 (read_multiple)"""
    print("\n" + "="*70)
    print("[ 섹션 5 ] 다중 항목 읽기 (read_multiple)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    names = [
        "내부현재온도",
        "내부현재습도",
        "외부현재온도",
        "외부현재습도",
    ]
    
    print(f"  요청: {len(names)}개 항목 동시 읽기")
    results = controller.read_multiple(names)
    
    print(f"  결과:")
    for name, value in results.items():
        spec = controller.get_spec_info(name)
        unit = spec.get('unit', '') if spec else ''
        status = "✓" if value is not None else "✗"
        print(f"    {status} {name}: {value} {unit}")
    
    print("\n섹션 5 완료")


def test_system_info(controller):
    """섹션 6: 시스템 정보"""
    print("\n" + "="*70)
    print("[ 섹션 6 ] 시스템 정보")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    # IO 보드 통신 체크
    io_check = controller.read_by_name("IO보드통신체크")
    io_status = "정상" if io_check != 100 else "연결끊김"
    print(f"  IO보드 통신: {io_status} (값: {io_check})")
    
    # 현재 시각
    hour = controller.read_by_name("현재시각_시")
    minute = controller.read_by_name("현재시각_분")
    second = controller.read_by_name("현재시각_초")
    if hour is not None and minute is not None and second is not None:
        print(f"  현재시각: {int(hour):02d}:{int(minute):02d}:{int(second):02d}")
    
    # PCB 온도
    pcb_temp = controller.read_by_name("PCB주위현재온도")
    print(f"  PCB 주위온도: {pcb_temp}°C")
    
    # 커튼 이동량
    curtains = [
        ("상부보온커튼이동량", "초"),
        ("측면보온커튼이동량", "초"),
        ("차광커튼이동량", "초"),
    ]
    print(f"\n  커튼 상태:")
    for name, unit in curtains:
        value = controller.read_by_name(name)
        print(f"    {name}: {value} {unit}")
    
    print("\n섹션 6 완료")


def test_output_status(controller):
    """섹션 7: 출력 상태 읽기 (워드 65~67)"""
    print("\n" + "="*70)
    print("[ 섹션 7 ] 출력 상태 읽기 (워드 65~67)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    print("\n  [ 워드 65: 출력 표시 상태 ]")
    output_bits_65 = [
        "유동팬습도조건출력중",
        "유동팬온도조건출력중",
        "차광열림출력표시",
        "차광닫힘출력표시",
        "상부보온열림출력표시",
        "상부보온닫힘출력표시",
        "천장우단열림출력표시",
        "천장우열림출력표시",
        "천장좌단열림출력표시",
        "천장좌열림출력표시",
        "제습출력표시",
        "난방출력표시",
        "관수출력표시",
        "유동팬출력표시",
        "PCB온도센서에러",
        "생정초기화체크",
    ]
    
    for name in output_bits_65:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        state = "ON" if value == 1 else "OFF" if value == 0 else "ERROR"
        print(f"  {status} {name}: {state}")
    
    print("\n  [ 워드 66: 조건별 출력 상태 ]")
    output_bits_66 = [
        "관수중",
        "감우센서감지중",
        "차광일사센서출력중",
        "차광시간조건출력중",
        "차광온도조건출력중",
        "보온시간조건출력중",
        "보온온도조건출력중",
        "천장좌감우조건출력중",
        "천장좌온도차조건출력중",
        "천장좌습도조건출력중",
        "천장좌온도조건출력중",
        "난방습도조건출력중",
        "난방온도조건출력중",
        "관수시간조건출력중",
        "관수함수율출력중",
        "유동팬시간조건출력중",
    ]
    
    for name in output_bits_66:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        state = "ON" if value == 1 else "OFF" if value == 0 else "ERROR"
        print(f"  {status} {name}: {state}")
    
    print("\n  [ 워드 67: 추가 출력 상태 ]")
    output_bits_67 = [
        "측면보온커튼닫힘출력표시",
        "측면보온커튼열림출력표시",
        "천장우풍속출력중",
        "천장우시간출력중",
        "천장좌풍속출력중",
        "천장좌시간출력중",
        "조명출력표시",
        "천장우감우조건출력중",
        "천장우온도차조건출력중",
        "천장우습도조건출력중",
        "천장우온도조건출력중",
        "관수반복횟수표시",
    ]
    
    for name in output_bits_67:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        state = "ON" if value == 1 else "OFF" if value == 0 else "ERROR"
        print(f"  {status} {name}: {state}")
    
    print("\n섹션 7 완료")


def test_sensor_errors(controller):
    """섹션 8: 센서 에러 상태 읽기 (워드 68~69)"""
    print("\n" + "="*70)
    print("[ 섹션 8 ] 센서 에러 상태 읽기 (워드 68~69)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    print("\n  [ 워드 68: 내부센서 에러 ]")
    internal_errors = [
        "내부센서정보_15",
        "내부센서정보_14",
        "내부센서시간출력중",
        "내부센서온도출력중",
        "내부수분장력센서에러",
        "내부함수율센서에러",
        "내부일사센서에러",
        "내부습도센서에러",
        "내부온도센서에러",
        "내부수분장력센서디바이스에러",
        "내부함수율센서디바이스에러",
        "내부일사센서디바이스에러",
        "내부습도센서디바이스에러",
        "내부온도센서디바이스에러",
        "내부센서노드에러",
        "내부센서통신에러",
    ]
    
    error_count = 0
    for name in internal_errors:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        if value == 1:
            state = "⚠️  ERROR"
            error_count += 1
        elif value == 0:
            state = "✓ OK"
        else:
            state = "? UNKNOWN"
        print(f"  {status} {name}: {state}")
    
    if error_count > 0:
        print(f"\n  ⚠️  내부센서 에러: {error_count}개")
    else:
        print(f"\n  ✓ 내부센서 정상")
    
    print("\n  [ 워드 69: 외부센서 에러 ]")
    external_errors = [
        "외부센서정보_15",
        "외부센서정보_14",
        "외부센서에러",
        "외부풍속센서에러",
        "외부풍향센서에러",
        "외부일사센서에러",
        "외부습도센서에러",
        "외부온도센서에러",
        "외부감우센서에러",
        "외부풍속센서디바이스에러",
        "외부풍향센서디바이스에러",
        "외부일사센서디바이스에러",
        "외부습도센서디바이스에러",
        "외부온도센서디바이스에러",
        "외부센서노드에러",
        "외부센서통신에러",
    ]
    
    error_count = 0
    for name in external_errors:
        value = controller.read_by_name(name)
        status = "✓" if value is not None else "✗"
        if value == 1:
            state = "⚠️  ERROR"
            error_count += 1
        elif value == 0:
            state = "✓ OK"
        else:
            state = "? UNKNOWN"
        print(f"  {status} {name}: {state}")
    
    if error_count > 0:
        print(f"\n  ⚠️  외부센서 에러: {error_count}개")
    else:
        print(f"\n  ✓ 외부센서 정상")
    
    print("\n섹션 8 완료")


def test_bit_write(controller):
    """섹션 9: 비트 쓰기 테스트 (BIT_WRITE)"""
    print("\n" + "="*70)
    print("[ 섹션 9 ] 비트 쓰기 테스트 (BIT_WRITE)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    print("  ⚠️  실제 장비를 제어합니다. 신중하게 선택하세요.")
    print()
    
    # 비트 쓰기 방법 선택
    print("  [ 빠른 선택 ]")
    print("  1. 유동팬 오토모드 토글 (주소 9, 비트 0)")
    print("  2. 관수 오토모드 토글 (주소 10, 비트 0)")
    print("  3. 유동팬 강제운전 토글 (주소 9, 비트 1)")
    print("  4. 관수 강제운전 토글 (주소 10, 비트 1)")
    print()
    print("  [ 직접 입력 ]")
    print("  5. 단일 비트 쓰기 (레지스터 주소 / 비트 번호 / 값)")
    print("  6. 비트 범위 쓰기 (레지스터 주소 / 시작비트 / 종료비트 / 값)")
    print()
    print("  0. 건너뛰기")
    print()
    
    try:
        choice = input("  선택 (0-6): ").strip()
        
        if choice == '0':
            print("\n  섹션 9 건너뛰기")
            return
        
        # 빠른 선택 맵
        test_map = {
            '1': (9, 0, "유동팬오토모드"),
            '2': (10, 0, "관수오토모드"),
            '3': (9, 1, "유동팬강제운전"),
            '4': (10, 1, "관수강제운전"),
        }
        
        if choice == '5':
            # 단일 비트 쓰기 모드
            print("\n  [ 단일 비트 쓰기 모드 ]")
            address = int(input("  레지스터 주소 (0-84): ").strip())
            bit_num = int(input("  비트 번호 (0-15): ").strip())
            
            # 현재 상태 읽기
            current = controller.read_bit(address, bit_num)
            if current is not None:
                print(f"\n  현재 상태: {current} ({'ON' if current == 1 else 'OFF'})")
            else:
                print("\n  현재 상태: 읽기 실패")
            
            # 값 입력
            new_value = int(input("  새로운 값 (0=OFF, 1=ON): ").strip())
            
            if new_value not in [0, 1]:
                print("  ✗ 잘못된 값입니다. 0 또는 1만 가능합니다.")
                return
            
            confirm = input(f"\n  주소 {address}, 비트 {bit_num}에 {new_value} ({'ON' if new_value == 1 else 'OFF'})을(를) 쓰시겠습니까? (y/n): ").strip().lower()
            
            if confirm == 'y':
                result = controller.write_bit(address, bit_num, new_value)
                if result:
                    print(f"  ✓ 쓰기 성공: 주소 {address}, 비트 {bit_num} → {new_value} ({'ON' if new_value == 1 else 'OFF'})")
                    
                    # 확인 읽기
                    verify = controller.read_bit(address, bit_num)
                    print(f"  ✓ 확인: {verify} ({'ON' if verify == 1 else 'OFF'})")
                else:
                    print(f"  ✗ 쓰기 실패")
            else:
                print("  취소됨")
        
        elif choice == '6':
            # 비트 범위 쓰기 모드
            print("\n  [ 비트 범위 쓰기 모드 ]")
            address = int(input("  레지스터 주소 (0-84): ").strip())
            bit_start = int(input("  시작 비트 번호 (0-15): ").strip())
            bit_end = int(input("  종료 비트 번호 (0-15): ").strip())
            
            if bit_start > bit_end:
                print("  ✗ 시작 비트가 종료 비트보다 클 수 없습니다.")
                return
            
            # 현재 상태 읽기
            current = controller.read_bit_range(address, bit_start, bit_end)
            if current is not None:
                bit_count = bit_end - bit_start + 1
                max_value = (1 << bit_count) - 1
                print(f"\n  현재 값: {current}")
                print(f"  값 범위: 0 ~ {max_value} ({bit_count}비트)")
            else:
                print("\n  현재 값: 읽기 실패")
            
            # 값 입력
            new_value = int(input(f"  새로운 값 (0-{max_value}): ").strip())
            
            if new_value < 0 or new_value > max_value:
                print(f"  ✗ 잘못된 값입니다. 0~{max_value} 범위만 가능합니다.")
                return
            
            confirm = input(f"\n  주소 {address}, 비트 {bit_start}~{bit_end}에 {new_value}을(를) 쓰시겠습니까? (y/n): ").strip().lower()
            
            if confirm == 'y':
                result = controller.write_bit_range(address, bit_start, bit_end, new_value)
                if result:
                    print(f"  ✓ 쓰기 성공: 주소 {address}, 비트 {bit_start}~{bit_end} → {new_value}")
                    
                    # 확인 읽기
                    verify = controller.read_bit_range(address, bit_start, bit_end)
                    print(f"  ✓ 확인: {verify}")
                else:
                    print(f"  ✗ 쓰기 실패")
            else:
                print("  취소됨")
        
        elif choice in test_map:
            # 빠른 선택 모드
            address, bit, name = test_map[choice]
            
            # 현재 상태 읽기
            current = controller.read_bit(address, bit)
            print(f"\n  현재 상태: {current} ({'ON' if current == 1 else 'OFF'})")
            
            # 토글할 값
            new_value = 0 if current == 1 else 1
            
            confirm = input(f"  {new_value} ({'ON' if new_value == 1 else 'OFF'})으로 변경하시겠습니까? (y/n): ").strip().lower()
            
            if confirm == 'y':
                result = controller.write_bit(address, bit, new_value)
                if result:
                    print(f"  ✓ 쓰기 성공: {name} → {new_value} ({'ON' if new_value == 1 else 'OFF'})")
                    
                    # 확인 읽기
                    verify = controller.read_bit(address, bit)
                    print(f"  ✓ 확인: {verify} ({'ON' if verify == 1 else 'OFF'})")
                else:
                    print(f"  ✗ 쓰기 실패")
            else:
                print("  취소됨")
        else:
            print("  잘못된 선택")
            
    except Exception as e:
        print(f"  ✗ 오류: {e}")
    
    print("\n섹션 9 완료")


def test_register_write(controller):
    """섹션 10: 레지스터 쓰기 테스트 (REGISTER_WRITE)"""
    print("\n" + "="*70)
    print("[ 섹션 10 ] 레지스터 쓰기 테스트 (REGISTER_WRITE)")
    print("="*70)
    
    if not ensure_connection(controller):
        print("  ✗ 연결 실패로 테스트 중단")
        return
    
    print("  ⚠️  실제 설정값을 변경합니다. 신중하게 입력하세요.")
    print()
    
    print("  테스트 항목:")
    print("  1. Raw 레지스터 쓰기 (주소 직접 지정)")
    print("  0. 건너뛰기")
    print()
    
    try:
        choice = input("  선택 (0-1): ").strip()
        
        if choice == '0':
            print("\n  섹션 8 건너뛰기")
            return
        
        if choice == '1':
            # Raw 레지스터 쓰기
            address = int(input("  워드 주소 입력 (0-65535): ").strip())
            
            # 현재 값 읽기
            current = controller.read_holding_register(address, 1)
            if current:
                print(f"  현재 값: {current[0]}")
            
            new_value = int(input("  새로운 값 입력 (0-65535): ").strip())
            
            confirm = input(f"  주소 {address}에 {new_value}를 쓰시겠습니까? (y/n): ").strip().lower()
            
            if confirm == 'y':
                result = controller.write_register(address, new_value)
                if result:
                    print(f"  ✓ 쓰기 성공: 주소 {address} → {new_value}")
                    
                    # 확인 읽기
                    verify = controller.read_holding_register(address, 1)
                    if verify:
                        print(f"  ✓ 확인: {verify[0]}")
                else:
                    print(f"  ✗ 쓰기 실패")
            else:
                print("  취소됨")
        else:
            print("  잘못된 선택")
            
    except ValueError:
        print("  ✗ 잘못된 입력 형식")
    except Exception as e:
        print(f"  ✗ 오류: {e}")
    
    print("\n섹션 10 완료")


def test_control_list(controller):
    """섹션 11: 제어 항목 목록"""
    print("\n" + "="*70)
    print("[ 섹션 11 ] 제어 항목 목록")
    print("="*70)
    
    all_controls = controller.list_all_controls()
    print(f"  총 등록된 제어 항목: {len(all_controls)}개")
    
    # 타입별 개수
    from control_specs import get_stats
    stats = get_stats()
    print(f"\n  타입별 개수:")
    for type_name, count in stats['by_type'].items():
        print(f"    - {type_name}: {count}개")
    
    # 샘플 5개 출력
    print(f"\n  항목 예시 (처음 5개):")
    for i, name in enumerate(all_controls[:5], 1):
        spec = controller.get_spec_info(name)
        print(f"    {i}. {name} (주소: {spec['address']}, 타입: {spec['type']})")
    
    print("\n섹션 11 완료")


# ============================================================================
# 메인 테스트 실행
# ============================================================================

def run_all_tests(controller):
    """모든 섹션 테스트 실행 (읽기만)"""
    print("\n" + "="*70)
    print("전체 읽기 테스트 시작")
    print("="*70)
    
    test_connection(controller)
    test_sensor_read(controller)
    test_register_read(controller)
    test_bit_read(controller)
    test_bit_range_read(controller)
    test_multiple_read(controller)
    test_system_info(controller)
    test_output_status(controller)
    test_sensor_errors(controller)
    
    print("\n" + "="*70)
    print("전체 읽기 테스트 완료")
    print("="*70)


def run_test_menu(controller):
    """대화형 테스트 메뉴"""
    while True:
        print("\n" + "="*70)
        print("Modbus TCP 테스트 메뉴")
        print("="*70)
        print("  [ 읽기 테스트 ]")
        print("  0. 연결 테스트")
        print("  1. 센서 현재값 읽기 (SENSOR_READ)")
        print("  2. 설정값 읽기 (REGISTER_READ)")
        print("  3. 비트 상태 읽기 (BIT_READ)")
        print("  4. 비트 범위 읽기 (BIT_RANGE_READ)")
        print("  5. 다중 항목 읽기 (read_multiple)")
        print("  6. 시스템 정보")
        print("  7. 출력 상태 읽기 (워드 65~67) 🆕")
        print("  8. 센서 에러 상태 (워드 68~69) 🆕")
        print()
        print("  [ 쓰기 테스트 ]")
        print("  9. 비트 쓰기 (BIT_WRITE) ⚠️")
        print("  10. 레지스터 쓰기 (REGISTER_WRITE) ⚠️")
        print()
        print("  [ 기타 ]")
        print("  11. 제어 항목 목록")
        print("  a. 전체 읽기 테스트 실행")
        print("  q. 종료")
        print("="*70)
        
        try:
            choice = input("선택: ").strip().lower()
            
            if choice == '0':
                test_connection(controller)
            elif choice == '1':
                test_sensor_read(controller)
            elif choice == '2':
                test_register_read(controller)
            elif choice == '3':
                test_bit_read(controller)
            elif choice == '4':
                test_bit_range_read(controller)
            elif choice == '5':
                test_multiple_read(controller)
            elif choice == '6':
                test_system_info(controller)
            elif choice == '7':
                test_output_status(controller)
            elif choice == '8':
                test_sensor_errors(controller)
            elif choice == '9':
                test_bit_write(controller)
            elif choice == '10':
                test_register_write(controller)
            elif choice == '11':
                test_control_list(controller)
            elif choice == 'a':
                run_all_tests(controller)
            elif choice == 'q':
                print("\n테스트 종료")
                break
            else:
                print("\n잘못된 선택입니다.")
                
        except KeyboardInterrupt:
            print("\n\n테스트 중단")
            break
        except Exception as e:
            print(f"\n오류 발생: {e}")


if __name__ == "__main__":
    # 컨트롤러 생성
    controller = ModbusController(host="aiseednaju.iptime.org", port=9139)
    
    # 대화형 메뉴 실행
    run_test_menu(controller)


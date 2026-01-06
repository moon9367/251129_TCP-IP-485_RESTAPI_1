#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
센서 데이터 수집 스크립트
================================================================================
주기적으로 Modbus 센서 값을 읽어서 출력하는 스크립트

사용법:
    python sensor_collector.py
    
또는:
    start.bat 실행
================================================================================
"""

import os
import sys

# 작업 디렉토리를 스크립트 위치로 변경 (나스 폴더 대응)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from modbus_tcp_controller import ModbusController
from control_specs import CONTROL_SPECS
import time
import socket
from datetime import datetime

# 수집할 센서 목록 (이미지에 표시된 11개 센서)
SENSOR_ITEMS = [
    "indoor_current_temperature",      # 내부 온도
    "indoor_current_humidity",          # 내부 습도
    "indoor_current_solar_radiation",   # 내부 일사량
    "indoor_current_moisture",          # 내부 현재 함수율
    "indoor_current_soil_tension",      # 내부 수분 장력
    "outdoor_current_temperature",      # 외부 온도
    "outdoor_current_humidity",         # 외부 습도
    "outdoor_solar_radiation",          # 외부 일사량
    "outdoor_wind_direction",            # 외부 풍향 (워드 주소 78 추정)
    "outdoor_wind_speed",               # 외부 풍속 (워드 주소 79 추정)
    "rain_sensor_detecting",            # 감우센서
]

# 수집 간격 (초)
COLLECT_INTERVAL = 10

# 연결 재시도 설정
MAX_RECONNECT_ATTEMPTS = 3
RECONNECT_DELAY = 5  # 재연결 대기 시간 (초)


def check_network_connection(host, port, timeout=3):
    """네트워크 연결 확인 (포트 체크)"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"   네트워크 확인 오류: {e}")
        return False


def diagnose_connection(host, port):
    """연결 문제 진단"""
    print("\n" + "="*80)
    print("🔍 연결 문제 진단")
    print("="*80)
    
    # 1. 호스트 이름 확인
    print(f"1. 호스트 확인: {host}")
    try:
        ip = socket.gethostbyname(host)
        print(f"   ✅ IP 주소: {ip}")
    except socket.gaierror:
        print(f"   ❌ 호스트 이름을 IP로 변환 실패")
        return False
    
    # 2. 포트 연결 확인
    print(f"2. 포트 연결 확인: {host}:{port}")
    if check_network_connection(host, port):
        print(f"   ✅ 포트 {port} 연결 가능")
        return True
    else:
        print(f"   ❌ 포트 {port} 연결 불가")
        print(f"   가능한 원인:")
        print(f"      - Modbus 서버가 실행 중이지 않음")
        print(f"      - 방화벽이 포트를 차단")
        print(f"      - 네트워크 연결 문제")
        print(f"      - IP 주소 또는 포트 번호 오류")
        return False


def collect_sensors(controller):
    """모든 센서 값 수집 및 출력"""
    # 연결 상태 확인
    if not controller.is_connected():
        return None
    
    # 현재 시간 정보
    now = datetime.now()
    next_hour = (now.hour + 1) % 24
    next_min = now.minute
    
    print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 데이터 수집 중... (다음 전송: {next_hour:02d}:{next_min:02d})")
    
    results = {}
    
    # 센서별 출력 형식 정의
    sensor_display = {
        "indoor_current_temperature": "내부 온도",
        "indoor_current_humidity": "내부 습도",
        "indoor_current_solar_radiation": "내부 일사량",
        "indoor_current_moisture": "내부 현재 함수율",
        "indoor_current_soil_tension": "내부 수분 장력",
        "outdoor_current_temperature": "외부 온도",
        "outdoor_current_humidity": "외부 습도",
        "outdoor_solar_radiation": "외부 일사량",
        "outdoor_wind_direction": "외부 풍향",
        "outdoor_wind_speed": "외부 풍속",
        "rain_sensor_detecting": "감우센서",
    }
    
    for sensor_name in SENSOR_ITEMS:
        try:
            # 외부 풍향/풍속은 control_specs에 없을 수 있으므로 직접 읽기
            if sensor_name == "outdoor_wind_direction":
                # 워드 주소 78 직접 읽기 (외부 풍향)
                value = controller.read_sensor(78, scale=1, signed=False)
                if value is not None:
                    print(f"외부 풍향: {value:.1f} °")
                    results[sensor_name] = {'value': value, 'unit': '°', 'name': '외부 풍향'}
                else:
                    print(f"외부 풍향: ❌ 읽기 실패")
                continue
            elif sensor_name == "outdoor_wind_speed":
                # 워드 주소 79 직접 읽기 (외부 풍속, /10 스케일)
                value = controller.read_sensor(79, scale=10, signed=False)
                if value is not None:
                    print(f"외부 풍속: {value:.1f} m/s")
                    results[sensor_name] = {'value': value, 'unit': 'm/s', 'name': '외부 풍속'}
                else:
                    print(f"외부 풍속: ❌ 읽기 실패")
                continue
            
            spec = CONTROL_SPECS.get(sensor_name)
            if not spec:
                display_name = sensor_display.get(sensor_name, sensor_name)
                print(f"{display_name}: ❌ 명세서에 없음")
                continue
            
            value = controller.read_by_name(sensor_name)
            if value is not None:
                unit = spec.get('unit', '')
                display_name = sensor_display.get(sensor_name, spec.get('korean_name', sensor_name))
                results[sensor_name] = {
                    'value': value,
                    'unit': unit,
                    'name': display_name
                }
                
                # 출력 형식: "센서명: 값 단위"
                if unit:
                    print(f"{display_name}: {value:.1f} {unit}")
                else:
                    print(f"{display_name}: {int(value)}")
            else:
                display_name = sensor_display.get(sensor_name, sensor_name)
                print(f"{display_name}: ❌ 읽기 실패")
                
        except Exception as e:
            display_name = sensor_display.get(sensor_name, sensor_name)
            print(f"{display_name}: ❌ 오류 - {e}")
    
    return results


def reconnect_controller(controller):
    """컨트롤러 재연결 시도"""
    print(f"\n⚠️  연결 끊김 감지. 재연결 시도 중...")
    
    for attempt in range(1, MAX_RECONNECT_ATTEMPTS + 1):
        print(f"   재연결 시도 {attempt}/{MAX_RECONNECT_ATTEMPTS}...")
        
        if controller.connect(max_retries=1, retry_delay=1):
            print(f"   ✅ 재연결 성공!")
            return True
        
        if attempt < MAX_RECONNECT_ATTEMPTS:
            print(f"   {RECONNECT_DELAY}초 후 재시도...")
            time.sleep(RECONNECT_DELAY)
    
    print(f"   ❌ 재연결 실패 (최대 시도 횟수 초과)")
    return False


def main():
    """메인 함수"""
    print("="*80)
    print("🌱 Smart Farm 센서 데이터 수집기")
    print("="*80)
    print(f"수집 간격: {COLLECT_INTERVAL}초")
    print(f"수집 항목: {len(SENSOR_ITEMS)}개")
    print("="*80)
    print("\n⚠️  종료하려면 Ctrl+C를 누르세요\n")
    
    # Modbus 컨트롤러 생성
    controller = ModbusController(
        host="aiseednaju.iptime.org",
        port=9139,
        unit_id=1
    )
    
    # 연결 시도
    print("🔌 Modbus 연결 시도 중...")
    if not controller.connect(max_retries=3, retry_delay=2):
        print("\n❌ Modbus 연결 실패!")
        print("   - 호스트 확인: aiseednaju.iptime.org")
        print("   - 포트 확인: 9139")
        print("   - 네트워크 연결 확인")
        
        # 연결 진단 실행
        if not diagnose_connection(controller.host, controller.port):
            print("\n💡 해결 방법:")
            print("   1. Modbus 서버가 실행 중인지 확인")
            print("   2. 방화벽 설정 확인 (포트 9139 허용)")
            print("   3. 네트워크 연결 상태 확인")
            print("   4. IP 주소 및 포트 번호 확인")
        
        return
    
    print("✅ Modbus 연결 성공!")
    print(f"   호스트: {controller.host}:{controller.port}")
    print()
    
    consecutive_failures = 0
    max_consecutive_failures = 3
    
    try:
        # 주기적으로 센서 값 수집
        while True:
            result = collect_sensors(controller)
            
            if result is None:
                # 연결 끊김
                consecutive_failures += 1
                if consecutive_failures >= max_consecutive_failures:
                    if not reconnect_controller(controller):
                        print("\n❌ 재연결 실패. 프로그램을 종료합니다.")
                        break
                    consecutive_failures = 0
            else:
                consecutive_failures = 0
            
            time.sleep(COLLECT_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("👋 센서 수집 중단 (사용자 요청)")
        print("="*80)
    except Exception as e:
        print(f"\n\n❌ 오류 발생: {e}")
    finally:
        controller.close()
        print("🔌 Modbus 연결 종료")


if __name__ == "__main__":
    main()


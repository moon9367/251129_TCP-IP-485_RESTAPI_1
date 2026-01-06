#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
임시 센서 데이터 수집기
10초마다 수집, 1분 평균값 저장
24시간 연속 가동
"""

import os
import sys
from datetime import datetime
import csv
import time

# 현재 디렉토리를 스크립트 위치로 설정 (독립 실행)
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

from modbus_tcp_controller import ModbusController
from control_specs import CONTROL_SPECS

# Modbus 서버 설정
MODBUS_HOST = "aiseednaju.iptime.org"
MODBUS_PORT = 9139
UNIT_ID = 1

# 수집 설정
COLLECT_INTERVAL = 10  # 10초마다 수집
SAVE_INTERVAL = 60     # 60초(1분)마다 평균값 저장

# 데이터 저장 폴더 (2곳에 저장 - 나스와 바탕화면 백업)
DATA_FOLDER = "sensor_data"
BACKUP_FOLDER = os.path.join(os.path.expanduser('~'), 'Desktop', 'sensor_backup')

# 수집할 센서 목록
SENSOR_ITEMS = [
    "indoor_current_temperature",      # 내부 온도
    "indoor_current_humidity",          # 내부 습도
    "indoor_current_solar_radiation",   # 내부 일사량
    "indoor_current_moisture",          # 내부 현재 함수율
    "indoor_current_soil_tension",      # 내부 수분 장력
    "outdoor_current_temperature",      # 외부 온도
    "outdoor_current_humidity",         # 외부 습도
    "outdoor_solar_radiation",          # 외부 일사량
    "outdoor_wind_direction",           # 외부 풍향 (워드 78)
    "outdoor_wind_speed",               # 외부 풍속 (워드 79)
    "rain_sensor_detecting",            # 감우센서
    # 워드 65번 - 출력 상태 (비트 15~2, 0 또는 1)
    "circulation_fan_humidity_condition_output_active",  # 비트 15
    "circulation_fan_temperature_condition_output_active",  # 비트 14
    "shading_open_output_indicator",  # 비트 13
    "shading_close_output_indicator",  # 비트 12
    "upper_insulation_open_output_indicator",  # 비트 11
    "upper_insulation_close_output_indicator",  # 비트 10
    "roof_right_end_open_output_indicator",  # 비트 9
    "roof_right_open_output_indicator",  # 비트 8
    "roof_left_end_open_output_indicator",  # 비트 7
    "roof_left_open_output_indicator",  # 비트 6
    "dehumidifier_output_indicator",  # 비트 5
    "heating_output_indicator",  # 비트 4
    "irrigation_output_indicator",  # 비트 3
    "circulation_fan_output_indicator",  # 비트 2
]

# 센서 이름의 한글 매핑
SENSOR_KOREAN_NAMES = {
    "indoor_current_temperature": "내부온도",
    "indoor_current_humidity": "내부습도",
    "indoor_current_solar_radiation": "내부일사량",
    "indoor_current_moisture": "내부함수율",
    "indoor_current_soil_tension": "내부수분장력",
    "outdoor_current_temperature": "외부온도",
    "outdoor_current_humidity": "외부습도",
    "outdoor_solar_radiation": "외부일사량",
    "outdoor_wind_direction": "외부풍향",
    "outdoor_wind_speed": "외부풍속",
    "rain_sensor_detecting": "감우센서",
    "circulation_fan_humidity_condition_output_active": "유동팬습도조건출력중",
    "circulation_fan_temperature_condition_output_active": "유동팬온도조건출력중",
    "shading_open_output_indicator": "차광닫힘출력",
    "shading_close_output_indicator": "차광열림출력",
    "upper_insulation_open_output_indicator": "상부보온닫힘출력",
    "upper_insulation_close_output_indicator": "상부보온열림출력",
    "roof_right_end_open_output_indicator": "천장우단닫힘출력",
    "roof_right_open_output_indicator": "천장우닫힘출력",
    "roof_left_end_open_output_indicator": "천장좌단닫힘출력",
    "roof_left_open_output_indicator": "천장좌닫힘출력",
    "dehumidifier_output_indicator": "제습출력",
    "heating_output_indicator": "난방출력",
    "irrigation_output_indicator": "관수출력",
    "circulation_fan_output_indicator": "유동팬출력",
}


def read_sensors(controller):
    """모든 센서 값 읽기"""
    results = {}

    # 워드 65번을 한 번만 읽어서 모든 비트 추출 (통신 부하 감소)
    word_65_bits = {}
    word_65_sensor_names = [
        "circulation_fan_humidity_condition_output_active",
        "circulation_fan_temperature_condition_output_active",
        "shading_open_output_indicator",
        "shading_close_output_indicator",
        "upper_insulation_open_output_indicator",
        "upper_insulation_close_output_indicator",
        "roof_right_end_open_output_indicator",
        "roof_right_open_output_indicator",
        "roof_left_end_open_output_indicator",
        "roof_left_open_output_indicator",
        "dehumidifier_output_indicator",
        "heating_output_indicator",
        "irrigation_output_indicator",
        "circulation_fan_output_indicator",
    ]

    try:
        # 워드 65번을 한 번만 읽기
        word_65_value = controller.read_sensor(65, scale=1, signed=False)

        # 비트 15~2 추출 (14개)
        bit_positions = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        for i, sensor_name in enumerate(word_65_sensor_names):
            bit_pos = bit_positions[i]
            bit_value = (int(word_65_value) >> bit_pos) & 1
            word_65_bits[sensor_name] = bit_value

    except Exception as e:
        print(f"워드 65번 읽기 오류: {e}")
        # 실패 시 모든 비트를 None으로 설정
        for sensor_name in word_65_sensor_names:
            word_65_bits[sensor_name] = None

    # 각 센서 읽기
    for sensor_name in SENSOR_ITEMS:
        try:
            # 워드 65번 비트는 이미 읽었으므로 캐시에서 가져오기
            if sensor_name in word_65_bits:
                results[sensor_name] = word_65_bits[sensor_name]
                continue

            # 외부 풍향/풍속은 직접 읽기 (CONTROL_SPECS에 실제 센서값 주소 없음)
            if sensor_name == "outdoor_wind_direction":
                # 워드 주소 78 (외부 풍향, 스케일 1, 0~360도)
                value = controller.read_sensor(78, scale=1, signed=False)
                results[sensor_name] = value
                continue

            elif sensor_name == "outdoor_wind_speed":
                # 워드 주소 79 (외부 풍속, 스케일 /10, m/s)
                value = controller.read_sensor(79, scale=10, signed=False)
                results[sensor_name] = value
                continue

            # CONTROL_SPECS에 있는 센서는 read_by_name 사용
            value = controller.read_by_name(sensor_name)
            results[sensor_name] = value

        except Exception as e:
            print(f"센서 읽기 오류 [{sensor_name}]: {e}")
            results[sensor_name] = None

    return results


def calculate_average(data_buffer):
    """버퍼에 있는 데이터의 평균값 계산"""
    if not data_buffer:
        return {}

    averages = {}

    for sensor_name in SENSOR_ITEMS:
        values = []
        for data in data_buffer:
            value = data.get(sensor_name)
            if value is not None:
                values.append(value)

        if values:
            averages[sensor_name] = sum(values) / len(values)
        else:
            averages[sensor_name] = None

    return averages


def save_to_csv_single(data, folder, location_name):
    """단일 폴더에 CSV 파일 저장"""
    now = datetime.now()

    # 데이터 폴더가 없으면 생성
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"데이터 저장 폴더 생성: {folder}")

    # 파일명: @2025-12-26.csv
    date_str = now.strftime("%Y-%m-%d")
    filename = os.path.join(folder, f"@{date_str}.csv")

    # 현재 시각 (절대시간 1분 단위로 반올림)
    # 초를 0으로 설정
    timestamp = now.strftime("%Y-%m-%d %H:%M:00")

    # 파일 존재 여부 확인 (헤더 작성용)
    file_exists = os.path.isfile(filename)

    # CSV 파일에 저장 (파일 잠금 오류 시 재시도)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # CSV 파일에 추가
            with open(filename, 'a', newline='', encoding='utf-8-sig') as f:
                # 헤더 정의 (한글)
                headers = ['시간'] + [SENSOR_KOREAN_NAMES[name] for name in SENSOR_ITEMS]

                # 실제 데이터 필드명 (영문)
                fieldnames = ['Timestamp'] + SENSOR_ITEMS

                # writer 생성
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # 파일이 새로 생성되면 한글 헤더 작성
                if not file_exists:
                    # 한글 헤더 먼저 쓰기
                    f.write(','.join(headers) + '\n')

                # 데이터 행 작성 (소수점 첫째자리까지만)
                row = {'Timestamp': timestamp}
                for sensor_name, value in data.items():
                    if value is not None:
                        # 소수점 첫째자리까지 반올림
                        row[sensor_name] = round(value, 1)
                    else:
                        row[sensor_name] = value
                writer.writerow(row)

            return True  # 성공

        except PermissionError:
            if attempt < max_retries - 1:
                print(f"[경고] {location_name} CSV 파일이 다른 프로그램에서 열려있습니다. 2초 후 재시도... ({attempt + 1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"[오류] {location_name} CSV 파일 저장 실패: {filename}")
                print(f"       파일이 Excel 등 다른 프로그램에서 열려있는지 확인하세요.")
                return False
        except Exception as e:
            print(f"[오류] {location_name} CSV 파일 저장 중 오류: {e}")
            return False

    return False


def save_to_csv(data):
    """CSV 파일로 2곳에 저장 (나스 + 바탕화면 백업)"""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:00")

    # 1. 나스(또는 프로그램 폴더)에 저장
    nas_success = save_to_csv_single(data, DATA_FOLDER, "나스")

    # 2. 바탕화면 백업 폴더에 저장
    backup_success = save_to_csv_single(data, BACKUP_FOLDER, "바탕화면")

    # 결과 출력
    if nas_success and backup_success:
        print(f"[{timestamp}] 평균값 저장 완료 (나스 + 바탕화면)")
    elif nas_success:
        print(f"[{timestamp}] 평균값 저장 완료 (나스만 저장, 바탕화면 실패)")
    elif backup_success:
        print(f"[{timestamp}] 평균값 저장 완료 (바탕화면만 저장, 나스 실패)")
    else:
        print(f"[{timestamp}] 평균값 저장 실패 (나스, 바탕화면 모두 실패)")
        raise Exception("CSV 파일 저장 실패 (모든 위치)")


def reconnect_controller(controller):
    """컨트롤러 재연결 시도"""
    print("\n연결 끊김 감지. 재연결 시도 중...")

    for attempt in range(1, 4):
        print(f"재연결 시도 {attempt}/3...")

        if controller.connect(max_retries=1, retry_delay=1):
            print("재연결 성공!")
            return True

        if attempt < 3:
            print("5초 후 재시도...")
            time.sleep(5)

    print("재연결 실패")
    return False


def main():
    """메인 함수"""
    print("="*70)
    print("임시 센서 데이터 수집기 (24시간 연속 가동)")
    print("="*70)
    print(f"수집 간격: {COLLECT_INTERVAL}초")
    print(f"저장 간격: {SAVE_INTERVAL}초 (1분 평균값)")
    print(f"수집 센서: {len(SENSOR_ITEMS)}개")
    print("="*70)
    print("\n종료하려면 Ctrl+C를 누르세요\n")

    # Modbus 컨트롤러 생성
    controller = ModbusController(
        host=MODBUS_HOST,
        port=MODBUS_PORT,
        unit_id=UNIT_ID
    )

    # 연결 시도
    print(f"Modbus 연결 중: {MODBUS_HOST}:{MODBUS_PORT}")
    if not controller.connect(max_retries=3, retry_delay=2):
        print("연결 실패!")
        return

    print("연결 성공!\n")

    # 데이터 버퍼 (1분간 수집된 데이터 저장)
    data_buffer = []
    last_save_minute = -1  # 마지막 저장한 분
    consecutive_failures = 0

    try:
        while True:
            # 연결 상태 확인
            if not controller.is_connected():
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    if not reconnect_controller(controller):
                        print("\n재연결 실패. 프로그램을 종료합니다.")
                        break
                    consecutive_failures = 0
                time.sleep(COLLECT_INTERVAL)
                continue

            # 센서 값 읽기
            data = read_sensors(controller)

            # 성공적으로 읽으면 실패 카운터 리셋
            if any(v is not None for v in data.values()):
                consecutive_failures = 0
                data_buffer.append(data)

                # 간단한 상태 출력
                now = datetime.now()
                valid_count = sum(1 for v in data.values() if v is not None)
                print(f"[{now.strftime('%H:%M:%S')}] 수집 완료 ({valid_count}/{len(SENSOR_ITEMS)} 센서)")

            # 절대시간 1분 단위로 저장 (분이 바뀔 때마다)
            now = datetime.now()
            current_minute = now.minute

            if current_minute != last_save_minute:
                if data_buffer:
                    # 평균값 계산
                    avg_data = calculate_average(data_buffer)

                    # CSV 저장
                    save_to_csv(avg_data)

                    # 버퍼 초기화
                    data_buffer = []
                    last_save_minute = current_minute
                    print(f"  -> 버퍼 초기화 완료\n")
                else:
                    # 데이터가 없어도 분이 바뀌었으면 마지막 저장 분 업데이트
                    last_save_minute = current_minute

            # 10초 대기
            time.sleep(COLLECT_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("사용자 중단 요청")

        # 종료 전 남은 데이터 저장
        if data_buffer:
            print("남은 데이터 저장 중...")
            avg_data = calculate_average(data_buffer)
            save_to_csv(avg_data)
            print("저장 완료")

        print("="*70)

    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()

    finally:
        controller.close()
        print("연결 종료\n")


if __name__ == "__main__":
    main()

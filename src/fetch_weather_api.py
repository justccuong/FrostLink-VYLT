"""
Module: fetch_weather_api.py
Muc dich: Trich xuat du lieu khi tuong thuc te (Nhiet do va Luong mua) cho huyen Luc Ngan, Bac Giang
Nguon du lieu: Open-Meteo Historical Archive API (Mo hinh tai phan tich ERA5 cua ECMWF - Chau Au)
Toa do Luc Ngan, Bac Giang: Latitude 21.3667, Longitude 106.5667
"""

import os
import json
import urllib.request
import pandas as pd
import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR) if os.path.basename(CURRENT_DIR) == 'src' else CURRENT_DIR
DATA_DIR = os.path.join(REPO_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)
CACHE_CSV = os.path.join(DATA_DIR, "weather_luc_ngan_api.csv")

LAT_LUC_NGAN = 21.3667
LON_LUC_NGAN = 106.5667

def fetch_luc_ngan_weather(start_date="2026-05-01", end_date="2026-07-31", force_refresh=False):
    """
    Trich xuat du lieu thoi tiet thuc dia Luc Ngan qua Open-Meteo Archive API.
    Neu da co file cache cuc bo va force_refresh=False, uu tien doc tu cache.
    """
    if os.path.exists(CACHE_CSV) and not force_refresh:
        try:
            df = pd.read_csv(CACHE_CSV)
            if len(df) >= 92:
                print(f"[+] Da doc du lieu thoi tiet Luc Ngan tu cache cuc bo: {CACHE_CSV} ({len(df)} ngay)")
                return df
        except Exception as e:
            print(f"[!] Loi doc cache ({e}), tien hanh goi API truc tiep...")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LAT_LUC_NGAN}&longitude={LON_LUC_NGAN}&"
        f"start_date={start_date}&end_date={end_date}&"
        f"daily=temperature_2m_max,temperature_2m_mean,precipitation_sum&"
        f"timezone=Asia%2FBangkok"
    )
    
    print(f"[*] Dang ket noi Open-Meteo ERA5 API trich xuat thoi tiet Luc Ngan...")
    print(f"    Toa do: {LAT_LUC_NGAN}N, {LON_LUC_NGAN}E | Giai doan: {start_date} -> {end_date}")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'FrostLink-VYLT-2026/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            
        daily = data.get('daily', {})
        df = pd.DataFrame({
            'Date': daily.get('time', []),
            'Temp_Max_C': [round(float(v), 1) for v in daily.get('temperature_2m_max', [])],
            'Temp_Mean_C': [round(float(v), 1) for v in daily.get('temperature_2m_mean', [])],
            'Precip_mm': [round(float(v), 1) for v in daily.get('precipitation_sum', [])],
            'Source': 'Open-Meteo ERA5 Reanalysis (ECMWF)'
        })
        
        df.to_csv(CACHE_CSV, index=False, encoding='utf-8')
        print(f"[+] Tai thanh cong {len(df)} ngay du lieu thoi tiet va luu vao: {CACHE_CSV}")
        return df
        
    except Exception as e:
        print(f"[!] Loi ket noi Open-Meteo API: {e}")
        if os.path.exists(CACHE_CSV):
            print(f"[->] Phuc hoi tu file cache san co: {CACHE_CSV}")
            return pd.read_csv(CACHE_CSV)
        else:
            raise RuntimeError(f"Khong the tai du lieu thoi tiet va khong tim thay cache: {e}")

if __name__ == "__main__":
    df = fetch_luc_ngan_weather(force_refresh=True)
    print("\n--- BAO CAO TONG HOP THOI TIET LUC NGAN (92 NGAY MUA VU) ---")
    print(f"Tong so ngay: {len(df)}")
    print(f"Nhiet do cuc dai (Max Temp): Min = {df['Temp_Max_C'].min():.1f}C | Mean = {df['Temp_Max_C'].mean():.1f}C | Max = {df['Temp_Max_C'].max():.1f}C")
    print(f"Tong luong mua mua vu: {df['Precip_mm'].sum():.1f} mm")
    print(f"So ngay mua lon (>= 20mm): {len(df[df['Precip_mm'] >= 20.0])} ngay")
    print(f"So ngay mua rat to / bao (>= 40mm): {len(df[df['Precip_mm'] >= 40.0])} ngay")

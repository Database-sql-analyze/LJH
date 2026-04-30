import os
import platform
import pandas as pd
import matplotlib.pyplot as plt

# 1. OS별 폰트 동적 세팅 (윈도우/맥/리눅스 에러 방지)
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# Seaborn 테마를 제거하고, 깔끔한 실무형 Matplotlib 기본 스타일 사용
plt.style.use('default') 

# 2. 동적 경로 설정 (스크립트 위치 기준)
# scripts 폴더 안에서 실행하든 밖에서 실행하든 정확히 폴더를 찾도록 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'output')

def plot_funnel_dropoff(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(file_path)
    
    # 깔끔한 실무형 그래프 세팅
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 단계별 역순 정렬 (위에서부터 아래로 퍼널 형태가 되도록)
    df = df.iloc[::-1].reset_index(drop=True)
    
    # 특정 단계(이메일 인증) 강조 색상
    colors = ['#1f497d' if step != '이메일 인증 완료' else '#c00000' for step in df['단계']]
    
    bars = ax.barh(df['단계'], df['사용자 수'], color=colors, height=0.6)
    
    # 테두리 제거 (데이터-잉크 비율을 높이는 Tufte 스타일)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color('#dddddd')
    
    # x축 숨기기 (텍스트로 직접 표시하므로 눈금 불필요)
    ax.get_xaxis().set_visible(False)
    
    # 바 옆에 수치 텍스트 직관적으로 추가
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 500, bar.get_y() + bar.get_height()/2,
                f'{int(width):,}', va='center', ha='left', fontsize=12, color='#333333')

    plt.title('가입 퍼널: 이메일 인증 단계에서 51%의 치명적 이탈 발생', fontsize=18, pad=20, weight='bold')
    plt.tight_layout()
    
    # output 폴더에 저장
    output_path = os.path.join(OUTPUT_DIR, 'funnel_dropoff.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_feature_conversion_matrix(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(file_path)
    
    df['유료 전환율'] = df['유료 전환율'].str.rstrip('%').astype('float')
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # 산점도 시각화 (Seaborn 제거, 순수 Matplotlib 활용)
    scatter = ax.scatter(
        df['기능 사용자 수'], df['유료 전환율'], 
        s=df['유료 전환율'] * 15,  # 전환율에 따른 버블 크기
        c=df['유료 전환율'],       # 색상 매핑
        cmap='coolwarm', 
        alpha=0.8,
        edgecolors='w', linewidth=1.5, zorder=2
    )
    
    # 사분면 구분을 위한 평균선 (배경으로 배치)
    ax.axvline(df['기능 사용자 수'].mean(), color='#999999', linestyle='--', linewidth=1.5, zorder=1)
    ax.axhline(df['유료 전환율'].mean(), color='#999999', linestyle='--', linewidth=1.5, zorder=1)
    
    # 텍스트 라벨링
    for i in range(df.shape[0]):
        ax.text(df['기능 사용자 수'][i] + 40, df['유료 전환율'][i] + 0.5, 
                df['기능'][i], fontsize=12, weight='bold', color='#333333')
                
    # 테두리 정리
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#dddddd')
    ax.spines['left'].set_color('#dddddd')

    plt.title('기능 효율 매트릭스: 고전환 기능의 낮은 노출도', fontsize=18, pad=20, weight='bold')
    plt.xlabel('기능 사용자 수 (노출도)', fontsize=14, color='#555555')
    plt.ylabel('유료 전환율 (%)', fontsize=14, color='#555555')
    
    # 은은한 그리드 추가
    ax.grid(True, linestyle=':', alpha=0.6, zorder=0)

    plt.tight_layout()
    
    # output 폴더에 저장
    output_path = os.path.join(OUTPUT_DIR, 'feature_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # 저장할 output 폴더가 없으면 자동 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 스크립트 실행
    plot_funnel_dropoff('landing_event_log.csv')
    plot_feature_conversion_matrix('trial_usage_summary.csv')

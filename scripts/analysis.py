import os
import platform
import pandas as pd
import matplotlib.pyplot as plt

# 1. OS별 폰트 동적 세팅
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False
plt.style.use('default') 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'output')

def plot_funnel_dropoff(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(file_path)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    df = df.iloc[::-1].reset_index(drop=True)
    colors = ['#1f497d' if step != '이메일 인증 완료' else '#c00000' for step in df['단계']]
    
    bars = ax.barh(df['단계'], df['사용자 수'], color=colors, height=0.6)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color('#dddddd')
    ax.get_xaxis().set_visible(False)
    
    # 텍스트 여백 동적 처리
    offset = df['사용자 수'].max() * 0.01

    for bar in bars:
        width = bar.get_width()
        ax.text(width + offset, bar.get_y() + bar.get_height()/2,
                f'{int(width):,}', va='center', ha='left', fontsize=12, color='#333333')

    plt.title('가입 퍼널: 이메일 인증 단계에서 51%의 치명적 이탈 발생', fontsize=18, pad=20, weight='bold')
    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'funnel_dropoff.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig) # [수정] 명확한 figure 지정으로 안전성 확보

def plot_feature_conversion_matrix(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(file_path)
    
    df['유료 전환율'] = df['유료 전환율'].str.rstrip('%').astype('float')
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    bubble_sizes = (df['유료 전환율'] * 20) + 50
    
    scatter = ax.scatter(
        df['기능 사용자 수'], df['유료 전환율'], 
        s=bubble_sizes,  
        c=df['유료 전환율'],       
        cmap='Blues', 
        alpha=0.8,
        edgecolors='w', linewidth=1.5, zorder=2
    )
    
    ax.axvline(df['기능 사용자 수'].mean(), color='#999999', linestyle='--', linewidth=1.5, zorder=1)
    ax.axhline(df['유료 전환율'].mean(), color='#999999', linestyle='--', linewidth=1.5, zorder=1)
    
    # [수정] x축 라벨 offset 동적화
    x_offset = df['기능 사용자 수'].max() * 0.015 

    for i in range(df.shape[0]):
        ax.text(df['기능 사용자 수'][i] + x_offset, df['유료 전환율'][i] + 0.5, 
                df['기능'][i], fontsize=12, weight='bold', color='#333333')
                
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#dddddd')
    ax.spines['left'].set_color('#dddddd')

    plt.title('기능 효율 매트릭스: 고전환 기능의 낮은 노출도', fontsize=18, pad=20, weight='bold')
    plt.xlabel('기능 사용자 수 (노출도)', fontsize=14, color='#555555')
    plt.ylabel('유료 전환율 (%)', fontsize=14, color='#555555')
    
    # [수정] Colorbar 테두리 날리기
    cbar = plt.colorbar(scatter)
    cbar.set_label('유료 전환율 (%)', fontsize=12)
    cbar.outline.set_visible(False) 
    
    ax.grid(True, linestyle=':', alpha=0.6, zorder=0)

    plt.tight_layout()
    
    output_path = os.path.join(OUTPUT_DIR, 'feature_matrix.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig) # [수정] 명확한 figure 지정

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plot_funnel_dropoff('landing_event_log.csv')
    plot_feature_conversion_matrix('trial_usage_summary.csv')

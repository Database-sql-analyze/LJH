import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")
plt.rcParams['font.family'] = 'AppleGothic' 
plt.rcParams['axes.unicode_minus'] = False

def plot_funnel_dropoff(file_path):
    df = pd.read_csv(file_path)
    
    plt.figure(figsize=(12, 6))
    

    colors = ['#1f497d', '#1f497d', '#1f497d', '#c00000', '#1f497d']
    
    ax = sns.barplot(x='사용자 수', y='단계', data=df, palette=colors)
    plt.title('가입 퍼널: 이메일 인증 단계에서 51%의 치명적 이탈 발생', fontsize=18, pad=20)
    plt.xlabel('사용자 수', fontsize=14)
    plt.ylabel('')
    
    for i, p in enumerate(ax.patches):
        width = p.get_width()
        ax.text(width + 500, p.get_y() + p.get_height()/2. + 0.1,
                f'{int(width):,}', ha="left", fontsize=12)

    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig('funnel_dropoff.png', dpi=300)
    plt.show()

def plot_feature_conversion_matrix(file_path):
    df = pd.read_csv(file_path)
    
    df['유료 전환율'] = df['유료 전환율'].str.rstrip('%').astype('float')
    
    plt.figure(figsize=(10, 7))
    
    sns.scatterplot(
        x='기능 사용자 수', y='유료 전환율', 
        size='유료 전환율', sizes=(200, 600), 
        hue='유료 전환율', palette='coolwarm', 
        data=df, legend=False
    )
    
    plt.axvline(df['기능 사용자 수'].mean(), color='gray', linestyle='--', alpha=0.7)
    plt.axhline(df['유료 전환율'].mean(), color='gray', linestyle='--', alpha=0.7)
    
    plt.title('기능 효율 매트릭스: 고전환 기능의 낮은 노출도', fontsize=18, pad=20)
    plt.xlabel('기능 사용자 수 (노출도)', fontsize=14)
    plt.ylabel('유료 전환율 (%)', fontsize=14)
    
    for i in range(df.shape[0]):
        plt.text(df['기능 사용자 수'][i] + 50, df['유료 전환율'][i], 
                 df['기능'][i], fontsize=12, weight='bold')

    plt.tight_layout()
    plt.savefig('feature_matrix.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_funnel_dropoff('data/landing_event_log.csv')
    plot_feature_conversion_matrix('data/trial_usage_summary.csv')
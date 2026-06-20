import pandas as pd

def calculate_rebalancing(current_assets, target_ratios):
    # 1. 현재 총 평가금액 계산
    total_value = sum(current_assets.values())
    
    rebalance_data = []
    
    print(f"=== 포트폴리오 리밸런싱 계산 결과 ===")
    print(f"현재 총 자산: {total_value:,.0f}원\n")
    
    # 2. 종목별 비교 및 매매 금액 계산
    for asset, current_val in current_assets.items():
        target_pct = target_ratios.get(asset, 0)
        target_val = total_value * (target_pct / 100)
        difference = target_val - current_val
        
        current_pct = (current_val / total_value) * 100
        
        # 매매 추천 메시지 생성
        if difference > 0:
            action = f"🟢 {difference:,.0f}원 추가 매수"
        elif difference < 0:
            action = f"🔴 {abs(difference):,.0f}원 매도"
        else:
            action = "⚪ 유지"
            
        rebalance_data.append({
            "종목명": asset,
            "현재 비중(%)": f"{current_pct:.1f}%",
            "목표 비중(%)": f"{target_pct:.1f}%",
            "현재 금액": f"{current_val:,.0f}원",
            "목표 금액": f"{target_val:,.0f}원",
            "매매 주문": action
        })
    
    # 보기 좋게 데이터프레임으로 변환 후 출력
    df = pd.DataFrame(rebalance_data)
    return df

# ========================================================
# 데이터 입력부 (네가 나중에 데이터를 긁어서 여기에 넣으면 돼!)
# ========================================================

# 1. 현재 자산 상황 (원화 기준 평가금액)
my_assets = {
    "DRAM": 5132527,
    "QLD": 4466057,
    "GGLL": 4465337,
    "CHAT": 2334077,
    "SPYM": 2138142,
    "SPMO": 1701757,
    "SOL AI반도체TOP2플러스": 757620
}

# 2. 네가 설정한 목표 비중 (%) - 합계가 100이 되도록 설정
my_target = {
    "DRAM": 30.0,
    "SPYM": 30.0,
    "SOL AI반도체TOP2플러스": 10.0,
    "QLD": 5.0,
    "GGLL": 5.0,
    "CHAT": 11.6,  # 기존 비율 유지 반영 값
    "SPMO": 8.4    # 기존 비율 유지 반영 값
}

# 프로그램 실행
result_df = calculate_rebalancing(my_assets, my_target)
import notebook.repr_html  # 프리티 출력을 위한 세팅
result_df

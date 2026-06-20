# 1. 터미널을 예쁘게 꾸며주는 rich 라이브러리 설치
pip install rich

# 2. rebalance.py 파일을 가시성 극대화 버전으로 완전히 새로 쓰기
cat << 'EOF' > rebalance.py
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

def calculate_rebalancing(current_assets, target_ratios):
    console = Console()
    total_value = sum(current_assets.values())
    
    # 상단 요약 패널 구성
    summary_text = f"[bold white]현재 총 자산:[/bold white] [bold cyan]{total_value:,.0f}원[/bold cyan]"
    console.print(Panel(summary_text, title="📊 내 투자 포트폴리오 리밸런싱", expand=False))
    
    # 예쁜 테이블 생성
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("종목명", style="bold dim", width=12, justify="center")
    table.add_column("현재 비중", justify="right")
    table.add_column("목표 비중", justify="right")
    table.add_column("현재 금액", justify="right")
    table.add_column("목표 금액", justify="right")
    table.add_column("매매 주문", justify="left")
    
    total_buy = 0
    total_sell = 0
    
    for asset, current_val in current_assets.items():
        target_pct = target_ratios.get(asset, 0)
        target_val = total_value * (target_pct / 100)
        difference = target_val - current_val
        
        current_pct = (current_val / total_value) * 100
        display_diff = int(difference)
        
        # 매매 주문 색상 및 텍스트 설정
        if display_diff > 0:
            action = f"[bold green]🟢 {display_diff:,.0f}원 추가 매수[/bold green]"
            total_buy += display_diff
        elif display_diff < 0:
            action = f"[bold red]🔴 {abs(display_diff):,.0f}원 매도[/bold red]"
            total_sell += abs(display_diff)
        else:
            action = "[white]⚪ 유지[/white]"
            
        table.add_row(
            asset,
            f"{current_pct:.1f}%",
            f"{target_pct:.1f}%",
            f"{current_val:,.0f}원",
            f"{target_val:,.0f}원",
            action
        )
        
    console.print(table)
    
    # 하단 자금 흐름 요약 패널
    flow_text = (
        f"[bold red]▶ 총 매도 (확보 금액):[/bold red] [red]{total_sell:,.0f}원[/red]\n"
        f"[bold green]▶ 총 매수 (필요 금액):[/bold green] [green]{total_buy:,.0f}원[/green]\n"
        f"[bold yellow]▶ 외부 추가 입금 필요액:[/bold yellow] [yellow]{max(0, total_buy - total_sell):,.0f}원[/yellow]"
    )
    console.print(Panel(flow_text, title="💰 자금 흐름 요약", expand=False))

# 데이터 입력
my_assets = {
    "DRAM": 5132527,
    "QLD": 4466057,
    "GGLL": 4465337,
    "CHAT": 2334077,
    "SPYM": 2138142,
    "SPMO": 1701757,
    "SOL": 757620
}

my_target = {
    "DRAM": 30.0,
    "SPYM": 30.0,
    "SOL": 10.0,
    "QLD": 5.0,
    "GGLL": 5.0,
    "CHAT": 11.6,
    "SPMO": 8.4
}

calculate_rebalancing(my_assets, my_target)
EOF

# 3. 즉시 실행하여 가시성 확인하기!
python rebalance.py

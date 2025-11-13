"""
포트폴리오 코드 품질 검증기 - 메인 실행 스크립트
"""
import click
import sys
import io
from pathlib import Path
from code_analyzer import CodeAnalyzer
from reporter import ReportGenerator
from colorama import init, Fore, Style

# Windows에서 인코딩 및 colorama 초기화
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
init(autoreset=True)


@click.command()
@click.argument('target_path', type=click.Path(exists=True))
@click.option('-o', '--output', default='report.html', help='리포트 출력 파일명')
@click.option('--detailed', is_flag=True, help='상세 분석 모드')
def main(target_path, output, detailed):
    """
    포트폴리오 코드 품질 검증기
    
    TARGET_PATH: 분석할 코드 경로 (파일 또는 디렉토리)
    """
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}포트폴리오 코드 품질 검증기")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        # 분석 시작
        print(f"{Fore.YELLOW}분석 중...{Style.RESET_ALL}")
        print(f"대상: {target_path}\n")
        
        analyzer = CodeAnalyzer(target_path)
        results = analyzer.analyze()
        
        # 결과 출력
        print(f"\n{Fore.GREEN}✓ 분석 완료!{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}분석 결과 요약:{Style.RESET_ALL}")
        print(f"  • 분석된 파일: {results['files_analyzed']}개")
        print(f"  • 총 코드 라인: {results['total_lines']:,}줄")
        print(f"  • 사용된 언어: {', '.join(results['languages'].keys()) or '없음'}")
        print(f"  • 평균 복잡도: {results['complexity']['avg']:.1f}")
        
        # 점수 출력
        score = results.get('overall_score', 0)
        grade = results.get('grade', 'F')
        
        if score >= 90:
            score_color = Fore.GREEN
        elif score >= 80:
            score_color = Fore.CYAN
        elif score >= 70:
            score_color = Fore.YELLOW
        else:
            score_color = Fore.RED
        
        print(f"\n{Fore.CYAN}종합 점수:{Style.RESET_ALL}")
        print(f"  {score_color}점수: {score}점{Style.RESET_ALL}")
        print(f"  {score_color}등급: {grade}{Style.RESET_ALL}\n")
        
        # 이슈 요약
        all_issues = []
        all_issues.extend(results.get('issues', []))
        all_issues.extend(results.get('readability', {}).get('issues', []))
        all_issues.extend(results.get('structure', {}).get('issues', []))
        
        if all_issues:
            high_count = sum(1 for i in all_issues if i.get('severity') == 'high')
            medium_count = sum(1 for i in all_issues if i.get('severity') == 'medium')
            low_count = sum(1 for i in all_issues if i.get('severity') == 'low')
            
            print(f"{Fore.CYAN}발견된 이슈:{Style.RESET_ALL}")
            if high_count > 0:
                print(f"  {Fore.RED}심각: {high_count}개{Style.RESET_ALL}")
            if medium_count > 0:
                print(f"  {Fore.YELLOW}중간: {medium_count}개{Style.RESET_ALL}")
            if low_count > 0:
                print(f"  {Fore.BLUE}낮음: {low_count}개{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}발견된 이슈 없음!{Style.RESET_ALL}")
        
        # 리포트 생성
        print(f"\n{Fore.YELLOW}리포트 생성 중...{Style.RESET_ALL}")
        reporter = ReportGenerator(results)
        report_path = reporter.generate_html(output)
        
        print(f"\n{Fore.GREEN}✓ 리포트 생성 완료!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}리포트 위치: {report_path}{Style.RESET_ALL}\n")
        
        # 상세 모드
        if detailed and all_issues:
            print(f"\n{Fore.CYAN}상세 이슈 목록:{Style.RESET_ALL}")
            print("-" * 60)
            for issue in all_issues[:20]:  # 최대 20개만 표시
                severity = issue.get('severity', 'low')
                if severity == 'high':
                    severity_color = Fore.RED
                elif severity == 'medium':
                    severity_color = Fore.YELLOW
                else:
                    severity_color = Fore.BLUE
                
                print(f"\n{severity_color}[{severity.upper()}]{Style.RESET_ALL} {issue.get('file', 'Unknown')}")
                print(f"  {issue.get('message', 'No message')}")
            if len(all_issues) > 20:
                print(f"\n{Fore.YELLOW}... 외 {len(all_issues) - 20}개 이슈 더 있음{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}분석 완료!")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"\n{Fore.RED}오류 발생: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == '__main__':
    main()


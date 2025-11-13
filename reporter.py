"""
리포트 생성기
분석 결과를 HTML 형식의 리포트로 생성합니다.

Copyright (c) 2025 Gaon
All rights reserved.

이 소프트웨어는 저작권법에 의해 보호됩니다.
무단 복제, 배포, 수정을 금지합니다.
사용 시 반드시 출처를 명시해야 합니다.

원본 출처: https://github.com/Gaon/portfolio-code-analyzer
"""
from typing import Dict
from pathlib import Path
from jinja2 import Template
from datetime import datetime


class ReportGenerator:
    """HTML 리포트 생성 클래스"""
    
    HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>코드 품질 분석 리포트</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .summary-card h3 {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        .summary-card .value {
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }
        .score-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }
        .score-card .score {
            font-size: 72px;
            font-weight: bold;
            margin: 20px 0;
        }
        .score-card .grade {
            font-size: 48px;
            opacity: 0.9;
        }
        .section {
            margin: 40px 0;
        }
        .section h2 {
            color: #2c3e50;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-bottom: 20px;
        }
        .issue-list {
            list-style: none;
        }
        .issue-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #e74c3c;
            border-radius: 5px;
        }
        .issue-item.medium {
            border-left-color: #f39c12;
        }
        .issue-item.low {
            border-left-color: #3498db;
        }
        .issue-item .severity {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }
        .severity.high {
            background: #e74c3c;
            color: white;
        }
        .severity.medium {
            background: #f39c12;
            color: white;
        }
        .severity.low {
            background: #3498db;
            color: white;
        }
        .language-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }
        .language-tag {
            background: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
        }
        .recommendations {
            background: #e8f5e9;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .recommendations h3 {
            color: #2e7d32;
            margin-bottom: 15px;
        }
        .recommendations ul {
            margin-left: 20px;
        }
        .recommendations li {
            margin: 8px 0;
            color: #1b5e20;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #777;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 코드 품질 분석 리포트</h1>
        
        <div class="score-card">
            <div class="score">{{ overall_score }}점</div>
            <div class="grade">등급: {{ grade }}</div>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>분석된 파일</h3>
                <div class="value">{{ files_analyzed }}</div>
            </div>
            <div class="summary-card">
                <h3>총 코드 라인</h3>
                <div class="value">{{ total_lines }}</div>
            </div>
            <div class="summary-card">
                <h3>발견된 이슈</h3>
                <div class="value">{{ total_issues }}</div>
            </div>
            <div class="summary-card">
                <h3>평균 복잡도</h3>
                <div class="value">{{ avg_complexity }}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🌐 사용된 언어</h2>
            <div class="language-stats">
                {% for lang, count in languages.items() %}
                <span class="language-tag">{{ lang }} ({{ count }}개 파일)</span>
                {% endfor %}
            </div>
        </div>
        
        <div class="section">
            <h2>⚠️ 발견된 이슈</h2>
            <ul class="issue-list">
                {% for issue in all_issues %}
                <li class="issue-item {{ issue.severity }}">
                    <span class="severity {{ issue.severity }}">{{ issue.severity.upper() }}</span>
                    <strong>{{ issue.file }}</strong><br>
                    {{ issue.message }}
                </li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="section">
            <h2>💡 개선 권장 사항</h2>
            <div class="recommendations">
                <h3>주요 개선 포인트</h3>
                <ul>
                    {% for rec in recommendations %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>생성 일시: {{ timestamp }}</p>
            <p>포트폴리오 코드 품질 검증기 v1.0</p>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
            <p style="font-size: 12px; color: #999;">
                Copyright (c) 2025 Gaon. All rights reserved.<br>
                이 리포트는 포트폴리오 코드 품질 검증기로 생성되었습니다.<br>
                원본 출처: <a href="https://github.com/Gaon/portfolio-code-analyzer" style="color: #3498db;">https://github.com/Gaon/portfolio-code-analyzer</a>
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    def __init__(self, analysis_results: Dict):
        self.results = analysis_results
    
    def generate_html(self, output_path: str = "report.html"):
        """HTML 리포트 생성"""
        template = Template(self.HTML_TEMPLATE)
        
        # 데이터 준비
        all_issues = []
        all_issues.extend(self.results.get('issues', []))
        all_issues.extend(self.results.get('readability', {}).get('issues', []))
        all_issues.extend(self.results.get('structure', {}).get('issues', []))
        
        # 심각도별 정렬
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        all_issues.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 2))
        
        # 권장 사항 생성
        recommendations = self._generate_recommendations()
        
        html_content = template.render(
            overall_score=self.results.get('overall_score', 0),
            grade=self.results.get('grade', 'F'),
            files_analyzed=self.results.get('files_analyzed', 0),
            total_lines=self.results.get('total_lines', 0),
            total_issues=len(all_issues),
            avg_complexity=round(self.results.get('complexity', {}).get('avg', 0), 1),
            languages=self.results.get('languages', {}),
            all_issues=all_issues,
            recommendations=recommendations,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        output_file = Path(output_path)
        output_file.write_text(html_content, encoding='utf-8')
        
        return str(output_file.absolute())
    
    def _generate_recommendations(self) -> list:
        """분석 결과 기반 권장 사항 생성"""
        recommendations = []
        
        score = self.results.get('overall_score', 0)
        
        if score < 70:
            recommendations.append("코드 품질이 개선이 필요합니다. 기본적인 코딩 규칙과 구조를 개선하세요.")
        
        # 복잡도 관련
        avg_complexity = self.results.get('complexity', {}).get('avg', 0)
        if avg_complexity > 10:
            recommendations.append("코드 복잡도가 높습니다. 함수를 더 작은 단위로 분리하고 로직을 단순화하세요.")
        
        # 이슈 관련
        high_issues = [i for i in self.results.get('issues', []) if i.get('severity') == 'high']
        if high_issues:
            recommendations.append(f"심각한 이슈 {len(high_issues)}개를 우선적으로 해결하세요.")
        
        # 가독성 관련
        readability_issues = len(self.results.get('readability', {}).get('issues', []))
        if readability_issues > 5:
            recommendations.append("코드 가독성을 개선하세요. 주석 추가, 네이밍 개선, 코드 구조화를 고려하세요.")
        
        # 구조 관련
        structure_issues = len(self.results.get('structure', {}).get('issues', []))
        if structure_issues > 3:
            recommendations.append("코드 구조를 개선하세요. 모듈화와 관심사 분리를 적용하세요.")
        
        if not recommendations:
            recommendations.append("전반적으로 양호한 코드 품질을 보이고 있습니다. 계속 유지하세요!")
        
        return recommendations


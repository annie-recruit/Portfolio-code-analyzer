"""
코드 품질 분석 엔진
다양한 지표를 통해 코드 품질을 평가합니다.
"""
import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import subprocess
import json


class CodeAnalyzer:
    """코드 품질을 분석하는 메인 클래스"""
    
    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.analysis_results = {
            'files_analyzed': 0,
            'total_lines': 0,
            'languages': defaultdict(int),
            'complexity': {'avg': 0, 'max': 0, 'high_complexity_files': []},
            'readability': {'score': 0, 'issues': []},
            'structure': {'score': 0, 'issues': []},
            'issues': [],
            'metrics': {}
        }
    
    def analyze(self) -> Dict:
        """전체 코드베이스 분석"""
        if not self.target_path.exists():
            raise ValueError(f"경로를 찾을 수 없습니다: {self.target_path}")
        
        # 파일 수집
        code_files = self._collect_code_files()
        self.analysis_results['files_analyzed'] = len(code_files)
        
        if not code_files:
            return self.analysis_results
        
        # 각 파일 분석
        for file_path in code_files:
            self._analyze_file(file_path)
        
        # 종합 점수 계산
        self._calculate_overall_score()
        
        return self.analysis_results
    
    def _collect_code_files(self) -> List[Path]:
        """분석할 코드 파일 수집"""
        code_files = []
        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP'
        }
        
        if self.target_path.is_file():
            if self.target_path.suffix in extensions:
                code_files.append(self.target_path)
                self.analysis_results['languages'][extensions[self.target_path.suffix]] += 1
        else:
            for ext, lang in extensions.items():
                for file_path in self.target_path.rglob(f'*{ext}'):
                    # 숨김 파일 및 특정 디렉토리 제외
                    if not any(part.startswith('.') for part in file_path.parts):
                        if 'node_modules' not in file_path.parts and 'venv' not in file_path.parts:
                            code_files.append(file_path)
                            self.analysis_results['languages'][lang] += 1
        
        return code_files
    
    def _analyze_file(self, file_path: Path):
        """개별 파일 분석"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                self.analysis_results['total_lines'] += len(lines)
            
            # 언어별 분석
            if file_path.suffix == '.py':
                self._analyze_python(file_path, content)
            elif file_path.suffix in ['.js', '.ts']:
                self._analyze_javascript(file_path, content)
            elif file_path.suffix == '.java':
                self._analyze_java(file_path, content)
            else:
                self._analyze_generic(file_path, content)
                
        except Exception as e:
            self.analysis_results['issues'].append({
                'file': str(file_path),
                'type': 'error',
                'message': f'파일 분석 중 오류: {str(e)}'
            })
    
    def _analyze_python(self, file_path: Path, content: str):
        """Python 코드 분석"""
        try:
            tree = ast.parse(content)
            
            # 복잡도 분석
            complexity = self._calculate_complexity_python(tree)
            files_count = self.analysis_results['files_analyzed']
            if files_count > 0:
                self.analysis_results['complexity']['avg'] = (
                    self.analysis_results['complexity']['avg'] * 
                    (files_count - 1) + complexity
                ) / files_count
            else:
                self.analysis_results['complexity']['avg'] = complexity
            
            if complexity > self.analysis_results['complexity']['max']:
                self.analysis_results['complexity']['max'] = complexity
                if complexity > 10:
                    self.analysis_results['complexity']['high_complexity_files'].append({
                        'file': str(file_path),
                        'complexity': complexity
                    })
            
            # 가독성 체크
            self._check_readability(file_path, content, 'Python')
            
            # 구조 체크
            self._check_structure_python(tree, file_path)
            
        except SyntaxError as e:
            self.analysis_results['issues'].append({
                'file': str(file_path),
                'type': 'syntax_error',
                'message': f'구문 오류: {str(e)}',
                'severity': 'high'
            })
    
    def _analyze_javascript(self, file_path: Path, content: str):
        """JavaScript/TypeScript 코드 분석"""
        lines = content.split('\n')
        
        # 기본 메트릭
        function_count = len(re.findall(r'\bfunction\s+\w+|const\s+\w+\s*=\s*\(|=>', content))
        class_count = len(re.findall(r'\bclass\s+\w+', content))
        
        # 가독성 체크
        self._check_readability(file_path, content, 'JavaScript')
        
        # 긴 함수 체크
        if len(lines) > 200:
            self.analysis_results['issues'].append({
                'file': str(file_path),
                'type': 'long_file',
                'message': f'파일이 너무 깁니다 ({len(lines)}줄). 모듈화를 고려하세요.',
                'severity': 'medium'
            })
    
    def _analyze_java(self, file_path: Path, content: str):
        """Java 코드 분석"""
        self._check_readability(file_path, content, 'Java')
        
        # 클래스 구조 체크
        class_count = len(re.findall(r'\bpublic\s+class\s+\w+', content))
        if class_count == 0:
            self.analysis_results['issues'].append({
                'file': str(file_path),
                'type': 'structure',
                'message': '클래스 정의가 없습니다.',
                'severity': 'low'
            })
    
    def _analyze_generic(self, file_path: Path, content: str):
        """일반적인 코드 분석 (언어 무관)"""
        self._check_readability(file_path, content, 'Generic')
    
    def _calculate_complexity_python(self, tree: ast.AST) -> int:
        """Python 코드의 복잡도 계산 (간단한 버전)"""
        complexity = 1  # 기본 복잡도
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def _check_readability(self, file_path: Path, content: str, language: str):
        """가독성 체크"""
        lines = content.split('\n')
        
        # 주석 비율
        comment_lines = sum(1 for line in lines if line.strip().startswith('#') or 
                           '//' in line or '/*' in line or '*/' in line)
        comment_ratio = comment_lines / len(lines) if lines else 0
        
        if comment_ratio < 0.1 and len(lines) > 50:
            self.analysis_results['readability']['issues'].append({
                'file': str(file_path),
                'type': 'low_comments',
                'message': '주석이 부족합니다. 코드 이해를 위해 주석을 추가하세요.',
                'severity': 'medium'
            })
        
        # 긴 줄 체크
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 120]
        if long_lines:
            self.analysis_results['readability']['issues'].append({
                'file': str(file_path),
                'type': 'long_lines',
                'message': f'120자를 초과하는 긴 줄이 {len(long_lines)}개 있습니다.',
                'severity': 'low'
            })
        
        # 빈 줄 비율 (구조적 가독성)
        empty_lines = sum(1 for line in lines if not line.strip())
        empty_ratio = empty_lines / len(lines) if lines else 0
        if empty_ratio < 0.05:
            self.analysis_results['readability']['issues'].append({
                'file': str(file_path),
                'type': 'dense_code',
                'message': '코드가 너무 밀집되어 있습니다. 가독성을 위해 빈 줄을 추가하세요.',
                'severity': 'low'
            })
    
    def _check_structure_python(self, tree: ast.AST, file_path: Path):
        """Python 구조 체크"""
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        # 긴 함수 체크
        for func in functions:
            if func.end_lineno and func.lineno:
                func_length = func.end_lineno - func.lineno
                if func_length > 50:
                    self.analysis_results['structure']['issues'].append({
                        'file': str(file_path),
                        'type': 'long_function',
                        'message': f'함수 "{func.name}"이 너무 깁니다 ({func_length}줄). 분리하는 것을 고려하세요.',
                        'severity': 'medium'
                    })
        
        # 전역 변수 남용 체크
        global_vars = [node for node in ast.walk(tree) if isinstance(node, ast.Global)]
        if len(global_vars) > 5:
            self.analysis_results['structure']['issues'].append({
                'file': str(file_path),
                'type': 'too_many_globals',
                'message': '전역 변수가 너무 많습니다. 구조를 개선하세요.',
                'severity': 'medium'
            })
    
    def _calculate_overall_score(self):
        """종합 점수 계산 (0-100)"""
        score = 100
        
        # 복잡도 감점
        if self.analysis_results['complexity']['avg'] > 10:
            score -= 20
        elif self.analysis_results['complexity']['avg'] > 5:
            score -= 10
        
        # 이슈 감점
        high_severity = sum(1 for issue in self.analysis_results['issues'] 
                          if issue.get('severity') == 'high')
        medium_severity = sum(1 for issue in self.analysis_results['issues'] 
                            if issue.get('severity') == 'medium')
        
        score -= high_severity * 5
        score -= medium_severity * 2
        
        # 가독성 감점
        score -= len(self.analysis_results['readability']['issues']) * 1
        score -= len(self.analysis_results['structure']['issues']) * 2
        
        # 최소 0점 보장
        score = max(0, min(100, score))
        
        self.analysis_results['overall_score'] = round(score, 1)
        
        # 등급 부여
        if score >= 90:
            grade = 'A'
        elif score >= 80:
            grade = 'B'
        elif score >= 70:
            grade = 'C'
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'F'
        
        self.analysis_results['grade'] = grade


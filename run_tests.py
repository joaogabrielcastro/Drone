#!/usr/bin/env python3
"""
Script para executar todos os testes do projeto
"""

import unittest
import sys
import os

def run_all_tests():
    """Executa todos os testes do projeto"""
    
    # Adicionar src ao path para imports
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Descobrir todos os testes
    loader = unittest.TestLoader()
    start_dir = os.path.join('src', 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retornar sucesso ou falha
    return result.wasSuccessful()

if __name__ == '__main__':
    print("🧪 Executando todos os testes...")
    print("=" * 50)
    
    success = run_all_tests()
    
    if success:
        print("\n✅ Todos os testes passaram!")
        sys.exit(0)
    else:
        print("\n❌ Alguns testes falharam!")
        sys.exit(1)
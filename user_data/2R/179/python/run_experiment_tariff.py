#!/usr/bin/env python3
import os
import pickle
import shutil
from parameters_2R_178 import ModelParameters  # モデルのパラメータ
from model_constants_2R_178 import Runner  # モデルの計算を行うRunnerクラス

# --- 1. ベースラインの読み込み ---
baseline_results_dir = os.path.join('user_data', 'results', 'run_baseline')

with open(os.path.join(baseline_results_dir, 'model_solution.pickle'), 'rb') as f:
    model_solution = pickle.load(f)

with open(os.path.join(baseline_results_dir, 'baseline_projections.pickle'), 'rb') as f:
    baseline_projections = pickle.load(f)

# --- 2. TIM（関税）に25%のショックを加える関数 ---
def apply_tariff_shock(projections, shock=0.25):
    """関税変数 'TIM' を25%引き上げる"""
    new_projections = projections.copy()
    new_projections['TIM'] = projections['TIM'] * (1 + shock)
    return new_projections

# ショックを適用
shock_projections = apply_tariff_shock(baseline_projections)

# --- 3. モデルのRunnerを使用してシミュレーションを実行 ---
runner = Runner(model_solution, baseline_projections)
runner.add_simulation_layer(shock_projections, name="25% Tariff Increase")

# --- 4. 実験結果の保存 ---
experiment_results_dir = os.path.join('user_data', 'results', 'run_experiment_tariff')
os.makedirs(experiment_results_dir, exist_ok=True)
runner.save_results(experiment_results_dir)

print("実験が完了しました。結果は以下に保存されました:", experiment_results_dir)

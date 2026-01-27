import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def compute_shap_values(model, X):
    """
    Compute SHAP values for a tree-based model.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    return explainer, shap_values

def plot_shap_summary(shap_values, X, show=True, save_path=None):
    """
    Generate summary plot.
    """
    plt.figure()
    shap.summary_plot(shap_values, X, show=False)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        print(f"saved plot to {save_path}")
    if show:
        plt.show()
    plt.close()

def check_stability(model, X_sample, n_perturbations=10, operational_noise=0.01):
    """
    Check if explanations are stable under small noise.
    Returns: Average variation in feature importance rank.
    """
    explainer = shap.TreeExplainer(model)
    base_shap = explainer.shap_values(X_sample)
    
    variations = []
    
    for _ in range(n_perturbations):
        # Add small Gaussian noise
        noise = np.random.normal(0, operational_noise, X_sample.shape)
        X_perturbed = X_sample + noise
        # Keep column names if dataframe
        if isinstance(X_sample, pd.DataFrame):
            X_perturbed = pd.DataFrame(X_perturbed, columns=X_sample.columns)
            
        perturbed_shap = explainer.shap_values(X_perturbed)
        
        # Calculate mean absolute difference
        diff = np.abs(base_shap - perturbed_shap).mean()
        variations.append(diff)
        
    return np.mean(variations)

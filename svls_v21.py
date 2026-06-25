"""
SVLS v2.1 (Formula M): Interactive Calculator with Input Validation
Scale-Variable Light Speed theory for pulsar luminosities

Author: Motrosov, A. A.
Email: kolatec@yandex.ru
Date: June 2026
License: MIT
Repository: https://github.com/Andrey281119/svls-v2.1
"""

import numpy as np


class SVLSv21:
    """SVLS v2.1 (Formula M) implementation"""
    
    def __init__(self, eta=2.32, theta_crit=1.0):
        self.eta = eta
        self.theta_crit = theta_crit
    
    def sigma(self, theta):
        """Switching function σ(Θ)"""
        return np.tanh(np.log10(theta / self.theta_crit))
    
    def eps_rad(self, theta):
        """Coherence efficiency multiplier ε_rad(Θ)"""
        return 1 + self.eta * (1 + self.sigma(theta)) / 2
    
    def luminosity(self, theta, L_micro):
        """Total luminosity prediction"""
        return self.eps_rad(theta) * L_micro
    
    def theta_1(self, P):
        """Channel 1: Light cylinder radius"""
        l_P = 1.616e-35
        c_0 = 2.998e8
        R_LC = c_0 * P / (2 * np.pi)
        return 1e10 * (l_P / R_LC)**2
    
    def theta_2(self, P, P_dot):
        """Channel 2: Surface magnetic field"""
        B_Q = 4.4e13
        B_s = 3.2e19 * np.sqrt(P * P_dot)
        return 1e10 * (B_s / B_Q)**2
    
    def theta_3(self, rho_c):
        """Channel 3: Curvature radius"""
        l_P = 1.616e-35
        return 1e10 * (l_P / rho_c)**2
    
    def theta_total(self, P, P_dot, rho_c=None):
        """Total coherence parameter Θ = max(Θ₁, Θ₂, Θ₃)"""
        t1 = self.theta_1(P)
        t2 = self.theta_2(P, P_dot)
        
        if rho_c is None:
            R_LC = 2.998e8 * P / (2 * np.pi)
            rho_c = 0.2 * R_LC
        
        t3 = self.theta_3(rho_c)
        
        return np.maximum(np.maximum(t1, t2), t3)
    
    def regime(self, theta):
        """Determine emission regime"""
        if theta < 0.1:
            return 'Incoherent'
        elif theta > 10:
            return 'Coherent'
        else:
            return 'Transition'


def validate_pulsar_params(P, P_dot):
    """Validate pulsar parameters and return warnings"""
    warnings = []
    
    # Period validation
    if P < 0.001:
        warnings.append(f"⚠️  WARNING: Period P = {P:.2e} s is TOO SMALL (< 0.001 s)")
    elif P > 10:
        warnings.append(f"⚠️  WARNING: Period P = {P:.2e} s is TOO LARGE (> 10 s)")
    
    # Period derivative validation
    if P_dot < 1e-21:
        warnings.append(f"⚠️  WARNING: P_dot = {P_dot:.2e} is TOO SMALL (< 1e-21)")
    elif P_dot > 1e-11:
        warnings.append(f"⚠️  WARNING: P_dot = {P_dot:.2e} is TOO LARGE (> 1e-11)")
    elif P_dot <= 0:
        warnings.append(f"⚠️  ERROR: P_dot must be POSITIVE (> 0)")
    
    return warnings


def calculate_pulsar(P, P_dot, name="Unknown"):
    """Calculate SVLS v2.1 parameters for a pulsar"""
    model = SVLSv21(eta=2.32, theta_crit=1.0)
    
    theta = model.theta_total(P, P_dot)
    eps = model.eps_rad(theta)
    regime = model.regime(theta)
    
    # Calculate B_s
    B_s = 3.2e19 * np.sqrt(P * P_dot)
    
    # Calculate standard luminosity
    E_dot = 4e47 * P * P_dot
    L_std = 1e28 * (E_dot / 1e36)**0.5
    
    # Calculate SVLS luminosity
    L_svls = model.luminosity(theta, L_std)
    
    return {
        'name': name,
        'P': P,
        'P_dot': P_dot,
        'B_s': B_s,
        'theta': theta,
        'eps_rad': eps,
        'regime': regime,
        'L_std': L_std,
        'L_svls': L_svls,
        'ratio': L_svls / L_std
    }


def print_results(results):
    """Print calculation results"""
    print("\n" + "=" * 80)
    print(f"SVLS v2.1 (Formula M) - Calculation Results".center(80))
    print("=" * 80)
    
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['name']}")
        print("-" * 80)
        print(f"  Period P:           {r['P']:.6f} s")
        print(f"  Period derivative:  {r['P_dot']:.2e} s/s")
        print(f"  Magnetic field B_s: {r['B_s']:.2e} G")
        print(f"  Θ (Theta):          {r['theta']:.2e}")
        print(f"  ε_rad:              {r['eps_rad']:.3f}")
        print(f"  Regime:             {r['regime']}")
        print(f"  L_std:              {r['L_std']:.2e} erg/s")
        print(f"  L_SVLS:             {r['L_svls']:.2e} erg/s")
        print(f"  Enhancement:        {r['ratio']:.2f}x")
    
    print("\n" + "=" * 80)
    print("© 2026 Motrosov, A. A. - MIT License")
    print("=" * 80)


def get_float_input(prompt, min_val=None, max_val=None):
    """Get float input with optional range validation"""
    while True:
        try:
            value = float(input(prompt).strip())
            
            if min_val is not None and value < min_val:
                print(f"❌ Value must be >= {min_val:.2e}. Try again.")
                continue
            
            if max_val is not None and value > max_val:
                print(f"❌ Value must be <= {max_val:.2e}. Try again.")
                continue
            
            return value
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")


def interactive_mode():
    """Interactive calculator mode with validation"""
    print("\n" + "=" * 80)
    print("SVLS v2.1 (Formula M) - Interactive Calculator".center(80))
    print("=" * 80)
    print("\n📊 VALID PARAMETER RANGES:")
    print("-" * 80)
    print("  Period P:           0.001 – 10 s")
    print("  Period derivative:  1e-21 – 1e-11 s/s")
    print("  (Typical values shown)")
    print("-" * 80)
    
    results = []
    
    while True:
        print("\n" + "-" * 80)
        name = input("Pulsar name (or 'done' to finish, 'examples' for samples): ").strip()
        
        if name.lower() == 'done':
            break
        
        if name.lower() == 'examples':
            # Add example pulsars
            examples = [
                ('Crab Pulsar', 0.033, 4.2e-13),
                ('Vela Pulsar', 0.089, 1.3e-13),
                ('PSR B1913+16', 0.059, 8.6e-18),
                ('Typical MSP', 0.005, 1e-20),
            ]
            
            for ex_name, P, P_dot in examples:
                result = calculate_pulsar(P, P_dot, ex_name)
                results.append(result)
            print(f"✓ Added {len(examples)} example pulsars")
            continue
        
        try:
            print("\n  Enter parameters (typical ranges in parentheses):")
            P = get_float_input("  Period P [s] (0.001-10): ", min_val=1e-6, max_val=100)
            P_dot = get_float_input("  Period derivative P_dot [s/s] (1e-21 to 1e-11): ", 
                                    min_val=1e-25, max_val=1e-8)
            
            # Validate and show warnings
            warnings = validate_pulsar_params(P, P_dot)
            if warnings:
                print("\n" + "!" * 80)
                for warning in warnings:
                    print(f"  {warning}")
                print("!" * 80)
                
                confirm = input("\nContinue with these values? (y/n): ").strip().lower()
                if confirm != 'y':
                    print("⚠️  Please re-enter values.")
                    continue
            
            result = calculate_pulsar(P, P_dot, name if name else f"Pulsar {len(results)+1}")
            results.append(result)
            print(f"✓ Calculated for {name}")
            
        except ValueError:
            print("❌ Invalid input. Please enter numeric values.")
            continue
    
    if results:
        print_results(results)


def demo_mode():
    """Demonstration with known pulsars"""
    print("\n" + "=" * 80)
    print("SVLS v2.1 (Formula M) - Demonstration".center(80))
    print("=" * 80)
    
    # Famous pulsars
    pulsars = [
        ('Crab Pulsar (PSR B0531+21)', 0.033, 4.2e-13),
        ('Vela Pulsar (PSR B0833-45)', 0.089, 1.3e-13),
        ('PSR B1913+16 (Hulse-Taylor)', 0.059, 8.6e-18),
        ('PSR J0437-4715 (MSP)', 0.00575, 5.7e-20),
        ('PSR B1937+21 (Fastest MSP)', 0.00156, 1.05e-19),
        ('Normal Pulsar', 1.0, 1e-15),
    ]
    
    results = []
    for name, P, P_dot in pulsars:
        result = calculate_pulsar(P, P_dot, name)
        results.append(result)
    
    print_results(results)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("SVLS v2.1 (Formula M) Calculator".center(80))
    print("=" * 80)
    print("\n📊 Valid parameter ranges:")
    print("  Period P:           0.001 – 10 s")
    print("  Period derivative:  1e-21 – 1e-11 s/s")
    print("\nChoose mode:")
    print("  1 - Demonstration (famous pulsars)")
    print("  2 - Interactive calculator (with validation)")
    print("  3 - Quick examples")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '1':
        demo_mode()
    elif choice == '2':
        interactive_mode()
    elif choice == '3':
        # Quick examples
        examples = [
            ('Crab Pulsar', 0.033, 4.2e-13),
            ('Vela Pulsar', 0.089, 1.3e-13),
            ('Normal Pulsar', 1.0, 1e-15),
        ]
        
        results = []
        for name, P, P_dot in examples:
            result = calculate_pulsar(P, P_dot, name)
            results.append(result)
        
        print_results(results)
    else:
        print("Invalid choice. Running demonstration...")
        demo_mode()
    
    input("\nPress Enter to exit...")

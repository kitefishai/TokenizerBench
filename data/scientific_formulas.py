dataset = {
    "math_science": {

        "algebra": [
            "x² + y² = z²",
            "(a + b)³ = a³ + 3a²b + 3ab² + b³",
            "f(x) = sin(x) + log(x)",
            "ax² + bx + c = 0"
        ],

        "calculus": [
            "lim(x→∞) 1/x = 0",
            "∫₀¹ x² dx = 1/3",
            "d/dx (x²) = 2x",
            "∂²u/∂x²"
        ],

        "physics": [
            "E = mc²",
            "F = ma",
            "v = u + at",
            "p = mv"
        ],

        "chemistry": [
            "H₂O + CO₂ → H₂CO₃",
            "NaCl → Na⁺ + Cl⁻",
            "pH = -log[H⁺]",
            "CH₄ + 2O₂ → CO₂ + 2H₂O"
        ],

        "symbols_edge_cases": [
            "∑(i=1 to n) i²",
            "α, β, γ, δ",
            "∞ ≠ NaN",
            "≈ ≠ ≤ ≥ ±"
        ],

        "advanced_algebra": [
            "(x + y + z)^2 = x^2 + y^2 + z^2 + 2xy + 2yz + 2zx",
            "det(A) = λ₁λ₂λ₃",
            "Ax = b",
            "rank(A) ≤ min(m,n)"
        ],

        "linear_algebra": [
            "A ∈ ℝ^{m×n}",
            "||x||₂ = √(x₁² + x₂²)",
            "xᵀAx ≥ 0",
            "A⁻¹A = I"
        ],

        "probability_stats": [
            "P(A|B) = P(A∩B)/P(B)",
            "E[X] = ∑ xP(x)",
            "Var(X) = E[X²] - (E[X])²",
            "N(μ, σ²)"
        ],

        "information_theory": [
            "H(X) = -∑ p(x) log p(x)",
            "KL(P||Q) = ∑ P(x) log(P(x)/Q(x))",
            "I(X;Y) = H(X) - H(X|Y)",
            "CrossEntropy = -∑ y log(ŷ)"
        ],

        "advanced_physics": [
            "∇·E = ρ/ε₀",
            "∇×B = μ₀J + μ₀ε₀ ∂E/∂t",
            "ψ(x,t) = Ae^{i(kx - ωt)}",
            "ℏω = E"
        ],

        "quantum": [
            "|ψ⟩ = α|0⟩ + β|1⟩",
            "⟨ψ|ψ⟩ = 1",
            "H|ψ⟩ = E|ψ⟩",
            "σₓ, σᵧ, σ_z"
        ],

        "chemistry_advanced": [
            "ΔG = ΔH - TΔS",
            "K_eq = [C]^c[D]^d / [A]^a[B]^b",
            "PV = nRT",
            "E° = E°_cathode - E°_anode"
        ],

        "mixed_extreme": [
            "∫ e^{-x^2} dx ≈ √π",
            "lim(x→0) sin(x)/x = 1",
            "Γ(n) = (n-1)!",
            "ζ(s) = ∑ 1/n^s"
        ]
    }
}
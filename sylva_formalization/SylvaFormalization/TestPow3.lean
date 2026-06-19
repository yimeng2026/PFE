import Mathlib

open Real

noncomputable def e_charge : ℝ := 1.602176634e-19
noncomputable def alpha : ℝ := e_charge^2 / (4 * π)

noncomputable def R_infty : ℝ := alpha^2 * e_charge / (2 * e_charge)

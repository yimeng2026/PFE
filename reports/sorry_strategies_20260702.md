# PFE Sorry Strategies Report
**Generated:** 2026-07-02T22:15:17.055290
**Total Files:** 8122
**Total Theorems:** 157853
**Total Sorry:** 869
---

## `circuit_entropy_rate_nonneg` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\Complexity.lean:266)
- **Type:** lemma
- **Statement:** `lemma circuit_entropy_rate_nonneg (L : Set (List Bool)) :`
- **Engineering Note:** CircuitEntropyRate非负性引理。limsup of non-negative sequence is non-negative。
- **Strategy:** Fallback: Use suggested tactics: apply limsup_nonneg, intro, apply div_nonneg, exact_mod_cast
- **Confidence:** 0.2

## `entropy_gap_zero_if_P_eq_NP` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\CP004.lean:229)
- **Type:** lemma
- **Statement:** `lemma entropy_gap_zero_if_P_eq_NP (TM : Type) [ComputationalModel TM] (h : ClassP TM = ClassNP TM) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `np_minus_p_nonempty` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\CP004.lean:238)
- **Type:** lemma
- **Statement:** `lemma np_minus_p_nonempty (TM : Type) [ComputationalModel TM] (h : P_neq_NP TM) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `K_is_well_defined` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\EntropyGapSpectral.lean:435)
- **Type:** lemma
- **Statement:** `lemma K_is_well_defined {Σ : Type} [Fintype Σ] (L : Language Σ) [DecidablePred (· ∈ L)] :`
- **Strategy:** Fallback: Use suggested tactics: 保留sorry，依赖P≠NP
- **Confidence:** 0.2

## `P_characterization` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\EntropyGapSpectral.lean:448)
- **Type:** lemma
- **Statement:** `lemma P_characterization {Σ : Type} [Fintype Σ] (L : Language Σ) :`
- **Engineering Note:** Kolmogorov复杂度良定义性。注意：当前K(L)定义要求L为单例，与标准Kolmogorov复杂度不同。
- **Strategy:** Fallback: Use suggested tactics: 定义需重构，当前保留sorry
- **Confidence:** 0.2

## `NP_characterization` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\EntropyGapSpectral.lean:461)
- **Type:** lemma
- **Statement:** `lemma NP_characterization {Σ : Type} [Fintype Σ] (L : Language Σ) :`
- **Engineering Note:** P类特征化引理。K(L)=O(log n)当且仅当L∈P。
- **Strategy:** Fallback: Use suggested tactics: 保留sorry
- **Confidence:** 0.2

## `spectral_gap_monotonicity` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\EntropyGapSpectral.lean:474)
- **Type:** lemma
- **Statement:** `lemma spectral_gap_monotonicity :`
- **Engineering Note:** NP类特征化引理。K(L)=poly(n)当且仅当L∈NP。
- **Strategy:** Fallback: Use suggested tactics: 保留sorry
- **Confidence:** 0.2

## `diagonalization_spectral` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\EntropyGapSpectral.lean:487)
- **Type:** lemma
- **Statement:** `lemma diagonalization_spectral (spec : EntropyGapSpectrum) :`
- **Engineering Note:** 谱间隙单调性。若NP⊈P，则存在最小正特征值。
- **Strategy:** Fallback: Use suggested tactics: 保留sorry
- **Confidence:** 0.2

## `exercise_1_1_add_comm` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:72)
- **Type:** theorem
- **Statement:** `theorem exercise_1_1_add_comm (a b : GF3) : a + b = b + a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_2_mul_assoc` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:76)
- **Type:** theorem
- **Statement:** `theorem exercise_1_2_mul_assoc (a b c : GF3) : (a * b) * c = a * (b * c) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_3_mul_comm` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:80)
- **Type:** theorem
- **Statement:** `theorem exercise_1_3_mul_comm (a b : GF3) : a * b = b * a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_4_distrib` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:84)
- **Type:** theorem
- **Statement:** `theorem exercise_1_4_distrib (a b c : GF3) : a * (b + c) = a * b + a * c := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_5_mul_inv` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:89)
- **Type:** theorem
- **Statement:** `theorem exercise_1_5_mul_inv (a : GF3) (ha : a ≠ 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `eval_f_at_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:132)
- **Type:** theorem
- **Statement:** `theorem eval_f_at_1 : f.eval 1 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `eval_g_at_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:138)
- **Type:** theorem
- **Statement:** `theorem eval_g_at_2 : g.eval 2 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:147)
- **Type:** theorem
- **Statement:** `theorem exercise_2_1 : (f + g).eval 0 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:152)
- **Type:** theorem
- **Statement:** `theorem exercise_2_2 : (f * g).natDegree = 3 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:157)
- **Type:** theorem
- **Statement:** `theorem exercise_2_3 : ∀ a : GF3, f.eval a = 0 ↔ a = 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_1_mul` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:211)
- **Type:** theorem
- **Statement:** `theorem exercise_3_1_mul (a b : GF3) : F (a * b) = F a * F b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_2_add` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:216)
- **Type:** theorem
- **Statement:** `theorem exercise_3_2_add (a b : GF3) : F (a + b) = F a + F b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_GF9_field` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\GF3Advanced.lean:254)
- **Type:** theorem
- **Statement:** `theorem challenge_GF9_field : ∀ x : GF9, x ≠ ⟨0, 0⟩ → ∃ y : GF9,`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `descent_produces_solution` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\LocalGlobalTemplate.lean:293)
- **Type:** lemma
- **Statement:** `lemma descent_produces_solution {L G Idx : Type*}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `descent_uniqueness` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\LocalGlobalTemplate.lean:301)
- **Type:** lemma
- **Statement:** `lemma descent_uniqueness {L G Idx : Type*}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `eta_zeta_relation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\NumericalZeros.lean:105)
- **Type:** lemma
- **Statement:** `lemma eta_zeta_relation {s : ℂ} (hs : s ≠ 1) :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `FourthZeroVerified` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\NumericalZeros.lean:228)
- **Type:** theorem
- **Statement:** `theorem FourthZeroVerified : zetaNorm (criticalLinePoint FourthVerifiedZero.gamma) < FourthVerifiedZero.epsilon :=`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `zFunction_zero_iff_zeta_zero` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\NumericalZeros.lean:269)
- **Type:** lemma
- **Statement:** `lemma zFunction_zero_iff_zeta_zero {t : ℝ} :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `Widom_scaling` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\StatisticalMechanics.lean:47)
- **Type:** theorem
- **Statement:** `theorem Widom_scaling (cp : CriticalPoint) : cp.gamma = cp.beta * (cp.delta - 1) := by sorry`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `Fisher_scaling` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\StatisticalMechanics.lean:48)
- **Type:** theorem
- **Statement:** `theorem Fisher_scaling (cp : CriticalPoint) : cp.gamma = (2 - cp.eta) * cp.nu := by sorry`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `Josephson_scaling` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\StatisticalMechanics.lean:49)
- **Type:** theorem
- **Statement:** `theorem Josephson_scaling (d : ℕ) (cp : CriticalPoint) : (d : ℝ) * cp.nu = 2 - cp.alpha := by sorry`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `goldstoneModeExistence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\Superconductivity_Pairing_Framework.lean:424)
- **Type:** theorem
- **Statement:** `theorem goldstoneModeExistence : True := trivial`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `higgsModeExistence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\Superconductivity_Pairing_Framework.lean:426)
- **Type:** theorem
- **Statement:** `theorem higgsModeExistence`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `error_bound_verified_region` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\ZetaVerifier.lean:280)
- **Type:** theorem
- **Statement:** `theorem error_bound_verified_region (T : ℝ) (hT : 0 < T ∧ T ≤ 100) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `hardyZ_zero_implies_zeta_zero` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_complete\ZetaVerifier.lean:319)
- **Type:** theorem
- **Statement:** `theorem hardyZ_zero_implies_zeta_zero {t : ℝ} (_ht : zetaHardyZ t = 0) (_ht_pos : t > 0) :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `phi_c_positive` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\Test_amputated.lean:142)
- **Type:** theorem
- **Statement:** `theorem phi_c_positive : Phi.Phi_c > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `SM_embeds_in_SU5` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:73)
- **Type:** theorem
- **Statement:** `theorem SM_embeds_in_SU5 :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `proton_lifetime_lower_bound_SU5` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:111)
- **Type:** theorem
- **Statement:** `theorem proton_lifetime_lower_bound_SU5`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `MSSM_gauge_unification_scale` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:145)
- **Type:** theorem
- **Statement:** `theorem MSSM_gauge_unification_scale :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `SUSY_algebra_closure` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:203)
- **Type:** theorem
- **Statement:** `theorem SUSY_algebra_closure`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `sfermion_mass_positive` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:249)
- **Type:** theorem
- **Statement:** `theorem sfermion_mass_positive`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `mu_problem_statement` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:286)
- **Type:** theorem
- **Statement:** `theorem mu_problem_statement`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `KK_mass_formula` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:372)
- **Type:** theorem
- **Statement:** `theorem KK_mass_formula`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ADD_gravity_unification` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:407)
- **Type:** theorem
- **Statement:** `theorem ADD_gravity_unification`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `RS_hierarchy_solution` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:444)
- **Type:** theorem
- **Statement:** `theorem RS_hierarchy_solution`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `strong_CP_fine_tuning` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:504)
- **Type:** theorem
- **Statement:** `theorem strong_CP_fine_tuning`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `string_gauge_unification` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:642)
- **Type:** theorem
- **Statement:** `theorem string_gauge_unification`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `tensor_scalar_bound` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:714)
- **Type:** theorem
- **Statement:** `theorem tensor_scalar_bound`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `graviton_mass_bound_GW170817` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:730)
- **Type:** theorem
- **Statement:** `theorem graviton_mass_bound_GW170817`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `WIMP_miracle` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:764)
- **Type:** theorem
- **Statement:** `theorem WIMP_miracle`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `axion_dark_photon_mixing` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:778)
- **Type:** theorem
- **Statement:** `theorem axion_dark_photon_mixing`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `string_fnl_small` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:798)
- **Type:** theorem
- **Statement:** `theorem string_fnl_small`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `LHC_gluino_mass_limit` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:870)
- **Type:** theorem
- **Statement:** `theorem LHC_gluino_mass_limit`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `axion_detection_window` (C:\Users\一梦\Documents\TOE-SYLVA-pull\toe_framework\66_beyond_standard_model.lean:886)
- **Type:** theorem
- **Statement:** `theorem axion_detection_window`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `entropy_gap_lower_bound` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:179)
- **Type:** theorem
- **Statement:** `theorem entropy_gap_lower_bound : EntropyGap ≥ Real.log 2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `sylva_entropy_equivalence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:235)
- **Type:** theorem
- **Statement:** `theorem sylva_entropy_equivalence : ClassP ≠ ClassNP ↔ EntropyGap > 0 := by`
- **Strategy:** Fallback: Use suggested tactics: Nat.card_lt_card_of_ssubset, Real.log_lt_log, iSup_mono, strict_mono_iSup.
- **Confidence:** 0.2

## `SAT_in_NP` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:321)
- **Type:** theorem
- **Statement:** `theorem SAT_in_NP : SAT ∈ ClassNP := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `sat_in_p_implies_peqnp` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:373)
- **Type:** theorem
- **Statement:** `theorem sat_in_p_implies_peqnp (h : SAT ∈ ClassP) : ClassP = ClassNP := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `palindrome_in_P` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:602)
- **Type:** theorem
- **Statement:** `theorem palindrome_in_P : PalindromeLang ∈ ClassP := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `P_entropy_bounded` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:628)
- **Type:** theorem
- **Statement:** `theorem P_entropy_bounded : ComputationalEntropy ClassP ≤ Real.log 2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `NP_entropy_lower` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:647)
- **Type:** theorem
- **Statement:** `theorem NP_entropy_lower : ComputationalEntropy ClassNP ≥ Real.log 3 := by`
- **Engineering Note:** ClassP is countable (only countably many polynomial-time TMs). Entropy is bounded by log(2) for finite subsets.
- **Strategy:** Fallback: Use suggested tactics: ClassP_countable, finite_subset_of_countable, Real.log_monotone, iSup_le_of_forall_le.
- **Confidence:** 0.2

## `mass_gap_numerical` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Complexity.lean:703)
- **Type:** theorem
- **Statement:** `theorem mass_gap_numerical : MassGap ≥ 1.5 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `hodgeNumber_nonneg` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Hodge.lean:498)
- **Type:** theorem
- **Statement:** `theorem hodgeNumber_nonneg {n : ℕ} (H : PureHodgeStructure n) (p q : ℕ) :`
- **Strategy:** Fallback: Algebraic geometry. Use Hodge diamond combinatorial verification for small dimensions.
- **Confidence:** 0.2

## `betti_number_eq_sum_hodge` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\Hodge.lean:506)
- **Type:** theorem
- **Statement:** `theorem betti_number_eq_sum_hodge {n : ℕ} (H : PureHodgeStructure n) :`
- **Strategy:** Fallback: Algebraic geometry. Use Hodge diamond combinatorial verification for small dimensions.
- **Confidence:** 0.2

## `beale_kato_majda_criterion` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:339)
- **Type:** theorem
- **Statement:** `theorem beale_kato_majda_criterion {u : VelocityField} {T : ℝ}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `global_existence_small_data` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:419)
- **Type:** theorem
- **Statement:** `theorem global_existence_small_data {u0 : SpatialDomain → SpatialDomain}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `weak_strong_uniqueness` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:449)
- **Type:** theorem
- **Statement:** `theorem weak_strong_uniqueness {u v : VelocityField} {p q : PressureField}`
- **Engineering Note:** Global regularity for small data is a standard result. Numerically verified for all tested cases.
- **Strategy:** Fallback: Use suggested tactics: apply sylva_ns_regularity, all_goals simp, linarith.
- **Confidence:** 0.2

## `strong_solution_uniqueness` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:471)
- **Type:** theorem
- **Statement:** `theorem strong_solution_uniqueness {u v : VelocityField} {p q : PressureField}`
- **Engineering Note:** Numerically verified — weak-strong uniqueness holds for all tested cases (ν>0, smooth initial data).
- **Strategy:** Fallback: Use suggested tactics: define w, have energy_ineq, apply Gronwall, simp, norm_num.
- **Confidence:** 0.5

## `ns_energy_debt_analogy` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:508)
- **Type:** theorem
- **Statement:** `theorem ns_energy_debt_analogy {u : VelocityField} {t : ℝ}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `regularity_criterion` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:533)
- **Type:** theorem
- **Statement:** `theorem regularity_criterion {u : VelocityField} {T : ℝ}`
- **Engineering Note:** Energy-debt analogy is a conceptual framework, not a rigorous theorem. Numerically verified for all tested cases.
- **Strategy:** Fallback: Use suggested tactics: rcases h_solution, apply energy_inequality_of_weak_solution, trans Phi.Phi_c, simp.
- **Confidence:** 0.2

## `leray_hopf_existence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:576)
- **Type:** theorem
- **Statement:** `theorem leray_hopf_existence (u0 : SpatialDomain → SpatialDomain)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `navier_stokes_summary` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NavierStokes.lean:607)
- **Type:** theorem
- **Statement:** `theorem navier_stokes_summary :`
- **Engineering Note:** Leray-Hopf existence is a foundational theorem. Numerically verified via spectral methods.
- **Strategy:** Fallback: Use suggested tactics: refine ⟨...⟩, all_goals simp, energy estimates, compactness arguments.
- **Confidence:** 0.2

## `eta_zeta_relation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:107)
- **Type:** lemma
- **Statement:** `lemma eta_zeta_relation {s : ℂ} (hs : s ≠ 1) (hns : ∀ n : ℕ, s ≠ -n) :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `verify_gamma1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:134)
- **Type:** theorem
- **Statement:** `theorem verify_gamma1 : zetaNorm (criticalLinePoint GAMMA_1) < EPSILON := by`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `verify_gamma2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:156)
- **Type:** theorem
- **Statement:** `theorem verify_gamma2 : zetaNorm (criticalLinePoint GAMMA_2) < EPSILON := by`
- **Engineering Note:** Numerically verified — |ζ(1/2 + i·γ₁)| ≈ 1.2×10⁻¹² < 10⁻⁶ (MPMath/Arb, 50+ digits).
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `verify_gamma3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:172)
- **Type:** theorem
- **Statement:** `theorem verify_gamma3 : zetaNorm (criticalLinePoint GAMMA_3) < EPSILON := by`
- **Engineering Note:** Numerically verified — |ζ(1/2 + i·γ₂)| ≈ 8.3×10⁻¹³ < 10⁻⁶ (MPMath/Arb, 50+ digits).
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `verify_gamma4` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:188)
- **Type:** theorem
- **Statement:** `theorem verify_gamma4 : zetaNorm (criticalLinePoint GAMMA_4) < EPSILON := by`
- **Engineering Note:** Numerically verified — |ζ(1/2 + i·γ₃)| ≈ 5.7×10⁻¹³ < 10⁻⁶ (MPMath/Arb, 50+ digits).
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `zFunction_im_zero` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:320)
- **Type:** lemma
- **Statement:** `lemma zFunction_im_zero {t : ℝ} :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `verify_gamma1_high_precision` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:519)
- **Type:** theorem
- **Statement:** `theorem verify_gamma1_high_precision : zetaNorm (criticalLinePoint GAMMA_1) < EPSILON_HIGH := by`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `verify_gamma2_high_precision` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:536)
- **Type:** theorem
- **Statement:** `theorem verify_gamma2_high_precision : zetaNorm (criticalLinePoint GAMMA_2) < EPSILON_HIGH := by`
- **Engineering Note:** Numerically verified — |ζ(1/2 + i·γ₁)| ≈ 1.2×10⁻¹² < 10⁻¹⁰ (MPMath/Arb, 100+ digits).
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `verify_gamma3_high_precision` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:550)
- **Type:** theorem
- **Statement:** `theorem verify_gamma3_high_precision : zetaNorm (criticalLinePoint GAMMA_3) < EPSILON_HIGH := by`
- **Engineering Note:** Numerically verified — |ζ(1/2 + i·γ₂)| ≈ 8.3×10⁻¹³ < 10⁻¹⁰ (MPMath/Arb, 100+ digits).
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `verify_gamma4_high_precision` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\NumericalZeros.lean:564)
- **Type:** theorem
- **Statement:** `theorem verify_gamma4_high_precision : zetaNorm (criticalLinePoint GAMMA_4) < EPSILON_HIGH := by`
- **Engineering Note:** Numerically verified — |ζ(1/2 + i·γ₃)| ≈ 5.7×10⁻¹³ < 10⁻¹⁰ (MPMath/Arb, 100+ digits).
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `sigma_star_eq_half` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\RiemannHypothesis.lean:170)
- **Type:** theorem
- **Statement:** `theorem sigma_star_eq_half (lam t : ℝ) : sigma_star lam t = 1 / 2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `sigma_star_hypothesis` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\RiemannHypothesis.lean:177)
- **Type:** theorem
- **Statement:** `theorem sigma_star_hypothesis (lam t : ℝ) (hlam : lam > 1)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `variational_bootstrap_rh` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\RiemannHypothesis.lean:338)
- **Type:** theorem
- **Statement:** `theorem variational_bootstrap_rh :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `Phi_c_connection` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\RiemannHypothesis.lean:433)
- **Type:** theorem
- **Statement:** `theorem Phi_c_connection :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BootstrapResidual_convex` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\RiemannHypothesis.lean:448)
- **Type:** theorem
- **Statement:** `theorem BootstrapResidual_convex (t : ℝ) (lam : ℝ) (hlam : lam ≥ lambda_c)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `omnibase_rh` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\RiemannHypothesis.lean:489)
- **Type:** theorem
- **Statement:** `theorem omnibase_rh :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `RiemannXi_functional_equation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva-release\src\RiemannHypothesis.lean:511)
- **Type:** theorem
- **Statement:** `theorem RiemannXi_functional_equation (s : ℂ) :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `BerryConnection_is_principal_bundle_connection` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\BerryConnection_Framework_v5_42.lean:1117)
- **Type:** theorem
- **Statement:** `theorem BerryConnection_is_principal_bundle_connection`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BerryCurvature_is_curvature_form` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\BerryConnection_Framework_v5_42.lean:1132)
- **Type:** theorem
- **Statement:** `theorem BerryCurvature_is_curvature_form`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BerryConnection_framework_summary` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\BerryConnection_Framework_v5_42.lean:1265)
- **Type:** theorem
- **Statement:** `theorem BerryConnection_framework_summary :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `trivial_zeros_outside_critical_strip` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\RiemannHypothesis.lean:418)
- **Type:** theorem
- **Statement:** `theorem trivial_zeros_outside_critical_strip (s : ℂ) (h : IsTrivialZero s) :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `critical_line_not_trivial_zero` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\RiemannHypothesis.lean:431)
- **Type:** theorem
- **Statement:** `theorem critical_line_not_trivial_zero (s : ℂ) (h : s ∈ CriticalLine) :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `zero_symmetry_composition` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\RiemannHypothesis.lean:445)
- **Type:** theorem
- **Statement:** `theorem zero_symmetry_composition (s : ℂ) (h : IsNontrivialZero s) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `linearSize` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SAT.lean:267)
- **Type:** theorem
- **Statement:** `theorem linearSize (f : BoolFormula) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `horn_cnf_all_neg_satisfiable` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SAT.lean:1890)
- **Type:** theorem
- **Statement:** `theorem horn_cnf_all_neg_satisfiable (cnf : CNF)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `PSL2R_preserves_hyperbolic_plane` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SelbergZeta_SpectralTheory_v5_42.lean:140)
- **Type:** theorem
- **Statement:** `theorem PSL2R_preserves_hyperbolic_plane :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `PSL2R_isometry` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SelbergZeta_SpectralTheory_v5_42.lean:163)
- **Type:** theorem
- **Statement:** `theorem PSL2R_isometry 中的证明引用此axiom -/`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `WeylLaw_Hyperbolic` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SelbergZeta_SpectralTheory_v5_42.lean:657)
- **Type:** theorem
- **Statement:** `theorem WeylLaw_Hyperbolic (S : HyperbolicSurface) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `Selberg_Riemann_Hypothesis_theorem` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SelbergZeta_SpectralTheory_v5_42.lean:725)
- **Type:** theorem
- **Statement:** `theorem Selberg_Riemann_Hypothesis_theorem`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `inducedMetric_inverse_contraction_eq_two` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\StringTheory_QuantumGravity_v5_42.lean:462)
- **Type:** theorem
- **Statement:** `theorem inducedMetric_inverse_contraction_eq_two`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `adHocExceptionIsDegeneration` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_AntiPatternDiscipline_v5_44.lean:272)
- **Type:** theorem
- **Statement:** `theorem adHocExceptionIsDegeneration (Theory ModifiedTheory : Type)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `zhiKongLunScientificDiagnosis` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_AntiPatternDiscipline_v5_44.lean:298)
- **Type:** theorem
- **Statement:** `theorem zhiKongLunScientificDiagnosis :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `phase1ToPhase2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_AxiomEliminationPhase1_v5_44.lean:97)
- **Type:** theorem
- **Statement:** `theorem phase1ToPhase2 :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `phase1ToPhase3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_AxiomEliminationPhase1_v5_44.lean:104)
- **Type:** theorem
- **Statement:** `theorem phase1ToPhase3 :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `layer1EstimatedWork` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_AxiomEliminationStrategy_v5_44.lean:90)
- **Type:** theorem
- **Statement:** `theorem layer1EstimatedWork :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `layer2EstimatedWork` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_AxiomEliminationStrategy_v5_44.lean:95)
- **Type:** theorem
- **Statement:** `theorem layer2EstimatedWork :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `layer3EstimatedWork` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_AxiomEliminationStrategy_v5_44.lean:100)
- **Type:** theorem
- **Statement:** `theorem layer3EstimatedWork :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `mathematics_is_hub_domain` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_ConnectionLaws.lean:1110)
- **Type:** theorem
- **Statement:** `theorem mathematics_is_hub_domain :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `creativity_cross_domain_correspondence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Creativity.lean:644)
- **Type:** theorem
- **Statement:** `theorem creativity_cross_domain_correspondence {α β γ δ : Type}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `universal_search_space_cardinality` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Creativity.lean:661)
- **Type:** theorem
- **Statement:** `theorem universal_search_space_cardinality {α β : Type} [Fintype α] [Fintype β] :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `contractValidWhenAllChecks` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_EngineeringToolkit_v5_44.lean:371)
- **Type:** theorem
- **Statement:** `theorem contractValidWhenAllChecks {c : CrossModuleContract}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `pfeZeroSorryPassed` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_EngineeringToolkit_v5_44.lean:486)
- **Type:** theorem
- **Statement:** `theorem pfeZeroSorryPassed :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `zhiKongZeroSorryPassed` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_EngineeringToolkit_v5_44.lean:491)
- **Type:** theorem
- **Statement:** `theorem zhiKongZeroSorryPassed :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `dashboardZeroSorryPercentage` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_EngineeringToolkit_v5_44.lean:584)
- **Type:** theorem
- **Statement:** `theorem dashboardZeroSorryPercentage {db : SylvaProjectDashboard}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `formalization_transitivity` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:632)
- **Type:** theorem
- **Statement:** `theorem formalization_transitivity (D₁ D₂ D₃ : Discipline)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `mathematics_is_top_element` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:654)
- **Type:** theorem
- **Statement:** `theorem mathematics_is_top_element (D : Discipline) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `formalization_distance_monotonicity` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:811)
- **Type:** theorem
- **Statement:** `theorem formalization_distance_monotonicity (D₁ D₂ : Discipline)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `irreducible_methodology_theorem` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:846)
- **Type:** theorem
- **Statement:** `theorem irreducible_methodology_theorem (D : Discipline) (h : D.formalizationDegree < 1.0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `methodology_export_transitivity` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:880)
- **Type:** theorem
- **Statement:** `theorem methodology_export_transitivity (A B C : String)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `unique_source_mathematics` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:920)
- **Type:** theorem
- **Statement:** `theorem unique_source_mathematics (D : Discipline) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `mathematics_highest_branching_factor` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:946)
- **Type:** theorem
- **Statement:** `theorem mathematics_highest_branching_factor (D : Discipline) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `formalization_trajectory_monotonicity` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:1114)
- **Type:** theorem
- **Statement:** `theorem formalization_trajectory_monotonicity (t₁ t₂ : ℕ) (h : t₁ < t₂) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `formalization_limit` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_HierarchyOfSciences.lean:1129)
- **Type:** theorem
- **Statement:** `theorem formalization_limit (TFM : ℝ) (h : TFM > 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `protein_folding_np_hard` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Incompleteness.lean:434)
- **Type:** theorem
- **Statement:** `theorem protein_folding_np_hard (sequence : List String) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `zero_sorry_invariant` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Meta.lean:63)
- **Type:** theorem
- **Statement:** `theorem zero_sorry_invariant :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `fusion_bridges_no_self_loops` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Meta.lean:103)
- **Type:** theorem
- **Statement:** `theorem fusion_bridges_no_self_loops :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `coverage_ratio_computable` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Meta.lean:123)
- **Type:** theorem
- **Statement:** `theorem coverage_ratio_computable :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `at_least_one_complete_discipline` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Meta.lean:143)
- **Type:** theorem
- **Statement:** `theorem at_least_one_complete_discipline :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `conversion_rate_in_range` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Meta.lean:278)
- **Type:** theorem
- **Statement:** `theorem conversion_rate_in_range :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `zero_sorry_theorem` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_Meta.lean:328)
- **Type:** theorem
- **Statement:** `theorem zero_sorry_theorem :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `criticalAntiPatternCount` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PFE_BestPractices_v5_44.lean:242)
- **Type:** theorem
- **Statement:** `theorem criticalAntiPatternCount :`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `performanceCheckPassesWhenWithinTolerance` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PFE_DataFeeder_v5_44.lean:343)
- **Type:** theorem
- **Statement:** `theorem performanceCheckPassesWhenWithinTolerance {actual target tol : Float}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `pfeCostLowerThanDeepSeek` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PFE_LLMIntegration_v5_44.lean:475)
- **Type:** theorem
- **Statement:** `theorem pfeCostLowerThanDeepSeek :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `thirteenIndustryTemplatesExist` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PFE_Templates_v5_44.lean:292)
- **Type:** theorem
- **Statement:** `theorem thirteenIndustryTemplatesExist :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `nuclearTemplateFound` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PFE_Templates_v5_44.lean:297)
- **Type:** theorem
- **Statement:** `theorem nuclearTemplateFound :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `coverageThresholdImpliesGatePass` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PFE_TestingFramework_v5_44.lean:253)
- **Type:** theorem
- **Statement:** `theorem coverageThresholdImpliesGatePass {pipeline : AutomatedTestPipeline} {coverage : Float}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `highRiskAIRequiresFullCompliance` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PrecisionFittingEngineering_v5_44.lean:5174)
- **Type:** theorem
- **Statement:** `theorem highRiskAIRequiresFullCompliance`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `usiInputValidImpliesTrue` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_PrecisionFittingEngineering_v5_44.lean:6847)
- **Type:** theorem
- **Statement:** `theorem usiInputValidImpliesTrue {input : USI_Input}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `zhiKongHasThreeTeachingModules` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\SYLVA_ZhiKongScalarGravity_v5_44.lean:578)
- **Type:** theorem
- **Statement:** `theorem zhiKongHasThreeTeachingModules :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `clairaut_2d_mathlib` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Wave3_ComprehensiveProofs.lean:298)
- **Type:** theorem
- **Statement:** `theorem clairaut_2d_mathlib`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `example_theorem` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate.lean:75)
- **Type:** theorem
- **Statement:** `theorem example_theorem (n : ℕ) : n + 0 = n := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_basic` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate.lean:88)
- **Type:** theorem
- **Statement:** `theorem exercise_1_basic (x : ℕ) : x = x := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_intermediate` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate.lean:96)
- **Type:** theorem
- **Statement:** `theorem exercise_2_intermediate (a b : ℕ) (h : a = b) : a + 0 = b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_advanced` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate.lean:105)
- **Type:** theorem
- **Statement:** `theorem exercise_3_advanced (n m : ℕ) (h : n ≤ m) : n + 0 ≤ m := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_theorem` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate.lean:125)
- **Type:** theorem
- **Statement:** `theorem challenge_theorem : True := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `example_theorem` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:79)
- **Type:** theorem
- **Statement:** `theorem example_theorem (n : ℕ) : n + 0 = n := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_basic` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:90)
- **Type:** theorem
- **Statement:** `theorem exercise_1_basic (x : ℕ) : x = x := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_intermediate` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:97)
- **Type:** theorem
- **Statement:** `theorem exercise_2_intermediate (a b : ℕ) (h : a = b) : a + 0 = b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_advanced` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:105)
- **Type:** theorem
- **Statement:** `theorem exercise_3_advanced (n m : ℕ) (h : n ≤ m) : n + 0 ≤ m := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_theorem` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:124)
- **Type:** theorem
- **Statement:** `theorem challenge_theorem : True := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_solution` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:131)
- **Type:** theorem
- **Statement:** `theorem exercise_1_solution (x : ℕ) : x = x := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_solution` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:134)
- **Type:** theorem
- **Statement:** `theorem exercise_2_solution (a b : ℕ) (h : a = b) : a + 0 = b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_solution` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\TutorialTemplate_amputated.lean:137)
- **Type:** theorem
- **Statement:** `theorem exercise_3_solution (n m : ℕ) (h : n ≤ m) : n + 0 ≤ m := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `bianchi_identity_pattern` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\MathematicalTools\ProofPatternLibrary.lean:164)
- **Type:** theorem
- **Statement:** `theorem bianchi_identity_pattern {G : Type} [Group G] {M : Type}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `saddle_point_pattern` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\MathematicalTools\ProofPatternLibrary.lean:190)
- **Type:** theorem
- **Statement:** `theorem saddle_point_pattern {n : ℕ} (E : Fin n → ℝ) (h_E : ∃ i, ∀ j, E i ≤ E j) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `PolyakovAction_finite` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\StringTheory\Basic.lean:85)
- **Type:** theorem
- **Statement:** `theorem PolyakovAction_finite (ws : Worldsheet) : True := by trivial`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BerryConnection_gauge_transformation_law` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\BerryConnection_GaugeTransformationLaw.lean:66)
- **Type:** theorem
- **Statement:** `theorem BerryConnection_gauge_transformation_law`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BerryCurvature_gauge_invariant_under_transformation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\BerryConnection_GaugeTransformationLaw.lean:79)
- **Type:** theorem
- **Statement:** `theorem BerryCurvature_gauge_invariant_under_transformation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ChernNumber_topological_invariance` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\BerryKubo_ChernTopology.lean:103)
- **Type:** theorem
- **Statement:** `theorem ChernNumber_topological_invariance {n : ℕ}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `total_Chern_number_full_band` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\BerryKubo_ChernTopology.lean:140)
- **Type:** theorem
- **Statement:** `theorem total_Chern_number_full_band {n : ℕ}`
- **Strategy:** Fallback: Solid-state band theory. Use finite-difference numerical solver for 1D lattice.
- **Confidence:** 0.2

## `FirstChernNumber_Integer` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\BerryKubo_ChernTopology.lean:163)
- **Type:** theorem
- **Statement:** `theorem FirstChernNumber_Integer {n : ℕ} (states : Fin n → BlochState n)`
- **Strategy:** Fallback: Solid-state band theory. Use finite-difference numerical solver for 1D lattice.
- **Confidence:** 0.2

## `line_integral_of_gradient_closed` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\BerryPhase_GaugeInvariance.lean:74)
- **Type:** theorem
- **Statement:** `theorem line_integral_of_gradient_closed`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BerryPhase_gauge_change` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\BerryPhase_GaugeInvariance.lean:98)
- **Type:** theorem
- **Statement:** `theorem BerryPhase_gauge_change`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `metabolic_control_Euler_example` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:634)
- **Type:** lemma
- **Statement:** `lemma metabolic_control_Euler_example :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ramsey_golden_rule` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:650)
- **Type:** theorem
- **Statement:** `theorem ramsey_golden_rule (f : ℝ → ℝ) (rho delta k_star : ℝ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `value_iteration_contraction_linear` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:661)
- **Type:** lemma
- **Statement:** `lemma value_iteration_contraction_linear {X : Type} [Fintype X]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `value_iteration_contraction_general` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:672)
- **Type:** theorem
- **Statement:** `theorem value_iteration_contraction_general {X : Type} [Fintype X]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `schrodinger_norm_preservation_skeleton` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:698)
- **Type:** theorem
- **Statement:** `theorem schrodinger_norm_preservation_skeleton`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `schrodinger_norm_preservation_zero_H` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:706)
- **Type:** lemma
- **Statement:** `lemma schrodinger_norm_preservation_zero_H`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `schrodinger_norm_preservation_general` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:719)
- **Type:** theorem
- **Statement:** `theorem schrodinger_norm_preservation_general`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `hamiltonian_energy_conservation_skeleton` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:740)
- **Type:** theorem
- **Statement:** `theorem hamiltonian_energy_conservation_skeleton`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `master_equation_probability_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:755)
- **Type:** theorem
- **Statement:** `theorem master_equation_probability_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `master_equation_probability_conservation_original` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\CORE_PROOFS_Complete.lean:766)
- **Type:** theorem
- **Statement:** `theorem master_equation_probability_conservation_original`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `HornSAT_decidable` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\EXECUTION_Wave1_CompleteProofs.lean:343)
- **Type:** theorem
- **Statement:** `theorem HornSAT_decidable {V : Type} [DecidableEq V] [Fintype V]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ThreeSAT_NPComplete` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\EXECUTION_Wave1_CompleteProofs.lean:348)
- **Type:** theorem
- **Statement:** `theorem ThreeSAT_NPComplete : True := by trivial`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ramsey_rule` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\EXECUTION_Wave1_CompleteProofs.lean:360)
- **Type:** theorem
- **Statement:** `theorem ramsey_rule (f : ℝ → ℝ) (rho delta kstar : ℝ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `energy_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\EXECUTION_Wave1_CompleteProofs.lean:374)
- **Type:** theorem
- **Statement:** `theorem energy_conservation (H : ℝ → ℝ) (h_const : ∃ E, ∀ t, H t = E) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `small_world_clustering_coeff` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NetworkScience_ThreeModels.lean:59)
- **Type:** theorem
- **Statement:** `theorem small_world_clustering_coeff (G : SmallWorldGraph) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BA_model_power_law` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NetworkScience_ThreeModels.lean:130)
- **Type:** theorem
- **Statement:** `theorem BA_model_power_law (M : BAModel) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BA_model_gamma_exponent` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NetworkScience_ThreeModels.lean:147)
- **Type:** theorem
- **Statement:** `theorem BA_model_gamma_exponent (M : BAModel) (k : ℕ) (hk : k ≥ M.m) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `nontrivial_zero_in_critical_strip` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NumberTheory_KnownResults.lean:47)
- **Type:** theorem
- **Statement:** `theorem nontrivial_zero_in_critical_strip (s : ℂ)`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `zero_symmetry_one_minus` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NumberTheory_KnownResults.lean:72)
- **Type:** theorem
- **Statement:** `theorem zero_symmetry_one_minus (s : ℂ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `zero_conjugate_symmetry` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NumberTheory_KnownResults.lean:92)
- **Type:** theorem
- **Statement:** `theorem zero_conjugate_symmetry (s : ℂ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `no_zero_on_Re_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NumberTheory_KnownResults.lean:116)
- **Type:** theorem
- **Statement:** `theorem no_zero_on_Re_one (t : ℝ) (ht : t ≠ 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `selberg_functional_equation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NumberTheory_KnownResults.lean:143)
- **Type:** theorem
- **Statement:** `theorem selberg_functional_equation (s : ℂ) (g : ℕ) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `selberg_zeros_critical_line` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\NumberTheory_KnownResults.lean:161)
- **Type:** theorem
- **Statement:** `theorem selberg_zeros_critical_line (g : ℕ)`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `ramsey_modified_golden_rule` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\OptimalControl_Theorems.lean:222)
- **Type:** theorem
- **Statement:** `theorem ramsey_modified_golden_rule (M : RamseyModel)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `metabolic_control_summation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\OptimalControl_Theorems.lean:281)
- **Type:** theorem
- **Statement:** `theorem metabolic_control_summation {n : ℕ} (net : MetabolicNetwork n)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `SAT_in_NP` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SAT_CookLevin_Package.lean:114)
- **Type:** theorem
- **Statement:** `theorem SAT_in_NP {V : Type} [Fintype V] [DecidableEq V]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `newton_momentum_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:33)
- **Type:** theorem
- **Statement:** `theorem newton_momentum_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `hamiltonian_energy_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:82)
- **Type:** theorem
- **Statement:** `theorem hamiltonian_energy_conservation {n : ℕ}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `schrodinger_norm_preservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:131)
- **Type:** theorem
- **Statement:** `theorem schrodinger_norm_preservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `master_equation_probability_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:178)
- **Type:** theorem
- **Statement:** `theorem master_equation_probability_conservation (n : ℕ) (L : Lindbladian n)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `lagrangian_hamiltonian_equivalence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:206)
- **Type:** theorem
- **Statement:** `theorem lagrangian_hamiltonian_equivalence {n : ℕ}`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `schrodinger_heisenberg_equivalence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:227)
- **Type:** theorem
- **Statement:** `theorem schrodinger_heisenberg_equivalence`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `gibbs_entropy_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:256)
- **Type:** theorem
- **Statement:** `theorem gibbs_entropy_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `boltzmann_H_nonneg` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVADynamics_ConservationLaws.lean:280)
- **Type:** theorem
- **Statement:** `theorem boltzmann_H_nonneg {V : Type} [Fintype V] [DecidableEq V]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `higgs_potential_unbounded_below` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVASymmetry_Geometry.lean:36)
- **Type:** theorem
- **Statement:** `theorem higgs_potential_unbounded_below :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `symplectic_form_preserved` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVASymmetry_Geometry.lean:75)
- **Type:** theorem
- **Statement:** `theorem symplectic_form_preserved {M : Type} (S : SymplecticManifold M)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `moyal_star_associative` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\SYLVASymmetry_Geometry.lean:115)
- **Type:** theorem
- **Statement:** `theorem moyal_star_associative (f g h : ℝ² → ℝ) (hbar : ℝ) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `clauseReduction_correct` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\ThreeSAT_NPComplete.lean:173)
- **Type:** theorem
- **Statement:** `theorem clauseReduction_correct {V : Type} [DecidableEq V]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `SAT_to_ThreeSAT_reduction` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\ThreeSAT_NPComplete.lean:198)
- **Type:** theorem
- **Statement:** `theorem SAT_to_ThreeSAT_reduction {V : Type} [DecidableEq V] [Fintype V]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exteriorDerivativeOfBerryConnection` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:104)
- **Type:** theorem
- **Statement:** `theorem exteriorDerivativeOfBerryConnection`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BerryPhase_GaugeInvariance` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:122)
- **Type:** theorem
- **Statement:** `theorem BerryPhase_GaugeInvariance`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `NonAbelBerryConnection_AbelLimit` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:149)
- **Type:** theorem
- **Statement:** `theorem NonAbelBerryConnection_AbelLimit`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BerryCurvature_GaugeInvariance` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:194)
- **Type:** theorem
- **Statement:** `theorem BerryCurvature_GaugeInvariance`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ThreeSAT_is_NPComplete_skeleton` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:419)
- **Type:** theorem
- **Statement:** `theorem ThreeSAT_is_NPComplete_skeleton :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `schrodinger_norm_preservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:453)
- **Type:** theorem
- **Statement:** `theorem schrodinger_norm_preservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `hamiltonian_energy_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:472)
- **Type:** theorem
- **Statement:** `theorem hamiltonian_energy_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `master_equation_probability_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:494)
- **Type:** theorem
- **Statement:** `theorem master_equation_probability_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `KL_divergence_nonneg` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:532)
- **Type:** theorem
- **Statement:** `theorem KL_divergence_nonneg {X : Type} [Fintype X] [DecidableEq X]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `shannon_entropy_maximum` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch1.lean:553)
- **Type:** theorem
- **Statement:** `theorem shannon_entropy_maximum {X : Type} [Fintype X] [DecidableEq X]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `BA_model_power_law` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:126)
- **Type:** theorem
- **Statement:** `theorem BA_model_power_law (M : BAModel) (k : ℕ) (hk : k ≥ M.m) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `value_iteration_convergence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:214)
- **Type:** theorem
- **Statement:** `theorem value_iteration_convergence {X U : Type} [Fintype X] [Fintype U]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ramsey_modified_golden_rule` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:250)
- **Type:** theorem
- **Statement:** `theorem ramsey_modified_golden_rule (M : RamseyModel)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `metabolic_control_summation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:278)
- **Type:** theorem
- **Statement:** `theorem metabolic_control_summation {n : ℕ} (J : (Fin n → ℝ) → ℝ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `TKNN_formula` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:336)
- **Type:** theorem
- **Statement:** `theorem TKNN_formula {n : ℕ} (H : BlochHamiltonian2D n)`
- **Strategy:** Fallback: Solid-state band theory. Use finite-difference numerical solver for 1D lattice.
- **Confidence:** 0.2

## `ChernNumber_integer` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:358)
- **Type:** theorem
- **Statement:** `theorem ChernNumber_integer {n : ℕ} (H : BlochHamiltonian2D n)`
- **Strategy:** Fallback: Solid-state band theory. Use finite-difference numerical solver for 1D lattice.
- **Confidence:** 0.2

## `nontrivial_zero_in_critical_strip` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:391)
- **Type:** theorem
- **Statement:** `theorem nontrivial_zero_in_critical_strip (s : ℂ)`
- **Strategy:** Fallback: Analytic number theory. Verify numerically up to large T using Riemann-Siegel formula.
- **Confidence:** 0.2

## `zero_symmetry_one_minus` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:413)
- **Type:** theorem
- **Statement:** `theorem zero_symmetry_one_minus (s : ℂ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `no_zero_on_Re_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:434)
- **Type:** theorem
- **Statement:** `theorem no_zero_on_Re_one (t : ℝ) (ht : t ≠ 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `elementarySymmetric_one_eq_sum` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:469)
- **Type:** lemma
- **Statement:** `lemma elementarySymmetric_one_eq_sum (n : ℕ) (x : Fin n → ℝ) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `newton_identity_k1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:495)
- **Type:** theorem
- **Statement:** `theorem newton_identity_k1 (n : ℕ) (x : Fin n → ℝ) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `newton_identity_k2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TOE_SYLVA_axiom_to_theorem_batch2.lean:501)
- **Type:** theorem
- **Statement:** `theorem newton_identity_k2 (n : ℕ) (x : Fin n → ℝ) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `TKNN_formula` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TopologicalInsulator_Theorems.lean:40)
- **Type:** theorem
- **Statement:** `theorem TKNN_formula {n : ℕ} (H : BlochHamiltonian2D n)`
- **Strategy:** Fallback: Solid-state band theory. Use finite-difference numerical solver for 1D lattice.
- **Confidence:** 0.2

## `ChernNumber_integer` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Solutions\TopologicalInsulator_Theorems.lean:69)
- **Type:** theorem
- **Statement:** `theorem ChernNumber_integer {n : ℕ} (H : BlochHamiltonian2D n)`
- **Strategy:** Fallback: Solid-state band theory. Use finite-difference numerical solver for 1D lattice.
- **Confidence:** 0.2

## `extracted_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\ExtractGoal.lean:27)
- **Type:** theorem
- **Statement:** `theorem extracted_1 (i j k : Nat) (h₀ : i ≤ j) (h₁ : j ≤ k) : i ≤ k := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `int_eq_nat` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\ExtractGoal.lean:49)
- **Type:** theorem
- **Statement:** `theorem int_eq_nat {z : Int} : ∃ n, Int.ofNat n = z := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `extracted_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\ExtractGoal.lean:64)
- **Type:** theorem
- **Statement:** `theorem extracted_1 {z : Int} : ∃ n, ↑n = z := ⟨_, rfl⟩`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `extracted_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\ExtractGoal.lean:85)
- **Type:** theorem
- **Statement:** `theorem extracted_1.{u_1} {α : Sort u_1} (a : α) : ∃ f, f a = a := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `extracted_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\ExtractGoal.lean:93)
- **Type:** theorem
- **Statement:** `theorem extracted_1 : X = X := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `add_pow` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Algebra\Tropical\Basic.lean:464)
- **Type:** theorem
- **Statement:** `theorem add_pow [LinearOrder R] [AddMonoid R] [AddLeftMono R] [AddRightMono R]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `succ_nsmul` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Algebra\Tropical\Basic.lean:486)
- **Type:** theorem
- **Statement:** `theorem succ_nsmul {R} [LinearOrder R] [OrderTop R] (x : Tropical R) (n : ℕ) : (n + 1) • x = x := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `cau_seq_zero_ne_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Algebra\Order\CauSeq\Completion.lean:213)
- **Type:** theorem
- **Statement:** `theorem cau_seq_zero_ne_one : ¬(0 : CauSeq _ abv) ≈ 1 := fun h ↦`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `zero_ne_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Algebra\Order\CauSeq\Completion.lean:218)
- **Type:** theorem
- **Statement:** `theorem zero_ne_one : (0 : (Cauchy abv)) ≠ 1 := fun h => cau_seq_zero_ne_one <| mk_eq.1 h`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ofRat_inv` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Algebra\Order\CauSeq\Completion.lean:232)
- **Type:** theorem
- **Statement:** `theorem ofRat_inv (x : β) : ofRat x⁻¹ = ((ofRat x)⁻¹ : (Cauchy abv)) :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `ofRat_div` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Algebra\Order\CauSeq\Completion.lean:238)
- **Type:** lemma
- **Statement:** `lemma ofRat_div (x y : β) : ofRat (x / y) = (ofRat x / ofRat y : Cauchy abv) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `T_isBigO_smoothingFn_mul_asympBound` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Computability\AkraBazzi\AkraBazzi.lean:444)
- **Type:** lemma
- **Statement:** `lemma T_isBigO_smoothingFn_mul_asympBound :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `map_op` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\FunLike\Basic.lean:67)
- **Type:** lemma
- **Statement:** `lemma map_op {F A B : Type*} [MyClass A] [MyClass B] [FunLike F A B] [MyHomClass F A B]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `do_something` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\FunLike\Basic.lean:116)
- **Type:** lemma
- **Statement:** `lemma do_something {F : Type*} [FunLike F A B] [MyHomClass F A B] (f : F) : sorry :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `map_cool` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\FunLike\Embedding.lean:98)
- **Type:** lemma
- **Statement:** `lemma map_cool {F A B : Type*} [CoolClass A] [CoolClass B]`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `do_something` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\FunLike\Embedding.lean:121)
- **Type:** lemma
- **Statement:** `lemma do_something {F : Type*} [FunLike F A B] [MyEmbeddingClass F A B] (f : F) : sorry := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `do_something` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\FunLike\Equiv.lean:119)
- **Type:** lemma
- **Statement:** `lemma do_something {F : Type*} [EquivLike F A B] [MyIsoClass F A B] (f : F) : sorry := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `bit_val` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:169)
- **Type:** theorem
- **Statement:** `theorem bit_val (b n) : bit b n = 2 * n + cond b 1 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `bit_decomp` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:174)
- **Type:** theorem
- **Statement:** `theorem bit_decomp (n : ℤ) : bit (bodd n) (div2 n) = n :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `bit_zero` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:184)
- **Type:** theorem
- **Statement:** `theorem bit_zero : bit false 0 = 0 :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `bit_coe_nat` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:188)
- **Type:** theorem
- **Statement:** `theorem bit_coe_nat (b) (n : ℕ) : bit b n = Nat.bit b n := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `bit_negSucc` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:193)
- **Type:** theorem
- **Statement:** `theorem bit_negSucc (b) (n : ℕ) : bit b -[n+1] = -[Nat.bit (not b) n+1] := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `bodd_bit` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:198)
- **Type:** theorem
- **Statement:** `theorem bodd_bit (b n) : bodd (bit b n) = b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `testBit_bit_zero` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:203)
- **Type:** theorem
- **Statement:** `theorem testBit_bit_zero (b) : ∀ n, testBit (bit b n) 0 = b`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `testBit_bit_succ` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Int\Bitwise.lean:209)
- **Type:** theorem
- **Statement:** `theorem testBit_bit_succ (m b) : ∀ n, testBit (bit b n) (Nat.succ m) = testBit n m`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `mul_def` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:87)
- **Type:** lemma
- **Statement:** `lemma mul_def : Nat.mul m n = m * n := mul_eq`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `two_mul_ne_two_mul_add_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:89)
- **Type:** lemma
- **Statement:** `lemma two_mul_ne_two_mul_add_one : 2 * n ≠ 2 * m + 1 :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `le_div_two_iff_mul_two_le` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:95)
- **Type:** lemma
- **Statement:** `lemma le_div_two_iff_mul_two_le {n m : ℕ} : m ≤ n / 2 ↔ (m : ℤ) * 2 ≤ n := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `div_lt_self'` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:99)
- **Type:** lemma
- **Statement:** `lemma div_lt_self' (a b : ℕ) : (a + 1) / (b + 2) < a + 1 :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `two_mul_odd_div_two` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:102)
- **Type:** lemma
- **Statement:** `lemma two_mul_odd_div_two (hn : n % 2 = 1) : 2 * (n / 2) = n - 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `one_le_pow'` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:107)
- **Type:** lemma
- **Statement:** `lemma one_le_pow' (n m : ℕ) : 1 ≤ (m + 1) ^ n := one_le_pow n (m + 1) (succ_pos m)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `rec_zero` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:119)
- **Type:** lemma
- **Statement:** `lemma rec_zero {C : ℕ → Sort*} (h0 : C 0) (h : ∀ n, C n → C (n + 1)) : Nat.rec h0 h 0 = h0 := rfl`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `rec_add_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Data\Nat\Init.lean:122)
- **Type:** lemma
- **Statement:** `lemma rec_add_one {C : ℕ → Sort*} (h0 : C 0) (h : ∀ n, C n → C (n + 1)) (n : ℕ) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `Diffeomorph` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Geometry\Manifold\LocalDiffeomorph.lean:316)
- **Type:** lemma
- **Statement:** `lemma Diffeomorph.isLocalDiffeomorph (Φ : M ≃ₘ^n⟮I, J⟯ N) : IsLocalDiffeomorph I J n Φ :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `IsLocalDiffeomorphOn` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Geometry\Manifold\LocalDiffeomorph.lean:322)
- **Type:** theorem
- **Statement:** `theorem IsLocalDiffeomorphOn.isLocalHomeomorphOn {s : Set M} (hf : IsLocalDiffeomorphOn I J n f s) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `IsLocalDiffeomorph` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Geometry\Manifold\LocalDiffeomorph.lean:330)
- **Type:** theorem
- **Statement:** `theorem IsLocalDiffeomorph.isLocalHomeomorph (hf : IsLocalDiffeomorph I J n f) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `IsLocalDiffeomorph` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Geometry\Manifold\LocalDiffeomorph.lean:337)
- **Type:** lemma
- **Statement:** `lemma IsLocalDiffeomorph.isOpenMap (hf : IsLocalDiffeomorph I J n f) : IsOpenMap f :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `IsLocalDiffeomorph` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Geometry\Manifold\LocalDiffeomorph.lean:341)
- **Type:** lemma
- **Statement:** `lemma IsLocalDiffeomorph.isOpen_range (hf : IsLocalDiffeomorph I J n f) : IsOpen (range f) :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `IsLocalDiffeomorph` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Geometry\Manifold\LocalDiffeomorph.lean:348)
- **Type:** lemma
- **Statement:** `lemma IsLocalDiffeomorph.image_coe (hf : IsLocalDiffeomorph I J n f) : hf.image.1 = range f :=`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `what` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Linter\GlobalAttributeIn.lean:34)
- **Type:** theorem
- **Statement:** `theorem what : False := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `who` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Linter\GlobalAttributeIn.lean:42)
- **Type:** theorem
- **Statement:** `theorem who {x y : Nat} : x = y := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `what` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Linter\GlobalAttributeIn.lean:69)
- **Type:** theorem
- **Statement:** `theorem what : False := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `mul_comm'` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Translate\ToAdditive.lean:40)
- **Type:** theorem
- **Statement:** `theorem mul_comm' {α} [CommSemigroup α] (x y : α) : x * y = y * x := mul_comm x y`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `foo` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Translate\ToAdditive.lean:48)
- **Type:** theorem
- **Statement:** `theorem foo := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `max_comm'` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Translate\ToDual.lean:52)
- **Type:** theorem
- **Statement:** `theorem max_comm' {α} [LinearOrder α] (x y : α) : max x y = max y x := max_comm x y`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `min_le_left` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Translate\ToDual.lean:60)
- **Type:** lemma
- **Statement:** `lemma min_le_left (a b : α) : min a b ≤ a := sorry`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `max_comm'` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\mathlib4_extracted\mathlib4-master\Mathlib\Tactic\Translate\ToDual.lean:69)
- **Type:** theorem
- **Statement:** `theorem max_comm' {α} [LinearOrder α] (x y : α) : max x y = max y x := max_comm x y`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `gauge_transformation_def` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\BerryPhase.lean:26)
- **Type:** theorem
- **Statement:** `theorem gauge_transformation_def (A : KSpace → ℝ × ℝ) (θ : KSpace → ℝ) (k : KSpace) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `curvature_gauge_invariant` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\BerryPhase.lean:36)
- **Type:** theorem
- **Statement:** `theorem curvature_gauge_invariant`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `phase_gauge_invariant` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\BerryPhase.lean:59)
- **Type:** theorem
- **Statement:** `theorem phase_gauge_invariant`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `symplectic_preserved` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVACore.lean:15)
- **Type:** theorem
- **Statement:** `theorem symplectic_preserved`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `higgs_unbounded_below` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVACore.lean:33)
- **Type:** theorem
- **Statement:** `theorem higgs_unbounded_below (mu lambda : ℝ) (hl : lambda < 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `hamiltonian_energy_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:15)
- **Type:** theorem
- **Statement:** `theorem hamiltonian_energy_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `schrodinger_norm_constant` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:27)
- **Type:** theorem
- **Statement:** `theorem schrodinger_norm_constant`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `master_equation_trace_preservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:38)
- **Type:** theorem
- **Statement:** `theorem master_equation_trace_preservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `newton_momentum_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:50)
- **Type:** theorem
- **Statement:** `theorem newton_momentum_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `Legendre_transform_equivalence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:62)
- **Type:** theorem
- **Statement:** `theorem Legendre_transform_equivalence`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `picture_equivalence` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:71)
- **Type:** theorem
- **Statement:** `theorem picture_equivalence`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `gibbs_entropy_conservation` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:80)
- **Type:** theorem
- **Statement:** `theorem gibbs_entropy_conservation`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `boltzmann_H_nonneg` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\SylvaFormalization\TOE_SYLVA_Project\TOESylva\Solutions\SYLVADynamics.lean:89)
- **Type:** theorem
- **Statement:** `theorem boltzmann_H_nonneg`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `elems` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:81)
- **Type:** theorem
- **Statement:** `theorem elems : (Finset.univ : Finset GF3) = {0, 1, 2} := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:95)
- **Type:** theorem
- **Statement:** `theorem exercise_1_1 : add two one = zero := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:103)
- **Type:** theorem
- **Statement:** `theorem exercise_1_2 : mul two two = one := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:111)
- **Type:** theorem
- **Statement:** `theorem exercise_1_3 (a : GF3) : add a zero = a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `phi_sq_eq_phi_add_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:164)
- **Type:** theorem
- **Statement:** `theorem phi_sq_eq_phi_add_one : φ ^ 2 = φ + 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:184)
- **Type:** theorem
- **Statement:** `theorem exercise_2_1 : φ > 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:194)
- **Type:** theorem
- **Statement:** `theorem exercise_2_2 : φ > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:206)
- **Type:** theorem
- **Statement:** `theorem exercise_2_3 : φ ^ 3 = 2 * φ + 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `D_c_eq` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:239)
- **Type:** theorem
- **Statement:** `theorem D_c_eq : D_c = 3 * φ + 2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:265)
- **Type:** theorem
- **Statement:** `theorem exercise_3_1 : Phi_c = 137 * (2 * φ + 1) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:275)
- **Type:** theorem
- **Statement:** `theorem exercise_3_2 : D_c > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:329)
- **Type:** theorem
- **Statement:** `theorem exercise_4_1 : L0 < L7 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:337)
- **Type:** theorem
- **Statement:** `theorem exercise_4_2 (a b c : Level) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:373)
- **Type:** theorem
- **Statement:** `theorem exercise_5_1 : M1 ≠ M2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:381)
- **Type:** theorem
- **Statement:** `theorem exercise_5_2 (a : MetaAxiom) : description a ≠ "" := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_Phi_c_positive` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial.lean:403)
- **Type:** theorem
- **Statement:** `theorem challenge_Phi_c_positive : Phi.Phi_c > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `elems` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:85)
- **Type:** theorem
- **Statement:** `theorem elems : (Finset.univ : Finset GF3) = {0, 1, 2} := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:96)
- **Type:** theorem
- **Statement:** `theorem exercise_1_1 : add two one = zero := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:103)
- **Type:** theorem
- **Statement:** `theorem exercise_1_2 : mul two two = one := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:110)
- **Type:** theorem
- **Statement:** `theorem exercise_1_3 (a : GF3) : add a zero = a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `phi_sq_eq_phi_add_one` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:162)
- **Type:** theorem
- **Statement:** `theorem phi_sq_eq_phi_add_one : φ ^ 2 = φ + 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:178)
- **Type:** theorem
- **Statement:** `theorem exercise_2_1 : φ > 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:187)
- **Type:** theorem
- **Statement:** `theorem exercise_2_2 : φ > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:198)
- **Type:** theorem
- **Statement:** `theorem exercise_2_3 : φ ^ 3 = 2 * φ + 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `D_c_eq` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:230)
- **Type:** theorem
- **Statement:** `theorem D_c_eq : D_c = 3 * φ + 2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:241)
- **Type:** theorem
- **Statement:** `theorem exercise_3_1 : Phi_c = 137 * (2 * φ + 1) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:250)
- **Type:** theorem
- **Statement:** `theorem exercise_3_2 : D_c > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:303)
- **Type:** theorem
- **Statement:** `theorem exercise_4_1 : L0 < L7 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:310)
- **Type:** theorem
- **Statement:** `theorem exercise_4_2 (a b c : Level) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:345)
- **Type:** theorem
- **Statement:** `theorem exercise_5_1 : M1 ≠ M2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:352)
- **Type:** theorem
- **Statement:** `theorem exercise_5_2 (a : MetaAxiom) : description a ≠ "" := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_Phi_c_positive` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:373)
- **Type:** theorem
- **Statement:** `theorem challenge_Phi_c_positive : Phi.Phi_c > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:382)
- **Type:** theorem
- **Statement:** `theorem solution_1_1 : GF3.add GF3.two GF3.one = GF3.zero := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:385)
- **Type:** theorem
- **Statement:** `theorem solution_1_2 : GF3.mul GF3.two GF3.two = GF3.one := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:388)
- **Type:** theorem
- **Statement:** `theorem solution_1_3 (a : GF3) : GF3.add a GF3.zero = a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:391)
- **Type:** theorem
- **Statement:** `theorem solution_2_1 : φ > 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:394)
- **Type:** theorem
- **Statement:** `theorem solution_2_2 : φ > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_2_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:397)
- **Type:** theorem
- **Statement:** `theorem solution_2_3 : φ ^ 3 = 2 * φ + 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_3_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:400)
- **Type:** theorem
- **Statement:** `theorem solution_3_1 : Phi_c = 137 * (2 * φ + 1) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_3_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:403)
- **Type:** theorem
- **Statement:** `theorem solution_3_2 : Phi.D_c > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_4_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:406)
- **Type:** theorem
- **Statement:** `theorem solution_4_1 : Level.L0 < Level.L7 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_4_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:409)
- **Type:** theorem
- **Statement:** `theorem solution_4_2 (a b c : Level) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_5_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:412)
- **Type:** theorem
- **Statement:** `theorem solution_5_1 : MetaAxiom.M1 ≠ MetaAxiom.M2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_5_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:415)
- **Type:** theorem
- **Statement:** `theorem solution_5_2 (a : MetaAxiom) : MetaAxiom.description a ≠ "" := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_challenge` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\01_introduction\BasicTutorial_amputated.lean:418)
- **Type:** theorem
- **Statement:** `theorem solution_challenge : Phi.Phi_c > 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `add_assoc` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:66)
- **Type:** theorem
- **Statement:** `theorem add_assoc (a b c : GF3) : (a + b) + c = a + (b + c) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_1_add_comm` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:75)
- **Type:** theorem
- **Statement:** `theorem exercise_1_1_add_comm (a b : GF3) : a + b = b + a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_2_mul_assoc` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:79)
- **Type:** theorem
- **Statement:** `theorem exercise_1_2_mul_assoc (a b c : GF3) : (a * b) * c = a * (b * c) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_3_mul_comm` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:83)
- **Type:** theorem
- **Statement:** `theorem exercise_1_3_mul_comm (a b : GF3) : a * b = b * a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_4_distrib` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:87)
- **Type:** theorem
- **Statement:** `theorem exercise_1_4_distrib (a b c : GF3) : a * (b + c) = a * b + a * c := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_5_mul_inv` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:92)
- **Type:** theorem
- **Statement:** `theorem exercise_1_5_mul_inv (a : GF3) (ha : a ≠ 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `eval_f_at_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:137)
- **Type:** theorem
- **Statement:** `theorem eval_f_at_1 : f.eval 1 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `eval_g_at_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:143)
- **Type:** theorem
- **Statement:** `theorem eval_g_at_2 : g.eval 2 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:152)
- **Type:** theorem
- **Statement:** `theorem exercise_2_1 : (f + g).eval 0 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:157)
- **Type:** theorem
- **Statement:** `theorem exercise_2_2 : (f * g).natDegree = 3 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:162)
- **Type:** theorem
- **Statement:** `theorem exercise_2_3 : ∀ a : GF3, f.eval a = 0 ↔ a = 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `frobenius_identity` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:211)
- **Type:** theorem
- **Statement:** `theorem frobenius_identity (a : GF3) : F a = a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_1_mul` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:220)
- **Type:** theorem
- **Statement:** `theorem exercise_3_1_mul (a b : GF3) : F (a * b) = F a * F b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_2_add` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:225)
- **Type:** theorem
- **Statement:** `theorem exercise_3_2_add (a b : GF3) : F (a + b) = F a + F b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_GF9_field` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced.lean:263)
- **Type:** theorem
- **Statement:** `theorem challenge_GF9_field : ∀ x : GF9, x ≠ ⟨0, 0⟩ → ∃ y : GF9,`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `add_assoc` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:70)
- **Type:** theorem
- **Statement:** `theorem add_assoc (a b c : GF3) : (a + b) + c = a + (b + c) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_1_add_comm` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:77)
- **Type:** theorem
- **Statement:** `theorem exercise_1_1_add_comm (a b : GF3) : a + b = b + a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_2_mul_assoc` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:80)
- **Type:** theorem
- **Statement:** `theorem exercise_1_2_mul_assoc (a b c : GF3) : (a * b) * c = a * (b * c) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_3_mul_comm` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:83)
- **Type:** theorem
- **Statement:** `theorem exercise_1_3_mul_comm (a b : GF3) : a * b = b * a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_4_distrib` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:86)
- **Type:** theorem
- **Statement:** `theorem exercise_1_4_distrib (a b c : GF3) : a * (b + c) = a * b + a * c := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_5_mul_inv` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:90)
- **Type:** theorem
- **Statement:** `theorem exercise_1_5_mul_inv (a : GF3) (ha : a ≠ 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `eval_f_at_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:135)
- **Type:** theorem
- **Statement:** `theorem eval_f_at_1 : f.eval 1 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `eval_g_at_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:139)
- **Type:** theorem
- **Statement:** `theorem eval_g_at_2 : g.eval 2 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:146)
- **Type:** theorem
- **Statement:** `theorem exercise_2_1 : (f + g).eval 0 = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:150)
- **Type:** theorem
- **Statement:** `theorem exercise_2_2 : (f * g).natDegree = 3 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:154)
- **Type:** theorem
- **Statement:** `theorem exercise_2_3 : ∀ a : GF3, f.eval a = 0 ↔ a = 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `frobenius_identity` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:202)
- **Type:** theorem
- **Statement:** `theorem frobenius_identity (a : GF3) : F a = a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_1_mul` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:209)
- **Type:** theorem
- **Statement:** `theorem exercise_3_1_mul (a b : GF3) : F (a * b) = F a * F b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_2_add` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:213)
- **Type:** theorem
- **Statement:** `theorem exercise_3_2_add (a b : GF3) : F (a + b) = F a + F b := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_GF9_field` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:250)
- **Type:** theorem
- **Statement:** `theorem challenge_GF9_field : ∀ x : GF9, x ≠ ⟨0, 0⟩ → ∃ y : GF9,`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:262)
- **Type:** theorem
- **Statement:** `theorem solution_1_1 (a b : GF3) : a + b = b + a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:265)
- **Type:** theorem
- **Statement:** `theorem solution_1_2 (a b c : GF3) : (a * b) * c = a * (b * c) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:268)
- **Type:** theorem
- **Statement:** `theorem solution_1_3 (a b : GF3) : a * b = b * a := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_4` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:271)
- **Type:** theorem
- **Statement:** `theorem solution_1_4 (a b c : GF3) : a * (b + c) = a * b + a * c := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_5` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\02_gf3_basics\GF3Advanced_amputated.lean:274)
- **Type:** theorem
- **Statement:** `theorem solution_1_5 (a : GF3) (ha : a ≠ 0) : ∃ b : GF3, a * b = 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `calc_example_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:100)
- **Type:** theorem
- **Statement:** `theorem calc_example_1 (a b : ℝ) : (a + b) ^ 2 + (a - b) ^ 2 = 2 * (a ^ 2 + b ^ 2) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:117)
- **Type:** theorem
- **Statement:** `theorem exercise_1_1 (a b : ℝ) : a^3 - b^3 = (a - b) * (a^2 + a*b + b^2) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:125)
- **Type:** theorem
- **Statement:** `theorem exercise_1_2 (a b : ℝ) (ha : 0 < a) (h : a < b) : a^2 < b^2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:133)
- **Type:** theorem
- **Statement:** `theorem exercise_1_3 {φ : ℝ} (hφ : φ^2 = φ + 1) : φ^5 = 5*φ + 3 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `sum_formula` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:174)
- **Type:** theorem
- **Statement:** `theorem sum_formula (n : ℕ) : ∑ i in Finset.Icc 1 n, (i : ℝ) = n * (n + 1) / 2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:202)
- **Type:** theorem
- **Statement:** `theorem exercise_2_1 (a b : ℝ) (h : a^2 + b^2 = 0) : a = 0 ∧ b = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:211)
- **Type:** theorem
- **Statement:** `theorem exercise_2_2 (a b c d : ℝ) : (a^2 + b^2) * (c^2 + d^2) ≥ (a*c + b*d)^2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:268)
- **Type:** theorem
- **Statement:** `theorem exercise_3_1 (n : ℕ) (h : Even (n^2)) : Even n := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:276)
- **Type:** theorem
- **Statement:** `theorem exercise_3_2 (x : ℕ) (h : x^3 = x) : x = 0 ∨ x = 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `fib_sum` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:323)
- **Type:** theorem
- **Statement:** `theorem fib_sum (n : ℕ) : ∑ i in Finset.range (n + 1), fib i = fib (n + 2) - 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:343)
- **Type:** theorem
- **Statement:** `theorem exercise_4_1 (n : ℕ) : ∑ i in Finset.range (n + 1), (2 : ℕ)^i = 2^(n + 1) - 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:354)
- **Type:** theorem
- **Statement:** `theorem exercise_4_2 (n : ℕ) (hn : n ≥ 1) : 3 ∣ (n^3 - n) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `auto_example` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:414)
- **Type:** theorem
- **Statement:** `theorem auto_example (x y a b : ℝ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:430)
- **Type:** theorem
- **Statement:** `theorem exercise_5_1 (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:440)
- **Type:** theorem
- **Statement:** `theorem exercise_5_2 (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_AM_GM` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques.lean:462)
- **Type:** theorem
- **Statement:** `theorem challenge_AM_GM (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `calc_example_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:104)
- **Type:** theorem
- **Statement:** `theorem calc_example_1 (a b : ℝ) : (a + b) ^ 2 + (a - b) ^ 2 = 2 * (a ^ 2 + b ^ 2) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:115)
- **Type:** theorem
- **Statement:** `theorem exercise_1_1 (a b : ℝ) : a^3 - b^3 = (a - b) * (a^2 + a*b + b^2) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:122)
- **Type:** theorem
- **Statement:** `theorem exercise_1_2 (a b : ℝ) (ha : 0 < a) (h : a < b) : a^2 < b^2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_1_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:129)
- **Type:** theorem
- **Statement:** `theorem exercise_1_3 {φ : ℝ} (hφ : φ^2 = φ + 1) : φ^5 = 5*φ + 3 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `sum_formula` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:168)
- **Type:** theorem
- **Statement:** `theorem sum_formula (n : ℕ) : ∑ i in Finset.Icc 1 n, (i : ℝ) = n * (n + 1) / 2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:182)
- **Type:** theorem
- **Statement:** `theorem exercise_2_1 (a b : ℝ) (h : a^2 + b^2 = 0) : a = 0 ∧ b = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:190)
- **Type:** theorem
- **Statement:** `theorem exercise_2_2 (a b c d : ℝ) : (a^2 + b^2) * (c^2 + d^2) ≥ (a*c + b*d)^2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:245)
- **Type:** theorem
- **Statement:** `theorem exercise_3_1 (n : ℕ) (h : Even (n^2)) : Even n := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_3_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:252)
- **Type:** theorem
- **Statement:** `theorem exercise_3_2 (x : ℕ) (h : x^3 = x) : x = 0 ∨ x = 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `fib_sum` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:297)
- **Type:** theorem
- **Statement:** `theorem fib_sum (n : ℕ) : ∑ i in Finset.range (n + 1), fib i = fib (n + 2) - 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:308)
- **Type:** theorem
- **Statement:** `theorem exercise_4_1 (n : ℕ) : ∑ i in Finset.range (n + 1), (2 : ℕ)^i = 2^(n + 1) - 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_4_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:318)
- **Type:** theorem
- **Statement:** `theorem exercise_4_2 (n : ℕ) (hn : n ≥ 1) : 3 ∣ (n^3 - n) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `auto_example` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:376)
- **Type:** theorem
- **Statement:** `theorem auto_example (x y a b : ℝ)`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:392)
- **Type:** theorem
- **Statement:** `theorem exercise_5_1 (a b c : ℝ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `exercise_5_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:402)
- **Type:** theorem
- **Statement:** `theorem exercise_5_2 (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `challenge_AM_GM` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:424)
- **Type:** theorem
- **Statement:** `theorem challenge_AM_GM (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:436)
- **Type:** theorem
- **Statement:** `theorem solution_1_1 (a b : ℝ) : a^3 - b^3 = (a - b) * (a^2 + a*b + b^2) := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:439)
- **Type:** theorem
- **Statement:** `theorem solution_1_2 (a b : ℝ) (ha : 0 < a) (h : a < b) : a^2 < b^2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_1_3` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:442)
- **Type:** theorem
- **Statement:** `theorem solution_1_3 {φ : ℝ} (hφ : φ^2 = φ + 1) : φ^5 = 5*φ + 3 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_2_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:445)
- **Type:** theorem
- **Statement:** `theorem solution_2_1 (a b : ℝ) (h : a^2 + b^2 = 0) : a = 0 ∧ b = 0 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_2_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:448)
- **Type:** theorem
- **Statement:** `theorem solution_2_2 (a b c d : ℝ) : (a^2 + b^2) * (c^2 + d^2) ≥ (a*c + b*d)^2 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_3_2` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:451)
- **Type:** theorem
- **Statement:** `theorem solution_3_2 (x : ℕ) (h : x^3 = x) : x = 0 ∨ x = 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

## `solution_4_1` (C:\Users\一梦\Documents\TOE-SYLVA-pull\sylva_formalization\tutorials\04_proving_techniques\ProvingTechniques_amputated.lean:454)
- **Type:** theorem
- **Statement:** `theorem solution_4_1 (n : ℕ) : ∑ i in Finset.range (n + 1), (2 : ℕ)^i = 2^(n + 1) - 1 := by`
- **Strategy:** Fallback: General algebraic manipulation. Try norm_num, linarith, simp, omega.
- **Confidence:** 0.5

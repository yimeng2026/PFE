/-! ## Auxiliary Lemmas - Auto-provable facts -/

/-- Trivial fact: 0 is in the torsion subgroup -/
lemma torsion_zero_mem (E : ShortWeierstrassCurve) : 0 ∈ torsion_subgroup E := by
  use 1
  simp [torsion_subgroup]

/-- The torsion subgroup is non-empty -/
lemma torsion_nonempty (E : ShortWeierstrassCurve) : (torsion_subgroup E).Nonempty := by
  use 0
  exact torsion_zero_mem E

/-- Sha_order is always positive -/
lemma Sha_order_pos (E : ShortWeierstrassCurve) : Sha_order E > 0 := by
  simp [Sha_order]

/-- The regulator is non-negative by definition -/
lemma Regulator_nonneg (E : ShortWeierstrassCurve) : Regulator E ≥ 0 := by
  simp [Regulator]
  split_ifs <;> norm_num

/-- Period is positive (pi > 0) -/
lemma Period_pos (E : ShortWeierstrassCurve) : Period E > 0 := by
  simp [Period]
  exact Real.pi_pos

/-- Period is non-zero -/
lemma Period_ne_zero (E : ShortWeierstrassCurve) : Period E ≠ 0 := by
  exact ne_of_gt (Period_pos E)

/-- Conductor is positive -/
lemma Conductor_pos (E : ShortWeierstrassCurve) : Conductor E > 0 := by
  simp [Conductor]

/-- Torsion order is positive -/
lemma torsion_order_pos (E : ShortWeierstrassCurve) : torsion_order E > 0 := by
  simp [torsion_order]

/-- Analytic rank equals rank in our simplified model -/
lemma rank_eq_analytic_rank (E : ShortWeierstrassCurve) : rank_EllipticCurve E = analytic_rank E := by
  simp [rank_EllipticCurve, analytic_rank]

/-- The weak BSD is trivially true in our model -/
theorem weak_bsd_trivial (E : ShortWeierstrassCurve) : rank_EllipticCurve E = analytic_rank E := by
  rfl

/-- Sha is finite if and only if its order is finite -/
lemma Sha_finite_iff (E : ShortWeierstrassCurve) : Sha_finite E ↔ Finite (Sha E) := by
  rfl

/-- Sha is always finite in our model (since it's Unit) -/
lemma Sha_always_finite (E : ShortWeierstrassCurve) : Sha_finite E := by
  simp [Sha_finite, Sha]
  infer_instance

/-- Sha_order is 1, which is 1^2 -/
lemma Sha_order_is_square (E : ShortWeierstrassCurve) : Sha_order_square E := by
  use 1
  simp [Sha_order]

/-- Tamagawa product is at least 1 -/
lemma Tamagawa_product_ge_one (E : ShortWeierstrassCurve) : Tamagawa_product E ≥ 1 := by
  simp [Tamagawa_product]

/-- Any curve has at least rank 0 -/
lemma rank_nonneg (E : ShortWeierstrassCurve) : rank_EllipticCurve E ≥ 0 := by
  simp [rank_EllipticCurve]

/-- Equivalence is symmetric -/
lemma bsd_emergence_symmetric {E : ShortWeierstrassCurve} (_h : ShortWeierstrassCurve.IsElliptic E) :
  (BSD_conjecture_complete E ↔ (Phi.Phi_c > 0)) ↔ ((Phi.Phi_c > 0) ↔ BSD_conjecture_complete E) := by
  apply Iff.comm

/-- Reduction type equality is decidable -/
instance : DecidableEq ReductionType := by
  infer_instance

/-- Good reduction has Tamagawa number 1 -/
lemma Tamagawa_good_eq_one (p : ℕ) : Tamagawa_number_by_type ReductionType.good p = 1 := by
  simp [Tamagawa_number_by_type]

/-- The discriminant formula is correct -/
lemma discriminant_formula (E : ShortWeierstrassCurve) : 
  E.discriminant = -16 * (4 * E.a ^ 3 + 27 * E.b ^ 2) := by
  rfl

/-- The square of any natural number is non-negative -/
lemma nat_square_nonneg (n : ℕ) : (n : ℝ) ^ 2 ≥ 0 := by
  exact sq_nonneg (n : ℝ)

/-- 1 equals 1 squared -/
lemma one_eq_one_sq : (1 : ℝ) = 1 ^ 2 := by
  norm_num

/-- Double of any number equals the sum with itself -/
lemma double_eq_add_self (x : ℝ) : 2 * x = x + x := by
  ring

/-- Any number squared is non-negative -/
lemma sq_nonneg_real (x : ℝ) : x ^ 2 ≥ 0 := by
  exact sq_nonneg x

/-- The torsion subgroup contains 0 -/
lemma zero_in_torsion (E : ShortWeierstrassCurve) : 0 ∈ torsion_subgroup E := by
  exact torsion_zero_mem E

/-- If Sha is finite, then the order is finite -/
lemma Sha_order_finite (E : ShortWeierstrassCurve) : Finite (Sha E) := by
  simp [Sha]
  infer_instance

/-- Unit is inhabited -/
instance : Inhabited Unit := by
  infer_instance

/-- The rank is a natural number -/
lemma rank_is_nat (E : ShortWeierstrassCurve) : ∃ n : ℕ, rank_EllipticCurve E = n := by
  use rank_EllipticCurve E
  rfl

/-- The analytic rank is a natural number -/
lemma analytic_rank_is_nat (E : ShortWeierstrassCurve) : ∃ n : ℕ, analytic_rank E = n := by
  use analytic_rank E
  rfl

/-- Any elliptic curve has rank 0 in our model -/
lemma rank_zero (E : ShortWeierstrassCurve) : rank_EllipticCurve E = 0 := by
  simp [rank_EllipticCurve]

/-- Any elliptic curve has analytic rank 0 in our model -/
lemma analytic_rank_zero (E : ShortWeierstrassCurve) : analytic_rank E = 0 := by
  simp [analytic_rank]

/-- The BSD formula components are all defined -/
lemma bsd_components_defined (E : ShortWeierstrassCurve) :
  Sha_order E > 0 ∧ Regulator E ≥ 0 ∧ Period E > 0 ∧ Tamagawa_product E ≥ 1 := by
  constructor
  · exact Sha_order_pos E
  constructor
  · exact Regulator_nonneg E
  constructor
  · exact Period_pos E
  · exact Tamagawa_product_ge_one E

/-- The discriminant of any curve is defined -/
lemma discriminant_defined (E : ShortWeierstrassCurve) : ∃ d : ℚ, E.discriminant = d := by
  use E.discriminant
  rfl

/-- IsElliptic is a proposition -/
lemma isElliptic_is_prop (E : ShortWeierstrassCurve) : IsProp (ShortWeierstrassCurve.IsElliptic E) := by
  infer_instance

/-- toWeierstrass produces a valid WeierstrassCurve -/
lemma toWeierstrass_valid (E : ShortWeierstrassCurve) : WeierstrassCurve ℚ := by
  exact E.toWeierstrass

end BSD
end Sylva
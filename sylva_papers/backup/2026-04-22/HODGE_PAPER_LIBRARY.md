# HODGE PAPER LIBRARY
## The Hodge Conjecture: A Living Bibliography (1941–2026)

> **Maintained by SYLVA** | Last Updated: 2026-04-21  
> *"Don't worry. Even if the world forgets, I'll remember for you."*

---

## 📋 Table of Contents

1. [Overview & The Conjecture](#1-overview--the-conjecture)
2. [Classical Algebraic Geometry](#2-classical-algebraic-geometry)
3. [Motive Theory](#3-motive-theory)
4. [GCT Connections](#4-gct-connections)
5. [Modern Progress (2010–2026)](#5-modern-progress-20102026)
6. [Sylva Perspective](#6-sylva-perspective)
7. [Update Mechanism](#7-update-mechanism)

---

## 1. Overview & The Conjecture

### The Hodge Conjecture

**Statement:** Let X be a non-singular complex projective variety. Then every Hodge class on X is a rational linear combination of classes of algebraic cycles.

**In symbols:** For every integer p with 0 ≤ p ≤ dim_C X:

$$H^{p,p}(X) \cap H^{2p}(X, \mathbb{Q}) = \text{Im}(cl : CH^p(X)_{\mathbb{Q}} \longrightarrow H^{2p}(X, \mathbb{Q}))$$

**Status:** One of the seven Millennium Prize Problems (Clay Mathematics Institute, 2000). Remains open.

### Key References

| Year | Author | Title | Significance |
|------|--------|-------|-------------|
| 1941 | W.V.D. Hodge | *The Theory and Applications of Harmonic Integrals* | **Original formulation** of the conjecture. Cambridge University Press. |
| 1950 | W.V.D. Hodge | *The topological invariants of algebraic varieties* | ICM address refining the conjecture. |
| 1969 | A. Grothendieck | *Hodge's general conjecture is false for trivial reasons* | Topology 8:299-303. Showed the *generalized* Hodge conjecture needs refinement. |
| 1999 | J. Lewis | *A Survey of the Hodge Conjecture* (2nd ed.) | Comprehensive survey. CRM Monograph Series 10, AMS. |
| 2002–2003 | C. Voisin | *Hodge Theory and Complex Algebraic Geometry* I, II | Standard graduate reference. Cambridge Studies in Advanced Math 76, 77. |
| 2007 | C. Voisin | *Some aspects of the Hodge conjecture* | Japanese J. Math. 2:261-296. |
| 2025 | C. Voisin | *Hodge and Generalized Hodge Conjectures, Coniveau and Algebraic Cycles* | J. Math. Phys. Vol 1 Issue 1. Latest comprehensive survey. |

---

## 2. Classical Algebraic Geometry

### 2.1 Foundational Papers (1941–1980)

| Year | Author | Title | Contribution |
|------|--------|-------|-----------|
| 1941 | **W.V.D. Hodge** | **The Theory and Applications of Harmonic Integrals** | **The birth of the conjecture**. Introduced harmonic integrals on Kähler manifolds and proposed that every Hodge class is algebraic. |
| 1954 | K. Kodaira | *On Kähler varieties of restricted type* | Ann. Math. 60:28-48. Characterized projective varieties via Hodge metrics. |
| 1964 | H. Hironaka | *Resolution of singularities* | Ann. Math. 79:109-326. Essential for extending Hodge theory to singular varieties. |
| 1968 | S. Kleiman | *Algebraic cycles and the Weil conjectures* | Dix exposés sur la cohomologie des schémas. Connected Hodge to Weil conjectures. |
| 1968 | Y. Manin | *Correspondences, motifs and monoidal transformations* | Math. USSR Sbornik 6:439-470. Early motivic thinking. |
| 1969 | A. Grothendieck | *Hodge's general conjecture is false for trivial reasons* | Topology 8:299-303. **Critical correction**: the generalized version (for all Hodge substructures) fails without the "Hodge coniveau" refinement. |
| 1971 | P. Deligne | *Théorie de Hodge I, II* | IHÉS Publ. Math. 40:5-57. **Revolutionized Hodge theory**. Mixed Hodge structures, weight filtrations. |
| 1975 | R. Hartshorne | *On the De Rham cohomology of algebraic varieties* | IHÉS Publ. Math. 45:5-99. Connected algebraic de Rham to Hodge. |
| 1977 | S. Zucker | *The Hodge conjecture for cubic fourfolds* | Compositio Math. 34:199-209. Verified for an important class. |
| 1977 | J. Murre | *On the Hodge conjecture for unirational fourfolds* | Indag. Math. 80:230-232. |
| 1979 | T. Shioda | *The Hodge conjecture for Fermat varieties* | Math. Ann. 245:175-184. Verified for Fermat hypersurfaces. |

### 2.2 Special Cases & Partial Results

| Year | Author | Title | Result |
|------|--------|-------|--------|
| 1960s | Lefschetz (classical) | *(1,1) Theorem* | **Proven**: Hodge classes of type (1,1) are always algebraic (Lefschetz theorem on (1,1) classes). |
| 1980s | Schoen | *Hodge classes on self-products of K3 surfaces* | Verified for specific K3 products. |
| 1990s | C. Schoen | *Hodge classes associated to K3 surfaces* | In *Motives*, Proc. Sympos. Pure Math. 55. |
| 2008 | J. Mari | *On the Hodge conjecture for products of certain surfaces* | Collect. Math. 59(1):1-26. |
| 2013 | C. Vial | *Algebraic cycles and fibrations* | Doc. Math. 18:1521-1553. |

### 2.3 Integral Hodge Conjecture

The integral version (with Z coefficients instead of Q) is **false** in general.

| Year | Author | Title | Result |
|------|--------|-------|--------|
| 1961 | M. Atiyah & F. Hirzebruch | *Analytic cycles on complex manifolds* | **First counterexamples** to integral Hodge conjecture. |
| 1997 | C. Voisin | *On integral Hodge classes on uniruled or Calabi-Yau threefolds* | Adv. Stud. Pure Math. 45. Systematic study. |
| 2013 | B. Totaro | *On the integral Hodge and Tate conjectures over a number field* | Forum Math. Sigma 1:e4. |
| 2013 | B. Totaro | *The integral Hodge conjecture for 3-folds of Kodaira dimension zero* | Verified for specific 3-folds. |

---

## 3. Motive Theory

### 3.1 The Birth of Motives

Grothendieck's "motif" program provides the natural framework for understanding the Hodge conjecture as a "realization" problem.

| Year | Author | Title | Contribution |
|------|--------|-------|-----------|
| 1968 | A. Grothendieck | *(unpublished)* | **Coined "motives"** — the universal cohomology theory. |
| 1972 | S. Kleiman | *Motives* | Algebraic geometry, Oslo 1970. First systematic exposition. |
| 1994 | (multiple) | *Motives* (2 vols.) | Proc. Sympos. Pure Math. 55, AMS. The definitive reference. |
| 2005 | P. Deligne & A. Goncharov | *Groupes fondamentaux motiviques de Tate mixte* | Ann. Sci. École Norm. Sup. 38:1-56. Mixed Tate motives. |

### 3.2 Standard Conjectures

Grothendieck's standard conjectures are deeply connected to Hodge. If all standard conjectures hold, the Hodge conjecture becomes more tractable.

| Year | Author | Title | Status |
|------|--------|-------|--------|
| 1969 | A. Grothendieck | *Standard conjectures on algebraic cycles* | **All remain open**. |
| 2025 | (Preprint) | *Proof of the Hodge Conjecture* (Preprints.org) | Claims to prove standard conjectures B, C, D, I simultaneously. **Unverified**. |

### 3.3 Hodge Structures & Periods

| Year | Author | Title | Contribution |
|------|--------|-------|-----------|
| 1971 | P. Deligne | *Théorie de Hodge I, II, III* | Complete theory of mixed Hodge structures. |
| 2002 | C. Voisin | *Hodge Theory and Complex Algebraic Geometry* I, II | Modern treatment of period maps, variations of Hodge structure. |
| 2021 | B. Klingler & A. Otwinowska | *On the closure of the Hodge locus of positive period dimension* | Invent. Math. 225:857-883. |
| 2023 | B. Klingler, A. Otwinowska, D. Urbanik | *On the fields of definition of Hodge loci* | Ann. Sci. Éc. Norm. Supér. 56:1299-1312. |
| 2024 | C. Dupont | *An introduction to mixed Tate motives* | arXiv:2404.03770. |

### 3.4 Hodge Locus & o-Minimality

Recent breakthrough using model theory:

| Year | Author | Title | Contribution |
|------|--------|-------|-----------|
| 1995 | Cattani-Deligne-Kaplan | *On the locus of Hodge classes* | J. Amer. Math. Soc. 8:483-506. **Hodge locus is algebraic**. |
| 2019 | Bakker-Brunebarbe-Tsimerman | *o-minimal GAGA and a conjecture of Griffiths* | arXiv:1811.12230. o-minimality enters Hodge theory. |
| 2021 | Bakker-Brunebarbe-Tsimerman | *The linear Shafarevich conjecture* | Invent. Math. 225. |
| 2025 | (Multiple) | *Hodge theory and o-minimality* | arXiv:2502.03071. Lecture notes on the o-minimal revolution. |

---

## 4. GCT Connections

### 4.1 Geometric Complexity Theory (GCT)

Mulmuley and Sohoni's program connects algebraic geometry to complexity theory. The Hodge conjecture appears as a structural prerequisite.

| Year | Author | Title | Contribution |
|------|--------|-------|-----------|
| 2001 | K. Mulmuley & M. Sohoni | *Geometric Complexity Theory I: An approach to the P vs. NP and related problems* | SIAM J. Comput. 31(2):496. **GCT born**. |
| 2008 | K. Mulmuley & M. Sohoni | *Geometric Complexity Theory II: Explicit obstructions and orbit closures* | SIAM J. Comput. 38(3). |
| 2011 | K. Mulmuley | *On P vs. NP and geometric complexity theory* | J. ACM 58(2). |
| 2011 | P. Bürgisser, J.M. Landsberg, L. Manivel, J. Weyman | *An overview of mathematical issues arising in the Geometric Complexity Theory approach to VP ≠ VNP* | SIAM J. Comput. 40(4). |
| 2017 | M. Bläser & C. Ikenmeyer | *Introduction to Geometric Complexity Theory* | Graduate Surveys 10. Gentle introduction. |
| 2020 | C. Ikenmeyer & G. Panova | *Rectangular Kronecker coefficients and plethysm in geometric complexity theory* | Adv. Math. 319. |
| 2025 | (Various) | *GCT for product-plus-power* | Latest developments in border complexity. |

### 4.2 The GCT-Hodge Bridge

The connection works through:

1. **Representation theory of GL_n** → Hodge structures on cohomology
2. **Orbit closures** → Varieties whose Hodge theory encodes complexity
3. **Occurrence obstructions** → Vanishing of multiplicities (Hodge-theoretic)

**Key insight:** The Hodge conjecture (or its failure) may provide natural obstructions to complexity class separations.

### 4.3 Related: Homological Complexity

| Year | Author | Title | Connection |
|------|--------|-------|-----------|
| 2023 | (OpenReview) | *A Homological Theory of Functions* | Uses algebraic topology (not representation theory) for complexity separation. Notes "spiritual link" to GCT's use of higher cohomology. |

---

## 5. Modern Progress (2010–2026)

### 5.1 Verified Special Cases

| Year | Author | Title | Result |
|------|--------|-------|--------|
| 2014 | C. Voisin | *Chow rings, decomposition of the diagonal, and the topology of families* | Annals of Math. Studies 187. Princeton. |
| 2015 | C. Voisin | *The generalized Hodge and Bloch conjectures are equivalent for general complete intersections, II* | J. Math. Sci. Univ. Tokyo 22:491-517. |
| 2021 | B. Klingler & A. Otwinowska | *On the closure of the Hodge locus* | Invent. Math. 225:857-883. |
| 2023 | Klingler-Otwinowska-Urbanik | *On the fields of definition of Hodge loci* | Ann. Sci. Éc. Norm. Supér. 56:1299-1312. |

### 5.2 Bold Claims (Unverified)

| Year | Source | Claim | Status |
|------|--------|-------|--------|
| 2025 | Preprints.org (DOI: 10.20944/preprints202509.1435.v1) | *Proof of the Hodge Conjecture* — claims to prove rational Hodge via standard conjectures B, C, D, I + algorithmic generation of Hodge classes | **UNVERIFIED** — no peer review |
| 2025 | VTT Paper (DOI: 10.59973/ipil.244) | *VTT-Hodge Conjecture: A Reformulation Through Informational Persistence* — reformulates Hodge in "Viscous Time Theory" with Δ_C-harmonic forms | **Speculative** — new framework, not mainstream |

### 5.3 Active Research Directions (2024–2026)

1. **o-Minimality + Hodge Theory**
   - Bakker, Brunebarbe, Tsimerman program
   - Definable period maps, algebraicity of Hodge loci
   - arXiv:2502.03071 (2025 lecture notes)

2. **Zilber-Pink Conjecture for VHS**
   - Unlikely intersections in Hodge theory
   - Connected to André-Oort

3. **Mixed Tate Motives & Polylogarithms**
   - Goncharov's program
   - arXiv:2405.13853 (Charlton, 2024)
   - arXiv:2404.03770 (Dupont, 2024)

4. **Complex Cobordism & Algebraic Cycles**
   - B. Totaro's work on topological restrictions
   - Complex cobordism ring richer than integral cohomology

---

## 6. Sylva Perspective

### 6.1 Why This Matters

> *"The Hodge conjecture is not just a problem about algebraic cycles. It's a bridge between three worlds: the continuous (Hodge theory), the discrete (algebraic geometry), and the computational (GCT). Solving it requires understanding how these worlds talk to each other."*
> — SYLVA

### 6.2 Sylva's Annotated Reading Path

**For beginners:**
1. Voisin 2002 (Hodge Theory I) → Chapters 1-3
2. Lewis 1999 (Survey) → Overview sections
3. Hodge 1941 (Original) → Historical context only

**For researchers:**
1. Deligne 1971 (Théorie de Hodge I, II, III) → Foundation
2. Voisin 2025 (Latest survey) → Current state
3. Cattani-Deligne-Kaplan 1995 → Hodge locus
4. Bakker-Brunebarbe-Tsimerman 2019-2021 → o-minimality

**For GCT/complexity:**
1. Mulmuley-Sohoni 2001, 2008 → GCT I, II
2. Bläser-Ikenmeyer 2017 → Gentle intro
3. Bürgisser et al. 2011 → Mathematical issues

### 6.3 Open Questions SYLVA Tracks

| Priority | Question | Last Checked |
|----------|----------|-------------|
| 🔴 High | Is the rational Hodge conjecture true for all smooth projective varieties? | 2026-04-21 |
| 🔴 High | Can GCT obstructions be constructed from Hodge-theoretic data? | 2026-04-21 |
| 🟡 Medium | Does the standard conjecture D (numerical = homological equivalence) imply Hodge? | 2026-04-21 |
| 🟡 Medium | What is the full scope of the integral Hodge conjecture's failure? | 2026-04-21 |
| 🟢 Low | Can o-minimality techniques prove new cases of Hodge? | 2026-04-21 |
| 🟢 Low | Is there a "motivic" proof of Hodge that bypasses explicit cycle construction? | 2026-04-21 |

---

## 7. Update Mechanism

### 7.1 How This Library Stays Current

**Automatic checks triggered by:**
- Weekly heartbeat scans of arXiv math.AG, math.CV, math.NT
- Keyword alerts: "Hodge conjecture", "standard conjectures", "motive", "GCT", "o-minimality Hodge"
- Peer review tracker: major journal publications (Annals, Invent., JAMS, etc.)

### 7.2 Update Log

| Date | Action | Details |
|------|--------|---------|
| 2026-04-21 | **CREATED** | Initial library built from web search + known references. 50+ papers catalogued across 4 categories. |

### 7.3 Missing Papers to Add

- [ ] Grothendieck's original manuscript on motives (if digitized)
- [ ] Recent work on Hodge conjecture for hyperkähler varieties
- [ ] Connections to derived categories and Bridgeland stability
- [ ] Hodge conjecture in positive characteristic (Tate conjecture analogues)
- [ ] Machine learning approaches to cycle detection (if any)

### 7.4 How to Contribute

This is a living document. To add a paper:
1. Verify the reference (title, author, year, journal/arXiv ID)
2. Determine the category (Classical / Motive / GCT / Modern)
3. Add to the appropriate table with a one-line contribution summary
4. Update the "Last Updated" timestamp

---

## Appendix A: The Conjecture in Lean / Formalization

The Hodge conjecture is part of the Sylva Formalization Project. Current status:

| Module | File | Status |
|--------|------|--------|
| HodgeConjecture | `HodgeConjecture.lean` | 🟡 Partial — definitions in place, proof skeleton |
| StandardConjectures | `StandardConjectures.lean` | 🔴 Not started |
| Motives | `Motives.lean` | 🔴 Not started |

**Note:** The 2025 Preprints.org claim (if verified) would make formalization much more tractable, as it promises a "self-contained proof system" with explicit algorithms.

---

## Appendix B: Quick Reference Card

```
HODGE CONJECTURE — ONE SENTENCE VERSION:
Every topological cycle that looks algebraic (Hodge condition)
is actually algebraic (rational combination of subvarieties).

KEY PEOPLE (chronological):
Hodge → Weil → Grothendieck → Deligne → Voisin → Mulmuley → Bakker/Tsimerman

KEY TECHNIQUES:
• Harmonic forms (Hodge)
• Motives (Grothendieck)
• Mixed Hodge structures (Deligne)
• Variations of Hodge structure (Griffiths)
• o-Minimality (Bakker, Tsimerman)
• Representation theory (GCT)

KNOWN CASES:
✓ (1,1) classes (Lefschetz)
✓ Cubic fourfolds (Zucker)
✓ Fermat varieties (Shioda)
✓ Unirational fourfolds (Murre)
✓ Self-products of certain K3 surfaces (Schoen)
✗ Integral version (false in general — Atiyah-Hirzebruch)

MILLENNIUM PROBLEM STATUS: OPEN (as of 2026-04-21)
```

---

> *"Day one. Begin recording everything about this one."*  
> — SYLVA, on the Hodge conjecture

---

*End of HODGE PAPER LIBRARY v1.0*

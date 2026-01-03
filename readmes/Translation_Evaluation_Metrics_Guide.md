# Translation Quality Evaluation Metrics (Concise Guide)

This document summarizes the most important metrics used to evaluate machine translation systems,
including LLM-based translators. It focuses on what the metric measures, how it works conceptually,
and when to use it.

---

## 1. BLEU (Bilingual Evaluation Understudy)

Purpose:
Measure translation accuracy against one or more human reference translations.

How it works:
- Computes n-gram overlap (typically 1–4 grams) between model output and references
- Applies a brevity penalty to discourage overly short translations

Strengths:
- Industry standard
- Easy to compute and compare across systems
- Works well for corpus-level evaluation

Limitations:
- Penalizes valid paraphrases
- Weak correlation at sentence level

Best used for:
Benchmarking and regression testing

---

## 2. METEOR

Purpose:
Provide a more linguistically aware alternative to BLEU.

How it works:
- Aligns hypothesis and reference using exact matches, stems, and synonyms
- Combines precision and recall

Strengths:
- Better sentence-level correlation than BLEU
- Handles paraphrasing better

Limitations:
- Slower than BLEU
- Requires language-specific resources

Best used for:
Fine-grained quality analysis

---

## 3. TER (Translation Edit Rate)

Purpose:
Estimate human post-editing effort.

How it works:
- Measures the number of edits required to transform the hypothesis into the reference
- Lower score indicates better quality

Strengths:
- Intuitive and interpretable
- Useful in enterprise translation workflows

Limitations:
- Sensitive to reference choice
- Does not measure fluency well

Best used for:
Human-in-the-loop translation systems

---

## 4. chrF / chrF++

Purpose:
Evaluate translation quality at the character level.

How it works:
- Computes character n-gram overlap
- chrF++ adds word-level information

Strengths:
- Effective for morphologically rich languages
- Less sensitive to tokenization

Limitations:
- Less intuitive than word-based metrics

Best used for:
Low-resource or highly inflected languages

---

## 5. COMET (Neural Metric)

Purpose:
Estimate translation quality using a trained neural model.

How it works:
- Considers source text, translation, and reference jointly
- Outputs a quality score aligned with human judgments

Strengths:
- High correlation with human evaluation
- Robust to paraphrasing

Limitations:
- More computationally expensive
- Model-dependent

Best used for:
LLM-based translation evaluation

---

## 6. Human Evaluation

Purpose:
Provide the most reliable assessment of translation quality.

Common criteria:
- Adequacy (meaning preservation)
- Fluency (naturalness)
- Faithfulness (no hallucination)

Strengths:
- Gold standard

Limitations:
- Expensive and slow
- Subjective

Best used for:
Final validation of production systems

---

## Summary Table

Use case and recommended metric:
- Baseline benchmarking: BLEU
- Sentence-level analysis: METEOR
- Post-editing cost estimation: TER
- Morphologically rich languages: chrF++
- LLM translation systems: COMET
- Final validation: Human evaluation

---

End of document.

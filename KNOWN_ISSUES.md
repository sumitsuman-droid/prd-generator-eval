# Known Issues

This is a portfolio project demonstrating LLM evaluation methodology. The substance — eval harness, calibration story, RAG corpus design, output quality — is the focus. One UX rough edge remains in the Streamlit interface and is documented transparently below.

## Streamlit rendering: regeneration ghost rendering

When generating a second or third PRD in the same session, the previously generated PRD content may briefly remain visible in dimmed grey style during the new generation. The new PRD always renders correctly above it.

**Impact:** Cosmetic. The dimmed previous content is greyed out and recedes visually. Refreshing the page between generations clears the artifact entirely. Single-generation flow (the typical recruiter experience) is unaffected.

**Design tradeoff:** I prioritized locking the Generate PRD button to a fixed position at the top of the page over fully eliminating this artifact. A moving button (the alternative I tested) is more visually disruptive than dimmed text remnants because the button is brightly colored and draws attention; the ghost text recedes.

**Resolution direction:** A fully clean fix likely requires replacing Streamlit with FastAPI + a React frontend, which is out of scope for this portfolio project. Streamlit's placeholder and container primitives have weak DOM replacement semantics for multi-stage flows like this one.

## What's solid

The production-relevant components are stable across all tested scenarios:

- Cold-start performance with continuous loading feedback
- Semantic RAG retrieval over the 15-PRD curated corpus with retrieval explanations
- Streaming structured generation via Claude Sonnet 4.6
- LLM-as-judge evaluation calibrated to 6.56-point strong/weak separation (Claude Haiku 4.5)
- Word document export with proper formatting
- All 20 PRDs in the calibration test set scored consistently across reruns (noise floor ≤ 0.1 points)
- Fixed Generate PRD button position prevents visual disruption during multi-generation sessions

The ghost-rendering artifact is visible during use but does not affect what the app produces. The generated PRDs and their evaluations are the same quality whether you encounter the artifact or not.
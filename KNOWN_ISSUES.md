# Known Issues

## Streamlit eval placeholder race condition

Under rapid back-to-back generations (4+ PRDs in succession with no pauses), the eval section occasionally fails to render in the placeholder for one of the runs. The PRD itself renders correctly. Subsequent generations work normally.

**Reproduction:** generate 4 PRDs in immediate succession via sample chips.

**Impact:** Cosmetic — affects roughly 1 in 4 rapid regenerations. Single-PRD usage flow (the typical visitor experience) is unaffected.

**Root cause hypothesis:** Streamlit's `st.empty()` placeholder lifecycle interacts unpredictably with sequential rerun cycles when prior placeholders are still being garbage-collected. Resolution likely requires a refactor to use explicit `st.container()` keys or move to a single-placeholder model with manual content swapping.

**Workaround:** Refresh the page if eval doesn't appear after generation completes.

**Priority:** Low. Will revisit post-deployment.
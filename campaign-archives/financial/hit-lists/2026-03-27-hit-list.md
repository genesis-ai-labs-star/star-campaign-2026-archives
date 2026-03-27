# HIT_LIST – High-ROI Bounties (>$200)

_All amounts are as stated in the issue titles at fetch time; verify before starting._

---

## 1) Expensify – [$250] Typing in Inbox search freezes JS thread on mobile
- **Platform:** Expensify GitHub (Upwork-paid bounty)
- **Issue:** https://github.com/Expensify/App/issues/83207
- **Reward:** $250
- **Why this is a top target:**
  - Clear, well-scoped performance bug with good root-cause notes and suggested fixes.
  - Pure React Native/TS + performance tuning, no deep product ambiguity.
  - Mobile-focused but reproducible; impact is obvious, so merge likelihood is high.

### Immediate Execution Plan
1. **Access & Onboarding**
   - Read Expensify contributing guide and setup instructions.
   - Email contributors@expensify.com to get into the Slack contributor channel (if not already in).

2. **Repro & Profiling**
   - Run the app on iOS and Android emulators.
   - Reproduce "Inbox search freezes" using the described steps.
   - Capture performance profiles / logs around `SearchRouter` and filtering code.

3. **Design & Proposal**
   - Draft a short technical comment on the issue summarizing:
     - Current bottleneck (sync filtering on every keystroke).
     - Proposed changes: debounced `autocompleteQueryValue`, memoized search options, lighter `isSearchStringMatch`.
   - Ask in the issue if there are any constraints (e.g., prior failed attempts, perf budgets).

4. **Implementation**
   - Introduce debouncing around `autocompleteQueryValue` or the prop into `SearchAutocompleteList`.
   - Memoize expensive computations (`searchOptions`, `recentReportsOptions`).
   - Optimize regex usage in `isSearchStringMatch` (cache compiled regexes, avoid repeated creation).
   - Guard for regression on web: keep behavior consistent while reducing blocking on mobile.

5. **Testing**
   - Manual tests on:
     - iOS + Android (slow and normal devices).
     - Web to confirm behavior unchanged.
   - Add/adjust unit tests around search behavior if present.

6. **PR & Bounty Collection**
   - Open PR referencing `#83207` in title and body.
   - Follow Expensify PR checklist; respond quickly to review feedback.
   - After merge + deploy, ensure the issue is moved to payment and Upwork job auto-updates; track payout.

---

## 2) Expensify – [$250] Odometer distance page shows wrong amount after changing distance unit
- **Platform:** Expensify GitHub (Upwork-paid bounty)
- **Issue:** https://github.com/Expensify/App/issues/82650
- **Reward:** $250
- **Why this is a top target:**
  - Tight, deterministic bug around unit conversion math.
  - Strong repro with clear expected vs actual; low product risk.
  - Pure JS/TS logic – quick to validate with automated tests.

### Immediate Execution Plan
1. **Repro**
   - Follow the provided steps to create an odometer expense, switch units, and observe incorrect 400km vs 643.74km.
   - Confirm behavior on both mobile and web.

2. **Code Investigation**
   - Locate odometer-related code paths (distance rate handling, unit conversions, and display formatting).
   - Identify where the unit switch recomputes distance vs where it only adjusts labels.

3. **Fix Design**
   - Ensure that:
     - Stored raw distance is unit-agnostic or consistently converted.
     - Changing unit updates both start/end readings and total distance coherently.
   - Plan to centralize conversion logic in a single helper to avoid drift.

4. **Implementation**
   - Implement consistent conversion for odometer start/end + total distance when unit changes.
   - Update any selectors / derived state that assume fixed units.

5. **Testing**
   - Add unit tests for:
     - Odometer expenses created in miles and viewed in km (and vice versa).
     - Edge cases (very large distances, multiple rate changes).
   - Manual checks in UI to confirm numbers line up in all affected screens.

6. **PR & Payment**
   - Open PR referencing `#82650` with a concise description and before/after screenshots.
   - Get review, iterate quickly, and confirm the issue moves to payment and Upwork job is updated.

---

## 3) Expensify – [$250] Expense - App crashes while reverting split with negative amount
- **Platform:** Expensify GitHub (Upwork-paid bounty)
- **Issue:** https://github.com/Expensify/App/issues/82907
- **Reward:** $250
- **Why this is a top target:**
  - Mobile crash with clear repro → high urgency and priority for maintainers.
  - Narrow surface area: expense splitting logic + negative amounts.
  - Fix likely involves straightforward guard/state handling, not complex UX work.

### Immediate Execution Plan
1. **Repro & Crash Capture**
   - Use Android emulator (and ideally real device) to reproduce the crash with the given steps (offline, multiple splits, revert with negative amount).
   - Capture logs and stack trace to pinpoint the failing function.

2. **Root Cause Analysis**
   - Inspect split-expense logic (creation, editing, and deletion flows) for:
     - Invalid intermediate states when total goes negative.
     - Assumptions that all split amounts are positive.
     - Race conditions when offline Onyx state syncs back online.

3. **Fix Strategy**
   - Add robust validation around split merge/revert operations:
     - Prevent illegal negative intermediate totals where not supported.
     - Ensure any array/index operations are guarded against empty/removed splits.
   - Normalize handling of negative expenses so the same code path is used consistently.

4. **Implementation**
   - Patch the split expense reducer/actions to handle negative amounts safely.
   - Ensure UI correctly reflects reverted state and does not attempt to operate on deleted splits.

5. **Testing**
   - Add regression tests around:
     - Splitting and reverting negative-amount expenses.
     - Performing the same flow offline then going back online.
   - Manual exploratory testing on Android (and, if applicable, iOS) for similar split flows.

6. **PR & Bounty Flow**
   - Open PR referencing `#82907` with attached crash logs and explanation of the fix.
   - Work through review; verify crash is gone in latest staging build.
   - Track the issue through to payment and confirm Upwork payout.

---

## Notes on Other Platforms
- **Algora:** The main Algora board at `https://algora.io/algora/bounties` currently shows **no open bounties** for the `algora/algora` project. Without broader search access to all org boards, there are no clearly discoverable >$200 tasks to target right now.
- **Bounti.fi / bounty.fi:** `bounti.fi` does not resolve; `bounty.fi` is an educational resource site, not a live bounty marketplace. No concrete, actionable bounties with priced rewards are exposed there.

Given current tool and platform state, **Expensify’s open Help Wanted issues with explicit dollar amounts are the only reliably accessible >$200 targets**, so this hit list focuses on the three with the cleanest scope and best risk/reward profile.
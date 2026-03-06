## Updated Proposal

### Please re-state the problem that we are trying to solve in this issue.
The app crashes immediately after login on NewDot Web, showing a Generic Error Page (ErrorBoundary). This is caused by an infinite redirect loop in the `OnboardingGuard`.

### What is the root cause of that problem?
The crash is a result of two compounding issues:

1. **Missing Cycle Detection in OnboardingGuard**: The `OnboardingGuard.evaluate()` function returns a `REDIRECT` result whenever onboarding is required, but it does not check if the current navigation state is already on the target onboarding route. This causes `RootStackRouter` to issue a `RESET` action, which re-triggers the guard evaluation, leading to an infinite loop and a 'Maximum update depth exceeded' error.

2. **Side Effects in getOnboardingInitialPath**: The `getOnboardingInitialPath` function, which is called during guard evaluation, contains `Onyx.set` calls that pre-select onboarding choices based on the user's signup qualifier (VSB, SMB, or Individual). Writing to Onyx during a navigation guard evaluation triggers subscription callbacks and re-renders, which can further amplify the redirect loop.

### What changes do you think we should make in order to solve the problem?

1. **Implement Cycle Detection in OnboardingGuard**:
Modify `src/libs/Navigation/guards/OnboardingGuard.ts` to compare the currently focused route with the target onboarding route. If the user is already on the target route, return `{type: 'ALLOW'}` instead of `{type: 'REDIRECT'}`.

2. **Extract Onyx Side Effects from getOnboardingInitialPath**:
Refactor `src/libs/actions/Welcome/OnboardingFlow.ts` to move the `Onyx.set` logic into a new function, `applyOnboardingQualifierDefaults()`. This function should be called from `startOnboardingFlow()` but NOT from `getOnboardingInitialPath()`. This ensures that path calculation remains a pure function without side effects during guard evaluation.

### What alternative solutions did you explore? (Optional)
- **Throttling the guard**: This would only hide the symptoms and could lead to a sluggish UI.
- **Broad check for any onboarding route**: This is too coarse and would prevent the guard from correctly advancing the user through different steps of the onboarding flow.

---
**Contributor Details**
Your Expensify account email: genesis.ai.labs.star@gmail.com
Upwork Profile Link: https://www.upwork.com/freelancers/~012f7d672872004dfd
# Progress Tracker Deployment Fix

## Problem Summary
The GitHub Pages site at https://coalescent-emergence.github.io/progress-tracker/mvp-tracker.html was showing the error:
```
⚠️ Error Loading Data
can't access property "toLowerCase", l.name is undefined
```

## Root Cause
1. **Data Format Mismatch**: The JavaScript code expected label objects `{name: "p0"}` but the `generate_issues_json.sh` script outputs label strings `"p0"`
2. **Workflow Architecture**: The deployment workflow syncs files FROM the Kerrigan repository, which may not have the fix
3. **Overwriting Issue**: Each sync could overwrite the `normalizeLabels()` fix that was added in PR #8

## Solution Applied
Added a post-sync fix step in `.github/workflows/deploy.yml` that:
- ✅ Checks if `normalizeLabels()` function exists after syncing from Kerrigan
- ✅ If missing, automatically injects the function before `categorizeIssue()`
- ✅ Replaces all direct `issue.labels.map(l => l.name.toLowerCase())` with `normalizeLabels(issue)`
- ✅ Ensures the fix persists regardless of Kerrigan's state

## How to Deploy the Fix

### Option 1: Automatic (Scheduled)
The workflow runs automatically daily at midnight UTC. The fix will be applied on the next scheduled run.

### Option 2: Manual Trigger
1. Go to [Actions tab](https://github.com/Coalescent-Emergence/progress-tracker/actions/workflows/deploy.yml)
2. Click "Run workflow"
3. Select branch: `main`
4. Click "Run workflow" button
5. Wait ~1-2 minutes for deployment to complete
6. Verify at: https://coalescent-emergence.github.io/progress-tracker/mvp-tracker.html

### Option 3: After Merging This PR
Once this PR is merged to `main`, trigger the workflow manually or wait for the next scheduled run.

## Verification Steps
After deployment, verify the fix by:
1. Visit https://coalescent-emergence.github.io/progress-tracker/mvp-tracker.html
2. Check that the page loads without errors
3. Verify all issues are displayed with correct priority/effort labels
4. Open browser console (F12) - should have no JavaScript errors
5. Confirm "Last updated" timestamp is recent

Expected result:
- Page shows "20% complete, 2 of 10 tasks done"
- Three phases with their respective tasks
- No error messages
- Priority and effort labels displayed correctly

## Long-Term Recommendation
While this PR ensures the deployed site works, the **ideal long-term solution** is:

### Apply Fix to Kerrigan Source Repository
1. **Location**: `Coalescent-Emergence/Kerrigan` repository
2. **File**: `docs/mvp-tracker.html`
3. **Change**: Add the `normalizeLabels()` helper function:
   ```javascript
   function normalizeLabels(issue) {
       return issue.labels.map(l => typeof l === 'string' ? l.toLowerCase() : l.name.toLowerCase());
   }
   
   function categorizeIssue(issue) {
       const labels = normalizeLabels(issue);  // Use helper instead of direct map
       // ... rest of function
   }
   ```
4. **Benefit**: Makes the source of truth correct; the post-sync fix becomes a safety net

### Why This Matters
- **Single Source of Truth**: Kerrigan is the source repository
- **Maintainability**: Future updates to the tracker should include the fix
- **Simplicity**: Less reliance on post-sync patching
- **Consistency**: Both repositories have the same code

## Files Changed
- `.github/workflows/deploy.yml` - Added "Apply post-sync fixes" step (lines 126-165)

## Testing Performed
✅ Local testing - page loads correctly with all issues  
✅ Code review - all feedback addressed  
✅ Security scan (CodeQL) - no vulnerabilities  
✅ YAML syntax validation - passed  
✅ Fix script testing - quote escaping and sed replacements work correctly  

## Security
✅ No vulnerabilities detected by CodeQL security analysis.

## Support
For questions or issues:
- Check workflow runs in [Actions tab](https://github.com/Coalescent-Emergence/progress-tracker/actions)
- Review this PR for implementation details
- Contact repository maintainers

# TeamCity Quick Start Guide

## 🚀 Quick Setup (5 Steps)

### Step 1: Prepare Your Build Agent

**CRITICAL**: The agent must run with UI access:

1. **Stop** TeamCity agent if running as Windows service
2. **Run agent as console application**:
   ```batch
   cd C:\TeamCity\buildAgent\bin
   agent.bat start
   ```
3. Keep the user logged in during builds
4. Ensure desktop is unlocked

**Why?** The tests need to interact with Windows Calculator GUI.

### Step 2: Create TeamCity Project

1. Log into TeamCity
2. Click **"Create Project"**
3. Choose **"From a repository URL"** or **"Manually"**
4. Set project name: `Windows Calculator Tests`

### Step 3: Add Build Configuration

1. Click **"Create Build Configuration"**
2. Name: `Calculator BDD Tests`
3. Add VCS root (your Git repository)

### Step 4: Add Build Steps

#### Build Step 1: Install Dependencies
```
Type: Command Line
Name: Install Dependencies
Run: Custom script

Script:
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Build Step 2: Run Tests
```
Type: Command Line
Name: Run BDD Tests
Run: Custom script

Script:
call venv\Scripts\activate.bat
if not exist "test-results" mkdir test-results
behave --junit --junit-directory test-results --format pretty
```

### Step 5: Configure Test Reporting

1. Go to **Build Features**
2. Click **"Add build feature"**
3. Select **"XML report processing"**
4. Settings:
   - Report type: `Ant JUnit`
   - Monitoring rules: `test-results/**/*.xml`

**Done!** Click **"Run"** to execute your first build.

---

## 📋 Alternative: Use the Build Script

Instead of configuring two build steps, you can use a single step with the provided `build.bat`:

### Single Build Step
```
Type: Command Line
Name: Run All Tests
Run: Custom script

Script:
build.bat
```

This script handles everything: environment setup, dependency installation, and test execution.

---

## 🔧 Advanced Configuration

### Add Build Artifacts

Go to **General Settings** → **Artifact paths**:
```
test-results/**/* => test-results.zip
reports/**/* => reports.zip
```

### Add Build Parameters

1. Go to **Parameters**
2. Add:
   - `env.PYTHONUNBUFFERED` = `1`
   - `env.PYTHONIOENCODING` = `utf-8`

### Add Build Triggers

**VCS Trigger** (run on every commit):
1. Go to **Triggers**
2. Add **"VCS Trigger"**
3. Branch filter: `+:*`

**Schedule Trigger** (daily runs):
1. Add **"Schedule Trigger"**
2. Daily at 2:00 AM
3. Branch: `main`

### Add Agent Requirements

1. Go to **Agent Requirements**
2. Add requirement:
   - Parameter: `system.os.name`
   - Condition: `contains`
   - Value: `Windows`

---

## 🐛 Troubleshooting

### "Calculator not found" error

**Problem**: Tests can't find Windows Calculator.

**Solution**: 
- Verify calc.exe exists: `C:\Windows\System32\calc.exe`
- Run `where calc.exe` on build agent

### "Python not found" error

**Problem**: Python not in PATH.

**Solution**:
1. Install Python on build agent
2. Add to system PATH
3. Restart TeamCity agent
4. Verify: `python --version`

### Tests fail with "Access Denied" or "Element not found"

**Problem**: Agent running as Windows service (session 0 isolation).

**Solution**:
1. Stop the service: `sc stop TCBuildAgent`
2. Disable service: `sc config TCBuildAgent start= disabled`
3. Run as console: `C:\TeamCity\buildAgent\bin\agent.bat start`
4. Keep user logged in

### Virtual environment issues

**Problem**: `venv` command fails or activation fails.

**Solution**:
```batch
REM Clean up old venv
rmdir /s /q venv

REM Create fresh venv
python -m venv venv

REM Activate
call venv\Scripts\activate.bat
```

---

## 📊 Viewing Test Results

### In TeamCity UI

1. **Overview Tab**: Shows pass/fail status
2. **Tests Tab**: Detailed test results, filterable
3. **Build Log Tab**: Complete console output
4. **Artifacts Tab**: Download test reports

### Understanding Test Output

```
✓ Green checkmarks = Tests passed
✗ Red X marks = Tests failed
Total: X scenarios (Y passed, Z failed)
```

---

## 🎯 Best Practices

### 1. Keep Agent Available
- Don't let Windows sleep/hibernate
- Keep user logged in
- Disable screen saver lock

### 2. Clean Workspace
Enable in **Build Configuration** → **Version Control Settings**:
- Clean checkout: `Always`
- Clean build: `Enabled`

### 3. Timeout Protection
Set in **Failure Conditions**:
- Execution timeout: `15 minutes`

### 4. Notifications
Configure in **Project Settings** → **Notifications**:
- Build failed → Email team
- Build successful after failed → Email team

---

## 📦 Using Kotlin DSL (Advanced)

If you want to version your TeamCity configuration:

1. Enable versioned settings: **Project Settings** → **Versioned Settings**
2. Format: **Kotlin**
3. Commit `.teamcity/settings.kts` to your repository
4. TeamCity will auto-apply configuration from Git

---

## 🔄 CI/CD Pipeline Example

```
[Commit to Git]
    ↓
[TeamCity VCS Trigger]
    ↓
[Checkout Code]
    ↓
[Install Dependencies]
    ↓
[Run BDD Tests]
    ↓
[Generate Reports]
    ↓
[Publish Results]
    ↓
[Notify Team]
```

---

## 📧 Need Help?

**Check these in order:**

1. **Build Log**: Look for Python errors, missing files
2. **Test Tab**: See which scenarios failed
3. **Agent Log**: `C:\TeamCity\buildAgent\logs\teamcity-agent.log`
4. **Environment**: Verify Python, pip, behave installed

**Common Issues Resolved:**
- 90% of issues: Agent running as service (needs to run as user)
- 5% of issues: Python not in PATH
- 5% of issues: Timing/synchronization in tests

---

## ✅ Success Checklist

After setup, verify:

- [ ] Build completes without errors
- [ ] Tests execute and report results
- [ ] Test results appear in Tests tab
- [ ] HTML reports available in Artifacts
- [ ] Build triggers work (VCS/Schedule)
- [ ] Notifications configured
- [ ] Agent requirements set

---

**Congratulations! Your Windows Calculator BDD tests are now running in TeamCity! 🎉**
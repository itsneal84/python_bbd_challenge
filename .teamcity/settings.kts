import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import jetbrains.buildServer.configs.kotlin.triggers.schedule
import jetbrains.buildServer.configs.kotlin.buildFeatures.PullRequests
import jetbrains.buildServer.configs.kotlin.buildFeatures.pullRequests

/*
TeamCity Kotlin DSL Configuration
For Windows Calculator BDD Tests

To use this configuration:
1. Place this file in .teamcity/settings.kts in your repository
2. Enable versioned settings in TeamCity project settings
3. Select Kotlin format
4. TeamCity will automatically apply this configuration
*/

version = "2023.11"

project {
    description = "Windows Calculator BDD Test Automation"

    buildType(CalculatorBDDTests)
}

object CalculatorBDDTests : BuildType({
    name = "Calculator BDD Tests"
    description = "Automated BDD tests for Windows Calculator using Behave and PyWinAuto"

    // VCS Settings
    vcs {
        root(DslContext.settingsRoot)
        cleanCheckout = true
    }

    // Build Steps
    steps {
        // Step 1: Setup Python Environment
        script {
            name = "Setup Python Environment"
            scriptContent = """
                python -m venv venv
                call venv\Scripts\activate.bat
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                pip list
            """.trimIndent()
        }

        // Step 2: Run BDD Tests
        script {
            name = "Run BDD Tests"
            scriptContent = """
                call venv\Scripts\activate.bat
                if not exist "test-results" mkdir test-results
                if not exist "reports" mkdir reports
                behave --junit --junit-directory test-results --format html --outfile reports/behave-report.html --format pretty
            """.trimIndent()
        }
    }

    // Build Features
    features {
        // XML Test Reporting
        feature {
            type = "xml-report-plugin"
            param("xmlReportParsing.reportType", "junit")
            param("xmlReportParsing.reportDirs", "test-results/**/*.xml")
        }
    }

    // Artifacts
    artifactRules = """
        test-results/**/* => test-results.zip
        reports/**/* => reports.zip
    """.trimIndent()

    // Parameters
    params {
        param("env.PYTHONUNBUFFERED", "1")
        param("env.PYTHONIOENCODING", "utf-8")
    }

    // Requirements - ensure agent can run UI tests
    requirements {
        contains("system.os.name", "Windows")
        // Add specific agent requirement if needed
        // equals("system.agent.name", "windows-ui-agent")
    }

    // Triggers
    triggers {
        // Trigger on VCS changes
        vcs {
            branchFilter = "+:*"
            triggerRules = "+:."
        }

        // Schedule daily runs
        schedule {
            schedulingPolicy = daily {
                hour = 2
                minute = 0
            }
            branchFilter = "+:main"
            triggerBuild = always()
            withPendingChangesOnly = false
        }
    }

    // Failure Conditions
    failureConditions {
        executionTimeoutMin = 15
        testFailure = false // We'll fail on step failure instead
    }
})
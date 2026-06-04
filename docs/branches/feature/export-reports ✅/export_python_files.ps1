# ==========================================
# export_python_files.ps1
# Purpose:
# Export all .py files into one text file
# and open automatically in Notepad.
# ==========================================

# Ask user for project path
# If Enter is pressed, current folder is used
$path = Read-Host "Enter project path (Press Enter for current folder)"

# Use current folder if blank
if ([string]::IsNullOrWhiteSpace($path)) {
    $path = (Get-Location).Path
}

# Output file location
$outputFile = Join-Path $path "project_python_files.txt"

# Delete old output file if it exists
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

# Find all Python files recursively
# Ignore __pycache__ folders
Get-ChildItem -Path $path -Recurse -File -Filter *.py |
Where-Object {
    $_.FullName -notmatch "\\__pycache__\\"
} |
ForEach-Object {

    # Add file header
    "`r`n==================== $($_.FullName) ====================`r`n" |
        Out-File $outputFile -Append

    # Add file contents
    Get-Content $_.FullName |
        Out-File $outputFile -Append
}

Write-Host ""
Write-Host "Export completed successfully."
Write-Host "Output File: $outputFile"

# Open output automatically
notepad $outputFile
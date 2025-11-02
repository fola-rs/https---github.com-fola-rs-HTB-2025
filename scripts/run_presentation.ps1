# Tides & Tomes Presentation Launcher
# PowerShell script to run the Streamlit dashboard

Write-Host "🌊 Tides & Tomes - Starting Presentation Dashboard..." -ForegroundColor Cyan
Write-Host ""

# Check if streamlit is installed
$streamlitCheck = python -m streamlit --version 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Streamlit not found. Installing dependencies..." -ForegroundColor Yellow
    python -m pip install -r presentation\requirements.txt
    Write-Host ""
}

Write-Host "✅ Launching dashboard..." -ForegroundColor Green
Write-Host ""
Write-Host "📱 The presentation will open in your browser at http://localhost:8501" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Challenge Pages:" -ForegroundColor White
Write-Host "   • Overview - Complete system visualization" -ForegroundColor Gray
Write-Host "   • CompSoc Challenge - Interactive sensitivity analysis" -ForegroundColor Gray
Write-Host "   • G-Research Challenge - Real-time data monitoring" -ForegroundColor Gray
Write-Host "   • Hoppers Challenge - Edinburgh impact stories" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Run streamlit
python -m streamlit run presentation\app.py

Write-Host "Running black..." -ForegroundColor Green
black .

Write-Host "`nRunning isort..." -ForegroundColor Green
isort .

Write-Host "`nRunning flake8..." -ForegroundColor Green
flake8 .

Write-Host "`nRunning tests with coverage..." -ForegroundColor Green
pytest tests/ --cov=shop --cov-report=term --cov-report=html
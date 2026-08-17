Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$chapterDir = Get-ChildItem -LiteralPath $root -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName '_audit\rendered_pages')
} | Select-Object -First 1

if ($null -eq $chapterDir) {
    throw 'Could not locate the chapter directory.'
}

$sourceDir = Join-Path $chapterDir.FullName '_audit\rendered_pages'
$outputDir = Join-Path $chapterDir.FullName 'images'

function Save-Crop {
    param(
        [string]$SourceName,
        [string]$OutputName,
        [int]$X,
        [int]$Y,
        [int]$Width,
        [int]$Height
    )

    $sourcePath = Join-Path $sourceDir $SourceName
    $outputPath = Join-Path $outputDir $OutputName
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        throw "Missing rendered source: $sourcePath"
    }

    $source = [System.Drawing.Image]::FromFile($sourcePath)
    try {
        $bounds = New-Object System.Drawing.Rectangle($X, $Y, $Width, $Height)
        $bitmap = New-Object System.Drawing.Bitmap($Width, $Height)
        try {
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            try {
                $graphics.DrawImage($source, (New-Object System.Drawing.Rectangle(0, 0, $Width, $Height)), $bounds, [System.Drawing.GraphicsUnit]::Pixel)
            }
            finally {
                $graphics.Dispose()
            }
            $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        }
        finally {
            $bitmap.Dispose()
        }
    }
    finally {
        $source.Dispose()
    }
}

Save-Crop 'page_008.png' 'ch01_greek_letters.png' 180 300 1625 575
Save-Crop 'page_012.png' 'ch01_row_column_structure.png' 180 725 900 480
Save-Crop 'page_054.png' 'ch02_kurtosis_comparison.png' 175 545 1110 420
Save-Crop 'page_081.png' 'ch03_bar_chart.png' 175 480 590 475
Save-Crop 'page_082.png' 'ch03_histogram.png' 175 565 785 490
Save-Crop 'page_087.png' 'ch03_scatter_patterns.png' 175 640 1235 440
Save-Crop 'page_088.png' 'ch03_line_chart.png' 175 550 680 655
Save-Crop 'page_089.png' 'ch03_grouped_bar.png' 175 465 815 545
Save-Crop 'page_090.png' 'ch03_stacked_bar.png' 175 470 815 545

$outputs = @(
    'ch01_greek_letters.png',
    'ch01_row_column_structure.png',
    'ch02_kurtosis_comparison.png',
    'ch03_bar_chart.png',
    'ch03_histogram.png',
    'ch03_scatter_patterns.png',
    'ch03_line_chart.png',
    'ch03_grouped_bar.png',
    'ch03_stacked_bar.png'
)

foreach ($name in $outputs) {
    Get-Item -LiteralPath (Join-Path $outputDir $name) | Select-Object Name, Length
}

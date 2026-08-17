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

Save-Crop 'page_532.png' 'ch20_kmeans_steps.png' 180 690 1170 320
Save-Crop 'page_533.png' 'ch20_centroid_profile.png' 180 555 1305 480
Save-Crop 'page_535.png' 'ch20_silhouette_example.png' 180 620 795 565
Save-Crop 'page_554.png' 'ch21_drop_column_importance.png' 180 545 1250 450
Save-Crop 'page_555.png' 'ch21_permutation_importance.png' 180 545 1180 395
Save-Crop 'page_571.png' 'ch22_ensemble_configurations.png' 180 340 1250 725
Save-Crop 'page_575.png' 'ch22_voting_example.png' 175 490 1350 315
Save-Crop 'page_592.png' 'ch23_tree_structure.png' 180 700 970 500
Save-Crop 'page_596.png' 'ch23_mdi_importance.png' 180 630 775 540

Get-ChildItem -LiteralPath $outputDir -Filter 'ch2*.png' |
    Where-Object Name -In @(
        'ch20_kmeans_steps.png',
        'ch20_centroid_profile.png',
        'ch20_silhouette_example.png',
        'ch21_drop_column_importance.png',
        'ch21_permutation_importance.png',
        'ch22_ensemble_configurations.png',
        'ch22_voting_example.png',
        'ch23_tree_structure.png',
        'ch23_mdi_importance.png'
    ) |
    Select-Object Name, Length
